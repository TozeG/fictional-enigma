"""Módulo fiscal: parametrização AGT, IVA, facturação, SAF-T, Imposto Industrial, calendário e base legal."""
from datetime import date
from openpyxl.utils import get_column_letter as CL
from core import *
from sheets_ledgers import MESES, listing, J
import data as D

S11, S12, S13, S14, S15, S34, S35 = ("11_FISCALIDADE_AGT", "12_IVA", "13_FACTURAÇÃO_FISCAL", "14_SAFT", "15_IMPOSTO_INDUSTRIAL",
                                     "34_CALENDÁRIO_FISCAL_AGT", "35_BASE_LEGAL")
DISCLAIMER = ("Estruturado para conformidade com o quadro legal identificado e sujeito à validação contabilística, fiscal e técnica "
              "antes da utilização oficial.")


def build_fiscalidade(wb):
    ws = wb.create_sheet(S11)
    title(ws, "11 — FISCALIDADE AGT: PARAMETRIZAÇÃO FISCAL RASTREÁVEL",
          "Cada taxa tem diploma, artigo, vigência, fonte e estado. 'Regra legal' = conteúdo da lei; 'Parâmetro do modelo' = pressuposto técnico a validar.",
          "CAMADA 1 — INPUT (parâmetros legais: protegido; alterar apenas após verificação)")
    put(ws, "A4", DISCLAIMER, "note")
    heads = ["Código", "Imposto", "Descrição", "Taxa", "Natureza (Regra legal / Parâmetro)", "Diploma", "Artigo / verba", "Vigência — início",
             "Vigência — fim", "Última verificação", "Fonte", "Estado de validação", "Observação", "Linhas no Diário", "Alerta"]
    header(ws, 6, 1, heads, [10, 16, 40, 8, 16, 40, 18, 11, 11, 11, 40, 22, 40, 8, 30])
    n = 40
    for i in range(n):
        r = 7 + i
        v = D.TAXAS[i] if i < len(D.TAXAS) else (None,) * 12
        fm = ["@", None, None, PCT, None, None, None, DATE, DATE, DATE, None, None, None]
        for j in range(12):
            put(ws, (r, 1 + j), v[j], "input", fm[j], wrap=j in (5, 10, 12))
        put(ws, (r, 14), f'=IF(A{r}="","",COUNTIF(J_CodF,A{r}))', "grey", "0")
        put(ws, (r, 15), f'=IF(A{r}="","",IF(AND(N{r}>0,ISNUMBER(SEARCH("VALIDAR",L{r}))),"🟡 Em uso com taxa POR VALIDAR",IF(AND(N{r}>0,D{r}=""),"🔴 Em uso sem taxa",IF(ISNUMBER(SEARCH("VALIDAR",L{r})),"🟡 POR VALIDAR","🟢 OK"))))', "grey")
    r1 = 6 + n
    for nm, c in [("TX_Cod", "A"), ("TX_Taxa", "D"), ("TX_Estado", "L"), ("TX_Uso", "N"), ("TX_Alerta", "O")]:
        name(wb, nm, S11, f"${c}$7:${c}${r1}")
    status_cf(ws, f"L7:L{r1}")
    status_cf(ws, f"O7:O{r1}")
    name(wb, "TX_II", S11, "$D$" + str(7 + [t[0] for t in D.TAXAS].index("II_GER")))
    name(wb, "TX_INSS_T", S11, "$D$" + str(7 + [t[0] for t in D.TAXAS].index("INSS_TRAB")))
    name(wb, "TX_RET", S11, "$D$" + str(7 + [t[0] for t in D.TAXAS].index("RET_SERV")))
    # ---------------- IRT ----------------
    r = r1 + 2
    section(ws, r, 1, "TABELA IRT — GRUPO A (carregar a partir do Diário da República — Lei do OGE 2026)", 8)
    put(ws, (r + 1, 1), "Estado: POR VALIDAR. Fontes secundárias divergem quanto ao limite de isenção (100 000 vs 150 000 Kz). O modelo NÃO assume valores: preencha com a tabela oficial.", "note")
    header(ws, r + 2, 1, ["Escalão", "Limite inferior (Kz)", "Limite superior (Kz)", "Parcela fixa (Kz)", "Taxa sobre o excesso"], None)
    t0 = r + 3
    for i in range(14):
        put(ws, (t0 + i, 1), i + 1, "label")
        for j in range(4):
            put(ws, (t0 + i, 2 + j), None, "input", PCT if j == 3 else NUM)
    t1 = t0 + 13
    name(wb, "IRT_Inf", S11, f"$B${t0}:$B${t1}")
    name(wb, "IRT_PF", S11, f"$D${t0}:$D${t1}")
    name(wb, "IRT_Tx", S11, f"$E${t0}:$E${t1}")
    c0 = t0
    put(ws, (c0, 8), "CALCULADORA IRT (Grupo A)", "label", bold=True)
    calc = [("Remuneração bruta mensal", 400_000, "input"), ("Rendimentos não sujeitos/isentos (input)", 0, "input"),
            ("Contribuição INSS do trabalhador", f"=ROUND(I{c0 + 1}*TX_INSS_T,2)", "grey"),
            ("Matéria colectável", f"=I{c0 + 1}-I{c0 + 2}-I{c0 + 3}", "grey"),
            ("IRT a reter", f'=IF(COUNT(IRT_Inf)=0,"TABELA POR VALIDAR",IFERROR(INDEX(IRT_PF,MATCH(I{c0 + 4},IRT_Inf,1))+(I{c0 + 4}-INDEX(IRT_Inf,MATCH(I{c0 + 4},IRT_Inf,1)))*INDEX(IRT_Tx,MATCH(I{c0 + 4},IRT_Inf,1)),0))', "grey")]
    for i, (lab, f, k) in enumerate(calc):
        put(ws, (c0 + 1 + i, 8), lab, "label")
        put(ws, (c0 + 1 + i, 9), f, k, NUM)
    ws.column_dimensions["H"].width = 36
    ws.column_dimensions["I"].width = 18
    # ---------------- impostos a entregar ----------------
    r = t1 + 2
    section(ws, r, 1, "POSIÇÃO FISCAL À DATA DE REPORTE (saldos das contas do Estado)", 8)
    header(ws, r + 1, 1, ["Conta", "Imposto / obrigação", "Saldo (credor + / devedor −)", "Estado"], None)
    rows = [("34.1", "Imposto Industrial (estimativa − retenções/pagamentos)"), ("34.3", "IRT — retenções a entregar"), ("34.4", "Imposto de Selo"),
            ("34.5", "IVA (líquido)"), ("34.6", "Retenções na fonte a terceiros"), ("34.9.1", "INSS"), ("34.9.2", "Imposto Predial"), ("34.9.3", "IAC")]
    for i, (c, lab) in enumerate(rows):
        rr = r + 2 + i
        put(ws, (rr, 1), c, "label")
        put(ws, (rr, 2), lab, "label")
        put(ws, (rr, 3), f'=-(SUMIFS(J_DC,J_Conta,"{c}",J_Ano,CFG_Ano,J_Data,"<="&CFG_DataRef)+SUMIFS(J_DC,J_Conta,"{c}.*",J_Ano,CFG_Ano,J_Data,"<="&CFG_DataRef))', "grey", NUM)
        put(ws, (rr, 4), f'=IF(C{rr}>0.005,"🟡 A entregar / regularizar",IF(C{rr}<-0.005,"🟢 Crédito do contribuinte","🟢 Sem saldo"))', "grey")
    re_ = r + 2 + len(rows)
    put(ws, (re_, 2), "Total a entregar ao Estado (saldos credores)", "label", bold=True)
    put(ws, (re_, 3), f"=SUMIF(C{r + 2}:C{re_ - 1},\">0\")", "grey", NUM, bold=True)
    name(wb, "FIS_Total", S11, f"$C${re_}")
    name(wb, "FIS_II", S11, f"$C${r + 2}")
    status_cf(ws, f"D{r + 2}:D{re_}")
    # ---------------- retenções ----------------
    r = re_ + 2
    section(ws, r, 1, "RETENÇÕES NA FONTE SOFRIDAS — CONTROLO", 8)
    put(ws, (r + 1, 1), "Base sujeita (código RET_SERV)", "label")
    put(ws, (r + 1, 3), '=SUMIFS(J_Base,J_CodF,"RET_SERV",J_Ano,CFG_Ano,J_Data,"<="&CFG_DataRef)', "grey", NUM)
    put(ws, (r + 2, 1), "Retenção calculada (base × taxa)", "label")
    put(ws, (r + 2, 3), f"=ROUND(C{r + 1}*TX_RET,2)", "grey", NUM)
    put(ws, (r + 3, 1), "Retenção contabilizada (34.1.2 débito, RET_SERV)", "label")
    put(ws, (r + 3, 3), '=SUMIFS(J_Deb,J_CodF,"RET_SERV",J_Ano,CFG_Ano,J_Data,"<="&CFG_DataRef)', "grey", NUM)
    put(ws, (r + 4, 1), "Estado", "label")
    put(ws, (r + 4, 3), f'=IF(ABS(C{r + 2}-C{r + 3})<=CFG_Tol,"🟢 Retenções conciliadas","🔴 Retenções inconsistentes")', "grey")
    status_cf(ws, f"C{r + 4}")
    name(wb, "RET_Estado", S11, f"$C${r + 4}")
    name(wb, "RET_Sofridas", S11, f"$C${r + 3}")
    # ---------------- protocolo ----------------
    r = r + 6
    section(ws, r, 1, "PROTOCOLO OBRIGATÓRIO ANTES DE APLICAR UM IMPOSTO A UMA OPERAÇÃO", 8)
    passos = ["1. Natureza da operação (transmissão de bens, prestação de serviços, importação, rendimento, acto sujeito a selo…)",
              "2. Sujeito passivo (quem liquida, quem retém, quem suporta)", "3. Regime fiscal da entidade e do terceiro (geral, simplificado, exclusão, não residente)",
              "4. Legislação vigente à data da operação (ver 35_BASE_LEGAL)", "5. Eventual isenção ou não sujeição (indicar o fundamento legal no documento)",
              "6. Taxa aplicável (ver tabela acima e o seu estado de validação)", "7. Base tributável (valor, câmbio, descontos, adiantamentos)"]
    for i, p in enumerate(passos):
        put(ws, (r + 1 + i, 1), p, "label")
    protect(ws)


def build_iva(wb):
    ws = wb.create_sheet(S12)
    title(ws, "12 — IVA: MAPA DE APURAMENTO MENSAL E CONCILIAÇÃO", "IVA liquidado − IVA dedutível ± regularizações − crédito do período anterior = IVA a pagar / (a recuperar).",
          "CAMADA 2/3 — PROCESSAMENTO E OUTPUT (reembolso pedido = input)")
    header(ws, 5, 1, ["Rubrica"] + MESES + ["Total ano"], [52] + [12] * 13)
    ws.freeze_panes = "B6"

    def mes(m):
        return f"J_Ano,CFG_Ano,J_Mes,{m}"
    rows = [
        ("OPERAÇÕES ACTIVAS (bases)", None, None),
        ("Operações tributáveis — taxa geral (IVA_GER)", lambda m: f'=SUMIFS(J_Base,J_CodF,"IVA_GER",J_TipoIVA,"Liquidado",{mes(m)})', "BASE_GER"),
        ("Operações tributáveis — hotelaria/restauração (IVA_HOT)", lambda m: f'=SUMIFS(J_Base,J_CodF,"IVA_HOT",J_TipoIVA,"Liquidado",{mes(m)})', None),
        ("Operações tributáveis — bens alimentares (IVA_ALI)", lambda m: f'=SUMIFS(J_Base,J_CodF,"IVA_ALI",J_TipoIVA,"Liquidado",{mes(m)})', None),
        ("Operações tributáveis — Cabinda (IVA_CAB)", lambda m: f'=SUMIFS(J_Base,J_CodF,"IVA_CAB",J_TipoIVA,"Liquidado",{mes(m)})', None),
        ("Operações isentas sem direito à dedução (IVA_ISE)", lambda m: f'=SUMIFS(J_Base,J_CodF,"IVA_ISE",{mes(m)})', "BASE_ISE"),
        ("Exportações / isentas com dedução (IVA_EXP)", lambda m: f'=SUMIFS(J_Base,J_CodF,"IVA_EXP",{mes(m)})', None),
        ("Operações não sujeitas (IVA_NSUJ)", lambda m: f'=SUMIFS(J_Base,J_CodF,"IVA_NSUJ",{mes(m)})', None),
        ("OPERAÇÕES PASSIVAS (bases)", None, None),
        ("Aquisições com IVA dedutível (base)", lambda m: f'=SUMIFS(J_Base,J_TipoIVA,"Dedutível",{mes(m)})', None),
        ("  das quais: importações (documento DU)", lambda m: f'=SUMIFS(J_Base,J_TipoIVA,"Dedutível",J_TipoDoc,"DU",{mes(m)})', None),
        ("APURAMENTO", None, None),
        ("IVA liquidado (contabilidade, 34.5.3)", lambda m: f'=-SUMIFS(J_DC,J_Conta,"34.5.3",J_Nat,"<>Apuramento de IVA",{mes(m)})', "LIQ"),
        ("  do qual: sobre adiantamentos recebidos", lambda m: f'=-SUMIFS(J_DC,J_Conta,"34.5.3",J_Nat,"<>Apuramento de IVA",J_Nat,"Recebimento de cliente",{mes(m)})', None),
        ("IVA dedutível (contabilidade, 34.5.2)", lambda m: f'=SUMIFS(J_DC,J_Conta,"34.5.2",J_Nat,"<>Apuramento de IVA",{mes(m)})', "DED"),
        ("IVA suportado não dedutível / a classificar (34.5.1)", lambda m: f'=SUMIFS(J_DC,J_Conta,"34.5.1",J_Nat,"<>Apuramento de IVA",{mes(m)})', None),
        ("Regularizações a favor do sujeito passivo (34.5.4.1)", lambda m: f'=SUMIFS(J_DC,J_Conta,"34.5.4.1",J_Nat,"<>Apuramento de IVA",{mes(m)})', "REGSP"),
        ("  das quais: notas de crédito emitidas", lambda m: f'=SUMIFS(J_DC,J_Conta,"34.5.4.1",J_Nat,"<>Apuramento de IVA",J_TipoDoc,"NC",{mes(m)})', None),
        ("Regularizações a favor do Estado (34.5.4.2)", lambda m: f'=-SUMIFS(J_DC,J_Conta,"34.5.4.2",J_Nat,"<>Apuramento de IVA",{mes(m)})', "REGE"),
        ("  das quais: notas de débito emitidas", lambda m: f'=-SUMIFS(J_DC,J_Conta,"34.5.4.2",J_Nat,"<>Apuramento de IVA",J_TipoDoc,"ND",{mes(m)})', None),
        ("Crédito de IVA do período anterior (reporte)", "CARRY", "CRED"),
        ("IVA APURADO DO PERÍODO", "APUR", "APUR"),
        ("IVA A PAGAR", "PAGAR", "PAGAR"),
        ("IVA A RECUPERAR", "RECUP", "RECUP"),
        ("Reembolso pedido (input)", "INPUT", "REEMB"),
        ("Crédito a reportar para o período seguinte", "REPORT", "REPORT"),
        ("CONCILIAÇÃO CONTABILIDADE × MAPA FISCAL", None, None),
        ("IVA liquidado calculado (Σ base × taxa)", lambda m: f'=SUMIFS(J_IVACalc,J_TipoIVA,"Liquidado",{mes(m)})', "LIQC"),
        ("Diferença liquidado (contab. − calculado)", "DIFLIQ", "DIFLIQ"),
        ("IVA dedutível calculado (Σ base × taxa)", lambda m: f'=SUMIFS(J_IVACalc,J_TipoIVA,"Dedutível",{mes(m)})', "DEDC"),
        ("Diferença dedutível (contab. − calculado)", "DIFDED", "DIFDED"),
        ("Estado do mês", "EST", "EST"),
    ]
    pos = {}
    r = 6
    for lab, f, key in rows:
        if f is None:
            section(ws, r, 1, lab, 14)
            r += 1
            continue
        pos[key or f"r{r}"] = r
        put(ws, (r, 1), lab, "label", bold=key in ("APUR", "PAGAR", "RECUP", "EST"))
        r += 1
    # preencher fórmulas
    r = 6
    for lab, f, key in rows:
        if f is None:
            r += 1
            continue
        for m in range(1, 13):
            c = CL(1 + m)
            p = CL(m)
            if callable(f):
                v = f(m)
            elif f == "CARRY":
                v = 0 if m == 1 else f"={p}{pos['REPORT']}"
            elif f == "APUR":
                v = f"={c}{pos['LIQ']}-{c}{pos['DED']}-{c}{pos['REGSP']}+{c}{pos['REGE']}-{c}{pos['CRED']}"
            elif f == "PAGAR":
                v = f"=MAX(0,{c}{pos['APUR']})"
            elif f == "RECUP":
                v = f"=MAX(0,-{c}{pos['APUR']})"
            elif f == "INPUT":
                v = None
            elif f == "REPORT":
                v = f"={c}{pos['RECUP']}-N({c}{pos['REEMB']})"
            elif f == "DIFLIQ":
                v = f"={c}{pos['LIQ']}-{c}{pos['LIQC']}"
            elif f == "DIFDED":
                v = f"={c}{pos['DED']}-{c}{pos['DEDC']}"
            elif f == "EST":
                v = f'=IF({m}>CFG_MesRep,"",IF(OR(ABS({c}{pos["DIFLIQ"]})>CFG_Tol,ABS({c}{pos["DIFDED"]})>CFG_Tol),"🔴 INCONSISTENTE",IF({c}{pos["PAGAR"]}>0,"🟡 IVA a pagar","🟢 Conforme")))'
            put(ws, (r, 1 + m), v, "input" if f == "INPUT" else "calc", NUM)
        if f not in ("EST",):
            put(ws, (r, 14), "" if f in ("CARRY", "REPORT") else f"=SUM(B{r}:M{r})", "grey", NUM)
        r += 1
    status_cf(ws, f"B{pos['EST']}:M{pos['EST']}")
    r += 1
    put(ws, (r, 1), "IVA a pagar acumulado até ao mês de reporte", "label", bold=True)
    put(ws, (r, 2), f"=SUMPRODUCT((COLUMN(B{pos['PAGAR']}:M{pos['PAGAR']})-1<=CFG_MesRep)*B{pos['PAGAR']}:M{pos['PAGAR']})", "grey", NUM, bold=True)
    name(wb, "IVA_PagarAcum", S12, f"$B${r}")
    put(ws, (r + 1, 1), "IVA a pagar do mês de reporte", "label")
    put(ws, (r + 1, 2), f"=INDEX(B{pos['PAGAR']}:M{pos['PAGAR']},CFG_MesRep)", "grey", NUM)
    name(wb, "IVA_PagarMes", S12, f"$B${r + 1}")
    put(ws, (r + 2, 1), "Crédito a reportar no mês de reporte", "label")
    put(ws, (r + 2, 2), f"=INDEX(B{pos['REPORT']}:M{pos['REPORT']},CFG_MesRep)", "grey", NUM)
    put(ws, (r + 3, 1), "Saldo líquido das contas 34.5 (credor +)", "label")
    put(ws, (r + 3, 2), '=-(SUMIFS(J_DC,J_Conta,"34.5.*",J_Ano,CFG_Ano,J_Data,"<="&CFG_DataRef))', "grey", NUM)
    put(ws, (r + 4, 1), "Apuramento acumulado − pagamentos/reembolsos contabilizados", "label")
    put(ws, (r + 4, 2), f"=SUMPRODUCT((COLUMN(B{pos['APUR']}:M{pos['APUR']})-1<=CFG_MesRep)*(B{pos['LIQ']}:M{pos['LIQ']}-B{pos['DED']}:M{pos['DED']}-B{pos['REGSP']}:M{pos['REGSP']}+B{pos['REGE']}:M{pos['REGE']}))"
                          '-SUMIFS(J_Deb,J_Conta,"34.5.6",J_Ano,CFG_Ano,J_Data,"<="&CFG_DataRef)-SUMIFS(J_Deb,J_Conta,"34.5.8",J_Ano,CFG_Ano,J_Data,"<="&CFG_DataRef)', "grey", NUM)
    name(wb, "IVA_Saldo345", S12, f"$B${r + 3}")
    name(wb, "IVA_ApurAcum", S12, f"$B${r + 4}")
    name(wb, "IVA_EstRow", S12, f"$B${pos['EST']}:$M${pos['EST']}")
    put(ws, (r + 5, 1), "ESTADO DA CONCILIAÇÃO DO IVA", "label", bold=True)
    put(ws, (r + 5, 2), f'=IF(AND(COUNTIF(B{pos["EST"]}:M{pos["EST"]},"🔴*")=0,ABS(B{r + 3}-B{r + 4})<=CFG_Tol),"🟢 IVA conciliado","🔴 IVA contabilístico ≠ mapa fiscal")', "grey", bold=True)
    status_cf(ws, f"B{r + 5}")
    name(wb, "IVA_Estado", S12, f"$B${r + 5}")
    name(wb, "IVA_PagarRow", S12, f"$B${pos['PAGAR']}:$M${pos['PAGAR']}")
    name(wb, "IVA_LiqRow", S12, f"$B${pos['LIQ']}:$M${pos['LIQ']}")
    put(ws, (r + 7, 1), "Nota: lançamentos directos em 34.5.2 (dedutível) e 34.5.3 (liquidado). O modelo apura por formula; os lançamentos de apuramento (34.5.5 → 34.5.6/34.5.7) são opcionais e, se feitos, devem usar a natureza 'Regularização'.", "note")
    protect(ws)


def build_facturacao(wb):
    ws = wb.create_sheet(S13)
    title(ws, "13 — FACTURAÇÃO FISCAL E CONFORMIDADE AGT (DP n.º 71/25)",
          "Registo gerado dos documentos emitidos (FT, FR, NC, ND, RC) a partir do Diário. A folha Excel NÃO substitui software de facturação validado pela AGT.",
          "CAMADA 3 — OUTPUT (checklist = input)")
    put(ws, "A4", DISCLAIMER, "note")
    cols = [("ID", 6, "0", J("ID")), ("Tipo", 5, None, J("TipoDoc", True)), ("Série", 6, None, J("Serie", True)), ("Nº", 6, "0", J("NumDoc")),
            ("Data", 10, DATE, J("Data")), ("NIF adquirente", 12, None, J("NIF", True)), ("Adquirente", 22, None, J("Terceiro", True)),
            ("Base tributável", 13, NUM, '=IF({L}="","",SUMIFS(J_Base,J_ID,C{r},J_CodF,"IVA*"))'),
            ("IVA", 12, NUM, '=IF({L}="","",ABS(SUMIFS(J_DC,J_ID,C{r},J_TipoIVA,"Liquidado")+SUMIFS(J_DC,J_ID,C{r},J_TipoIVA,"Regularização")))'),
            ("Total do documento", 13, NUM, '=IF({L}="","",IF(D{r}="RC",SUMIFS(J_Cred,J_ID,C{r},J_G2,"31"),J{r}+K{r}))'),
            ("Hash", 7, None, J("Hash", True)), ("Certificado software", 18, None, J("Cert", True)), ("Estado doc.", 10, None, J("EstDoc", True)),
            ("Estado AGT", 11, None, J("EstAGT", True)), ("Data comunicação", 10, DATE, '=IF({L}="","",IF(N(INDEX(J_DtCom,{L}))=0,"",INDEX(J_DtCom,{L})))'),
            ("Erro comunicação", 18, None, J("ErroCom", True)),
            ("Sequência", 14, None, '=IF({L}="","",IF(F{r}=1,"🟢 OK",IF(COUNTIFS($D$12:$D$311,D{r},$E$12:$E$311,E{r},$F$12:$F$311,F{r}-1)>0,"🟢 OK","🔴 Quebra de sequência")))'),
            ("Validação do documento", 30, None, '=IF({L}="","",IF(M{r}="","🔴 Sem hash",IF(N{r}="","🔴 Sem certificado de software",IF(P{r}="Erro","🔴 Erro de comunicação: "&R{r},IF(S{r}<>"🟢 OK",S{r},IF(AND(D{r}<>"RC",H{r}=""),"🔴 Sem NIF do adquirente",IF(P{r}="Pendente","🟡 Comunicação pendente",IF(INDEX(J_Dup,{L})=1,"🔴 Documento duplicado","🟢 Conforme"))))))))')]
    last = listing(ws, 12, 300, "SeqFact", cols)
    status_cf(ws, f"S12:T{last}")
    for nm, c in [("FAT_Tipo", "D"), ("FAT_Val", "T"), ("FAT_Hash", "M"), ("FAT_Seq", "S"), ("FAT_AGT", "P"), ("FAT_Total", "L")]:
        name(wb, nm, S13, f"${c}$12:${c}${last}")
    # resumo
    section(ws, 5, 1, "RESUMO", 10)
    res = [("Documentos emitidos", "=A10"), ("Conformes", '=COUNTIF(FAT_Val,"🟢*")'), ("Com alertas (🟡)", '=COUNTIF(FAT_Val,"🟡*")'),
           ("Não conformes (🔴)", '=COUNTIF(FAT_Val,"🔴*")')]
    for i, (lab, f) in enumerate(res):
        put(ws, (6, 1 + 3 * i), lab, "label")
        put(ws, (6, 3 + 3 * i), f, "grey", "0")
    put(ws, "A7", "Estado", "label", bold=True)
    put(ws, "C7", '=IF(COUNTIF(FAT_Val,"🔴*")>0,"🔴 Documentos fiscais inconsistentes",IF(COUNTIF(FAT_Val,"🟡*")>0,"🟡 Documentos com pendências","🟢 Facturação conforme"))', "grey", bold=True)
    status_cf(ws, "C7")
    name(wb, "FAT_Estado", S13, "$C$7")
    # checklist
    c0 = 23
    section(ws, 4, c0, "CHECKLIST DE CONFORMIDADE AGT", 5)
    header(ws, 5, c0, ["#", "Requisito", "Base legal", "Estado (auto / input)", "Evidência"], [4, 60, 26, 26, 30])
    items = [
        ("Software de facturação validado/certificado pela AGT", "DP 71/25", '=IF(COUNTIF(FAT_Hash,"?*")=0,"🟡 Por verificar",IF(COUNTIFS(FAT_Tipo,"?*",FAT_Hash,"")>0,"🔴 Documentos sem hash","🟢 Hash e certificado presentes"))'),
        ("Facturação electrónica: Grandes Contribuintes e fornecedores do Estado desde 01/01/2026", "DP 71/25 + regulamentação", '=IF(CFG_GC="S",IF(COUNTIF(FAT_AGT,"Erro")+COUNTIF(FAT_AGT,"Pendente")>0,"🟡 Obrigatória — há documentos por comunicar","🟢 Obrigatória — cumprida"),"🟢 Não aplicável até 01/01/2027 (confirmar enquadramento)")'),
        ("Facturação electrónica: regimes geral e simplificado de IVA desde 01/01/2027", "DP 71/25 + regulamentação", '=IF(CFG_Ano>=2027,"🟡 Obrigatória — verificar","🟡 Preparar transição até 31/12/2026")'),
        ("Séries de facturação registadas/comunicadas", "DP 71/25", "🟡 Por verificar"),
        ("Numeração sequencial sem quebras", "DP 71/25", '=IF(COUNTIF(FAT_Seq,"🔴*")>0,"🔴 Quebras de sequência","🟢 Sequência íntegra")'),
        ("Documentos comunicados à AGT sem erros", "DP 71/25", '=IF(COUNTIF(FAT_AGT,"Erro")>0,"🔴 "&COUNTIF(FAT_AGT,"Erro")&" com erro",IF(COUNTIF(FAT_AGT,"Pendente")>0,"🟡 "&COUNTIF(FAT_AGT,"Pendente")&" pendente(s)","🟢 Todos comunicados"))'),
        ("Menções obrigatórias (NIF, data, descrição, base, taxa, IVA, motivo de isenção)", "DP 71/25 / CIVA", "🟡 Por verificar"),
        ("Motivo legal de isenção indicado nas operações isentas", "Código do IVA", '=IF(COUNTIF(J_CodF,"IVA_ISE")+COUNTIF(J_CodF,"IVA_EXP")=0,"🟢 Sem operações isentas","🟡 Confirmar menção do artigo nos documentos")'),
        ("Cópias de segurança periódicas e integridade dos dados", "DP 71/25", "🟡 Por verificar"),
        ("Ficheiro SAF-T (AO) exportável e validado", "Regulamentação SAF-T", "=SAFT_Estado"),
        ("Documentos anulados com motivo e comunicação", "DP 71/25", '=IF(COUNTIF(J_EstDoc,"Anulado")=0,"🟢 Sem anulações","🟡 Verificar motivo e comunicação")'),
        ("Arquivo e conservação dos documentos pelo prazo legal", "CGT (prazo POR VALIDAR)", "🟡 Por verificar"),
    ]
    for i, (req, base, f) in enumerate(items):
        r = 6 + i
        put(ws, (r, c0), i + 1, "label")
        put(ws, (r, c0 + 1), req, "label", wrap=True)
        put(ws, (r, c0 + 2), base, "label")
        put(ws, (r, c0 + 3), f, "input" if not str(f).startswith("=") else "grey")
        put(ws, (r, c0 + 4), None, "input")
    status_cf(ws, f"{CL(c0 + 3)}6:{CL(c0 + 3)}{6 + len(items)}")
    name(wb, "AGT_Check", S13, f"${CL(c0 + 3)}$6:${CL(c0 + 3)}${5 + len(items)}")
    protect(ws)


def build_saft(wb):
    ws = wb.create_sheet(S14)
    title(ws, "14 — SAF-T (AO): MAPEAMENTO E VALIDADOR", "Prepara e valida os dados necessários ao SAF-T. A exportação XML oficial deve ser feita por software validado pela AGT.",
          "CAMADA 3 — OUTPUT")
    put(ws, "A4", "Esta folha NÃO constitui software certificado nem gera, por si só, o ficheiro SAF-T oficial. " + DISCLAIMER, "note")
    header(ws, 6, 1, ["Secção SAF-T (AO)", "Elemento", "Fonte na Matriz", "Registos", "Problemas", "Estado", "Regra de validação"], [26, 30, 34, 10, 10, 18, 60])
    rows = [
        ("Header", "TaxRegistrationNumber / CompanyName", "00_CONFIGURAÇÃO", "=1", '=IF(AND(LEN(CFG_NIF)=10,ISNUMBER(-CFG_NIF),CFG_Nome<>""),0,1)', "NIF da entidade com 10 dígitos e nome preenchido."),
        ("Header", "FiscalYear / StartDate / EndDate / CurrencyCode", "00_CONFIGURAÇÃO", "=1", '=IF(AND(CFG_Ano>2000,CFG_Moeda="AOA"),0,1)', "Exercício válido e moeda AOA."),
        ("Header", "ProductCompanyTaxID / SoftwareValidationNumber", "Diário: Nº_Certificado_Software", '=COUNTIF(J_Cert,"?*")', '=IF(COUNTIF(J_Cert,"?*")=0,1,0)', "Certificado do software presente nos documentos emitidos."),
        ("MasterFiles", "GeneralLedgerAccounts", "01_PLANO_CONTAS", '=COUNTIF(PC_Cod,"?*")', '=COUNTIFS(PC_Cod,"?*",PC_Desig,"")+COUNTIF(PC_Val,"🔴*")', "Contas com designação e sem erros de estrutura."),
        ("MasterFiles", "Customer", "01B_TERCEIROS", '=COUNTIF(T_Tipo,"Cliente*")', '=COUNTIFS(T_Tipo,"Cliente*",T_NIFok,0)', "Clientes com NIF em formato válido."),
        ("MasterFiles", "Supplier", "01B_TERCEIROS", '=COUNTIF(T_Tipo,"Fornecedor")+COUNTIF(T_Tipo,"Cliente/Fornecedor")', '=COUNTIFS(T_Tipo,"Fornecedor",T_NIFok,0)', "Fornecedores com NIF em formato válido."),
        ("MasterFiles", "Product", "09_INVENTÁRIOS", '=COUNTIF(INV_Cod,"?*")', '=COUNTIF(INV_Alerta,"🔴 Stock negativo")', "Artigos com código e sem stock negativo."),
        ("MasterFiles", "TaxTable", "11_FISCALIDADE_AGT", '=COUNTIF(TX_Cod,"?*")', '=COUNTIF(TX_Alerta,"🟡 Em uso*")+COUNTIF(TX_Alerta,"🔴*")', "Taxas em uso devem estar validadas (🟡 se POR VALIDAR)."),
        ("GeneralLedgerEntries", "Journal / Transaction / Lines", "02_DIÁRIO_LANÇAMENTOS", "=SUM(J_Primeira)", "=SUM(J_ErrFlag)", "Todos os lançamentos equilibrados e sem erros."),
        ("SourceDocuments", "SalesInvoices (FT/FR/NC/ND)", "13_FACTURAÇÃO_FISCAL", '=COUNTIF(FAT_Tipo,"FT")+COUNTIF(FAT_Tipo,"FR")+COUNTIF(FAT_Tipo,"NC")+COUNTIF(FAT_Tipo,"ND")', '=COUNTIF(FAT_Val,"🔴*")', "Hash, certificado, sequência e comunicação."),
        ("SourceDocuments", "Payments (RC)", "13_FACTURAÇÃO_FISCAL", '=COUNTIF(FAT_Tipo,"RC")', '=COUNTIFS(FAT_Tipo,"RC",FAT_Val,"🔴*")', "Recibos com hash e sequência."),
        ("SourceDocuments", "PurchaseInvoices", "02_DIÁRIO_LANÇAMENTOS", '=COUNTIFS(J_TipoDoc,"FC",J_Primeira,1)+COUNTIFS(J_TipoDoc,"FRF",J_Primeira,1)+COUNTIFS(J_TipoDoc,"NCF",J_Primeira,1)+COUNTIFS(J_TipoDoc,"DU",J_Primeira,1)', '=COUNTIFS(J_TipoDoc,"FC",J_NIF,"")', "Documentos de compra com NIF do fornecedor."),
        ("SourceDocuments", "MovementOfGoods / Stock", "09_INVENTÁRIOS", '=COUNTIF(J_Artigo,"?*")', "=0", "Movimentos de stock identificados por artigo."),
    ]
    for i, (sec, el, src, cnt, prob, rule) in enumerate(rows):
        r = 7 + i
        put(ws, (r, 1), sec, "label")
        put(ws, (r, 2), el, "label")
        put(ws, (r, 3), src, "label")
        put(ws, (r, 4), cnt, "grey", "0")
        put(ws, (r, 5), prob, "grey", "0")
        yellow = el in ("TaxTable",)
        put(ws, (r, 6), f'=IF(D{r}=0,"🟡 INCOMPLETO",IF(E{r}>0,"{"🟡 INCOMPLETO" if yellow else "🔴 INCONSISTENTE"}","🟢 CONFORME"))', "grey")
        put(ws, (r, 7), rule, "label", wrap=True)
    r = 7 + len(rows) + 1
    put(ws, (r, 1), "VALIDADOR SAF-T — ESTADO GLOBAL", "label", bold=True)
    put(ws, (r, 3), f'=IF(COUNTIF(F7:F{r - 2},"🔴*")>0,"🔴 Inconsistente",IF(COUNTIF(F7:F{r - 2},"🟡*")>0,"🟡 Incompleto","🟢 Conforme"))', "grey", bold=True)
    status_cf(ws, f"F7:F{r}")
    status_cf(ws, f"C{r}")
    name(wb, "SAFT_Estado", S14, f"$C${r}")
    put(ws, (r + 2, 1), "Legenda: 🟢 Conforme | 🟡 Incompleto | 🔴 Inconsistente. Estrutura XSD do SAF-T (AO) a confirmar no Portal da AGT (35_BASE_LEGAL).", "note")
    protect(ws)


def build_ii(wb):
    ws = wb.create_sheet(S15)
    title(ws, "15 — IMPOSTO INDUSTRIAL: RECONCILIAÇÃO CONTABILÍSTICO-FISCAL (estimativa)",
          "Resultado contabilístico ± correcções fiscais = matéria colectável × taxa = imposto estimado. Correcções com base legal a validar.",
          "CAMADA 2 — PROCESSAMENTO (correcções = input)")
    put(ws, "A4", DISCLAIMER, "note")
    ws.column_dimensions["A"].width = 58
    for c, w in zip("BCDEF", [16, 16, 30, 22, 30]):
        ws.column_dimensions[c].width = w
    # Quadro de gastos e rendimentos
    section(ws, 6, 1, "QUADRO A — GASTOS E RENDIMENTOS POR RUBRICA (acumulado até ao mês de reporte)", 6)
    header(ws, 7, 1, ["Rubrica DR", "Valor contabilístico", "% não dedutível / não tributável (input)", "Valor não dedutível / não tributável",
                      "Dedutível / tributável", "Fundamento (a validar)"], None)
    r = 8
    first = r
    for code, nome, nat, sig in D.RUBRICAS_DR:
        if code == "DR13":
            continue
        put(ws, (r, 1), f"{code} — {nome}", "label")
        put(ws, (r, 2), f'=-SUMIFS(J_DC,J_RubDR,"{code}",J_Ano,CFG_Ano,J_Mes,"<="&CFG_MesRep,J_IncDR,1)', "grey", NUM)
        put(ws, (r, 3), 0, "input", PCT)
        put(ws, (r, 4), f"=ROUND(ABS(B{r})*C{r},2)", "grey", NUM)
        put(ws, (r, 5), f"=ABS(B{r})-D{r}", "grey", NUM)
        put(ws, (r, 6), None, "input")
        put(ws, (r, 7), sig, "note")
        r += 1
    last = r - 1
    put(ws, (r, 1), "Σ gastos não dedutíveis (→ acréscimo)", "label", bold=True)
    put(ws, (r, 4), f'=SUMIFS(D{first}:D{last},G{first}:G{last},"C")', "grey", NUM, bold=True)
    gnd = r
    put(ws, (r + 1, 1), "Σ rendimentos não tributáveis (→ dedução)", "label", bold=True)
    put(ws, (r + 1, 4), f'=SUMIFS(D{first}:D{last},G{first}:G{last},"S")', "grey", NUM, bold=True)
    rnt = r + 1
    # Reconciliação
    r = rnt + 2
    section(ws, r, 1, "QUADRO B — MAPA DE RECONCILIAÇÃO CONTABILÍSTICO-FISCAL", 6)
    header(ws, r + 1, 1, ["Descrição", "Valor", "Tipo de diferença", "Base legal (a validar)", "Estado"], None)
    r += 2
    put(ws, (r, 1), "Resultado contabilístico antes de impostos (RAI)", "label", bold=True)
    put(ws, (r, 2), "=DR_RAI", "grey", NUM, bold=True)
    rai = r
    r += 1
    put(ws, (r, 1), "ACRÉSCIMOS", "label", bold=True)
    r += 1
    a0 = r
    put(ws, (r, 1), "Gastos não dedutíveis (Quadro A)", "label")
    put(ws, (r, 2), f"=D{gnd}", "grey", NUM)
    put(ws, (r, 3), "Permanente", "label")
    r += 1
    acres = ["Multas, coimas e juros compensatórios", "Amortizações acima das taxas fiscais máximas", "Provisões não aceites fiscalmente",
             "Gastos sem documento de suporte válido", "Donativos acima dos limites legais", "Outros acréscimos"]
    for a in acres:
        put(ws, (r, 1), a, "input")
        put(ws, (r, 2), 0, "input", NUM)
        put(ws, (r, 3), "Permanente" if "Amortiza" not in a and "Provis" not in a else "Temporária", "input")
        put(ws, (r, 4), "POR VALIDAR", "input")
        r += 1
    a1 = r - 1
    put(ws, (r, 1), "DEDUÇÕES", "label", bold=True)
    r += 1
    d0 = r
    put(ws, (r, 1), "Rendimentos não tributáveis (Quadro A)", "label")
    put(ws, (r, 2), f"=D{rnt}", "grey", NUM)
    put(ws, (r, 3), "Permanente", "label")
    r += 1
    for a in ["Rendimentos já tributados em IAC (se aplicável)", "Reversão de provisões anteriormente tributadas", "Benefícios fiscais", "Outras deduções"]:
        put(ws, (r, 1), a, "input")
        put(ws, (r, 2), 0, "input", NUM)
        put(ws, (r, 3), "Permanente", "input")
        put(ws, (r, 4), "POR VALIDAR", "input")
        r += 1
    d1 = r - 1
    lines = [
        ("Lucro tributável antes de prejuízos", f"=B{rai}+SUM(B{a0}:B{a1})-SUM(B{d0}:B{d1})", "grey", "LT"),
        ("Prejuízos fiscais reportáveis a deduzir (input — prazo/limite POR VALIDAR)", 0, "input", "PREJ"),
        ("MATÉRIA COLECTÁVEL", None, "grey", "MC"),
        ("Taxa aplicável (11_FISCALIDADE_AGT: II_GER)", "=TX_II", "grey", "TX"),
        ("COLECTA / IMPOSTO ESTIMADO", None, "grey", "COL"),
        ("(−) Retenções na fonte sofridas (34.1.2)", "=RET_Sofridas", "grey", "RET"),
        ("(−) Liquidação provisória / pagamentos por conta (input)", 0, "input", "LP"),
        ("IMPOSTO A PAGAR / (A RECUPERAR)", None, "grey", "PAG"),
        ("Imposto contabilizado (conta 87, acumulado)", '=SUMIFS(J_DC,J_G2,"87",J_Ano,CFG_Ano,J_Mes,"<="&CFG_MesRep)', "grey", "CONT"),
        ("Diferença contabilizado − estimado", None, "grey", "DIF"),
    ]
    pos = {}
    for lab, f, k, key in lines:
        pos[key] = r
        put(ws, (r, 1), lab, "label", bold=key in ("MC", "COL", "PAG"))
        r += 1
    formulas = {"MC": f"=MAX(0,B{pos['LT']}-B{pos['PREJ']})", "COL": f"=ROUND(B{pos['MC']}*B{pos['TX']},2)",
                "PAG": f"=B{pos['COL']}-B{pos['RET']}-B{pos['LP']}", "DIF": f"=B{pos['CONT']}-B{pos['COL']}"}
    for lab, f, k, key in lines:
        put(ws, (pos[key], 2), formulas.get(key, f), k, PCT if key == "TX" else NUM, bold=key in ("MC", "COL", "PAG"))
    put(ws, (pos["DIF"], 5), f'=IF(ABS(B{pos["DIF"]})<=CFG_Tol,"🟢 Fiscalidade conciliada",IF(B{pos["CONT"]}=0,"🟡 Estimativa por contabilizar","🔴 Imposto contabilizado ≠ estimado"))', "grey")
    status_cf(ws, f"E{pos['DIF']}")
    name(wb, "II_Estimado", S15, f"$B${pos['COL']}")
    name(wb, "II_APagar", S15, f"$B${pos['PAG']}")
    name(wb, "II_MC", S15, f"$B${pos['MC']}")
    name(wb, "II_Estado", S15, f"$E${pos['DIF']}")
    r += 1
    section(ws, r, 1, "QUADRO C — DIFERENÇAS PERMANENTES E TEMPORÁRIAS", 6)
    put(ws, (r + 1, 1), "Σ diferenças permanentes (acréscimos − deduções)", "label")
    put(ws, (r + 1, 2), f'=SUMIFS(B{a0}:B{a1},C{a0}:C{a1},"Permanente")-SUMIFS(B{d0}:B{d1},C{d0}:C{d1},"Permanente")', "grey", NUM)
    put(ws, (r + 2, 1), "Σ diferenças temporárias (acréscimos − deduções)", "label")
    put(ws, (r + 2, 2), f'=SUMIFS(B{a0}:B{a1},C{a0}:C{a1},"Temporária")-SUMIFS(B{d0}:B{d1},C{d0}:C{d1},"Temporária")', "grey", NUM)
    put(ws, (r + 3, 1), "Taxa efectiva de imposto (colecta / RAI)", "label")
    put(ws, (r + 3, 2), f"=IF(B{rai}<=0,0,B{pos['COL']}/B{rai})", "grey", PCT)
    put(ws, (r + 5, 1), "Enquadramento: contribuintes do regime geral estão obrigados a contabilidade organizada nos termos do PGC; a matéria colectável parte do resultado contabilístico (Código do Imposto Industrial — confirmar artigos).", "note")
    protect(ws)


def build_calendario(wb):
    ws = wb.create_sheet(S34)
    title(ws, "34 — CALENDÁRIO FISCAL AGT", "Prazos = PARAMETRIZAÇÃO a validar (não assumidos como regra legal). Alertas calculados face à data de referência (00_CONFIGURAÇÃO).",
          "CAMADA 1 — INPUT (estado, entrega, comprovativo)  |  CAMADA 3 — alertas")
    heads = ["Obrigação", "Imposto", "Período", "Mês", "Regra de prazo (parâmetro)", "Estado da regra", "Data limite", "Responsável", "Estado",
             "Data de entrega", "Comprovativo", "Valor (Kz)", "Penalização potencial", "Dias para o prazo", "Alerta"]
    header(ws, 5, 1, heads, [34, 12, 9, 5, 34, 14, 11, 14, 12, 11, 16, 13, 30, 8, 30])
    ws.freeze_panes = "B6"
    obr = [
        ("Declaração periódica e pagamento do IVA", "IVA", "Último dia do mês seguinte", "IVA"),
        ("Entrega das retenções de IRT (Grupo A)", "IRT", "Último dia do mês seguinte", "IRT"),
        ("Contribuições INSS", "INSS", "Último dia do mês seguinte", "INSS"),
        ("Entrega das retenções na fonte (Imp. Industrial) a terceiros", "II", "Último dia do mês seguinte", "RET"),
        ("Entrega do Imposto de Selo liquidado", "IS", "Último dia do mês seguinte", "IS"),
    ]
    val = {"IVA": "=INDEX(IVA_PagarRow,{m})", "IRT": '=-SUMIFS(J_DC,J_Conta,"34.3.1",J_Ano,CFG_Ano,J_Mes,{m},J_IsAbe,0)*(1)',
           "INSS": '=-SUMIFS(J_DC,J_Conta,"34.9.1",J_Ano,CFG_Ano,J_Mes,{m},J_IsAbe,0)', "RET": '=-SUMIFS(J_DC,J_Conta,"34.6",J_Ano,CFG_Ano,J_Mes,{m},J_IsAbe,0)',
           "IS": '=-SUMIFS(J_DC,J_Conta,"34.4.1",J_Ano,CFG_Ano,J_Mes,{m},J_IsAbe,0)'}
    r = 6
    for m in range(1, 13):
        for ob, imp, regra, k in obr:
            put(ws, (r, 1), ob, "label")
            put(ws, (r, 2), imp, "label")
            put(ws, (r, 3), f"{m:02d}/{D.ANO}", "label")
            put(ws, (r, 4), m, "label")
            put(ws, (r, 5), regra, "input")
            put(ws, (r, 6), "POR VALIDAR", "input")
            put(ws, (r, 7), f"=EOMONTH(DATE(CFG_Ano,D{r},1),1)", "calc", DATE)
            put(ws, (r, 8), "Contabilidade", "input")
            est = "Entregue" if m <= 2 else "Por entregar"
            put(ws, (r, 9), est, "input")
            put(ws, (r, 10), date(D.ANO, m + 1, 20) if m <= 2 else None, "input", DATE)
            put(ws, (r, 11), f"Comprovativo {imp} {m:02d}/{D.ANO}" if m <= 2 else None, "input")
            put(ws, (r, 12), val[k].format(m=m), "calc", NUM)
            put(ws, (r, 13), "Multa e juros de mora nos termos do CGT (montantes POR VALIDAR)", "note")
            put(ws, (r, 14), f"=G{r}-CFG_DataRef", "calc", "0")
            put(ws, (r, 15), f'=IF(D{r}>CFG_MesRep,"—",IF(I{r}="Entregue",IF(N(J{r})>G{r},"🔴 Entregue fora do prazo","🟢 Entregue"),IF(I{r}="Dispensado","🟢 Dispensado",IF(N{r}<0,"🔴 Prazo ultrapassado",IF(N{r}<=10,"🟡 Vence em "&N{r}&" dias",IF(L{r}=0,"🟡 Verificar se há valor a declarar","🟡 Por entregar"))))))', "calc")
            r += 1
    anual = [("Declaração de rendimentos Modelo 1 (Imposto Industrial)", "II", "Até 31/05 do ano seguinte (validar)", f"=DATE(CFG_Ano+1,5,31)"),
             ("Liquidação provisória do Imposto Industrial", "II", "Data a parametrizar (validar)", None),
             ("Declaração anual de rendimentos do trabalho (IRT)", "IRT", "Data a parametrizar (validar)", None)]
    for ob, imp, regra, f in anual:
        put(ws, (r, 1), ob, "label")
        put(ws, (r, 2), imp, "label")
        put(ws, (r, 3), "Anual", "label")
        put(ws, (r, 4), 12, "label")
        put(ws, (r, 5), regra, "input")
        put(ws, (r, 6), "POR VALIDAR", "input")
        put(ws, (r, 7), f, "input", DATE)
        put(ws, (r, 8), "Direcção Financeira", "input")
        put(ws, (r, 9), "Por entregar", "input")
        put(ws, (r, 10), None, "input", DATE)
        put(ws, (r, 11), None, "input")
        put(ws, (r, 12), "=II_APagar" if "Modelo 1" in ob else None, "calc", NUM)
        put(ws, (r, 13), "Multa e juros de mora (CGT — POR VALIDAR)", "note")
        put(ws, (r, 14), f'=IF(N(G{r})=0,"",G{r}-CFG_DataRef)', "calc", "0")
        put(ws, (r, 15), f'=IF(N(G{r})=0,"🟡 Data por parametrizar",IF(I{r}="Entregue","🟢 Entregue",IF(N{r}<0,"🔴 Prazo ultrapassado",IF(N{r}<=10,"🟡 Vence em "&N{r}&" dias","🟢 Dentro do prazo"))))', "calc")
        r += 1
    dv_list(ws, f"I6:I{r - 1}", '"Por entregar,Entregue,Dispensado"')
    status_cf(ws, f"O6:O{r - 1}")
    status_cf(ws, f"F6:F{r - 1}")
    name(wb, "CAL_Alerta", S34, f"$O$6:$O${r - 1}")
    put(ws, (r + 1, 1), "Obrigações vencidas não entregues", "label", bold=True)
    put(ws, (r + 1, 12), '=COUNTIF(CAL_Alerta,"🔴 Prazo*")', "grey", "0")
    name(wb, "CAL_Vencidas", S34, f"$L${r + 1}")
    put(ws, (r + 2, 1), "Obrigações a vencer em ≤ 10 dias", "label")
    put(ws, (r + 2, 12), '=COUNTIF(CAL_Alerta,"🟡 Vence*")', "grey", "0")
    name(wb, "CAL_AVencer", S34, f"$L${r + 2}")
    protect(ws)


def build_base_legal(wb):
    ws = wb.create_sheet(S35)
    title(ws, "35 — MATRIZ LEGAL (BASE LEGAL RASTREÁVEL)", "Pesquisa efectuada em 24/09/2026 a partir de fontes secundárias (consultoras, imprensa, MINFIN). Confirmar sempre no Diário da República.",
          "CAMADA 1 — INPUT (referência)")
    put(ws, "A4", DISCLAIMER, "note")
    heads = ["Diploma", "Número", "Data", "Artigo", "Matéria", "Regra", "Aplicabilidade", "Entrada em vigor", "Revogação / alteração", "Fonte oficial / consultada", "Última verificação", "Estado"]
    header(ws, 6, 1, heads, [16, 22, 11, 14, 16, 50, 40, 12, 26, 50, 11, 26])
    for i in range(40):
        r = 7 + i
        v = D.BASE_LEGAL[i] if i < len(D.BASE_LEGAL) else (None,) * 12
        for j in range(12):
            put(ws, (r, 1 + j), v[j], "input", DATE if j == 10 else None, wrap=j in (5, 6, 9))
    status_cf(ws, "L7:L46")
    r = 49
    section(ws, r, 1, "CHECKLIST DE CONFORMIDADE LEGAL ANTES DA UTILIZAÇÃO OFICIAL", 8)
    header(ws, r + 1, 1, ["#", "Verificação", "Estado", "Responsável", "Data", "Observação"], None)
    chk = ["Pesquisar legislação angolana vigente", "Confirmar o PGC / normativo contabilístico aplicável à entidade", "Confirmar legislação fiscal vigente",
           "Confirmar Código do IVA (Lei n.º 14/23 e alterações posteriores)", "Confirmar Código do Imposto Industrial (Lei n.º 26/20 e alterações)",
           "Confirmar Código do Imposto de Selo", "Confirmar Código do IRT e tabela do OGE 2026", "Confirmar regime de facturação (DP 71/25)",
           "Confirmar requisitos da facturação electrónica (faseamento 2026/2027)", "Confirmar requisitos SAF-T (AO) — estrutura XSD vigente",
           "Confirmar obrigações declarativas e prazos perante a AGT", "Confirmar legislação posterior que altere qualquer regra", "Identificar normas revogadas",
           "Identificar normas transitórias", "Identificar regras específicas por regime (geral, simplificado, exclusão, sectoriais)"]
    for i, c in enumerate(chk):
        rr = r + 2 + i
        put(ws, (rr, 1), i + 1, "label")
        put(ws, (rr, 2), c, "label")
        put(ws, (rr, 3), "🟢 Pesquisa inicial feita (fontes secundárias)" if i == 0 else "🟡 POR VALIDAR", "input")
        put(ws, (rr, 4), None, "input")
        put(ws, (rr, 5), None, "input", DATE)
        put(ws, (rr, 6), None, "input")
    status_cf(ws, f"C{r + 2}:C{r + 1 + len(chk)}")
    name(wb, "LEG_Check", S35, f"$C${r + 2}:$C${r + 1 + len(chk)}")
    protect(ws)


def build_all(wb):
    build_fiscalidade(wb)
    build_iva(wb)
    build_facturacao(wb)
    build_saft(wb)
    build_ii(wb)
