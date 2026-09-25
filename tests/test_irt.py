"""Calculadora IRT (11_FISCALIDADE_AGT): Lei 28/20 (≤ 2024), Lei 18/24 Anexo I (2025), 2026 sem escalões (Lei 14/25 por carregar)."""
import os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = os.environ.get("MATRIZ_WORK", "/tmp/claude-0/w/irt")
os.makedirs(W, exist_ok=True)
RECALC = "/root/.claude/skills/synced/340ef685-a7ef-441c-a11a-f5069102cc9b_8be6ce2a-fc99-417e-ab54-d042138b7cfd/xlsx/scripts/recalc.py"
from openpyxl import load_workbook  # noqa: E402
sys.path.insert(0, os.path.join(ROOT, "src"))
import data as D  # noqa: E402

def esperado(mc, ano):
    T, isencao, _ = D.irt_tabela(ano)
    if mc <= isencao:
        return 0
    for lo, hi, pf, tx in reversed(T):
        if mc > lo:
            return pf + (mc - lo) * tx


def calc(ano, bruto):
    base = os.path.join(W, f"irt_{ano}.xlsx")
    if not os.path.exists(base):
        env = dict(os.environ, MATRIZ_ANO=str(ano), MATRIZ_LINHAS="100")
        subprocess.run([sys.executable, os.path.join(ROOT, "src", "build.py"), base], env=env, check=True, capture_output=True)
    wb = load_workbook(base)
    ws = wb["11_FISCALIDADE_AGT"]
    cel = [c for c in ws["I"] if c.value == 400_000][0]
    cel.value = bruto
    f = os.path.join(W, f"irt_{ano}_{bruto}.xlsx")
    wb.save(f)
    subprocess.run([sys.executable, RECALC, f, "300"], capture_output=True)
    v = [c.value for c in load_workbook(f, data_only=True)["11_FISCALIDADE_AGT"]["I"]]
    i = v.index(bruto)
    return v[i + 3], v[i + 5]


ok = True
casos = {2024: (60_000, 100_000, 160_000, 400_000, 1_200_000, 12_000_000),
         2025: (100_000, 110_000, 160_000, 400_000, 1_200_000, 12_000_000)}
fixos = {(2025, 110_000): 870.87, (2025, 400_000): 65_969.81}  # cálculo manual: (106 700−100 001)×13%; 49 250+(388 000−300 001)×19%
for ano, lista in casos.items():
    for bruto in lista:
        mc, irt = calc(ano, bruto)
        e = esperado(bruto * 0.97, ano)
        r = abs(irt - e) < 0.01 and abs(irt - fixos.get((ano, bruto), irt)) < 0.01
        ok &= r
        print(("✅" if r else "❌"), f"{ano} · bruto {bruto:,} · MC {mc:,.0f} · IRT {irt:,.2f} (esperado {e:,.2f})")
for bruto, exp in ((140_000, 0), (400_000, "TABELA POR VALIDAR")):
    mc, irt = calc(2026, bruto)
    r = irt == exp
    ok &= r
    print(("✅" if r else "❌"), f"2026 · bruto {bruto:,} · IRT {irt!r} (esperado {exp!r})")
sys.exit(0 if ok else 1)
