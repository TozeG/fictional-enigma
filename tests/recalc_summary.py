"""Recalcula com LibreOffice e resume erros por folha/coluna."""
import json, subprocess, sys, re, collections
SK = "/root/.claude/skills/synced/340ef685-a7ef-441c-a11a-f5069102cc9b_8be6ce2a-fc99-417e-ab54-d042138b7cfd/xlsx/scripts/recalc.py"
f = sys.argv[1]
out = subprocess.run([sys.executable, SK, f, sys.argv[2] if len(sys.argv) > 2 else "600"], capture_output=True, text=True).stdout
j = json.loads(out)
print(j.get("status"), j.get("total_formulas"), "errors:", j.get("total_errors"), j.get("error"))
for et, d in (j.get("error_summary") or {}).items():
    c = collections.Counter(re.sub(r"\d+$", "", x) for x in d["locations"])
    print(et, d["count"], dict(c.most_common(15)))
