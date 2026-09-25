"""Importação em massa (opcional): carga inicial de lançamentos, terceiros e activos a partir de Excel, com validação e comparação com um balancete de referência.

Fluxo:
  1. python src/importar.py modelo [dist/MODELO_IMPORTACAO.xlsx]
       → gera o modelo de importação (ENTIDADE, LANÇAMENTOS, TERCEIROS, ACTIVOS, PLANO_CONTAS, BALANCETE_REFERÊNCIA).
  2. Preencher o modelo (ou colar a exportação do sistema actual) — um mês completo.
  3. python src/importar.py carregar modelo_preenchido.xlsx [--saida matriz.xlsx]
       → valida linha a linha (sem gerar nada se houver erros bloqueantes, salvo --forcar),
         gera a matriz em modo produção com os dados reais,
         compara os saldos com o BALANCETE_REFERÊNCIA do sistema actual,
         escreve o relatório <saida>_RELATORIO.md.
"""
import argparse
import os
import sys
from collections import defaultdict
from datetime import date, datetime

os.environ.setdefault("MATRIZ_MODO", "producao")
sys.path.insert(0, os.path.dirname(__file__))
from openpyxl import Workbook, load_workbook  # noqa: E402
from openpyxl.styles import Font, PatternFill, Alignment  # noqa: E402
from openpyxl.worksheet.datavalidation import DataValidation  # noqa: E402

import data as D  # noqa: E402
import sheets_base as SB  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOL = 1.0

ENTIDADE = [("Nome da entidade", "CFG_Nome", "[Nome]"), ("Denominação social", "CFG_Denom", ""), ("NIF", "CFG_NIF", ""),
            ("Ano económico", "CFG_Ano", D.ANO), ("Mês de reporte (1–12)", "CFG_MesRep", 1), ("Regime de IVA", "CFG_RegIVA", "Regime Geral"),
            ("Regime do Imposto Industrial", "CFG_RegII", "Regime Geral"), ("Grande Contribuinte (S/N)", "CFG_GC", "N"),
            ("Reserva mínima de liquidez (Kz)", "CFG_SaldoMin", 0)]
TERC_H = ["NIF", "Nome", "Tipo de terceiro", "País", "Prazo (dias)", "Limite de crédito (Kz)", "Parte relacionada (S/N)"]
ACT_H = ["Código", "Descrição", "Conta activo", "Conta amort. acum.", "Conta custo", "Data aquisição", "Valor aquisição", "Vida útil (anos)",
         "Método", "Valor residual", "Localização", "Responsável", "Estado", "Data alienação", "Valor alienação", "C. custo", "Projecto"]
PC_H = ["Código", "Designação", "Tipo (M = movimento / A = agregação)"]
BAL_H = ["Conta", "Designação (opcional)", "Saldo final D−C no sistema actual (Kz)"]
HEAD = Font(name="Arial", bold=True, color="FFFFFF")
FILL = PatternFill("solid", start_color="1F3864", end_color="1F3864")


def _sheet(wb, name, headers, rows=(), widths=None):
    ws = wb.create_sheet(name)
    for j, h in enumerate(headers):
        c = ws.cell(row=1, column=1 + j, value=h)
        c.font, c.fill = HEAD, FILL
        c.alignment = Alignment(wrap_text=True, vertical="center")
        ws.column_dimensions[c.column_letter].width = (widths or {}).get(j, max(12, min(40, len(h) + 2)))
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            ws.cell(row=2 + i, column=1 + j, value=v)
    ws.freeze_panes = "A2"
    return ws


def modelo(out):
    wb = Workbook()
    ins = wb.active
    ins.title = "INSTRUÇÕES"
    txt = [
        "MODELO DE IMPORTAÇÃO — MATRIZ PRO MASTER (carga em massa, opcional)",
        "",
        "1. ENTIDADE: identificação, exercício e mês de reporte (o último mês importado).",
        "2. LANÇAMENTOS: uma linha por conta movimentada; mesmo ID_Lançamento para todas as linhas da operação; Σ Débito = Σ Crédito.",
        "   • Conta como TEXTO (ex.: 43.1.1). • Natureza_Operação obrigatória (lista em 01A_TABELAS). • NIF obrigatório em 31/32.",
        "   • Recibos/pagamentos/notas de crédito: Ref_Origem_ID = ID do documento liquidado. • Linhas de IVA: Código_Fiscal + Base_Tributável.",
        "   • Primeiro lançamento: saldos de abertura (natureza 'Abertura') a partir do balanço de fecho do ano anterior.",
        "3. TERCEIROS: todos os NIF usados nos lançamentos (clientes, fornecedores).",
        "4. ACTIVOS (opcional): registo do imobilizado.",
        "5. PLANO_CONTAS (opcional): contas a acrescentar ao PGC do modelo (mesmo código = substitui a designação/tipo).",
        "7. IRT_ESCALOES: copiar do Diário da República (Lei n.º 14/25) (opcional) escalões que substituam a tabela legal do exercício — limite inferior («excesso de»), limite superior, parcela fixa, taxa (ex.: 0.16). Vazio = usa a tabela legal carregada (Lei 28/20, 18/24 ou 14/25).",
        "6. BALANCETE_REFERÊNCIA: saldos finais (D−C, credores negativos) do balancete do sistema actual no fim do mês de reporte.",
        "   Pode usar contas de movimento ou de agregação (ex.: 31, 43, 6, 7).",
        "",
        "Depois: python src/importar.py carregar <este ficheiro> --saida dist/MATRIZ_<ENTIDADE>_<AAAA-MM>.xlsx",
        "As linhas 2 dos separadores são EXEMPLOS: apague-as antes de importar.",
    ]
    for i, t in enumerate(txt):
        ins.cell(row=1 + i, column=1, value=t).font = Font(name="Arial", bold=i == 0, size=12 if i == 0 else 10)
    ins.column_dimensions["A"].width = 130
    ent = _sheet(wb, "ENTIDADE", ["Campo", "Valor", "Código interno"], [(a, v, c) for a, c, v in ENTIDADE], {0: 38, 1: 40, 2: 16})
    heads = [h for _, h, _, _ in SB.J_IN]
    ex = [(1, date(D.ANO, 1, 1), "ABE", str(D.ANO), 1, date(D.ANO, 1, 1), None, "", "43.1.1", "Saldo de abertura — banco", 1000, None, "", "", "", "",
           "Abertura", "", None, None, "", None, None, "", "", None, "Balanço de fecho", "utilizador1", "utilizador2", date(D.ANO, 1, 1), None,
           "", "", "", "", None, "", "EXEMPLO — apagar"),
          (1, date(D.ANO, 1, 1), "ABE", str(D.ANO), 1, date(D.ANO, 1, 1), None, "", "51.1", "Saldo de abertura — capital", None, 1000, "", "", "", "",
           "Abertura", "", None, None, "", None, None, "", "", None, "Balanço de fecho", "utilizador1", "utilizador2", date(D.ANO, 1, 1), None,
           "", "", "", "", None, "", "EXEMPLO — apagar")]
    lan = _sheet(wb, "LANÇAMENTOS", heads, ex)
    for j, (k, _, _, fmt) in enumerate(SB.J_IN):
        col = lan.cell(row=1, column=1 + j).column_letter
        for r in range(2, 5002):
            if fmt:
                lan[f"{col}{r}"].number_format = fmt
    nat = ",".join(n[0] for n in D.NATUREZAS)
    if len(nat) < 255:
        dv = DataValidation(type="list", formula1=f'"{nat}"', allow_blank=True)
        lan.add_data_validation(dv)
        dv.add(f"{lan.cell(row=1, column=1 + [k for k, *_ in SB.J_IN].index('Nat')).column_letter}2:{lan.cell(row=1, column=1 + [k for k, *_ in SB.J_IN].index('Nat')).column_letter}5001")
    _sheet(wb, "TERCEIROS", TERC_H, [("5000000001", "Cliente exemplo, Lda", "Cliente", "Angola", 30, 0, "N")])
    _sheet(wb, "ACTIVOS", ACT_H)
    _sheet(wb, "PLANO_CONTAS", PC_H, [("62.1.1", "Serviços de consultoria (exemplo)", "M")])
    _sheet(wb, "BALANCETE_REFERÊNCIA", BAL_H, [("43.1.1", "Banco A", 1000), ("51.1", "Capital social", -1000)])
    _sheet(wb, "IRT_ESCALOES", ["Escalão", "Limite inferior (Kz)", "Limite superior (Kz)", "Parcela fixa (Kz)", "Taxa sobre o excesso (ex.: 0.16)", "Fonte (DR, página)"],
           [(i + 1, None, None, None, None, "") for i in range(12)])
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    wb.save(out)
    print("Modelo gerado:", os.path.abspath(out))


def _rows(ws, ncols):
    for row in ws.iter_rows(min_row=2, max_col=ncols, values_only=True):
        if any(v not in (None, "") for v in row):
            yield list(row) + [None] * (ncols - len(row))


def _date(v):
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, date) or v in (None, ""):
        return v or None
    for f in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(str(v).strip(), f).date()
        except ValueError:
            pass
    return str(v)


def _txt(v):
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return str(v).strip()


def ler(path):
    wb = load_workbook(path, data_only=True)
    cfg = {}
    for row in _rows(wb["ENTIDADE"], 3):
        if row[2]:
            cfg[row[2]] = row[1]
    heads = [h for _, h, _, _ in SB.J_IN]
    ws = wb["LANÇAMENTOS"]
    idx = {c.value: i for i, c in enumerate(ws[1]) if c.value}
    falta = [h for h in heads if h not in idx]
    if falta:
        raise SystemExit(f"Colunas em falta em LANÇAMENTOS: {falta}")
    journal = []
    textos = {"TipoDoc", "Serie", "NIF", "Conta", "CC", "CR", "Proj", "Fonte", "Nat", "CodF", "Moeda", "FormaPag", "Artigo", "Suporte", "User",
              "Validador", "EstDoc", "Hash", "Cert", "EstAGT", "ErroCom", "Obs", "Desc"}
    datas = {"Data", "DataDoc", "Venc", "DtIns", "DtAlt", "DtCom"}
    for n, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        if not any(v not in (None, "") for v in row):
            continue
        rec = {"_linha": n}
        for k, h, _, _ in SB.J_IN:
            v = row[idx[h]] if idx[h] < len(row) else None
            if k in textos:
                v = _txt(v)
            elif k in datas:
                v = _date(v)
            elif v == "":
                v = None
            rec[k] = v
        if not rec["DtIns"]:
            rec["DtIns"] = rec["Data"]
        journal.append(rec)
    terc = [tuple(_txt(x) if j in (0, 1, 2, 3, 6) else x for j, x in enumerate(r[:7])) for r in _rows(wb["TERCEIROS"], 7)]
    act = [tuple(_date(x) if j in (5, 13) else (_txt(x) if j in (0, 2, 3, 4, 15, 16) else x) for j, x in enumerate(r[:17]))
           for r in _rows(wb["ACTIVOS"], 17)] if "ACTIVOS" in wb.sheetnames else []
    plano = [(_txt(r[0]), _txt(r[1]), (_txt(r[2]) or "M").upper()[0]) for r in _rows(wb["PLANO_CONTAS"], 3)] if "PLANO_CONTAS" in wb.sheetnames else []
    ref = [(_txt(r[0]), float(r[2] or 0)) for r in _rows(wb["BALANCETE_REFERÊNCIA"], 3) if r[0]] if "BALANCETE_REFERÊNCIA" in wb.sheetnames else []
    irt = []
    if "IRT_ESCALOES" in wb.sheetnames:
        for r in _rows(wb["IRT_ESCALOES"], 5):
            if isinstance(r[1], (int, float)) and isinstance(r[4], (int, float)):
                irt.append((r[1], r[2], r[3] or 0, r[4] if r[4] < 1 else r[4] / 100))
    return cfg, journal, terc, act, plano, ref, irt


def validar(cfg, journal, terc, plano):
    """Replica em Python as validações bloqueantes do Diário. Devolve lista (linha, ID, gravidade, mensagem)."""
    ano = int(cfg.get("CFG_Ano") or D.ANO)
    tipos = {c: t for c, _, t in plano}
    nif_ok = {t[0] for t in terc}
    nat_ok = {n[0] for n in D.NATUREZAS}
    tx = {t[0]: t[3] for t in D.TAXAS}
    ids = {l["ID"] for l in journal}
    saldo = defaultdict(float)
    for l in journal:
        saldo[l["ID"]] += (l["Deb"] or 0) - (l["Cred"] or 0)
    chaves = {}
    out = []
    for l in journal:
        e = lambda g, m: out.append((l["_linha"], l["ID"], g, m))
        if l["ID"] in (None, ""):
            e("ERRO", "ID_Lançamento em falta")
        if not isinstance(l["Data"], date):
            e("ERRO", f"Data inválida: {l['Data']!r}")
        elif l["Data"].year != ano:
            e("ERRO", "Fora do exercício")
        c = l["Conta"]
        if c not in tipos:
            e("ERRO", f"Conta inexistente: {c!r}")
        elif tipos[c] != "M":
            e("ERRO", f"Conta de agregação (não movimentável): {c}")
        deb, cre = l["Deb"] or 0, l["Cred"] or 0
        if not isinstance(deb, (int, float)) or not isinstance(cre, (int, float)):
            e("ERRO", "Débito/Crédito não numérico")
            continue
        if deb < 0 or cre < 0:
            e("ERRO", "Valor negativo")
        if (deb > 0) == (cre > 0):
            e("ERRO", "Linha deve ter valor só a débito ou só a crédito")
        if abs(saldo[l["ID"]]) > 0.005:
            e("ERRO", f"Lançamento não equilibrado (diferença {saldo[l['ID']]:,.2f})")
        if c[:2] in ("31", "32") and l["NIF"] not in nif_ok:
            e("ERRO", f"NIF em falta ou não registado em TERCEIROS: {l['NIF']!r}")
        if l["Nat"] not in nat_ok:
            e("ERRO", f"Natureza inválida: {l['Nat']!r}")
        if not l["Suporte"]:
            e("ERRO", "Sem documento de suporte")
        if l["Ref"] not in (None, "") and l["Ref"] not in ids:
            e("ERRO", f"Ref_Origem_ID inexistente: {l['Ref']}")
        if l["CodF"] and l["CodF"] not in tx:
            e("ERRO", f"Código fiscal desconhecido: {l['CodF']}")
        if c in ("34.5.2", "34.5.3") or c.startswith("34.5.4"):
            if not l["CodF"] and l["Nat"] != "Apuramento de IVA":
                e("ERRO", "Linha de IVA sem código fiscal")
            elif l["CodF"] and isinstance(tx.get(l["CodF"]), float) and abs(deb + cre - (l["Base"] or 0) * tx[l["CodF"]]) > TOL:
                e("ERRO", f"IVA ≠ base × taxa ({l['Base']} × {tx[l['CodF']]:.0%})")
        if l["Moeda"] and l["Moeda"] != "AOA" and abs((l["ValME"] or 0) * (l["Cambio"] or 0) - (deb + cre)) > TOL:
            e("ERRO", "Câmbio inconsistente")
        if l["NumDoc"] not in (None, ""):
            k = (l["TipoDoc"], l["Serie"], _txt(l["NumDoc"]), l["NIF"])
            if k in chaves and chaves[k] != l["ID"]:
                e("ERRO", f"Documento duplicado (também no ID {chaves[k]})")
            chaves.setdefault(k, l["ID"])
        if not l["Validador"]:
            e("AVISO", "Lançamento por aprovar (Validado_Por vazio)")
        elif l["Validador"] == l["User"]:
            e("AVISO", "Segregação de funções: Validado_Por = Utilizador")
    return out


def saldos(journal, plano, mes):
    ano_ok = lambda d: isinstance(d, date) and d.month <= mes
    mov = defaultdict(float)
    for l in journal:
        if ano_ok(l["Data"]):
            mov[l["Conta"]] += (l["Deb"] or 0) - (l["Cred"] or 0)

    def saldo(code):
        if len(code) == 1:
            return sum(v for c, v in mov.items() if c[:1] == code)
        return sum(v for c, v in mov.items() if c == code or c.startswith(code + "."))
    return mov, saldo


def carregar(path, saida, forcar=False):
    cfg, journal, terc, act, plano_extra, ref, irt = ler(path)
    probs_irt = []
    for i in range(1, len(irt)):
        if irt[i][0] <= irt[i - 1][0]:
            probs_irt.append(("IRT_ESCALOES", i + 1, "ERRO", "Limites inferiores dos escalões têm de ser crescentes"))
    if irt and irt[0][3] == 0 and irt[0][0] > 0:
        probs_irt.append(("IRT_ESCALOES", 1, "AVISO", "1.º escalão com taxa 0 — confirme que corresponde à isenção legal do exercício"))
    # plano: PGC do modelo + contas do cliente
    plano = list(D.PLANO)
    pos = {c: i for i, (c, _, _) in enumerate(plano)}
    for c, n, t in plano_extra:
        if c in pos:
            plano[pos[c]] = (c, n, t)
        else:
            plano.append((c, n, t))
    plano.sort(key=lambda x: [int(p) if p.isdigit() else p for p in x[0].split(".")])
    probs = validar(cfg, journal, terc, plano)
    probs = probs_irt + probs
    erros = [p for p in probs if p[2] == "ERRO"]
    mes = int(cfg.get("CFG_MesRep") or 12)
    base = os.path.splitext(saida)[0]
    rel = [f"# Relatório de importação — {cfg.get('CFG_Nome', '')}", "", f"Ficheiro: `{os.path.basename(path)}` · Exercício {cfg.get('CFG_Ano')} · mês de reporte {mes}",
           "", f"- Linhas importadas: **{len(journal)}** · Lançamentos: **{len({l['ID'] for l in journal})}** · Terceiros: {len(terc)} · Activos: {len(act)} · Escalões IRT: {len(irt)}"
           + ("" if irt else " ⚠️ tabela IRT não carregada (calculadora mostrará 'TABELA POR VALIDAR')"),
           f"- Erros bloqueantes: **{len(erros)}** · Avisos: {len(probs) - len(erros)}", ""]
    if probs:
        rel += ["## Problemas por linha do modelo", "", "| Linha | ID | Gravidade | Problema |", "|---|---|---|---|"]
        rel += [f"| {a} | {b} | {'🔴' if g == 'ERRO' else '🟡'} {g} | {m} |" for a, b, g, m in probs[:500]]
        rel.append("")
    gerar = not erros or forcar
    if gerar:
        D.JOURNAL = [{k: v for k, v in l.items() if k != "_linha"} for l in journal]
        D.TERCEIROS = terc or D.TERCEIROS
        D.ACTIVOS = act
        D.PLANO = plano
        esc, ise, fonte = D.irt_tabela(D.ANO)
        D.IRT_ESCALOES, D.IRT_ISENCAO = (irt or esc), ise
        D.IRT_FONTE_ANO = fonte if not irt else "escalões importados do modelo (IRT_ESCALOES)"
        D.ANO = int(cfg.get("CFG_Ano") or D.ANO)
        D.MES_REP = mes
        D.CFG_OVERRIDE.update({k: v for k, v in cfg.items() if v not in (None, "")})
        import importlib
        import sheets_base
        sheets_base.D = D
        import build
        build.main(saida)
        rel += [f"Matriz gerada: `{saida}`", ""]
    else:
        rel += ["**Matriz NÃO gerada**: corrija os erros bloqueantes (ou use `--forcar` para gerar e ver os erros dentro do Excel).", ""]
    # comparação com o sistema actual
    if ref:
        mov, saldo = saldos(journal, plano, mes)
        rel += ["## Comparação com o balancete de referência", "",
                f"Saldos acumulados até ao fim do mês {mes} (D−C).", "", "| Conta | Matriz | Sistema actual | Diferença | Estado |", "|---|---|---|---|---|"]
        dif = 0
        for c, v in ref:
            m = saldo(c)
            ok = abs(m - v) <= TOL
            dif += 0 if ok else 1
            rel.append(f"| {c} | {m:,.2f} | {v:,.2f} | {m - v:,.2f} | {'🟢' if ok else '🔴'} |")
        refc = {c for c, _ in ref}
        fora = [c for c, v in mov.items() if abs(v) > TOL and not any(c == r or c.startswith(r + ".") or (len(r) == 1 and c[:1] == r) for r in refc)]
        rel += ["", f"**Contas com diferença: {dif} de {len(ref)}.**"]
        if fora:
            rel += ["", "Contas com saldo na matriz sem correspondência no balancete de referência: " + ", ".join(sorted(fora))]
        rel += ["", "Leitura: diferenças costumam vir de (1) lançamentos em falta na importação, (2) contas mapeadas de forma diferente, "
                "(3) saldos de abertura, (4) arredondamentos/câmbio. Corrigir na origem e reimportar até 🟢 em todas as contas."]
    with open(base + "_RELATORIO.md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(rel) + "\n")
    print("\n".join(rel[:8]))
    print("Relatório:", base + "_RELATORIO.md")
    return len(erros), ref and dif


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    m = sp.add_parser("modelo")
    m.add_argument("saida", nargs="?", default=os.path.join(ROOT, "dist", "MODELO_IMPORTACAO.xlsx"))
    c = sp.add_parser("carregar")
    c.add_argument("ficheiro")
    c.add_argument("--saida", default=os.path.join(ROOT, "dist", "MATRIZ_IMPORTADA.xlsx"))
    c.add_argument("--forcar", action="store_true", help="gerar a matriz mesmo com erros bloqueantes")
    a = ap.parse_args()
    if a.cmd == "modelo":
        modelo(a.saida)
    else:
        n, _ = carregar(a.ficheiro, a.saida, a.forcar)
        sys.exit(1 if n and not a.forcar else 0)
