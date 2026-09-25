"""Validação da Matriz PRO MASTER.

1. Constrói a matriz com os casos de teste, recalcula com LibreOffice e compara ~200 valores com um
   modelo contabilístico independente escrito em Python (a partir de src/data.py).
2. Testes negativos: injecta erros no Diário e confirma que o sistema os detecta/bloqueia.
3. Escreve docs/09_RELATORIO_VALIDACAO.md.

Uso: python tests/verify.py
"""
import copy
import json
import os
import subprocess
import sys
from collections import defaultdict
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "tests"))
os.environ.setdefault("MATRIZ_LINHAS", "200")
os.environ.setdefault("MATRIZ_OPERACOES", "40")

import data as D  # noqa: E402
import build  # noqa: E402
from names import load  # noqa: E402

RECALC = "/root/.claude/skills/synced/340ef685-a7ef-441c-a11a-f5069102cc9b_8be6ce2a-fc99-417e-ab54-d042138b7cfd/xlsx/scripts/recalc.py"
WORK = os.environ.get("MATRIZ_WORK", "/tmp/claude-0/w/verify")
os.makedirs(WORK, exist_ok=True)
REF = date(D.ANO, 3, 31)
MESREP = 3
TOL = 0.01
results = []


def recalc(path):
    out = subprocess.run([sys.executable, RECALC, path, "600"], capture_output=True, text=True).stdout
    return json.loads(out)


def check(area, desc, got, exp, tol=TOL):
    ok = (abs((got or 0) - exp) <= tol) if isinstance(exp, (int, float)) else (str(exp) in str(got))
    results.append((area, desc, got, exp, ok))
    return ok


# ------------------------------------------------------------------ modelo independente
def model(journal):
    nat = {n[0]: n for n in D.NATUREZAS}
    tipo = {c: t for c, _, t in D.PLANO}
    M = {}
    M["dr"] = defaultdict(float)          # (rubrica, mês) -> valor (proveitos +)
    M["bal"] = defaultdict(float)         # conta -> saldo D-C até REF
    M["abe"] = defaultdict(float)
    M["iva"] = defaultdict(float)         # (linha, mês)
    M["dfc"] = defaultdict(float)
    M["cash_open"] = 0.0
    for l in journal:
        dc = (l["Deb"] or 0) - (l["Cred"] or 0)
        c = l["Conta"]
        n = nat[l["Nat"]]
        m = l["Data"].month
        if l["Data"] <= REF:
            M["bal"][c] += dc
        if l["Nat"] == "Abertura":
            M["abe"][c] += dc
        r = D.classify(c)[4]
        if r and n[3] == "S" and m <= MESREP:
            M["dr"][(r, m)] += -dc
        if l["Nat"] != "Apuramento de IVA":
            if c == "34.5.3":
                M["iva"][("LIQ", m)] += -dc
            if c == "34.5.2":
                M["iva"][("DED", m)] += dc
            if c == "34.5.4.1":
                M["iva"][("REGSP", m)] += dc
        if c[:2] in ("43", "45"):
            if l["Nat"] == "Abertura":
                M["cash_open"] += dc
            elif m <= MESREP:
                M["dfc"][n[2]] += dc
    # balanço por rubrica
    bs = defaultdict(float)
    for c, s in M["bal"].items():
        _, _, rd, rc, *_ = D.classify(c)
        side = "A" if rd.startswith("BA_") else "P"
        if s > 0:
            bs[rd] += s if rd.startswith("BA_") else -s
        elif s < 0:
            bs[rc] += s if rc.startswith("BA_") else -s
    M["bs"] = bs
    # clientes / fornecedores
    def openitems(g2, side):
        items = {}
        for l in journal:
            if l["Conta"][:2] == g2 and (l[side] or 0) > 0 and not l["Ref"] and l["Data"] <= REF:
                items[l["ID"]] = l[side]
        other = "Cred" if side == "Deb" else "Deb"
        for l in journal:
            if l["Conta"][:2] == g2 and l["Ref"] and l["Data"] <= REF:
                items[l["Ref"]] -= (l[other] or 0) - (l[side] or 0)
        return items
    M["cli"] = openitems("31", "Deb")
    M["frn"] = openitems("32", "Cred")
    # inventário
    q = v = 0.0
    for l in journal:
        if l["Artigo"] == "A001" and l["Conta"][0] == "2":
            q += l["Qtd"] or 0
            v += (l["Deb"] or 0) - (l["Cred"] or 0)
    M["inv"] = (q, v)
    rai = sum(val for (r, m), val in M["dr"].items() if r != "DR13")
    M["rai"] = rai
    M["ii"] = round(max(0, rai) * 0.25, 2)
    M["rl"] = sum(M["dr"].values())
    return M


def read_rows(ws, keycol, valcols, r0=1, r1=None, strip=True):
    out = {}
    for row in ws.iter_rows(min_row=r0, max_row=r1 or ws.max_row):
        k = row[keycol].value
        if k is None:
            continue
        k = str(k).strip() if strip else k
        out[k] = [row[c].value for c in valcols]
    return out


def verify_baseline():
    path = os.path.join(WORK, "base.xlsx")
    build.main(path)
    rc = recalc(path)
    results.append(("Recálculo", f"{rc.get('total_formulas')} fórmulas, erros = {rc.get('total_errors')}", rc.get("total_errors"), 0, rc.get("total_errors") == 0))
    wv, g = load(path)
    M = model(D.JOURNAL)
    # DR mensal por rubrica
    dre = read_rows(wv["22_DRE"], 0, list(range(2, 14)), 6, 40)
    for (r, m), val in sorted(M["dr"].items()):
        check("DR mensal", f"{r} mês {m}", dre[r][m - 1], val)
    check("DR", "Resultado antes de impostos (acum.)", g("DR_RAI"), M["rai"])
    check("DR", "Resultado líquido (acum.)", g("DR_RL"), M["rl"])
    # Balanço por rubrica
    bsr = read_rows(wv["21_BALANÇO"], 0, [2], 6, 60)
    for code, *_ in D.RUBRICAS_BAL:
        check("Balanço", code, bsr[code][0], M["bs"].get(code, 0.0))
    check("Balanço", "Activo = CP + Passivo", g("BS_Check"), "🟢")
    check("Balanço", "Activo total", g("BS_AT"), sum(v for k, v in M["bs"].items() if k.startswith("BA_")))
    # Plano (saldos por conta de movimento)
    pc = read_rows(wv["01_PLANO_CONTAS"], 0, [4, 20], 6, 405)
    for c, s in sorted(M["bal"].items()):
        check("Razão/Plano", f"saldo {c}", pc[c][1], s)
    # IVA mensal
    ivaws = wv["12_IVA"]
    iv = read_rows(ivaws, 0, list(range(1, 13)), 6, 60)
    lab = {"LIQ": "IVA liquidado (contabilidade, 34.5.3)", "DED": "IVA dedutível (contabilidade, 34.5.2)", "REGSP": "Regularizações a favor do sujeito passivo (34.5.4.1)"}
    for (k, m), val in sorted(M["iva"].items()):
        check("IVA mensal", f"{k} mês {m}", iv[lab[k]][m - 1], val)
    tot = sum(M["iva"][("LIQ", m)] - M["iva"][("DED", m)] - M["iva"][("REGSP", m)] for m in (1, 2, 3))
    check("IVA", "IVA a pagar acumulado", g("IVA_PagarAcum"), tot)
    check("IVA", "Conciliação contabilidade × mapa", g("IVA_Estado"), "🟢")
    # DFC
    dfc = read_rows(wv["23_DFC"], 0, [1], 6, 40)
    for linha, val in M["dfc"].items():
        check("DFC", linha, dfc[linha][0], val)
    check("DFC", "Caixa no fim do período", g("DFC_Fim"), M["cash_open"] + sum(M["dfc"].values()))
    check("DFC", "DFC = saldo das contas de meios monetários", g("DFC_Estado"), "🟢")
    # clientes / fornecedores
    cli = read_rows(wv["07_CLIENTES"], 2, [10], 26, 325)
    for k, v in M["cli"].items():
        check("Clientes", f"saldo em aberto doc ID {k}", cli[str(k)][0], v)
    check("Clientes", "Auxiliar = Razão (conta 31)", g("CLI_Estado"), "🟢")
    frn = read_rows(wv["08_FORNECEDORES"], 2, [10], 26, 325)
    for k, v in M["frn"].items():
        check("Fornecedores", f"saldo em aberto doc ID {k}", frn[str(k)][0], v)
    check("Fornecedores", "Auxiliar = Razão (conta 32)", g("FRN_Estado"), "🟢")
    # inventário
    inv = read_rows(wv["09_INVENTÁRIOS"], 0, [12, 13], 6, 35)
    check("Inventário", "A001 quantidade final", inv["A001"][0], M["inv"][0])
    check("Inventário", "A001 valor", inv["A001"][1], M["inv"][1])
    check("Inventário", "Kardex: saídas ao custo médio ponderado", wv["09_INVENTÁRIOS"]["H42"].value, 0)
    # activos
    af = wv["10_ACTIVOS_FIXOS"]
    check("Activos", "AF001 depreciação acumulada 31/03", af["W6"].value, 50_000)
    check("Activos", "AF001 VLC", af["Y6"].value, 1_150_000)
    check("Activos", "Registo = contabilidade", g("AF_Estado"), "🟢")
    # imposto industrial
    check("Imposto Industrial", "Matéria colectável", g("II_MC"), M["rai"])
    check("Imposto Industrial", "Imposto estimado (25%)", g("II_Estimado"), M["ii"])
    check("Imposto Industrial", "A pagar após retenções (195 000)", g("II_APagar"), M["ii"] - 195_000)
    check("Imposto Industrial", "Contabilizado = estimado", g("II_Estado"), "🟢")
    # caixa, bancos, retenções, facturação
    check("Caixa", "Saldo 45.1", g("CX_Saldo"), M["bal"]["45.1"])
    check("Bancos", "Saldo contabilístico 43", g("BK_Saldo"), M["bal"]["43.1.1"])
    check("Bancos", "Diferença de reconciliação", g("BK_Dif"), 0)
    check("Bancos", "Item pendente detectado (despesa 2 500 não contabilizada)", g("BK_Pend"), 1)
    check("Retenções", "6,5% sobre 3 000 000", g("RET_Sofridas"), 195_000)
    fat = [c.value for c in wv["13_FACTURAÇÃO_FISCAL"]["T"][11:19]]
    check("Facturação", "8 documentos emitidos no registo", g("FAT_Estado") and sum(1 for x in fat if x), 8)
    check("Facturação", "Erro de comunicação AGT detectado (FR A/2)", "|".join(str(x) for x in fat), "🔴 Erro de comunicação")
    check("Facturação", "Comunicação pendente detectada (FT A/3)", "|".join(str(x) for x in fat), "🟡 Comunicação pendente")
    # provas globais 99
    ws99 = wv["99_CONTROLO_SISTEMA"]
    for row in ws99.iter_rows(min_row=30, max_row=50):
        if row[7].value and row[1].value and row[7].value != "Estado":
            check("Reconciliação global", row[1].value, row[7].value, "🟢 Provado")
    for row in ws99.iter_rows(min_row=6, max_row=27):
        if row[3].value == "S":
            check("Integridade (críticas)", row[1].value, row[2].value, "🟢")
    check("Sistema", "Estado global (esperado: pendências intencionais, sem bloqueio)", g("SYS_Estado"), "🟡 SISTEMA COM PENDÊNCIAS")
    # investimento / sensibilidade / encerramento
    check("Investimentos", "Grelha de sensibilidade reproduz o VAL do modelo", g("INV_SensEst"), "🟢")
    check("Encerramento", "Apuramento proposto equilibrado", g("ENC_Estado"), "🟢")
    check("Encerramento", "Resultado apurado = RL da DR", g("ENC_RL"), M["rl"])
    check("Encerramento", "Abertura N+1 equilibrada", g("ENC_AbeEstado"), "🟢")
    return g


def neg(label, mutate, expect_text, expect_sys="🔴 SISTEMA BLOQUEADO"):
    j = copy.deepcopy(D.JOURNAL)
    mutate(j)
    orig = D.JOURNAL
    D.JOURNAL = j
    import sheets_base
    sheets_base.D.JOURNAL = j
    try:
        path = os.path.join(WORK, f"neg_{len(results)}.xlsx")
        build.main(path)
    finally:
        D.JOURNAL = orig
        sheets_base.D.JOURNAL = orig
    recalc(path)
    wv, g = load(path)
    errs = " | ".join(str(x) for x in g("J_Erros") if x)
    check("Teste negativo", label + " → erro detectado no Diário", errs, expect_text)
    if expect_sys:
        check("Teste negativo", label + " → estado do sistema", g("SYS_Estado"), expect_sys)


def verify_negative():
    def unbalanced(j):
        j[6]["Cred"] = 99_999
    neg("Lançamento desequilibrado (FR A/1 crédito alterado)", unbalanced, "LANÇAMENTO NÃO EQUILIBRADO")

    def dup(j):
        extra = [copy.deepcopy(x) for x in j if x["ID"] == 4]
        for x in extra:
            x["ID"] = 99
        j.extend(extra)
    neg("Factura de fornecedor lançada em duplicado", dup, "Documento duplicado")

    def badacc(j):
        j[6]["Conta"] = "61.9"
    neg("Conta inexistente", badacc, "Conta inexistente")

    def agg(j):
        j[6]["Conta"] = "61"
    neg("Movimento em conta de agregação", agg, "Conta não movimentável")

    def closed(j):
        j[6]["DtAlt"] = date(D.ANO, 3, 15)
    neg("Alteração em Janeiro após o fecho (10/02)", closed, "Alteração em período encerrado")

    def rate(j):
        j[7]["Cred"] = 15_000
        j[6]["Cred"] = 99_000
    neg("IVA com taxa incompatível (15 000 em vez de 14 000)", rate, "Taxa fiscal incompatível")

    def nif(j):
        for x in j:
            if x["ID"] == 3 and x["Conta"] == "31.1.1":
                x["NIF"] = ""
    neg("Venda a crédito sem NIF do cliente", nif, "NIF inválido")

    def sup(j):
        j[6]["Suporte"] = ""
    neg("Lançamento sem documento de suporte", sup, "Sem documento de suporte")

    def year(j):
        for x in j:
            if x["ID"] == 5:
                x["Data"] = date(D.ANO + 1, 1, 15)
    neg("Lançamento fora do exercício", year, "Fora do exercício")

    def fx(j):
        for x in j:
            if x["ID"] == 17 and x["Conta"] == "32.1.2":
                x["Cambio"] = 950
    neg("Câmbio inconsistente (valor ME × câmbio ≠ Kz)", fx, "Câmbio inconsistente")


def write_report():
    ok = sum(1 for r in results if r[4])
    lines = ["# 09 — Relatório de Validação", "",
             f"Gerado automaticamente por `tests/verify.py` em {date.today().isoformat()}.",
             "",
             "Método: a matriz é gerada com os casos de teste, recalculada com o LibreOffice Calc (motor independente do Excel) e cada valor",
             "é comparado com um modelo contabilístico independente escrito em Python a partir dos mesmos lançamentos. Os testes negativos",
             "injectam erros no Diário e confirmam que o sistema os detecta.", "",
             f"**Resultado: {ok} / {len(results)} verificações aprovadas.**", "",
             "| Área | Verificação | Obtido | Esperado | Resultado |", "|---|---|---|---|---|"]
    for a, d_, got, exp, k in results:
        fmt = lambda x: f"{x:,.2f}" if isinstance(x, (int, float)) and not isinstance(x, bool) else str(x)[:70].replace("|", "/")
        lines.append(f"| {a} | {d_} | {fmt(got)} | {fmt(exp)} | {'✅' if k else '❌'} |")
    p = os.path.join(ROOT, "docs", "09_RELATORIO_VALIDACAO.md")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"{ok}/{len(results)} OK — relatório: {p}")
    return ok == len(results)


if __name__ == "__main__":
    verify_baseline()
    if "--quick" not in sys.argv:
        verify_negative()
    for r in results:
        if not r[4]:
            print("FALHOU:", r)
    sys.exit(0 if write_report() else 1)
