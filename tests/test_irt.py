"""Calculadora IRT (11_FISCALIDADE_AGT): tabela da Lei n.º 28/20 para exercícios ≤ 2025; 2026 sem escalões (Anexo I da Lei 14/25 por carregar)."""
import os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = os.environ.get("MATRIZ_WORK", "/tmp/claude-0/w/irt")
os.makedirs(W, exist_ok=True)
RECALC = "/root/.claude/skills/synced/340ef685-a7ef-441c-a11a-f5069102cc9b_8be6ce2a-fc99-417e-ab54-d042138b7cfd/xlsx/scripts/recalc.py"
from openpyxl import load_workbook  # noqa: E402
sys.path.insert(0, os.path.join(ROOT, "src"))
T = [(0, 70_000, 0, 0.0), (70_000, 100_000, 3_000, 0.10), (100_000, 150_000, 6_000, 0.13), (150_000, 200_000, 12_500, 0.16),
     (200_000, 300_000, 31_250, 0.18), (300_000, 500_000, 49_250, 0.19), (500_000, 1_000_000, 87_250, 0.20),
     (1_000_000, 1_500_000, 187_250, 0.21), (1_500_000, 2_000_000, 292_000, 0.22), (2_000_000, 2_500_000, 402_250, 0.23),
     (2_500_000, 5_000_000, 517_250, 0.24), (5_000_000, 10_000_000, 1_117_250, 0.245), (10_000_000, None, 2_342_250, 0.25)]


def esperado(mc, isencao):
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
for bruto in (60_000, 100_000, 160_000, 400_000, 1_200_000, 12_000_000):
    mc, irt = calc(2025, bruto)
    e = esperado(bruto * 0.97, 70_000)
    r = abs(irt - e) < 0.01
    ok &= r
    print(("✅" if r else "❌"), f"2025 · bruto {bruto:,} · MC {mc:,.0f} · IRT {irt:,.2f} (esperado {e:,.2f})")
for bruto, exp in ((140_000, 0), (400_000, "TABELA POR VALIDAR")):
    mc, irt = calc(2026, bruto)
    r = irt == exp
    ok &= r
    print(("✅" if r else "❌"), f"2026 · bruto {bruto:,} · IRT {irt!r} (esperado {exp!r})")
sys.exit(0 if ok else 1)
