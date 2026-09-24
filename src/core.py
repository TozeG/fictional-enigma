"""Utilitários de construção da Matriz PRO MASTER (estilos, nomes, formatação condicional)."""
import re
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, Protection
from openpyxl.utils import get_column_letter
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.formatting.rule import Rule
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.worksheet.datavalidation import DataValidation

FONT = "Arial"
NUM = '#,##0.00;(#,##0.00);"-"'
NUM0 = '#,##0;(#,##0);"-"'
PCT = '0.0%;(0.0%);"-"'
DATE = "dd/mm/yyyy"
MULT = '0.00"x"'

C_INPUT_FONT = "0000FF"
C_INPUT_FILL = "DDEBF7"
C_CALC_FILL = "F2F2F2"
C_HEAD_FILL = "1F3864"
C_SUB_FILL = "D9E1F2"
C_OK = ("C6EFCE", "006100")
C_WARN = ("FFEB9C", "9C5700")
C_ERR = ("FFC7CE", "9C0006")

THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def q(sheet):
    return "'" + sheet + "'"


def font(bold=False, color="000000", size=10, italic=False):
    return Font(name=FONT, bold=bold, color=color, size=size, italic=italic)


def fill(color):
    return PatternFill("solid", start_color=color, end_color=color)


def title(ws, text, subtitle=None, layer=None):
    ws["A1"] = text
    ws["A1"].font = font(True, "1F3864", 14)
    if subtitle:
        ws["A2"] = subtitle
        ws["A2"].font = font(False, "595959", 9, True)
    if layer:
        ws["A3"] = layer
        ws["A3"].font = font(True, "7F7F7F", 8)
    ws.sheet_view.showGridLines = False


def header(ws, row, col, labels, widths=None):
    for i, lab in enumerate(labels):
        c = ws.cell(row=row, column=col + i, value=lab)
        c.font = font(True, "FFFFFF", 9)
        c.fill = fill(C_HEAD_FILL)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BORDER
        if widths:
            ws.column_dimensions[get_column_letter(col + i)].width = widths[i]


def section(ws, row, col, text, span=8):
    c = ws.cell(row=row, column=col, value=text)
    c.font = font(True, "1F3864", 11)
    c.fill = fill(C_SUB_FILL)
    for i in range(1, span):
        ws.cell(row=row, column=col + i).fill = fill(C_SUB_FILL)


def put(ws, ref, value, kind="calc", fmt=None, bold=False, wrap=False, align=None):
    """kind: input | calc | label | link"""
    c = ws[ref] if isinstance(ref, str) else ws.cell(row=ref[0], column=ref[1])
    c.value = value
    if kind == "input":
        c.font = font(bold, C_INPUT_FONT)
        c.fill = fill(C_INPUT_FILL)
        c.protection = Protection(locked=False)
    elif kind == "calc":
        c.font = font(bold)
    elif kind == "grey":
        c.font = font(bold)
        c.fill = fill(C_CALC_FILL)
    elif kind == "label":
        c.font = font(bold)
    elif kind == "note":
        c.font = font(False, "7F7F7F", 8, True)
    if kind in ("input", "calc", "grey"):
        c.border = BORDER
    if fmt:
        c.number_format = fmt
    if wrap or align:
        c.alignment = Alignment(wrap_text=wrap, horizontal=align, vertical="top" if wrap else None)
    return c


def name(wb, nm, sheet, ref):
    dn = DefinedName(nm, attr_text=f"{q(sheet)}!{ref}")
    wb.defined_names[nm] = dn


def abs_ref(col, r0, r1=None):
    if r1 is None:
        return f"${col}${r0}"
    return f"${col}${r0}:${col}${r1}"


def status_cf(ws, rng):
    """Semáforo por texto: vermelho / amarelo / verde."""
    tl = rng.split(":")[0].replace("$", "")
    rules = [
        (["ERRO", "🔴", "BLOQUEADO", "CRÍTICO", "Violação", "INCONSISTENTE"], C_ERR),
        (["🟡", "ATENÇÃO", "PENDEN", "Por aprovar", "POR VALIDAR", "Pendente", "INCOMPLETO"], C_WARN),
        (["🟢", "OK", "CONFORME", "Validado", "ENCERRADO", "Normal"], C_OK),
    ]
    for words, (bg, fg) in rules:
        for w in words:
            dxf = DifferentialStyle(font=Font(name=FONT, color=fg, bold=True), fill=PatternFill("solid", start_color=bg, end_color=bg, bgColor=bg))
            rule = Rule(type="containsText", operator="containsText", text=w, dxf=dxf, stopIfTrue=True)
            rule.formula = [f'NOT(ISERROR(SEARCH("{w}",{tl})))']
            ws.conditional_formatting.add(rng, rule)


def value_cf(ws, rng, formula, colors):
    bg, fg = colors
    dxf = DifferentialStyle(font=Font(name=FONT, color=fg, bold=True), fill=PatternFill("solid", start_color=bg, end_color=bg, bgColor=bg))
    rule = Rule(type="expression", dxf=dxf, stopIfTrue=True)
    rule.formula = [formula]
    ws.conditional_formatting.add(rng, rule)


def dv_list(ws, rng, source, allow_blank=True):
    dv = DataValidation(type="list", formula1=source, allow_blank=allow_blank, showErrorMessage=True,
                        errorTitle="Valor inválido", error="Seleccione um valor da lista parametrizada.")
    ws.add_data_validation(dv)
    dv.add(rng)
    return dv


def protect(ws):
    ws.protection.sheet = True
    ws.protection.formatColumns = False
    ws.protection.formatRows = False
    ws.protection.autoFilter = False
    ws.protection.sort = False


TOKEN = re.compile(r"\[([A-Za-z0-9_]+)(-1)?\]|\{([A-Za-z0-9_]+)\}")


def render(template, cols, r):
    """[X] -> coluna X na linha r ; [X-1] -> linha anterior ; {X} -> letra da coluna."""
    def rep(m):
        if m.group(3):
            return cols[m.group(3)]
        col = cols[m.group(1)]
        return f"{col}{r - 1 if m.group(2) else r}"
    return TOKEN.sub(rep, template)
