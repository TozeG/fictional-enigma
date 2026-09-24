"""Lê valores de nomes definidos num workbook já recalculado."""
from openpyxl import load_workbook
def load(f):
    wv = load_workbook(f, data_only=True)
    def get(nm):
        dn = wv.defined_names[nm]
        sh, ref = dn.attr_text.split("!")
        sh = sh.strip("'")
        ref = ref.replace("$", "")
        c = wv[sh][ref]
        if isinstance(c, tuple):
            return [x.value for row in c for x in row]
        return c.value
    return wv, get
