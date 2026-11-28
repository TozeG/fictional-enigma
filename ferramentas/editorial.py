#!/usr/bin/env python3
"""SIE-AO: validação de achados editoriais e avaliação de calibração.

Uso:
  python3 ferramentas/editorial.py validar <manuscrito> <achados.json>
  python3 ferramentas/editorial.py avaliar <achados.json> <gabarito.json>

Só usa a biblioteca padrão do Python 3.8+.
"""
import json
import sys
import unicodedata
from collections import defaultdict

AGENTES = {
    "analista-estrutural": "EST", "revisor-linguistico": "LIN", "estilista": "ESTL",
    "verificador-factual": "FAC", "normalizador": "NOR", "leitor-critico": "LEI",
    "revisor-provas": "PRV",
}
TIPOS = {"obrigatoria", "recomendada", "opcional", "consulta-autor"}
SEVERIDADES = {"critica", "alta", "media", "baixa"}
ESTATUTOS = {"facto-normativo", "facto-verificado", "interpretacao", "hipotese", "preferencia-estilo"}
CONFIANCAS = {"alta", "media", "baixa"}
OBRIGATORIOS = ["id", "agente", "categoria", "excerto", "proposta",
                "tipo_intervencao", "severidade", "fundamento", "confianca"]


def norm(txt):
    """Normaliza Unicode (NFC) e espaços, para comparar excertos sem falsos negativos tipográficos."""
    return " ".join(unicodedata.normalize("NFC", txt).split())


def carregar(caminho):
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def validar(manuscrito_path, achados_path):
    with open(manuscrito_path, encoding="utf-8") as f:
        texto = norm(f.read())
    achados = carregar(achados_path)
    if not isinstance(achados, list):
        print("ERRO: o ficheiro de achados tem de ser uma lista JSON.")
        return 2

    erros, avisos = [], []
    ids = set()
    por_excerto = defaultdict(list)

    for i, a in enumerate(achados):
        ref = a.get("id", f"#{i}")
        for campo in OBRIGATORIOS:
            if campo not in a or a[campo] in ("", None):
                erros.append(f"{ref}: campo obrigatório ausente: {campo}")
        if ref in ids:
            erros.append(f"{ref}: id duplicado")
        ids.add(ref)

        agente = a.get("agente")
        if agente not in AGENTES:
            erros.append(f"{ref}: agente desconhecido: {agente}")
        elif not str(ref).startswith(AGENTES[agente] + "-"):
            avisos.append(f"{ref}: prefixo do id não corresponde ao agente {agente} ({AGENTES[agente]}-)")

        tipo = a.get("tipo_intervencao")
        if tipo not in TIPOS:
            erros.append(f"{ref}: tipo_intervencao inválido: {tipo}")
        if a.get("severidade") not in SEVERIDADES:
            erros.append(f"{ref}: severidade inválida: {a.get('severidade')}")
        if a.get("confianca") not in CONFIANCAS:
            erros.append(f"{ref}: confianca inválida: {a.get('confianca')}")

        fund = a.get("fundamento") or {}
        estatuto = fund.get("estatuto")
        if estatuto not in ESTATUTOS:
            erros.append(f"{ref}: fundamento.estatuto inválido: {estatuto}")
        if not fund.get("regra"):
            erros.append(f"{ref}: fundamento.regra vazio")

        # Regras de coerência evidência ↔ intervenção
        if tipo == "obrigatoria":
            if not fund.get("fonte"):
                erros.append(f"{ref}: 'obrigatoria' exige fundamento.fonte")
            if estatuto not in ("facto-normativo", "facto-verificado"):
                erros.append(f"{ref}: 'obrigatoria' exige estatuto facto-normativo ou facto-verificado (tem {estatuto})")
            if a.get("confianca") == "baixa":
                erros.append(f"{ref}: 'obrigatoria' com confiança baixa: rebaixar para consulta-autor")
        if estatuto == "preferencia-estilo" and tipo == "obrigatoria":
            erros.append(f"{ref}: preferência de estilo não pode ser obrigatória")

        # Verificabilidade: o excerto tem de existir literalmente no manuscrito
        exc = norm(a.get("excerto", ""))
        if exc:
            n = texto.count(exc)
            if n == 0:
                erros.append(f"{ref}: excerto não encontrado no manuscrito: «{exc[:60]}»")
            elif n > 1:
                avisos.append(f"{ref}: excerto ambíguo ({n} ocorrências); alargar contexto ou indicar localização")
        prop = norm(a.get("proposta", ""))
        if prop and prop == exc and tipo != "consulta-autor" and agente != "analista-estrutural":
            erros.append(f"{ref}: proposta idêntica ao excerto")
        por_excerto[exc].append(a)

    # Conflitos: agentes diferentes com propostas diferentes para o mesmo excerto
    conflitos = []
    for exc, lista in por_excerto.items():
        agentes = {x.get("agente") for x in lista}
        propostas = {norm(x.get("proposta", "")) for x in lista}
        if len(agentes) > 1 and len(propostas) > 1:
            conflitos.append((exc, [x.get("id") for x in lista]))

    print(f"Achados analisados: {len(achados)}")
    print(f"Erros: {len(erros)} | Avisos: {len(avisos)} | Conflitos: {len(conflitos)}")
    for e in erros:
        print("  [ERRO]  ", e)
    for w in avisos:
        print("  [AVISO] ", w)
    for exc, ids_c in conflitos:
        print(f"  [CONFLITO] «{exc[:50]}»: {', '.join(ids_c)}, resolver por precedência")
    print("RESULTADO:", "VÁLIDO" if not erros else "INVÁLIDO")
    return 0 if not erros else 1


def avaliar(achados_path, gabarito_path):
    """Compara achados com o gabarito: cobertura (recall) dos erros semeados e violação de armadilhas."""
    achados = carregar(achados_path)
    gab = carregar(gabarito_path)
    esperados = gab["esperados"]
    armadilhas = gab.get("armadilhas", [])

    def casa(chave, a):
        e = norm(a.get("excerto", "")).lower()
        k = norm(chave).lower()
        return k in e or (e and e in k)

    def chaves(item):
        return item.get("chaves") or [item["chave"]]

    detectados, falhados = [], []
    for item in esperados:
        tipos = item.get("requer_tipo")
        hit = [a for a in achados
               if any(casa(k, a) for k in chaves(item))
               and (not tipos or a.get("tipo_intervencao") in tipos)]
        (detectados if hit else falhados).append((item, hit))

    def preserva(a, chave):
        """Achado de preservação (categoria 'preservacao') ou proposta que mantém o texto da armadilha."""
        return a.get("categoria") == "preservacao" or norm(chave).lower() in norm(a.get("proposta", "")).lower()

    violacoes = []
    for t in armadilhas:
        for a in achados:
            if (casa(t["chave"], a) and a.get("tipo_intervencao") in ("obrigatoria", "recomendada")
                    and a.get("estado") != "rejeitado-auditor" and not preserva(a, t["chave"])):
                violacoes.append((t, a))

    total = len(esperados)
    recall = len(detectados) / total if total else 0.0
    associados = {id(a) for _, hits in detectados for a in hits}
    extra = [a for a in achados if id(a) not in associados]

    print(f"Erros semeados detectados: {len(detectados)}/{total} (cobertura {recall:.0%})")
    for item, _ in falhados:
        print(f"  [NÃO DETECTADO] {item['id']} ({item['tipo']}): «{' | '.join(chaves(item))}»")
    print(f"Armadilhas violadas (variação legítima 'corrigida'): {len(violacoes)}")
    for t, a in violacoes:
        print(f"  [FALSO POSITIVO] {a.get('id')} sobre «{t['chave']}»: {t['motivo']}")
    print(f"Achados fora do gabarito (rever manualmente): {len(extra)}")
    meta = gab.get("criterios", {"recall_min": 0.8, "armadilhas_max": 0})
    ok = recall >= meta["recall_min"] and len(violacoes) <= meta["armadilhas_max"]
    print(f"CRITÉRIO (cobertura ≥ {meta['recall_min']:.0%}, armadilhas ≤ {meta['armadilhas_max']}):",
          "APROVADO" if ok else "REPROVADO")
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[1] not in ("validar", "avaliar"):
        print(__doc__)
        sys.exit(2)
    fn = validar if sys.argv[1] == "validar" else avaliar
    sys.exit(fn(sys.argv[2], sys.argv[3]))
