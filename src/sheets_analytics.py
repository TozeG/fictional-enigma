"""Camada analítica: KPI, sustentabilidade, dashboard, planeamento, projectos, investimentos, risco e break-even."""
from openpyxl.utils import get_column_letter as CL
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.chart.series import SeriesLabel
from core import *
from sheets_ledgers import MESES
import data as D

S17, S24, S25, S26, S27, S28, S29, S36 = ("17_PLANEAMENTO_FINANCEIRO", "24_GESTÃO_DE_PROJECTOS", "25_ANÁLISE_DE_INVESTIMENTOS", "26_RISCO_FINANCEIRO",
                                          "27_SUSTENTABILIDADE", "28_KPI_FINANCEIROS", "29_DASHBOARD_EXECUTIVO", "36_BREAK_EVEN")

DIVIDA = "(BS_BPNC_EMP+BS_BPC_EMP)"
LIQ = "(BS_BA_DISP+BS_BA_APLIC)"


def sem(v, verde, verm, sentido):
    """Fórmula de semáforo parametrizável."""
    return (f'=IF(NOT(ISNUMBER({v})),"—",IF({sentido}="Maior",IF({v}>={verde},"🟢 Normal",IF({v}<{verm},"🔴 Crítico","🟡 Atenção")),'
            f'IF({v}<={verde},"🟢 Normal",IF({v}>{verm},"🔴 Crítico","🟡 Atenção"))))')


def build_kpi(wb):
    ws = wb.create_sheet(S28)
    title(ws, "28 — KPI FINANCEIROS", "Valores acumulados até ao mês de reporte; fluxos anualizados quando comparados com saldos. Limites = parâmetros da entidade (não universais).",
          "CAMADA 3 — OUTPUT (limites = input)")
    heads = ["Categoria", "Indicador", "Fórmula", "Valor", "Unidade", "Limite verde", "Limite vermelho", "Sentido (Maior/Menor é melhor)", "Semáforo", "Nome"]
    header(ws, 5, 1, heads, [14, 30, 52, 14, 8, 12, 12, 12, 16, 12])
    k = [
        ("Rentabilidade", "ROA", "RL anualizado / Activo total", "=IF(BS_AT=0,0,DR_RL*CFG_Anual/BS_AT)", PCT, 0.05, 0.0, "Maior", "K_ROA"),
        ("Rentabilidade", "ROE", "RL anualizado / Capital próprio", "=IF(BS_CP<=0,0,DR_RL*CFG_Anual/BS_CP)", PCT, 0.12, 0.0, "Maior", "K_ROE"),
        ("Rentabilidade", "ROIC", "EBIT×(1−t) anualizado / (CP + dívida − liquidez)", f"=IF((BS_CP+{DIVIDA}-{LIQ})<=0,0,DR_RO*(1-TX_II)*CFG_Anual/(BS_CP+{DIVIDA}-{LIQ}))", PCT, 0.12, 0.05, "Maior", "K_ROIC"),
        ("Rentabilidade", "Margem bruta", "(Receita − CMV) / Receita", "=DR_MB", PCT, 0.30, 0.15, "Maior", "K_MB"),
        ("Rentabilidade", "Margem EBITDA", "EBITDA / Receita", "=DR_MEBITDA", PCT, 0.15, 0.05, "Maior", "K_MEBITDA"),
        ("Rentabilidade", "Margem operacional", "EBIT / Receita", "=DR_MO", PCT, 0.10, 0.03, "Maior", "K_MO"),
        ("Rentabilidade", "Margem líquida", "RL / Receita", "=DR_ML", PCT, "=CFG_MargMin", 0.0, "Maior", "K_ML"),
        ("Liquidez", "Liquidez geral", "Activo corrente / Passivo corrente", "=IF(BS_PC=0,0,BS_AC/BS_PC)", MULT, 1.5, 1.0, "Maior", "K_LG"),
        ("Liquidez", "Liquidez reduzida", "(AC − Existências) / PC", "=IF(BS_PC=0,0,(BS_AC-BS_BA_EXIST)/BS_PC)", MULT, 1.0, 0.7, "Maior", "K_LR"),
        ("Liquidez", "Liquidez imediata", "(Disponibilidades + aplicações) / PC", f"=IF(BS_PC=0,0,{LIQ}/BS_PC)", MULT, 0.3, 0.1, "Maior", "K_LI"),
        ("Estrutura", "Autonomia financeira", "Capital próprio / Activo", "=IF(BS_AT=0,0,BS_CP/BS_AT)", PCT, 0.40, 0.20, "Maior", "K_AF"),
        ("Estrutura", "Endividamento", "Passivo / Activo", "=IF(BS_AT=0,0,BS_PT/BS_AT)", PCT, 0.60, 0.80, "Menor", "K_END"),
        ("Estrutura", "Solvabilidade", "Capital próprio / Passivo", "=IF(BS_PT=0,0,BS_CP/BS_PT)", MULT, 0.7, 0.25, "Maior", "K_SOLV"),
        ("Estrutura", "Cobertura de juros", "EBIT / Custos financeiros", "=IF(DR_Juros=0,99,DR_RO/ABS(DR_Juros))", MULT, 3.0, 1.5, "Maior", "K_COB"),
        ("Estrutura", "Dívida financeira / EBITDA", "Dívida / EBITDA anualizado", f"=IF(DR_EBITDA<=0,99,{DIVIDA}/(DR_EBITDA*CFG_Anual))", MULT, 2.0, "=CFG_DivEBITDA", "Menor", "K_DEB"),
        ("Eficiência", "PMR (dias)", "Clientes / facturação × dias", "=CLI_PM", "0", "=CFG_PMRalvo", "=CFG_PMRalvo*2", "Menor", "K_PMR"),
        ("Eficiência", "PMP (dias)", "Fornecedores / compras × dias", "=FRN_PM", "0", "=CFG_PMPalvo", "=CFG_PMPalvo*2", "Menor", "K_PMP"),
        ("Eficiência", "Rotação de inventários", "CMV anualizado / Existências", "=IF(BS_BA_EXIST=0,0,ABS(DR_CMV)*CFG_Anual/BS_BA_EXIST)", MULT, 6, 3, "Maior", "K_ROT"),
        ("Eficiência", "Prazo médio de stocks (dias)", "Existências / CMV × dias", "=IF(DR_CMV=0,0,BS_BA_EXIST/ABS(DR_CMV)*CFG_Dias)", "0", 60, 120, "Menor", "K_PMS"),
        ("Eficiência", "Ciclo operacional (dias)", "PMS + PMR", "=K_PMS+K_PMR", "0", 90, 150, "Menor", "K_CO"),
        ("Eficiência", "Ciclo financeiro (dias)", "Ciclo operacional − PMP", "=K_CO-K_PMP", "0", 45, 90, "Menor", "K_CF"),
        ("Crescimento", "Crescimento das vendas", "Receita anualizada / Receita N−1 − 1", "=IF(CFG_VendasN1=0,0,DR_Rec*CFG_Anual/CFG_VendasN1-1)", PCT, 0.05, 0.0, "Maior", "K_GV"),
        ("Crescimento", "Crescimento do EBITDA", "EBITDA anualizado / EBITDA N−1 − 1", "=IF(CFG_EBITDAN1=0,0,DR_EBITDA*CFG_Anual/CFG_EBITDAN1-1)", PCT, 0.05, 0.0, "Maior", "K_GE"),
        ("Crescimento", "Crescimento do activo", "Activo / Activo de abertura − 1", "=IF(BSA_AT=0,0,BS_AT/BSA_AT-1)", PCT, 0.0, -0.10, "Maior", "K_GA"),
        ("Crescimento", "Crescimento do capital próprio", "CP / CP de abertura − 1", "=IF(BSA_CP=0,0,BS_CP/BSA_CP-1)", PCT, 0.0, -0.10, "Maior", "K_GCP"),
    ]
    for i, (cat, ind, txt, f, fmt, ve, vr, sen, nm) in enumerate(k):
        r = 6 + i
        put(ws, (r, 1), cat, "label")
        put(ws, (r, 2), ind, "label", bold=True)
        put(ws, (r, 3), txt, "note")
        put(ws, (r, 4), f, "calc", fmt)
        put(ws, (r, 5), {PCT: "%", MULT: "x", "0": "dias"}.get(fmt, ""), "label")
        put(ws, (r, 6), ve, "input", fmt)
        put(ws, (r, 7), vr, "input", fmt)
        put(ws, (r, 8), sen, "input")
        put(ws, (r, 9), sem(f"D{r}", f"F{r}", f"G{r}", f"H{r}"), "calc")
        put(ws, (r, 10), nm, "note")
        name(wb, nm, S28, f"$D${r}")
        name(wb, nm + "_S", S28, f"$I${r}")
    status_cf(ws, f"I6:I{5 + len(k)}")
    dv_list(ws, f"H6:H{5 + len(k)}", '"Maior,Menor"')
    r = 7 + len(k)
    put(ws, (r, 1), "Nota: limites iniciais = referências técnicas genéricas. Devem ser recalibrados pela Administração em função do sector, covenants bancários e política de risco da entidade.", "note")
    put(ws, (r + 1, 1), "Indicadores críticos (🔴)", "label", bold=True)
    put(ws, (r + 1, 4), f'=COUNTIF(I6:I{5 + len(k)},"🔴*")', "grey", "0")
    name(wb, "K_Red", S28, f"$D${r + 1}")
    put(ws, (r + 2, 1), "Indicadores em atenção (🟡)", "label")
    put(ws, (r + 2, 4), f'=COUNTIF(I6:I{5 + len(k)},"🟡*")', "grey", "0")
    name(wb, "K_Yellow", S28, f"$D${r + 2}")
    name(wb, "K_Tab", S28, f"$B$6:$I${5 + len(k)}")
    protect(ws)


def build_sustentabilidade(wb):
    ws = wb.create_sheet(S27)
    title(ws, "27 — SUSTENTABILIDADE ECONÓMICO-FINANCEIRA", "Equilíbrio financeiro (CCL vs NFM), capacidade de autofinanciamento e geração de caixa.", "CAMADA 3 — OUTPUT")
    header(ws, 5, 1, ["Indicador", "Valor", "Semáforo / leitura"], [48, 18, 60])
    rows = [
        ("Autonomia financeira", "=K_AF", PCT, "=K_AF_S"), ("Solvabilidade", "=K_SOLV", MULT, "=K_SOLV_S"), ("Liquidez geral", "=K_LG", MULT, "=K_LG_S"),
        ("Liquidez reduzida", "=K_LR", MULT, "=K_LR_S"), ("Liquidez imediata", "=K_LI", MULT, "=K_LI_S"), ("Endividamento", "=K_END", PCT, "=K_END_S"),
        ("Cobertura de juros", "=K_COB", MULT, "=K_COB_S"),
        ("Capacidade de autofinanciamento (RL + amortizações + provisões)", "=DR_RL-DR_Amort", NUM, '=IF(B13>0,"🟢 Gera meios internos","🔴 Não gera meios internos")'),
        ("Geração de caixa operacional (DFC)", "=DFC_Op", NUM, '=IF(B14>0,"🟢 Operação gera caixa","🔴 Operação consome caixa")'),
        ("Margem líquida", "=K_ML", PCT, "=K_ML_S"), ("ROA", "=K_ROA", PCT, "=K_ROA_S"), ("ROE", "=K_ROE", PCT, "=K_ROE_S"), ("ROIC", "=K_ROIC", PCT, "=K_ROIC_S"),
        ("EBITDA (acumulado)", "=DR_EBITDA", NUM, '=IF(B19>0,"🟢 Positivo","🔴 Negativo")'), ("Ciclo financeiro (dias)", "=K_CF", "0", "=K_CF_S"),
        ("Capital circulante líquido (AC − PC)", "=BS_AC-BS_PC", NUM, '=IF(B21>0,"🟢 Fundo de maneio positivo","🔴 Fundo de maneio negativo")'),
        ("Necessidades de fundo de maneio (NFM)", "=(BS_BA_EXIST+BS_BA_CLIENTES+BS_BA_ESTADO+BS_BA_OUTROS_REC+BS_BA_ACRESC)-(BS_BPC_FORN+BS_BPC_ESTADO+BS_BPC_OUTROS+BS_BPC_ACRESC)", NUM, '=IF(B22>0,"NFM positivas: o ciclo de exploração consome recursos","NFM negativas: o ciclo de exploração gera recursos")'),
        ("Tesouraria líquida (CCL − NFM)", "=B21-B22", NUM, '=IF(B23>=0,"🟢 Equilíbrio financeiro: NFM cobertas por capitais permanentes","🔴 Desequilíbrio: NFM financiadas por dívida de curto prazo")'),
    ]
    for i, (lab, f, fmt, s) in enumerate(rows):
        r = 6 + i
        put(ws, (r, 1), lab, "label")
        put(ws, (r, 2), f, "calc", fmt)
        put(ws, (r, 3), s, "calc")
    status_cf(ws, "C6:C23")
    put(ws, "A25", "DIAGNÓSTICO GLOBAL", "label", bold=True)
    put(ws, "B25", '=IF(COUNTIF(C6:C23,"🔴*")=0,IF(COUNTIF(C6:C23,"🟡*")=0,"🟢 Sustentável","🟡 Sustentável com pontos de atenção"),IF(COUNTIF(C6:C23,"🔴*")<=2,"🟡 Sustentabilidade condicionada","🔴 Sustentabilidade em risco"))', "grey", bold=True)
    status_cf(ws, "B25")
    name(wb, "SUS_Estado", S27, "$B$25")
    name(wb, "SUS_TL", S27, "$B$23")
    name(wb, "SUS_CCL", S27, "$B$21")
    protect(ws)


def build_breakeven(wb):
    ws = wb.create_sheet(S36)
    title(ws, "36 — PONTO DE EQUILÍBRIO (BREAK-EVEN) E MARGEM DE SEGURANÇA", "Classificação fixo/variável por rubrica em 01A_TABELAS (% variável). Valores anualizados a partir do acumulado.", "CAMADA 3 — OUTPUT")
    header(ws, 5, 1, ["Rubrica de custo", "Custo anualizado", "% variável", "Custo variável", "Custo fixo"], [46, 16, 10, 16, 16])
    r = 6
    first = r
    for code, nome, nat, sig in D.RUBRICAS_DR:
        if sig != "C" or code == "DR13":
            continue
        put(ws, (r, 1), f"{code} — {nome}", "label")
        put(ws, (r, 2), f'=-SUMIFS(DR_Acum,DR_Codes,"{code}")*CFG_Anual', "calc", NUM)
        put(ws, (r, 3), f'=SUMIFS(RD_Var,RD_Cod,"{code}")', "calc", PCT)
        put(ws, (r, 4), f"=B{r}*C{r}", "calc", NUM)
        put(ws, (r, 5), f"=B{r}-D{r}", "calc", NUM)
        r += 1
    last = r - 1
    put(ws, (r, 1), "TOTAL", "label", bold=True)
    for c in "BDE":
        put(ws, (r, "ABCDE".index(c) + 1), f"=SUM({c}{first}:{c}{last})", "grey", NUM, bold=True)
    tot = r
    r += 2
    put(ws, (r, 1), "Preço médio de venda por unidade (input)", "label")
    put(ws, (r, 2), 1000, "input", NUM)
    pu = r
    r += 1
    res = [("Receita anualizada (vendas + serviços + outros proveitos operacionais)", "=DR_Prov*CFG_Anual", NUM, "BE_Rec"),
           ("Custos variáveis", f"=D{tot}", NUM, None), ("Margem de contribuição", "=B{a}-B{b}", NUM, "BE_MC"),
           ("Margem de contribuição (%)", "=IF(B{a}=0,0,B{c}/B{a})", PCT, "BE_MCp"), ("Custos fixos", f"=E{tot}", NUM, "BE_CF"),
           ("PONTO DE EQUILÍBRIO (Kz)", "=IF(B{d}<=0,\"n.d.\",B{e}/B{d})", NUM, "BE_Kz"),
           ("Ponto de equilíbrio (unidades equivalentes)", f"=IF(ISNUMBER(B{{f}}),B{{f}}/B{pu},\"n.d.\")", "#,##0", "BE_Un"),
           ("Margem de segurança (Kz)", "=IF(ISNUMBER(B{f}),B{a}-B{f},\"n.d.\")", NUM, None),
           ("Margem de segurança (%)", "=IF(AND(ISNUMBER(B{f}),B{a}<>0),(B{a}-B{f})/B{a},\"n.d.\")", PCT, "BE_MS"),
           ("Grau de alavancagem operacional (MC / EBIT)", "=IF(DR_RO=0,\"n.d.\",B{c}/(DR_RO*CFG_Anual))", MULT, "BE_GAO")]
    base = r
    idx = {"a": base, "b": base + 1, "c": base + 2, "d": base + 3, "e": base + 4, "f": base + 5}
    for i, (lab, f, fmt, nm) in enumerate(res):
        put(ws, (r, 1), lab, "label", bold="EQUIL" in lab)
        put(ws, (r, 2), f.format(**idx), "grey", fmt, bold="EQUIL" in lab)
        if nm:
            name(wb, nm, S36, f"$B${r}")
        r += 1
    put(ws, (r, 1), "Leitura", "label", bold=True)
    put(ws, (r, 2), '=IF(NOT(ISNUMBER(BE_MS)),"🔴 Margem de contribuição insuficiente",IF(BE_MS<0,"🔴 Abaixo do ponto de equilíbrio",IF(BE_MS<0.2,"🟡 Margem de segurança reduzida","🟢 Margem de segurança confortável")))', "grey")
    status_cf(ws, f"B{r}")
    name(wb, "BE_Estado", S36, f"$B${r}")
    protect(ws)


def build_planeamento(wb):
    ws = wb.create_sheet(S17)
    title(ws, "17 — PLANEAMENTO FINANCEIRO E SIMULADOR DE CENÁRIOS", "Projecção a 5 anos (12/24/36/60 meses) em 4 cenários a partir do acumulado anualizado. Pressupostos = input.",
          "CAMADA 1 — INPUT (pressupostos)  |  CAMADA 2/3 — projecção")
    ws.column_dimensions["A"].width = 44
    scen = ["Base", "Optimista", "Conservador", "Stress"]
    header(ws, 5, 1, ["Pressuposto"] + scen, [44, 13, 13, 13, 13])
    drivers = [("Crescimento anual da receita", [0.10, 0.20, 0.03, -0.20], PCT), ("CMV em % da receita", [0.13, 0.12, 0.14, 0.16], PCT),
               ("FSE em % da receita", [0.30, 0.27, 0.32, 0.36], PCT), ("Crescimento anual dos custos com pessoal", [0.08, 0.10, 0.06, 0.05], PCT),
               ("Inflação / actualização de outros custos", [0.15, 0.12, 0.18, 0.25], PCT), ("Depreciação do Kwanza (custos em ME)", [0.10, 0.05, 0.15, 0.35], PCT),
               ("% de custos operacionais em moeda estrangeira", [0.20, 0.20, 0.20, 0.20], PCT), ("Taxa de juro da dívida", [0.18, 0.16, 0.20, 0.25], PCT),
               ("Capex anual (Kz)", [1_000_000, 2_000_000, 500_000, 0], NUM), ("Vida útil média do capex (anos)", [4, 4, 4, 4], "0"),
               ("Novos empréstimos anuais (Kz)", [0, 1_000_000, 0, 0], NUM), ("Reembolso anual da dívida existente (Kz)", [1_000_000, 1_000_000, 1_000_000, 1_000_000], NUM),
               ("NFM em % da receita", [0.10, 0.08, 0.12, 0.18], PCT), ("Distribuição de dividendos (% RL)", [0.30, 0.40, 0.0, 0.0], PCT)]
    for i, (lab, vals, fmt) in enumerate(drivers):
        put(ws, (6 + i, 1), lab, "label")
        for j, v in enumerate(vals):
            put(ws, (6 + i, 2 + j), v, "input", fmt)
    dr = {lab: 6 + i for i, (lab, _, _) in enumerate(drivers)}
    put(ws, (21, 1), "Cenário seleccionado", "label", bold=True)
    put(ws, (21, 2), "Base", "input")
    dv_list(ws, "B21", '"Base,Optimista,Conservador,Stress"')
    put(ws, (22, 1), "Horizonte (meses)", "label", bold=True)
    put(ws, (22, 2), 36, "input", "0")
    dv_list(ws, "B22", '"12,24,36,60"')
    name(wb, "PL_Cen", S17, "$B$21")
    name(wb, "PL_Hor", S17, "$B$22")
    # ano 0 = acumulado anualizado
    base = [("Receita", "=DR_Prov*CFG_Anual"), ("CMV", "=-DR_CMV*CFG_Anual"), ("FSE", "=-DR_FSE*CFG_Anual"), ("Pessoal", "=-DR_Pessoal*CFG_Anual"),
            ("Outros custos operacionais", '=-SUMIFS(DR_Acum,DR_Codes,"DR08")*CFG_Anual'), ("Amortizações", "=-DR_Amort*CFG_Anual"),
            ("Dívida financeira", f"={DIVIDA}"), ("Capital próprio", "=BS_CP"), ("Meios monetários e aplicações", f"={LIQ}")]
    put(ws, (24, 1), "BASE DE PARTIDA (ano 0 = acumulado anualizado)", "label", bold=True)
    for i, (lab, f) in enumerate(base):
        put(ws, (25 + i, 1), lab, "label")
        put(ws, (25 + i, 2), f, "grey", NUM)
    b0 = {lab: f"$B${25 + i}" for i, (lab, _) in enumerate(base)}
    lines = ["Receita", "CMV", "FSE", "Pessoal", "Outros custos operacionais", "EBITDA", "Amortizações", "EBIT", "Juros", "RAI", "Imposto Industrial",
             "Resultado líquido", "Cash flow operacional (RL + amortizações − ΔNFM)", "Capex", "Novos empréstimos", "Reembolsos", "Dividendos",
             "Cash flow líquido", "Dívida financeira (fim)", "Capital próprio (fim)", "Meios monetários (fim)", "Necessidade de financiamento (caixa < mínimo)",
             "Dívida / EBITDA", "Autonomia (CP / (CP + dívida))"]
    blocks = {}
    r = 36
    for si, sname in enumerate(scen):
        col = CL(2 + si)
        section(ws, r, 1, f"PROJECÇÃO — CENÁRIO {sname.upper()}", 7)
        header(ws, r + 1, 1, ["Rubrica", "Ano 1", "Ano 2", "Ano 3", "Ano 4", "Ano 5"], None)
        L = {lab: r + 2 + i for i, lab in enumerate(lines)}
        for lab in lines:
            put(ws, (L[lab], 1), lab, "label", bold=lab in ("EBITDA", "Resultado líquido", "Cash flow líquido"))
        g = lambda d: f"${col}${dr[d]}"
        for y in range(1, 6):
            c = CL(1 + y)
            p = CL(y)
            prev = lambda lab: (b0[lab] if y == 1 else f"{p}{L[lab]}")
            f = {
                "Receita": f"={b0['Receita'] if y == 1 else p + str(L['Receita'])}*(1+{g('Crescimento anual da receita')})",
                "CMV": f"={c}{L['Receita']}*{g('CMV em % da receita')}",
                "FSE": f"={c}{L['Receita']}*{g('FSE em % da receita')}*(1+{g('% de custos operacionais em moeda estrangeira')}*{g('Depreciação do Kwanza (custos em ME)')})",
                "Pessoal": f"={prev('Pessoal')}*(1+{g('Crescimento anual dos custos com pessoal')})",
                "Outros custos operacionais": f"={prev('Outros custos operacionais')}*(1+{g('Inflação / actualização de outros custos')})",
                "EBITDA": f"={c}{L['Receita']}-{c}{L['CMV']}-{c}{L['FSE']}-{c}{L['Pessoal']}-{c}{L['Outros custos operacionais']}",
                "Amortizações": f"={b0['Amortizações']}+{g('Capex anual (Kz)')}*{y}/{g('Vida útil média do capex (anos)')}",
                "EBIT": f"={c}{L['EBITDA']}-{c}{L['Amortizações']}",
                "Juros": f"={(b0['Dívida financeira'] if y == 1 else p + str(L['Dívida financeira (fim)']))}*{g('Taxa de juro da dívida')}",
                "RAI": f"={c}{L['EBIT']}-{c}{L['Juros']}",
                "Imposto Industrial": f"=MAX(0,{c}{L['RAI']})*TX_II",
                "Resultado líquido": f"={c}{L['RAI']}-{c}{L['Imposto Industrial']}",
                "Cash flow operacional (RL + amortizações − ΔNFM)": f"={c}{L['Resultado líquido']}+{c}{L['Amortizações']}-({c}{L['Receita']}-{b0['Receita'] if y == 1 else p + str(L['Receita'])})*{g('NFM em % da receita')}",
                "Capex": f"={g('Capex anual (Kz)')}",
                "Novos empréstimos": f"={g('Novos empréstimos anuais (Kz)')}",
                "Reembolsos": f"=MIN({g('Reembolso anual da dívida existente (Kz)')},{(b0['Dívida financeira'] if y == 1 else p + str(L['Dívida financeira (fim)']))}+{c}{L['Novos empréstimos']})",
                "Dividendos": f"=MAX(0,{c}{L['Resultado líquido']})*{g('Distribuição de dividendos (% RL)')}",
                "Cash flow líquido": f"={c}{L['Cash flow operacional (RL + amortizações − ΔNFM)']}-{c}{L['Capex']}+{c}{L['Novos empréstimos']}-{c}{L['Reembolsos']}-{c}{L['Dividendos']}",
                "Dívida financeira (fim)": f"={(b0['Dívida financeira'] if y == 1 else p + str(L['Dívida financeira (fim)']))}+{c}{L['Novos empréstimos']}-{c}{L['Reembolsos']}",
                "Capital próprio (fim)": f"={b0['Capital próprio'] if y == 1 else p + str(L['Capital próprio (fim)'])}+{c}{L['Resultado líquido']}-{c}{L['Dividendos']}",
                "Meios monetários (fim)": f"={(b0['Meios monetários e aplicações'] if y == 1 else p + str(L['Meios monetários (fim)']))}+{c}{L['Cash flow líquido']}",
                "Necessidade de financiamento (caixa < mínimo)": f"=MAX(0,CFG_SaldoMin-{c}{L['Meios monetários (fim)']})",
                "Dívida / EBITDA": f"=IF({c}{L['EBITDA']}<=0,99,{c}{L['Dívida financeira (fim)']}/{c}{L['EBITDA']})",
                "Autonomia (CP / (CP + dívida))": f"=IF(({c}{L['Capital próprio (fim)']}+{c}{L['Dívida financeira (fim)']})=0,0,{c}{L['Capital próprio (fim)']}/({c}{L['Capital próprio (fim)']}+{c}{L['Dívida financeira (fim)']}))",
            }
            if y > 1:
                f["Capital próprio (fim)"] = f"={p}{L['Capital próprio (fim)']}+{c}{L['Resultado líquido']}-{c}{L['Dividendos']}"
            for lab in lines:
                fmt = MULT if lab == "Dívida / EBITDA" else (PCT if lab.startswith("Autonomia") else NUM)
                put(ws, (L[lab], 1 + y), f[lab], "calc", fmt)
        blocks[sname] = L
        r = r + 3 + len(lines)
    # comparação de cenários (horizonte seleccionado)
    section(ws, r, 1, "COMPARAÇÃO DE CENÁRIOS NO HORIZONTE SELECCIONADO", 7)
    header(ws, r + 1, 1, ["Indicador (ano do horizonte)"] + scen + ["Seleccionado"], None)
    comp = ["Receita", "EBITDA", "Resultado líquido", "Cash flow líquido", "Dívida financeira (fim)", "Capital próprio (fim)", "Meios monetários (fim)",
            "Necessidade de financiamento (caixa < mínimo)", "Dívida / EBITDA", "Autonomia (CP / (CP + dívida))"]
    for i, lab in enumerate(comp):
        rr = r + 2 + i
        put(ws, (rr, 1), lab, "label")
        for si, sname in enumerate(scen):
            L = blocks[sname]
            put(ws, (rr, 2 + si), f"=INDEX(B{L[lab]}:F{L[lab]},PL_Hor/12)" if lab not in ("Cash flow líquido", "Necessidade de financiamento (caixa < mínimo)")
                else (f"=SUMPRODUCT((COLUMN(B{L[lab]}:F{L[lab]})-1<=PL_Hor/12)*B{L[lab]}:F{L[lab]})" if lab == "Cash flow líquido" else f"=MAX(INDEX(B{L[lab]}:F{L[lab]},1,1):INDEX(B{L[lab]}:F{L[lab]},1,PL_Hor/12))"),
                "calc", MULT if lab == "Dívida / EBITDA" else (PCT if lab.startswith("Autonomia") else NUM))
        put(ws, (rr, 6), f'=INDEX(B{rr}:E{rr},MATCH(PL_Cen,$B$5:$E$5,0))', "grey", MULT if lab == "Dívida / EBITDA" else (PCT if lab.startswith("Autonomia") else NUM))
    name(wb, "PL_NecSel", S17, f"$F${r + 2 + comp.index('Necessidade de financiamento (caixa < mínimo)')}")
    r = r + 3 + len(comp)
    # simulador de impacto
    section(ws, r, 1, "SIMULADOR DE IMPACTO (sobre o ano 0 anualizado)", 7)
    header(ws, r + 1, 1, ["Choque", "Variação", "Δ EBITDA", "Δ Resultado líquido", "RL simulado", "Caixa simulada (1 ano)", "Leitura"], [44, 12, 15, 15, 15, 15, 30])
    mc = "(1-SUMIFS(RD_Var,RD_Cod,\"DR04\")*" + "ABS(DR_CMV)/MAX(1,DR_Prov)-SUMIFS(RD_Var,RD_Cod,\"DR05\")*ABS(DR_FSE)/MAX(1,DR_Prov)-SUMIFS(RD_Var,RD_Cod,\"DR08\")*ABS(SUMIFS(DR_Acum,DR_Codes,\"DR08\"))/MAX(1,DR_Prov))"
    shocks = [("Queda de vendas", -0.10, f"=B{{r}}*DR_Prov*CFG_Anual*{mc}"), ("Queda de vendas", -0.20, f"=B{{r}}*DR_Prov*CFG_Anual*{mc}"),
              ("Queda de vendas", -0.30, f"=B{{r}}*DR_Prov*CFG_Anual*{mc}"),
              ("Aumento dos custos operacionais (excl. amortizações)", 0.10, "=-B{r}*(ABS(DR_Cust)-ABS(DR_Amort))*CFG_Anual"),
              ("Depreciação cambial (custos em ME)", 0.20, f"=-B{{r}}*$B$12*(ABS(DR_Cust)-ABS(DR_Amort))*CFG_Anual"),
              ("Aumento da taxa de juro (pontos percentuais)", 0.05, f"=0"),
              ("Aumento dos salários", 0.15, "=-B{r}*ABS(DR_Pessoal)*CFG_Anual")]
    for i, (lab, v, f) in enumerate(shocks):
        rr = r + 2 + i
        put(ws, (rr, 1), lab, "label")
        put(ws, (rr, 2), v, "input", PCT)
        put(ws, (rr, 3), f.format(r=rr), "calc", NUM)
        if "juro" in lab:
            put(ws, (rr, 4), f"=-B{rr}*{DIVIDA}*(1-TX_II)", "calc", NUM)
        else:
            put(ws, (rr, 4), f"=C{rr}*IF(DR_RAI>0,1-TX_II,1)", "calc", NUM)
        put(ws, (rr, 5), f"=DR_RL*CFG_Anual+D{rr}", "calc", NUM)
        put(ws, (rr, 6), f"={LIQ}+DFC_Op*CFG_Anual+D{rr}", "calc", NUM)
        put(ws, (rr, 7), f'=IF(E{rr}<0,"🔴 Resultado passa a negativo",IF(F{rr}<CFG_SaldoMin,"🟡 Caixa abaixo do mínimo","🟢 Absorvível"))', "calc")
    status_cf(ws, f"G{r + 2}:G{r + 1 + len(shocks)}")
    name(wb, "PL_Sim", S17, f"$A${r + 2}:$G${r + 1 + len(shocks)}")
    put(ws, (r + 3 + len(shocks), 1), "Metodologia: queda de vendas × margem de contribuição (% variável em 01A_TABELAS); custos, câmbio e juros aplicados ao acumulado anualizado. Efeito fiscal à taxa II_GER quando RAI > 0.", "note")
    protect(ws)


def build_projectos(wb):
    ws = wb.create_sheet(S24)
    title(ws, "24 — GESTÃO DE PROJECTOS (Projectado × Realizado)", "Plano do projecto = input; realizado vem do Diário pelo campo Projecto. VAL/TIR/Payback sobre os fluxos projectados.",
          "CAMADA 1 — INPUT (A:Q)  |  CAMADA 3 — output")
    heads = ["ID", "Nome", "Responsável", "Orçamento total", "Investimento previsto", "Financiamento", "Início", "Fim", "Risco (1–5)", "Taxa de desconto",
             "FC ano 0", "FC ano 1", "FC ano 2", "FC ano 3", "FC ano 4", "FC ano 5", "Receita prevista ano 1",
             "Investimento real", "Custos reais", "Receitas reais", "Cash flow real", "Execução orçamental", "Margem real", "ROI real",
             "VAL", "TIR", "Payback (anos)", "Prazo", "Estado"]
    header(ws, 5, 1, heads, [7, 26, 14, 13, 13, 12, 10, 10, 6, 8] + [12] * 7 + [13] * 6 + [9, 13, 8, 8, 10, 26])
    ws.freeze_panes = "C6"
    prj = [] if D.PRODUCAO else [("PRJ01", "Modernização informática", "Dir. Administrativo", 1_500_000, 1_200_000, "Capitais próprios", "2026-02-01", "2026-06-30", 2, 0.20,
            -1_200_000, 450_000, 450_000, 450_000, 450_000, 0, 0),
           ("PRJ02", "Consultoria Epsilon", "Dir. Operações", 1_000_000, 0, "Receitas do projecto", "2026-02-01", "2026-12-31", 3, 0.25,
            0, 2_500_000, 1_000_000, 0, 0, 0, 3_600_000)]
    from datetime import date as _d
    for i in range(20):
        r = 6 + i
        v = list(prj[i]) if i < len(prj) else [None] * 17
        if v[6]:
            v[6] = _d.fromisoformat(v[6])
            v[7] = _d.fromisoformat(v[7])
        fm = ["@", None, None, NUM, NUM, None, DATE, DATE, "0", PCT] + [NUM] * 7
        for j in range(17):
            put(ws, (r, 1 + j), v[j], "input", fm[j])
        yt = 'J_Ano,CFG_Ano,J_Data,"<="&CFG_DataRef'
        put(ws, (r, 18), f'=IF(A{r}="","",SUMIFS(J_Deb,J_Proj,A{r},J_Classe,"1",{yt}))', "calc", NUM)
        put(ws, (r, 19), f'=IF(A{r}="","",SUMIFS(J_DC,J_Proj,A{r},J_Classe,"7",{yt}))', "calc", NUM)
        put(ws, (r, 20), f'=IF(A{r}="","",-SUMIFS(J_DC,J_Proj,A{r},J_Classe,"6",{yt}))', "calc", NUM)
        put(ws, (r, 21), f'=IF(A{r}="","",SUMIFS(J_DC,J_Proj,A{r},J_Caixa,1,{yt}))', "calc", NUM)
        put(ws, (r, 22), f'=IF(OR(A{r}="",N(D{r})=0),"",(R{r}+S{r})/D{r})', "calc", PCT)
        put(ws, (r, 23), f'=IF(A{r}="","",T{r}-S{r})', "calc", NUM)
        put(ws, (r, 24), f'=IF(A{r}="","",IF((R{r}+S{r})=0,"",(T{r}-S{r}-R{r})/(R{r}+S{r})))', "calc", PCT)
        put(ws, (r, 25), f'=IF(A{r}="","",K{r}+NPV(J{r},L{r}:P{r}))', "calc", NUM)
        put(ws, (r, 26), f'=IF(OR(A{r}="",N(K{r})>=0),"n.a.",IFERROR(IRR(K{r}:P{r}),"n.d."))', "calc", PCT)
        pb = (f'=IF(OR(A{r}="",N(K{r})>=0),"n.a.",IF(K{r}+L{r}>=0,-K{r}/L{r},IF(K{r}+L{r}+M{r}>=0,1+(-(K{r}+L{r}))/M{r},IF(K{r}+L{r}+M{r}+N{r}>=0,2+(-(K{r}+L{r}+M{r}))/N{r},'
              f'IF(K{r}+L{r}+M{r}+N{r}+O{r}>=0,3+(-(K{r}+L{r}+M{r}+N{r}))/O{r},IF(SUM(K{r}:P{r})>=0,4+(-(K{r}+L{r}+M{r}+N{r}+O{r}))/P{r},"> 5"))))))')
        put(ws, (r, 27), pb, "calc", "0.0")
        put(ws, (r, 28), f'=IF(A{r}="","",IF(CFG_DataRef>N(H{r}),"Terminado/atrasado","Em curso"))', "calc")
        put(ws, (r, 29), f'=IF(A{r}="","",IF(AND(ISNUMBER(V{r}),V{r}>1),"🔴 Orçamento excedido",IF(AND(ISNUMBER(Y{r}),Y{r}<0),"🟡 VAL negativo",IF(N(I{r})>=4,"🟡 Risco elevado","🟢 Normal"))))', "calc")
    status_cf(ws, "AC6:AC25")
    put(ws, "A27", "TOTAIS", "label", bold=True)
    for c in "DERSTUW":
        put(ws, f"{c}27", f"=SUM({c}6:{c}25)", "grey", NUM, bold=True)
    put(ws, "A29", "Projecto mais intensivo em capital", "label", bold=True)
    put(ws, "D29", '=IFERROR(INDEX(B6:B25,MATCH(MAX(E6:E25),E6:E25,0)),"—")', "grey")
    name(wb, "PRJ_MaisCapital", S24, "$D$29")
    put(ws, "A30", "Projectos com alertas", "label")
    put(ws, "D30", '=COUNTIF(AC6:AC25,"🔴*")+COUNTIF(AC6:AC25,"🟡*")', "grey", "0")
    name(wb, "PRJ_Alertas", S24, "$D$30")
    protect(ws)


def build_investimentos(wb):
    ws = wb.create_sheet(S25)
    title(ws, "25 — ANÁLISE DE INVESTIMENTOS (VAL, TIR, Payback, IR, ROI, ROIC, WACC) E SENSIBILIDADE",
          "Modelo incremental a 10 anos. Pressupostos em azul. Sensibilidade recalcula o VAL com choques em cada variável.", "CAMADA 1 — INPUT  |  CAMADA 2/3 — cálculo")
    ws.column_dimensions["A"].width = 40
    inp = [("Investimento inicial (Kz)", 5_000_000, NUM), ("Vida útil / horizonte (anos, ≤10)", 8, "0"), ("Valor residual no fim (Kz)", 500_000, NUM),
           ("Volume anual — ano 1 (unidades)", 4_000, "#,##0"), ("Crescimento anual do volume", 0.05, PCT), ("Preço unitário — ano 1 (Kz)", 1_500, NUM),
           ("Actualização anual do preço (inflação)", 0.12, PCT), ("Custo variável unitário — ano 1 (Kz)", 800, NUM), ("Actualização anual do custo variável", 0.14, PCT),
           ("Custos fixos anuais — ano 1 (Kz)", 1_200_000, NUM), ("Actualização dos custos fixos", 0.12, PCT), ("% dos custos em moeda estrangeira", 0.30, PCT),
           ("Depreciação cambial anual", 0.10, PCT), ("NFM em % da receita", 0.10, PCT), ("Taxa de imposto (II_GER)", "=TX_II", PCT),
           ("Capital próprio (E, Kz)", 3_000_000, NUM), ("Dívida (D, Kz)", 2_000_000, NUM), ("Custo do capital próprio (Ke)", 0.25, PCT),
           ("Custo da dívida antes de impostos (Kd)", 0.18, PCT), ("Usar WACC como taxa de desconto (1=Sim)", 1, "0"), ("Taxa de desconto manual", 0.22, PCT)]
    header(ws, 5, 1, ["Pressuposto", "Valor"], [40, 16])
    for i, (lab, v, fmt) in enumerate(inp):
        put(ws, (6 + i, 1), lab, "label")
        put(ws, (6 + i, 2), v, "input" if not str(v).startswith("=") else "grey", fmt)
    P = {lab.split(" (")[0]: f"$B${6 + i}" for i, (lab, _, _) in enumerate(inp)}
    rr = 6 + len(inp)
    put(ws, (rr, 1), "WACC = E/(D+E)×Ke + D/(D+E)×Kd×(1−t)", "label", bold=True)
    put(ws, (rr, 2), f"=({P['Capital próprio']}*{P['Custo do capital próprio']}+{P['Dívida']}*{P['Custo da dívida antes de impostos']}*(1-{P['Taxa de imposto']}))/({P['Capital próprio']}+{P['Dívida']})", "grey", PCT)
    wacc = f"$B${rr}"
    put(ws, (rr + 1, 1), "Taxa de desconto utilizada", "label", bold=True)
    put(ws, (rr + 1, 2), f"=IF({P['Usar WACC como taxa de desconto']}=1,{wacc},{P['Taxa de desconto manual']})", "grey", PCT)
    tx = f"$B${rr + 1}"
    # modelo (colunas D..N = anos 0..10)
    r0 = 5
    put(ws, (r0, 4), "Ano", "label", bold=True)
    for y in range(11):
        put(ws, (r0, 5 + y), y, "label", bold=True)
    lines = ["Activo (1=ano activo)", "Volume", "Preço", "Receita", "Custo variável", "Custos fixos", "EBITDA", "Depreciação", "EBIT", "Imposto", "NOPAT",
             "NFM", "Variação NFM", "Investimento / valor residual", "Cash flow incremental", "Cash flow descontado", "Cash flow acumulado", "CF descontado acumulado",
             "Aux. payback simples", "Aux. payback actualizado"]
    L = {lab: r0 + 1 + i for i, lab in enumerate(lines)}
    for lab in lines:
        put(ws, (L[lab], 4), lab, "label")
    ws.column_dimensions["D"].width = 30
    fx = f"(1+{P['% dos custos em moeda estrangeira']}*((1+{P['Depreciação cambial anual']})^({{c}}$5-1)-1))"
    for y in range(11):
        c = CL(5 + y)
        p = CL(4 + y)
        f = {
            "Activo (1=ano activo)": f"=IF(AND({c}$5>=1,{c}$5<={P['Vida útil / horizonte']}),1,0)",
            "Volume": f"={c}{L['Activo (1=ano activo)']}*{P['Volume anual — ano 1']}*(1+{P['Crescimento anual do volume']})^MAX(0,{c}$5-1)",
            "Preço": f"={P['Preço unitário — ano 1']}*(1+{P['Actualização anual do preço']})^MAX(0,{c}$5-1)",
            "Receita": f"={c}{L['Volume']}*{c}{L['Preço']}",
            "Custo variável": f"={c}{L['Volume']}*{P['Custo variável unitário — ano 1']}*(1+{P['Actualização anual do custo variável']})^MAX(0,{c}$5-1)*" + fx.format(c=c),
            "Custos fixos": f"={c}{L['Activo (1=ano activo)']}*{P['Custos fixos anuais — ano 1']}*(1+{P['Actualização dos custos fixos']})^MAX(0,{c}$5-1)*" + fx.format(c=c),
            "EBITDA": f"={c}{L['Receita']}-{c}{L['Custo variável']}-{c}{L['Custos fixos']}",
            "Depreciação": f"={c}{L['Activo (1=ano activo)']}*({P['Investimento inicial']}-{P['Valor residual no fim']})/{P['Vida útil / horizonte']}",
            "EBIT": f"={c}{L['EBITDA']}-{c}{L['Depreciação']}",
            "Imposto": f"=MAX(0,{c}{L['EBIT']})*{P['Taxa de imposto']}",
            "NOPAT": f"={c}{L['EBIT']}-{c}{L['Imposto']}",
            "NFM": f"={c}{L['Receita']}*{P['NFM em % da receita']}",
            "Variação NFM": f"={c}{L['NFM']}-{('0' if y == 0 else p + str(L['NFM']))}",
            "Investimento / valor residual": f"=IF({c}$5=0,-{P['Investimento inicial']},IF({c}$5={P['Vida útil / horizonte']},{P['Valor residual no fim']}+{c}{L['NFM']},0))",
            "Cash flow incremental": f"={c}{L['NOPAT']}+{c}{L['Depreciação']}-{c}{L['Variação NFM']}+{c}{L['Investimento / valor residual']}",
            "Cash flow descontado": f"={c}{L['Cash flow incremental']}/(1+{tx})^{c}$5",
            "Cash flow acumulado": f"={c}{L['Cash flow incremental']}" + ("" if y == 0 else f"+{p}{L['Cash flow acumulado']}"),
            "CF descontado acumulado": f"={c}{L['Cash flow descontado']}" + ("" if y == 0 else f"+{p}{L['CF descontado acumulado']}"),
            "Aux. payback simples": '=""' if y == 0 else f'=IF(AND({p}{L["Cash flow acumulado"]}<0,{c}{L["Cash flow acumulado"]}>=0),{y - 1}+(-{p}{L["Cash flow acumulado"]})/{c}{L["Cash flow incremental"]},"")',
            "Aux. payback actualizado": '=""' if y == 0 else f'=IF(AND({p}{L["CF descontado acumulado"]}<0,{c}{L["CF descontado acumulado"]}>=0),{y - 1}+(-{p}{L["CF descontado acumulado"]})/{c}{L["Cash flow descontado"]},"")',
        }
        for lab in lines:
            put(ws, (L[lab], 5 + y), f[lab], "calc", "0" if lab.startswith("Activo") else NUM)
        ws.column_dimensions[c].width = 13
    cf = f"E{L['Cash flow incremental']}:O{L['Cash flow incremental']}"
    cum = f"E{L['Cash flow acumulado']}:O{L['Cash flow acumulado']}"
    dcum = f"E{L['CF descontado acumulado']}:O{L['CF descontado acumulado']}"
    rr = L["Aux. payback actualizado"] + 2
    res = [("VAL (NPV)", f"=E{L['Cash flow incremental']}+NPV({tx},F{L['Cash flow incremental']}:O{L['Cash flow incremental']})", NUM, "INV_VAL"),
           ("TIR (IRR)", f'=IFERROR(IRR({cf}),"n.d.")', PCT, "INV_TIR"),
           ("Payback simples (anos)", f'=IF(COUNT(E{L["Aux. payback simples"]}:O{L["Aux. payback simples"]})=0,"> horizonte",MIN(E{L["Aux. payback simples"]}:O{L["Aux. payback simples"]}))', "0.00", "INV_PB"),
           ("Payback actualizado (anos)", f'=IF(COUNT(E{L["Aux. payback actualizado"]}:O{L["Aux. payback actualizado"]})=0,"> horizonte",MIN(E{L["Aux. payback actualizado"]}:O{L["Aux. payback actualizado"]}))', "0.00", "INV_PBA"),
           ("Índice de rendibilidade (VAL/Inv. + 1)", f"=IF({P['Investimento inicial']}=0,0,1+INV_VAL/{P['Investimento inicial']})", MULT, "INV_IR"),
           ("Margem EBITDA média", f"=IF(SUM(E{L['Receita']}:O{L['Receita']})=0,0,SUM(E{L['EBITDA']}:O{L['EBITDA']})/SUM(E{L['Receita']}:O{L['Receita']}))", PCT, None),
           ("ROI (Σ CF − investimento) / investimento", f"=IF({P['Investimento inicial']}=0,0,SUM(F{L['Cash flow incremental']}:O{L['Cash flow incremental']})/{P['Investimento inicial']}-1)", PCT, "INV_ROI"),
           ("ROIC médio (NOPAT médio / capital investido)", f"=IF({P['Investimento inicial']}=0,0,AVERAGEIF(E{L['Activo (1=ano activo)']}:O{L['Activo (1=ano activo)']},1,E{L['NOPAT']}:O{L['NOPAT']})/({P['Investimento inicial']}+MAX(E{L['NFM']}:O{L['NFM']})))", PCT, "INV_ROIC"),
           ("Custo de capital (taxa utilizada)", f"={tx}", PCT, None),
           ("DECISÃO", f'=IF(INV_VAL>0,IF(AND(ISNUMBER(INV_TIR),INV_TIR>{tx}),"🟢 Criar valor: VAL > 0 e TIR > custo de capital","🟡 VAL > 0 — verificar TIR"),"🔴 Destrói valor: VAL < 0")', None, "INV_Dec")]
    for i, (lab, f, fmt, nm) in enumerate(res):
        put(ws, (rr + i, 4), lab, "label", bold=True)
        put(ws, (rr + i, 5), f, "grey", fmt, bold=lab == "DECISÃO")
        if nm:
            name(wb, nm, S25, f"$E${rr + i}")
    status_cf(ws, f"E{rr + len(res) - 1}")
    # Sensibilidade: grelha de cenários com multiplicadores
    rs = rr + len(res) + 2
    section(ws, rs, 1, "ANÁLISE DE SENSIBILIDADE — VAL recalculado por choque (restantes variáveis constantes)", 16)
    header(ws, rs + 1, 1, ["Variável", "Choque", "× Preço", "× Volume", "× Custo var.", "× Custos fixos", "+ Δ câmbio", "+ Δ taxa desc.", "+ Δ inflação", "VAL", "Δ VAL", "Δ VAL %"],
           [40, 9, 8, 8, 8, 8, 8, 8, 8, 14, 14, 9])
    sh = [("Base", 0, (1, 1, 1, 1, 0, 0, 0))]
    for v, idx in [("Preço", 0), ("Volume", 1), ("Custo variável", 2), ("Custos fixos", 3)]:
        for s in (-0.2, -0.1, 0.1, 0.2):
            m = [1, 1, 1, 1, 0, 0, 0]
            m[idx] = 1 + s
            sh.append((v, s, tuple(m)))
    for s in (0.1, 0.25):
        sh.append(("Taxa de câmbio (depreciação adicional)", s, (1, 1, 1, 1, s, 0, 0)))
    for s in (-0.03, 0.03, 0.05):
        sh.append(("Taxa de desconto (p.p.)", s, (1, 1, 1, 1, 0, s, 0)))
    for s in (0.05, 0.10):
        sh.append(("Inflação de custos (p.p. adicionais)", s, (1, 1, 1, 1, 0, 0, s)))
    sh.append(("Financiamento: +10 p.p. de dívida no WACC", 0.10, (1, 1, 1, 1, 0, "W", 0)))
    base_row = rs + 2
    yrs = range(0, 11)
    for i, (v, s, m) in enumerate(sh):
        r = rs + 2 + i
        put(ws, (r, 1), v, "label")
        put(ws, (r, 2), s, "label", PCT)
        for j, x in enumerate(m):
            if x == "W":
                x = f"=({P['Capital próprio']}-0.1*({P['Capital próprio']}+{P['Dívida']}))/({P['Capital próprio']}+{P['Dívida']})*{P['Custo do capital próprio']}+({P['Dívida']}+0.1*({P['Capital próprio']}+{P['Dívida']}))/({P['Capital próprio']}+{P['Dívida']})*{P['Custo da dívida antes de impostos']}*(1-{P['Taxa de imposto']})-{wacc}"
            put(ws, (r, 3 + j), x, "input", "0.00" if j < 4 else PCT)
        # VAL recalculado em forma fechada ano a ano
        terms = []
        for y in yrs:
            act = f"(({y}>=1)*({y}<={P['Vida útil / horizonte']}))"
            vol = f"{act}*{P['Volume anual — ano 1']}*D{r}*(1+{P['Crescimento anual do volume']})^MAX(0,{y}-1)"
            fxm = f"(1+{P['% dos custos em moeda estrangeira']}*((1+{P['Depreciação cambial anual']}+G{r})^MAX(0,{y}-1)-1))"
            rec = f"({vol}*{P['Preço unitário — ano 1']}*C{r}*(1+{P['Actualização anual do preço']})^MAX(0,{y}-1))"
            cv = f"({vol}*{P['Custo variável unitário — ano 1']}*E{r}*(1+{P['Actualização anual do custo variável']}+I{r})^MAX(0,{y}-1)*{fxm})"
            cfx = f"({act}*{P['Custos fixos anuais — ano 1']}*F{r}*(1+{P['Actualização dos custos fixos']}+I{r})^MAX(0,{y}-1)*{fxm})"
            dep = f"({act}*({P['Investimento inicial']}-{P['Valor residual no fim']})/{P['Vida útil / horizonte']})"
            ebit = f"({rec}-{cv}-{cfx}-{dep})"
            terms.append((ebit, dep, rec, act, y))
        # construir por colunas auxiliares (Q..AA) para manter fórmulas legíveis
        for y in yrs:
            ebit, dep, rec, act, _ = terms[y]
            c = CL(17 + y)
            nfm = f"{rec}*{P['NFM em % da receita']}"
            prev_nfm = "0" if y == 0 else terms[y - 1][2] + f"*{P['NFM em % da receita']}"
            inv = f"IF({y}=0,-{P['Investimento inicial']},IF({y}={P['Vida útil / horizonte']},{P['Valor residual no fim']}+{nfm},0))"
            cfy = f"({ebit}-MAX(0,{ebit})*{P['Taxa de imposto']}+{dep}-({nfm}-{prev_nfm})+{inv})/(1+{tx}+H{r})^{y}"
            put(ws, (r, 17 + y), "=" + cfy, "grey", NUM)
        put(ws, (r, 10), f"=SUM(Q{r}:AA{r})", "calc", NUM)
        put(ws, (r, 11), f"=J{r}-$J${base_row}", "calc", NUM)
        put(ws, (r, 12), f"=IF($J${base_row}=0,0,K{r}/ABS($J${base_row}))", "calc", PCT)
    for y in yrs:
        put(ws, (rs + 1, 17 + y), f"CF desc. ano {y}", "note")
    put(ws, (rs + 3 + len(sh), 1), "Controlo: VAL base da grelha = VAL do modelo", "label")
    put(ws, (rs + 3 + len(sh), 10), f'=IF(ABS(J{base_row}-INV_VAL)<1,"🟢 Modelo de sensibilidade consistente","🔴 Divergência")', "grey")
    status_cf(ws, f"J{rs + 3 + len(sh)}")
    name(wb, "INV_SensEst", S25, f"$J${rs + 3 + len(sh)}")
    protect(ws)


def build_risco(wb):
    ws = wb.create_sheet(S26)
    title(ws, "26 — GESTÃO DE RISCO FINANCEIRO: MATRIZ 5×5 E PLANO DE MITIGAÇÃO", "Probabilidade × Impacto = Exposição. Indicador automático sugere a avaliação; a decisão final é do gestor (input).",
          "CAMADA 1 — INPUT (P, I, mitigação)  |  CAMADA 3 — matriz")
    heads = ["Risco", "Indicador automático", "Valor do indicador", "Probabilidade sugerida", "Probabilidade (1–5)", "Impacto (1–5)", "Exposição (P×I)",
             "Nível", "Plano de mitigação", "Responsável", "Prazo"]
    header(ws, 5, 1, heads, [26, 36, 14, 10, 10, 10, 10, 14, 44, 16, 11])
    riscos = [
        ("Risco de liquidez", "Liquidez imediata (x)", "=K_LI", "=IF(C6<0.1,5,IF(C6<0.3,3,1))", 2, 4, "Manter reserva mínima; linha de crédito contratada; previsão de 13 semanas semanal."),
        ("Risco de crédito", "% saldo de clientes vencido", "=IF(CLI_Total=0,0,CLI_Venc/CLI_Total)", "=IF(C7>0.5,5,IF(C7>0.25,3,1))", 3, 3, "Limites de crédito, cobrança activa, adiantamentos, garantias."),
        ("Risco cambial", "% custos operacionais em ME (pressuposto)", "=INDEX('17_PLANEAMENTO_FINANCEIRO'!B6:B19,7)", "=IF(C8>0.4,5,IF(C8>0.2,3,1))", 3, 4, "Indexar preços, contas em ME, cobertura natural, antecipar pagamentos."),
        ("Risco de taxa de juro", "Dívida / (dívida + CP)", f"=IF((BS_CP+{DIVIDA})=0,0,{DIVIDA}/(BS_CP+{DIVIDA}))", "=IF(C9>0.5,5,IF(C9>0.3,3,1))", 2, 3, "Negociar taxa fixa ou tectos; reduzir dívida de curto prazo."),
        ("Risco operacional", "Linhas do Diário com erro", "=SUM(J_ErrFlag)", "=IF(C10>5,5,IF(C10>0,3,1))", 2, 3, "Controlo interno, segregação de funções, fecho mensal."),
        ("Risco fiscal", "Obrigações vencidas + taxas POR VALIDAR em uso", '=CAL_Vencidas+COUNTIF(TX_Alerta,"🟡 Em uso*")', "=IF(C11>3,5,IF(C11>0,3,1))", 3, 4, "Validar parametrização fiscal; calendário AGT; revisão por técnico de contas."),
        ("Risco de concentração", "Maior cliente (% saldo)", "=CLI_Conc1", "=IF(C12>CFG_ConcCli,5,IF(C12>CFG_ConcCli/2,3,1))", 3, 3, "Diversificar carteira; contratos de médio prazo."),
        ("Risco de mercado", "Crescimento da receita anualizada", "=K_GV", "=IF(C13<-0.1,5,IF(C13<0,3,1))", 2, 4, "Monitorização de preços, diferenciação, marketing."),
        ("Risco de financiamento", "Necessidade de financiamento (13 semanas + plano)", "=TES_Necess+PL_NecSel", "=IF(C14>CFG_LimTes,5,IF(C14>0,3,1))", 2, 4, "Plano de financiamento antecipado; relação com 2+ bancos."),
    ]
    for i, (n, ind, f, sug, p, im, mit) in enumerate(riscos):
        r = 6 + i
        put(ws, (r, 1), n, "label", bold=True)
        put(ws, (r, 2), ind, "label")
        put(ws, (r, 3), f, "calc", "0.00")
        put(ws, (r, 4), sug, "calc", "0")
        put(ws, (r, 5), p, "input", "0")
        put(ws, (r, 6), im, "input", "0")
        put(ws, (r, 7), f"=E{r}*F{r}", "calc", "0")
        put(ws, (r, 8), f'=IF(G{r}>=15,"🔴 Crítico",IF(G{r}>=8,"🟡 Atenção","🟢 Normal"))', "calc")
        put(ws, (r, 9), mit, "input", wrap=True)
        put(ws, (r, 10), "Director Financeiro", "input")
        put(ws, (r, 11), None, "input", DATE)
    status_cf(ws, "H6:H14")
    name(wb, "RSK_Exp", S26, "$G$6:$G$14")
    name(wb, "RSK_Nome", S26, "$A$6:$A$14")
    name(wb, "RSK_Nivel", S26, "$H$6:$H$14")
    put(ws, "A16", "Risco com maior exposição", "label", bold=True)
    put(ws, "C16", "=INDEX(RSK_Nome,MATCH(MAX(RSK_Exp),RSK_Exp,0))&\" (\"&MAX(RSK_Exp)&\")\"", "grey")
    name(wb, "RSK_Top", S26, "$C$16")
    put(ws, "A17", "Riscos críticos", "label")
    put(ws, "C17", '=COUNTIF(RSK_Nivel,"🔴*")', "grey", "0")
    name(wb, "RSK_Red", S26, "$C$17")
    # matriz 5x5
    section(ws, 19, 1, "MATRIZ DE RISCO 5 × 5 (nº de riscos em cada célula)", 8)
    put(ws, "A20", "Probabilidade ↓ / Impacto →", "label", bold=True)
    for i in range(5):
        put(ws, (20, 2 + i), i + 1, "label", bold=True, align="center")
    for pi, p in enumerate(range(5, 0, -1)):
        r = 21 + pi
        put(ws, (r, 1), p, "label", bold=True, align="center")
        for i in range(5):
            put(ws, (r, 2 + i), f"=COUNTIFS($E$6:$E$14,{p},$F$6:$F$14,{i + 1})", "calc", '0;-0;""', align="center")
            score = p * (i + 1)
            colr = C_ERR[0] if score >= 15 else (C_WARN[0] if score >= 8 else C_OK[0])
            ws.cell(row=r, column=2 + i).fill = fill(colr)
    protect(ws)


def build_dashboard(wb):
    ws = wb.create_sheet(S29)
    title(ws, "29 — DASHBOARD EXECUTIVO", "Leitura em 60 segundos. Semáforos com limites parametrizados (28_KPI_FINANCEIROS / 00_CONFIGURAÇÃO).", "CAMADA 3 — OUTPUT")
    put(ws, "A4", '=CFG_Nome&" — situação a "&TEXT(CFG_DataRef,"dd/mm/yyyy")', "label", bold=True)
    tiles = [("Receita (acum.)", "=DR_Rec", NUM, "=K_GV_S"), ("EBITDA (acum.)", "=DR_EBITDA", NUM, "=K_MEBITDA_S"), ("Resultado líquido", "=DR_RL", NUM, "=K_ML_S"),
             ("Caixa + aplicações", f"={LIQ}", NUM, "=TES_Estado"), ("Dívida financeira", f"={DIVIDA}", NUM, "=K_DEB_S"), ("Clientes (saldo)", "=CLI_Total", NUM, "=K_PMR_S"),
             ("Clientes vencidos", "=CLI_Venc", NUM, '=IF(CLI_V90>0,"🔴 Crítico",IF(CLI_Venc>0,"🟡 Atenção","🟢 Normal"))'), ("Fornecedores (saldo)", "=FRN_Total", NUM, "=K_PMP_S"),
             ("IVA a pagar (mês)", "=IVA_PagarMes", NUM, "=IVA_Estado"), ("Imposto Industrial estimado", "=II_Estimado", NUM, "=II_Estado"),
             ("Margem líquida", "=K_ML", PCT, "=K_ML_S"), ("Liquidez geral", "=K_LG", MULT, "=K_LG_S"), ("ROE (anualizado)", "=K_ROE", PCT, "=K_ROE_S"),
             ("Execução orçamental (custos)", "=BVA_ExecCustos", PCT, '=IF(BVA_Exced>0,"🔴 Crítico",IF(BVA_Red>0,"🟡 Atenção","🟢 Normal"))'),
             ("Cash flow operacional", "=DFC_Op", NUM, '=IF(DFC_Op<0,"🔴 Crítico","🟢 Normal")'), ("Risco financeiro (topo)", "=RSK_Top", None, '=IF(RSK_Red>0,"🔴 Crítico",IF(MAX(RSK_Exp)>=8,"🟡 Atenção","🟢 Normal"))')]
    for i, (lab, f, fmt, s) in enumerate(tiles):
        r = 6 + (i // 4) * 4
        c = 1 + (i % 4) * 3
        ws.merge_cells(start_row=r, start_column=c, end_row=r, end_column=c + 1)
        ws.merge_cells(start_row=r + 1, start_column=c, end_row=r + 1, end_column=c + 1)
        ws.merge_cells(start_row=r + 2, start_column=c, end_row=r + 2, end_column=c + 1)
        x = ws.cell(row=r, column=c, value=lab)
        x.font = font(True, "FFFFFF", 9)
        x.fill = fill(C_HEAD_FILL)
        y = ws.cell(row=r + 1, column=c, value=f)
        y.font = font(True, "1F3864", 14)
        y.alignment = Alignment(horizontal="center")
        if fmt:
            y.number_format = fmt
        z = ws.cell(row=r + 2, column=c, value=s)
        z.font = font(True, "000000", 9)
        z.alignment = Alignment(horizontal="center")
        status_cf(ws, z.coordinate)
    for col in range(1, 13):
        ws.column_dimensions[CL(col)].width = 13 if col % 3 else 3
    put(ws, "A23", "Estado do sistema:", "label", bold=True)
    put(ws, "C23", "=SYS_Estado", "grey", bold=True)
    status_cf(ws, "C23")
    put(ws, "A24", "Alertas activos:", "label", bold=True)
    put(ws, "C24", "=ALR_Count", "grey", "0")
    # gráficos
    ch = BarChart()
    ch.type = "col"
    ch.title = "Receita, custos operacionais e resultado líquido (mensal)"
    ch.y_axis.title = "Kz"
    dre = wb["22_DRE"]
    for key, lab in [("DRM_Rec", "Receita"), ("DRM_Cust", "Custos operacionais"), ("DRM_RL", "Resultado líquido")]:
        ref = wb.defined_names[key].attr_text.split("!")[1].replace("$", "")
        a, b = ref.split(":")
        row = int("".join(ch_ for ch_ in a if ch_.isdigit()))
        data = Reference(dre, min_col=3, max_col=14, min_row=row, max_row=row)
        ch.add_data(data, from_rows=True, titles_from_data=False)
        ch.series[-1].tx = SeriesLabel(v=lab)
    ch.set_categories(Reference(dre, min_col=3, max_col=14, min_row=5, max_row=5))
    ch.height, ch.width = 8, 18
    ws.add_chart(ch, "A27")
    fc = wb["19_FLUXO_DE_CAIXA"]
    ref = wb.defined_names["FC_SF"].attr_text.split("!")[1].replace("$", "")
    row = int("".join(ch_ for ch_ in ref.split(":")[0] if ch_.isdigit()))
    lc = LineChart()
    lc.title = "Saldo de meios monetários (fim do mês)"
    lc.add_data(Reference(fc, min_col=2, max_col=13, min_row=row, max_row=row), from_rows=True, titles_from_data=False)
    lc.series[0].tx = SeriesLabel(v="Saldo final")
    lc.set_categories(Reference(fc, min_col=2, max_col=13, min_row=5, max_row=5))
    lc.height, lc.width = 8, 14
    ws.add_chart(lc, "H27")
    cl = wb["07_CLIENTES"]
    bc = BarChart()
    bc.type = "bar"
    bc.title = "Aging de clientes"
    bc.add_data(Reference(cl, min_col=2, max_col=8, min_row=6, max_row=6), from_rows=True, titles_from_data=False)
    bc.series[0].tx = SeriesLabel(v="Saldo")
    bc.set_categories(Reference(cl, min_col=2, max_col=8, min_row=5, max_row=5))
    bc.height, bc.width = 8, 18
    ws.add_chart(bc, "A45")
    iv = wb["12_IVA"]
    ref = wb.defined_names["IVA_PagarRow"].attr_text.split("!")[1].replace("$", "")
    row = int("".join(ch_ for ch_ in ref.split(":")[0] if ch_.isdigit()))
    ic = BarChart()
    ic.title = "IVA a pagar por mês"
    ic.add_data(Reference(iv, min_col=2, max_col=13, min_row=row, max_row=row), from_rows=True, titles_from_data=False)
    ic.series[0].tx = SeriesLabel(v="IVA a pagar")
    ic.set_categories(Reference(iv, min_col=2, max_col=13, min_row=5, max_row=5))
    ic.height, ic.width = 8, 14
    ws.add_chart(ic, "H45")
    protect(ws)
