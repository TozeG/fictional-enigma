"""Equivalência: o cenário de demonstração registado por OPERAÇÕES (02A) dá os mesmos resultados que lançado à mão no Diário.

18 operações substituem os lançamentos manuais equivalentes; ficam manuais os especiais (abertura, NC, moeda estrangeira,
diferimentos, retenções, apuramento do IVA, estimativa de imposto). Tolerância 0,05 Kz: o custo médio automático é
104 385,96 (arredondamento a cêntimos) contra 104 386 lançado à mão.
"""
import copy
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "tests"))
os.environ.setdefault("MATRIZ_LINHAS", "200")
os.environ.setdefault("MATRIZ_OPERACOES", "40")
import data as D  # noqa: E402
import build  # noqa: E402
from names import load  # noqa: E402

W = os.environ.get("MATRIZ_WORK", "/tmp/claude-0/w/ops")
os.makedirs(W, exist_ok=True)
RECALC = "/root/.claude/skills/synced/340ef685-a7ef-441c-a11a-f5069102cc9b_8be6ce2a-fc99-417e-ab54-d042138b7cfd/xlsx/scripts/recalc.py"
NAMES = ["DR_Rec", "DR_RO", "DR_RAI", "DR_RL", "BS_AT", "BS_CP", "BS_PT", "IVA_PagarAcum", "CLI_Total", "FRN_Total", "DFC_Op", "DFC_Inv",
         "DFC_Fin", "DFC_Fim", "CX_Saldo", "BK_Saldo", "II_Estimado", "FIS_Total"] + ["BS_" + r[0] for r in D.RUBRICAS_BAL]
STATES = ["BS_Check", "IVA_Estado", "CLI_Estado", "FRN_Estado", "INV_Estado", "AF_Estado", "FC_Estado", "DFC_Estado", "BT_Estado", "DR_Estado"]


def cenario_operacoes():
    return D.demo_operacoes()


def gerar(path, ops=None, manual=None):
    orig = (D.JOURNAL, D.OPERACOES)
    if ops is not None:
        D.JOURNAL, D.OPERACOES = manual, ops
    try:
        build.main(path)
    finally:
        D.JOURNAL, D.OPERACOES = orig
    rc = json.loads(subprocess.run([sys.executable, RECALC, path, "600"], capture_output=True, text=True).stdout)
    return rc, load(path)


if __name__ == "__main__":
    ok = []
    rcA, (wa, ga) = gerar(os.path.join(W, "manual.xlsx"))
    ops, manual = cenario_operacoes()
    rcB, (wb, gb) = gerar(os.path.join(W, "operacoes.xlsx"), ops, manual)
    ok.append(("fórmulas sem erros (operações)", rcB.get("total_errors") == 0, rcB.get("total_errors")))
    for n in NAMES:
        a, b = ga(n) or 0, gb(n) or 0
        ok.append((f"{n}: manual {a:,.2f} = operações {b:,.2f}", abs(a - b) <= 0.05, b - a))
    for n in STATES:
        ok.append((f"{n}: {gb(n)}", str(gb(n)).startswith("🟢"), None))
    import sheets_ops
    est = [wb["02A_OPERAÇÕES"][f"{sheets_ops.OC['Estado']}{sheets_ops.OR0 + i}"].value for i in range(len(ops))]
    ok.append((f"18 operações registadas sem erro", sum(1 for e in est if str(e).startswith("🔴")) == 0 and len([e for e in est if e]) == 18, est))
    ok.append(("nenhuma linha do Diário com erro", sum(x or 0 for x in gb("J_ErrFlag")) == 0, None))
    ok.append(("kardex: custo das saídas = custo médio", wb["09_INVENTÁRIOS"]["H42"].value == 0, wb["09_INVENTÁRIOS"]["H42"].value))
    ok.append((f"sistema: {gb('SYS_Estado')}", "BLOQUEADO" not in str(gb("SYS_Estado")), None))
    for d, r, x in ok:
        print(("✅ " if r else "❌ ") + d + ("" if r or x is None else f"  → {x}"))
    n = sum(1 for _, r, _ in ok if r)
    print(f"{n}/{len(ok)} OK")
    sys.exit(0 if n == len(ok) else 1)
