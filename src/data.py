"""Dados-mestre, parametrização e casos de teste da Matriz PRO MASTER.

Regra: nenhuma taxa ou prazo fiscal é apresentado como regra legal sem fonte.
Os campos 'estado' distinguem  CONFIRMADO (fonte identificada) de  POR VALIDAR.
"""
from datetime import date

ANO = 2026

# ---------------------------------------------------------------------------
# PLANO DE CONTAS — estrutura baseada no PGC (Decreto n.º 82/01).
# (código, designação, tipo M=Movimento/A=Agregação)
# Subcontas analíticas (3.º/4.º nível) são SUGESTÕES do modelo: validar com o
# plano efectivamente adoptado pela entidade.
# ---------------------------------------------------------------------------
PLANO = [
    ("1", "Meios fixos e investimentos", "A"),
    ("11", "Imobilizações corpóreas", "A"),
    ("11.1", "Terrenos e recursos naturais", "M"),
    ("11.2", "Edifícios e outras construções", "M"),
    ("11.3", "Equipamento básico", "M"),
    ("11.4", "Equipamento de carga e transporte", "M"),
    ("11.5", "Equipamento administrativo", "A"),
    ("11.5.1", "Equipamento informático", "M"),
    ("11.5.2", "Mobiliário de escritório", "M"),
    ("11.9", "Outras imobilizações corpóreas", "M"),
    ("12", "Imobilizações incorpóreas", "A"),
    ("12.1", "Trespasses", "M"),
    ("12.2", "Despesas de investigação e desenvolvimento", "M"),
    ("12.3", "Propriedade industrial e outros direitos", "M"),
    ("12.9", "Outras imobilizações incorpóreas", "M"),
    ("13", "Investimentos financeiros", "A"),
    ("13.1", "Empresas subsidiárias", "M"),
    ("13.9", "Outros investimentos financeiros", "M"),
    ("14", "Imobilizações em curso", "A"),
    ("14.1", "Obras em curso", "M"),
    ("18", "Amortizações acumuladas", "A"),
    ("18.1", "Amortizações acumuladas — imobilizações corpóreas", "A"),
    ("18.1.2", "Amort. acum. — edifícios e outras construções", "M"),
    ("18.1.3", "Amort. acum. — equipamento básico", "M"),
    ("18.1.4", "Amort. acum. — equipamento de carga e transporte", "M"),
    ("18.1.5", "Amort. acum. — equipamento administrativo", "M"),
    ("18.2", "Amortizações acumuladas — imobilizações incorpóreas", "M"),
    ("2", "Existências", "A"),
    ("21", "Compras", "A"),
    ("21.1", "Compras de mercadorias", "M"),
    ("22", "Matérias-primas, subsidiárias e de consumo", "A"),
    ("22.1", "Matérias-primas", "M"),
    ("24", "Produtos acabados e intermédios", "M"),
    ("26", "Mercadorias", "A"),
    ("26.1", "Mercadorias — armazém", "M"),
    ("29", "Provisão para depreciação de existências", "M"),
    ("3", "Terceiros", "A"),
    ("31", "Clientes", "A"),
    ("31.1", "Clientes — correntes", "A"),
    ("31.1.1", "Clientes nacionais", "M"),
    ("31.1.2", "Clientes estrangeiros", "M"),
    ("31.8", "Clientes de cobrança duvidosa", "M"),
    ("32", "Fornecedores", "A"),
    ("32.1", "Fornecedores — correntes", "A"),
    ("32.1.1", "Fornecedores nacionais", "M"),
    ("32.1.2", "Fornecedores estrangeiros", "M"),
    ("32.2", "Fornecedores de imobilizado", "M"),
    ("33", "Empréstimos", "A"),
    ("33.1", "Empréstimos bancários", "A"),
    ("33.1.1", "Empréstimos bancários — médio e longo prazo", "M"),
    ("33.1.2", "Empréstimos bancários — curto prazo", "M"),
    ("34", "Estado", "A"),
    ("34.1", "Imposto sobre os lucros (Imposto Industrial)", "A"),
    ("34.1.1", "Imposto Industrial — estimativa / a pagar", "M"),
    ("34.1.2", "Imposto Industrial — retenções sofridas e pagamentos por conta", "M"),
    ("34.3", "Imposto sobre os Rendimentos do Trabalho (IRT)", "A"),
    ("34.3.1", "IRT — retenções a entregar", "M"),
    ("34.4", "Imposto de Selo", "A"),
    ("34.4.1", "Imposto de Selo a entregar", "M"),
    ("34.5", "Imposto sobre o Valor Acrescentado (IVA)", "A"),
    ("34.5.1", "IVA suportado", "M"),
    ("34.5.2", "IVA dedutível", "M"),
    ("34.5.3", "IVA liquidado", "M"),
    ("34.5.4", "IVA regularizado", "A"),
    ("34.5.4.1", "IVA — regularizações a favor do sujeito passivo", "M"),
    ("34.5.4.2", "IVA — regularizações a favor do Estado", "M"),
    ("34.5.5", "IVA — apuramento", "M"),
    ("34.5.6", "IVA a pagar", "M"),
    ("34.5.7", "IVA a recuperar", "M"),
    ("34.5.8", "IVA — reembolsos pedidos", "M"),
    ("34.6", "Retenções na fonte a entregar (terceiros)", "M"),
    ("34.9", "Outros impostos e contribuições", "A"),
    ("34.9.1", "INSS — contribuições a entregar", "M"),
    ("34.9.2", "Imposto Predial", "M"),
    ("34.9.3", "Imposto sobre a Aplicação de Capitais", "M"),
    ("35", "Entidades participantes e participadas", "M"),
    ("36", "Pessoal", "A"),
    ("36.1", "Pessoal — remunerações", "A"),
    ("36.1.1", "Remunerações a pagar", "M"),
    ("36.2", "Pessoal — adiantamentos", "M"),
    ("37", "Outros valores a receber e a pagar", "A"),
    ("37.1", "Compras de imobilizado", "M"),
    ("37.2", "Vendas de imobilizado", "M"),
    ("37.3", "Proveitos a facturar", "M"),
    ("37.4", "Encargos a repartir por períodos futuros", "A"),
    ("37.4.1", "Custos diferidos — seguros", "M"),
    ("37.5", "Encargos a pagar", "A"),
    ("37.5.1", "Encargos a pagar — fornecimentos", "M"),
    ("37.6", "Proveitos a repartir por períodos futuros", "A"),
    ("37.6.1", "Proveitos diferidos — adiantamentos de clientes", "M"),
    ("37.9", "Outros devedores e credores", "M"),
    ("38", "Provisões para cobranças duvidosas", "M"),
    ("39", "Provisões para outros riscos e encargos", "M"),
    ("4", "Meios monetários", "A"),
    ("41", "Títulos negociáveis", "M"),
    ("42", "Depósitos a prazo", "A"),
    ("42.1", "Depósitos a prazo — Banco A", "M"),
    ("43", "Depósitos à ordem", "A"),
    ("43.1", "Depósitos à ordem — moeda nacional", "A"),
    ("43.1.1", "Banco A — conta Kz", "M"),
    ("43.1.2", "Banco B — conta Kz", "M"),
    ("43.2", "Depósitos à ordem — moeda estrangeira", "A"),
    ("43.2.1", "Banco A — conta USD", "M"),
    ("45", "Caixa", "A"),
    ("45.1", "Caixa — fundo fixo", "M"),
    ("48", "Conta transitória", "M"),
    ("5", "Capital e reservas", "A"),
    ("51", "Capital", "A"),
    ("51.1", "Capital social", "M"),
    ("55", "Reservas legais", "M"),
    ("56", "Reservas de reavaliação", "M"),
    ("57", "Reservas com fins especiais", "M"),
    ("58", "Reservas livres", "M"),
    ("6", "Proveitos e ganhos por natureza", "A"),
    ("61", "Vendas", "A"),
    ("61.1", "Vendas de mercadorias", "M"),
    ("61.2", "Vendas de produtos", "M"),
    ("61.8", "Devoluções e descontos em vendas", "M"),
    ("62", "Prestações de serviço", "A"),
    ("62.1", "Serviços principais", "M"),
    ("63", "Outros proveitos operacionais", "M"),
    ("66", "Proveitos e ganhos financeiros gerais", "A"),
    ("66.1", "Juros obtidos", "M"),
    ("66.5", "Diferenças de câmbio favoráveis", "M"),
    ("68", "Outros proveitos e ganhos não operacionais", "M"),
    ("69", "Proveitos e ganhos extraordinários", "M"),
    ("7", "Custos e perdas por natureza", "A"),
    ("71", "Custo das existências vendidas e consumidas", "A"),
    ("71.1", "Custo das mercadorias vendidas", "M"),
    ("72", "Custos com o pessoal", "A"),
    ("72.2", "Remunerações — pessoal", "M"),
    ("72.5", "Encargos sobre remunerações", "M"),
    ("73", "Amortizações do exercício", "A"),
    ("73.1", "Amortizações — imobilizações corpóreas", "M"),
    ("73.2", "Amortizações — imobilizações incorpóreas", "M"),
    ("75", "Outros custos e perdas operacionais", "A"),
    ("75.2", "Fornecimentos e serviços de terceiros", "A"),
    ("75.2.1", "Material de escritório", "M"),
    ("75.2.2", "Assistência técnica e subcontratos", "M"),
    ("75.2.3", "Seguros", "M"),
    ("75.2.4", "Electricidade e água", "M"),
    ("75.2.9", "Outros fornecimentos e serviços", "M"),
    ("75.3", "Impostos e taxas", "M"),
    ("75.8", "Outros custos operacionais", "M"),
    ("76", "Custos e perdas financeiros gerais", "A"),
    ("76.1", "Juros suportados", "M"),
    ("76.5", "Diferenças de câmbio desfavoráveis", "M"),
    ("76.8", "Serviços bancários", "M"),
    ("78", "Outros custos e perdas não operacionais", "M"),
    ("79", "Custos e perdas extraordinários", "M"),
    ("8", "Resultados", "A"),
    ("81", "Resultados transitados", "A"),
    ("81.1", "Resultados transitados — exercícios anteriores", "M"),
    ("82", "Resultados operacionais", "M"),
    ("83", "Resultados financeiros", "M"),
    ("85", "Resultados não operacionais", "M"),
    ("86", "Resultados extraordinários", "M"),
    ("87", "Imposto sobre os lucros", "A"),
    ("87.1", "Imposto Industrial do exercício", "M"),
    ("88", "Resultado líquido do exercício", "M"),
    ("89", "Dividendos antecipados", "M"),
]


def classify(code):
    """Devolve natureza, B/R, rubrica balanço devedor, rubrica balanço credor, rubrica DR, conta corrente, reconciliação, fiscal, encerra."""
    c1 = code[0]
    p2 = code[:2]
    nat = "Devedora" if c1 in "1247" else "Credora" if c1 in "56" else "Mista"
    if p2 in ("18", "29", "38", "39"):
        nat = "Credora"
    br = "Resultado" if c1 in "67" or p2 in ("82", "83", "85", "86", "87", "88") else "Balanço"
    rd = rc = dr = ""
    if p2 in ("11", "14") or code.startswith("18.1"):
        rd = rc = "BA_IMOB_CORP"
    elif p2 == "12" or code.startswith("18.2"):
        rd = rc = "BA_IMOB_INC"
    elif p2 == "13":
        rd = rc = "BA_INV_FIN"
    elif c1 == "2":
        rd = rc = "BA_EXIST"
    elif p2 in ("31", "38"):
        rd, rc = "BA_CLIENTES", "BPC_OUTROS"
        if p2 == "38":
            rd = rc = "BA_CLIENTES"
    elif p2 == "32":
        rd, rc = "BA_OUTROS_REC", "BPC_FORN"
    elif code.startswith("33.1.2"):
        rd, rc = "BA_OUTROS_REC", "BPC_EMP"
    elif p2 == "33":
        rd, rc = "BA_OUTROS_REC", "BPNC_EMP"
    elif p2 == "34":
        rd, rc = "BA_ESTADO", "BPC_ESTADO"
    elif p2 in ("35", "36") or code.startswith("37.1") or code.startswith("37.2") or code.startswith("37.9"):
        rd, rc = "BA_OUTROS_REC", "BPC_OUTROS"
    elif code.startswith("37.3") or code.startswith("37.4") or code.startswith("37.5") or code.startswith("37.6"):
        rd, rc = "BA_ACRESC", "BPC_ACRESC"
    elif p2 == "39":
        rd = rc = "BPNC_PROV"
    elif p2 in ("41", "42"):
        rd, rc = "BA_APLIC", "BPC_EMP"
    elif p2 in ("43", "45", "48"):
        rd, rc = "BA_DISP", "BPC_EMP"
        if p2 == "45":
            rc = "BA_DISP"
    elif p2 == "51" or p2 in ("52", "53", "54"):
        rd = rc = "BCP_CAPITAL"
    elif p2 in ("55", "56", "57", "58"):
        rd = rc = "BCP_RESERVAS"
    elif p2 == "81":
        rd = rc = "BCP_RT"
    elif c1 in "67" or p2 in ("82", "83", "85", "86", "87", "88", "89"):
        rd = rc = "BCP_RL"
    # Rubricas da Demonstração de Resultados
    m = {"61": "DR01", "62": "DR02", "63": "DR03", "64": "DR03", "65": "DR03", "66": "DR09", "67": "DR09",
         "68": "DR11", "69": "DR11", "71": "DR04", "72": "DR06", "73": "DR07", "74": "DR08", "76": "DR10",
         "77": "DR10", "78": "DR12", "79": "DR12", "87": "DR13"}
    dr = m.get(p2, "")
    if p2 == "75":
        dr = "DR05" if code.startswith("75.2") else "DR08"
    ccorr = "S" if p2 in ("31", "32") else "N"
    rec = "S" if p2 in ("31", "32", "34", "42", "43", "45") else "N"
    fiscal = "IVA" if code.startswith("34.5") else ("II" if code.startswith("34.1") or p2 == "87" else ("IRT" if code.startswith("34.3") else ("IS" if code.startswith("34.4") else "")))
    enc = "S" if br == "Resultado" else "N"
    return nat, br, rd, rc, dr, ccorr, rec, fiscal, enc


RUBRICAS_BAL = [
    ("BA_IMOB_CORP", "Imobilizações corpóreas", "Activo não corrente"),
    ("BA_IMOB_INC", "Imobilizações incorpóreas", "Activo não corrente"),
    ("BA_INV_FIN", "Investimentos financeiros", "Activo não corrente"),
    ("BA_EXIST", "Existências", "Activo corrente"),
    ("BA_CLIENTES", "Contas a receber — clientes", "Activo corrente"),
    ("BA_ESTADO", "Estado — saldos devedores", "Activo corrente"),
    ("BA_OUTROS_REC", "Outros activos correntes", "Activo corrente"),
    ("BA_ACRESC", "Acréscimos e diferimentos activos", "Activo corrente"),
    ("BA_APLIC", "Aplicações financeiras de curto prazo", "Activo corrente"),
    ("BA_DISP", "Disponibilidades (caixa e depósitos à ordem)", "Activo corrente"),
    ("BCP_CAPITAL", "Capital", "Capital próprio"),
    ("BCP_RESERVAS", "Reservas", "Capital próprio"),
    ("BCP_RT", "Resultados transitados", "Capital próprio"),
    ("BCP_RL", "Resultado líquido do exercício", "Capital próprio"),
    ("BPNC_EMP", "Empréstimos de médio e longo prazos", "Passivo não corrente"),
    ("BPNC_PROV", "Provisões para outros riscos e encargos", "Passivo não corrente"),
    ("BPC_FORN", "Contas a pagar — fornecedores", "Passivo corrente"),
    ("BPC_EMP", "Empréstimos de curto prazo e descobertos", "Passivo corrente"),
    ("BPC_ESTADO", "Estado — saldos credores", "Passivo corrente"),
    ("BPC_OUTROS", "Outros passivos correntes", "Passivo corrente"),
    ("BPC_ACRESC", "Acréscimos e diferimentos passivos", "Passivo corrente"),
]

RUBRICAS_DR = [
    ("DR01", "Vendas", "Operacional", "S"),
    ("DR02", "Prestações de serviço", "Operacional", "S"),
    ("DR03", "Outros proveitos operacionais", "Operacional", "S"),
    ("DR04", "Custo das mercadorias vendidas e matérias consumidas", "Operacional", "C"),
    ("DR05", "Fornecimentos e serviços de terceiros", "Operacional", "C"),
    ("DR06", "Custos com o pessoal", "Operacional", "C"),
    ("DR07", "Amortizações e depreciações", "Operacional", "C"),
    ("DR08", "Outros custos e perdas operacionais", "Operacional", "C"),
    ("DR09", "Proveitos e ganhos financeiros", "Financeiro", "S"),
    ("DR10", "Custos e perdas financeiros", "Financeiro", "C"),
    ("DR11", "Outros proveitos não operacionais e extraordinários", "Não operacional", "S"),
    ("DR12", "Outros custos não operacionais e extraordinários", "Não operacional", "C"),
    ("DR13", "Imposto sobre os lucros", "Imposto", "C"),
]

# (natureza, fluxo, linha DFC, inclui na DR)
NATUREZAS = [
    ("Abertura", "N/A", "", "N"),
    ("Venda", "Operacional", "Recebimentos de clientes", "S"),
    ("Recebimento de cliente", "Operacional", "Recebimentos de clientes", "S"),
    ("Compra", "Operacional", "Pagamentos a fornecedores", "S"),
    ("Pagamento a fornecedor", "Operacional", "Pagamentos a fornecedores", "S"),
    ("Processamento salarial", "N/A", "", "S"),
    ("Pagamento ao pessoal", "Operacional", "Pagamentos ao pessoal", "S"),
    ("Pagamento de impostos", "Operacional", "Pagamentos/recebimentos de impostos", "S"),
    ("Outros recebimentos operacionais", "Operacional", "Outros recebimentos/pagamentos operacionais", "S"),
    ("Outros pagamentos operacionais", "Operacional", "Outros recebimentos/pagamentos operacionais", "S"),
    ("Aquisição de imobilizado", "Investimento", "Pagamentos de imobilizações", "S"),
    ("Alienação de imobilizado", "Investimento", "Recebimentos de imobilizações", "S"),
    ("Investimento financeiro", "Investimento", "Aplicações e investimentos financeiros", "S"),
    ("Juros recebidos", "Investimento", "Juros e proveitos similares recebidos", "S"),
    ("Empréstimo obtido", "Financiamento", "Empréstimos obtidos", "S"),
    ("Reembolso de empréstimo", "Financiamento", "Reembolsos de empréstimos", "S"),
    ("Juros pagos", "Financiamento", "Juros e custos similares pagos", "S"),
    ("Aumento de capital", "Financiamento", "Aumentos de capital", "S"),
    ("Dividendos pagos", "Financiamento", "Dividendos pagos", "S"),
    ("Transferência interna", "Excluído", "Transferências entre contas de disponibilidades", "S"),
    ("Depreciação", "N/A", "", "S"),
    ("Acréscimo", "N/A", "", "S"),
    ("Diferimento", "N/A", "", "S"),
    ("Diferença de câmbio", "N/A", "", "S"),
    ("Imposto sobre lucros (estimativa)", "N/A", "", "S"),
    ("Regularização", "N/A", "", "S"),
    ("Apuramento de IVA", "N/A", "", "S"),
    ("Apuramento de resultados", "N/A", "", "N"),
    ("Encerramento", "N/A", "", "N"),
]

DFC_LINHAS = [
    ("Operacional", "Recebimentos de clientes"),
    ("Operacional", "Pagamentos a fornecedores"),
    ("Operacional", "Pagamentos ao pessoal"),
    ("Operacional", "Pagamentos/recebimentos de impostos"),
    ("Operacional", "Outros recebimentos/pagamentos operacionais"),
    ("Investimento", "Recebimentos de imobilizações"),
    ("Investimento", "Pagamentos de imobilizações"),
    ("Investimento", "Aplicações e investimentos financeiros"),
    ("Investimento", "Juros e proveitos similares recebidos"),
    ("Financiamento", "Empréstimos obtidos"),
    ("Financiamento", "Reembolsos de empréstimos"),
    ("Financiamento", "Juros e custos similares pagos"),
    ("Financiamento", "Aumentos de capital"),
    ("Financiamento", "Dividendos pagos"),
]

# (código, descrição, emitido pela entidade S/N, tipo SAF-T)
TIPOS_DOC = [
    ("FT", "Factura", "S", "SalesInvoices/FT"),
    ("FR", "Factura-recibo", "S", "SalesInvoices/FR"),
    ("NC", "Nota de crédito", "S", "SalesInvoices/NC"),
    ("ND", "Nota de débito", "S", "SalesInvoices/ND"),
    ("RC", "Recibo emitido", "S", "Payments/RC"),
    ("FC", "Factura de fornecedor", "N", "PurchaseInvoices"),
    ("FRF", "Factura-recibo de fornecedor", "N", "PurchaseInvoices"),
    ("NCF", "Nota de crédito de fornecedor", "N", "PurchaseInvoices"),
    ("RCF", "Recibo/comprovativo de pagamento a fornecedor", "N", "—"),
    ("DU", "Documento aduaneiro (importação)", "N", "PurchaseInvoices"),
    ("EXT", "Extracto / aviso bancário", "N", "—"),
    ("FS", "Folha salarial", "N", "—"),
    ("DI", "Documento interno / nota de lançamento", "N", "—"),
    ("DLI", "Declaração / guia de imposto", "N", "—"),
    ("ABE", "Lançamento de abertura", "N", "—"),
]

# Parametrização fiscal: (código, imposto, descrição, taxa, natureza, diploma, artigo, vigência, verificação, fonte, estado, observação)
SRC_IVA = "https://www.minfin.gov.ao/sala-de-imprensa/noticias/noticia/nova-taxa-do-iva-em-5-para-os-bens-alimentares-de-amplo-consumo-e-cesta-basica-entra-em-vigor-a-1-de-janeiro-de-2024 ; https://cms.law/pt/prt/publication/angola-alteracoes-ao-codigo-do-imposto-sobre-o-valor-acrescentado"
VERIF = date(2026, 9, 24)
TAXAS = [
    ("IVA_GER", "IVA", "Taxa geral", 0.14, "Regra legal", "Código do IVA, republicado pela Lei n.º 14/23, de 28 de Dezembro", "Artigo das taxas — confirmar no DR", date(2023, 12, 28), VERIF, SRC_IVA, "CONFIRMADO (fonte secundária)", "Confirmar no Diário da República antes do uso oficial."),
    ("IVA_HOT", "IVA", "Taxa — serviços de hotelaria e restauração", 0.07, "Regra legal", "Código do IVA (Lei n.º 14/23)", "Confirmar", None, VERIF, SRC_IVA, "POR VALIDAR", "Vigência e âmbito a confirmar."),
    ("IVA_ALI", "IVA", "Taxa — bens alimentares de amplo consumo e insumos agrícolas (lista legal)", 0.05, "Regra legal", "Código do IVA (Lei n.º 14/23) e lista anexa", "Confirmar", date(2024, 1, 1), VERIF, SRC_IVA, "CONFIRMADO (fonte secundária)", "Aplicável apenas aos bens da lista legal."),
    ("IVA_CAB", "IVA", "Taxa — regime especial da Província de Cabinda", 0.01, "Regra legal", "Código do IVA (Lei n.º 14/23)", "Confirmar", None, VERIF, SRC_IVA, "POR VALIDAR", "Âmbito objectivo e subjectivo a confirmar."),
    ("IVA_ISE", "IVA", "Operação isenta sem direito à dedução", 0.0, "Regra legal", "Código do IVA — isenções", "Confirmar artigo da isenção concreta", None, VERIF, "", "POR VALIDAR", "Indicar o fundamento legal de cada isenção no documento."),
    ("IVA_EXP", "IVA", "Exportação / isenção com direito à dedução", 0.0, "Regra legal", "Código do IVA — isenções nas exportações", "Confirmar", None, VERIF, "", "POR VALIDAR", ""),
    ("IVA_NSUJ", "IVA", "Operação não sujeita", 0.0, "Regra legal", "Código do IVA — incidência", "Confirmar", None, VERIF, "", "POR VALIDAR", ""),
    ("II_GER", "Imposto Industrial", "Taxa geral do Imposto Industrial", 0.25, "Regra legal", "Código do Imposto Industrial, alterado pela Lei n.º 26/20, de 20 de Julho", "Artigo da taxa — confirmar no DR", date(2020, 7, 20), VERIF, "https://lex.ao/docs/assembleia-nacional/2020/lei-n-o-26-20-de-20-de-julho/", "CONFIRMADO (fonte secundária)", "Existem taxas especiais por sector (ex.: banca, seguros, telecomunicações, agricultura) — parametrizar se aplicável."),
    ("RET_SERV", "Imposto Industrial", "Retenção na fonte sobre prestações de serviços", 0.065, "Parâmetro do modelo", "Código do Imposto Industrial (Lei n.º 26/20)", "Confirmar artigo, incidência e dispensas", None, VERIF, "", "POR VALIDAR", "Taxa usada no teste. Confirmar incidência e excepções antes do uso oficial."),
    ("IS_REC", "Imposto de Selo", "Recibo de quitação (verba 23.3 da Tabela)", 0.01, "Regra legal", "Código do Imposto de Selo — Tabela anexa, verba 23.3", "Verba 23.3", None, VERIF, "https://www.expansao.co.ao/gestao/detalhe/imposto-de-selo-do-recibo-regresso-ou-retrocesso-60218.html", "POR VALIDAR", "Aplicação limitada (ex.: sujeitos passivos com operações isentas sem direito à dedução). Confirmar."),
    ("INSS_TRAB", "Segurança Social", "Contribuição do trabalhador", 0.03, "Parâmetro do modelo", "Regime jurídico de protecção social obrigatória (confirmar diploma vigente)", "Confirmar", None, VERIF, "", "POR VALIDAR", ""),
    ("INSS_EMP", "Segurança Social", "Contribuição da entidade empregadora", 0.08, "Parâmetro do modelo", "Regime jurídico de protecção social obrigatória (confirmar diploma vigente)", "Confirmar", None, VERIF, "", "POR VALIDAR", ""),
    ("IRT_A", "IRT", "IRT Grupo A — ver tabela de escalões", None, "Regra legal", "Código do IRT, alterado pela Lei n.º 28/20 e pela Lei do OGE 2026 (Lei n.º 14/25)", "Tabela anexa", date(2026, 1, 1), VERIF, "https://kpmg.com/ao/pt/insights/tax-news/lei-orcamento-geral-estado-2026.html", "POR VALIDAR", "Fontes secundárias divergem no limite de isenção (100 000 vs 150 000 Kz). Carregar a tabela oficial do DR."),
    ("IRT_C", "IRT", "IRT Grupo C — taxa sobre vendas/serviços não sujeitos a retenção (volume 2025 ≥ 10 M Kz)", 0.065, "Regra legal", "Lei do OGE 2026 (Lei n.º 14/25)", "Confirmar", date(2026, 1, 1), VERIF, "https://kpmg.com/ao/pt/insights/tax-news/lei-orcamento-geral-estado-2026.html", "CONFIRMADO (fonte secundária)", ""),
    ("IAC", "Imposto sobre a Aplicação de Capitais", "Taxas por tipo de rendimento", None, "Regra legal", "Código do IAC (confirmar diploma e alterações)", "Confirmar", None, VERIF, "", "POR VALIDAR", "Não parametrizado: carregar taxas oficiais."),
    ("IP", "Imposto Predial", "Taxas e isenções (OGE 2026: isenção transmissões habitacionais ≤ 40 M Kz)", None, "Regra legal", "Código do Imposto Predial e Lei do OGE 2026", "Confirmar", date(2026, 1, 1), VERIF, "https://kpmg.com/ao/pt/insights/tax-news/lei-orcamento-geral-estado-2026.html", "POR VALIDAR", "Não parametrizado: carregar taxas oficiais."),
]

# Base legal: (diploma, número, data, artigo, matéria, regra, aplicabilidade, vigor, revogação, fonte, verificação, estado)
BASE_LEGAL = [
    ("Decreto", "82/01", "16/11/2001", "—", "Contabilidade", "Aprova o Plano Geral de Contabilidade (PGC)", "Entidades abrangidas pelo PGC (confirmar normativo aplicável: IFRS para certas entidades, planos sectoriais BNA/ARSEG)", "2001", "—", "Diário da República", VERIF, "POR VALIDAR data exacta"),
    ("Lei", "14/23", "28/12/2023", "Vários", "IVA", "Altera e republica o Código do IVA (taxas 14% / 7% / 5% / 1%; dedução até 12 meses; reembolso mínimo 700 000 Kz)", "Sujeitos passivos de IVA", "28/12/2023", "—", "https://cms.law/pt/prt/publication/angola-alteracoes-ao-codigo-do-imposto-sobre-o-valor-acrescentado", VERIF, "CONFIRMADO (fonte secundária)"),
    ("Regulamentação IVA / PGC", "Instrutivo/Decreto Executivo — a identificar", "—", "—", "IVA / Contabilidade", "Cria as contas de IVA no PGC (34.5.x)", "Sujeitos passivos de IVA", "—", "—", "—", VERIF, "POR VALIDAR"),
    ("Lei", "26/20", "20/07/2020", "Vários", "Imposto Industrial", "Altera o Código do Imposto Industrial (taxa geral 25%)", "Pessoas colectivas e singulares com actividade comercial/industrial", "20/07/2020", "—", "https://lex.ao/docs/assembleia-nacional/2020/lei-n-o-26-20-de-20-de-julho/", VERIF, "CONFIRMADO (fonte secundária)"),
    ("Lei", "28/20", "22/07/2020", "Tabela", "IRT", "Altera o Código do IRT", "Rendimentos do trabalho", "01/09/2020", "Alterada pela Lei do OGE 2026", "https://www.ucm.minfin.gov.ao/cs/groups/public/documents/document/aw4x/mjm3/~edisp/minfin1237855.pdf", VERIF, "CONFIRMADO (fonte secundária)"),
    ("Lei", "14/25", "30/12/2025", "Várias", "OGE 2026", "Lei do OGE 2026: alterações ao IRT (isenção e escalões), IRT Grupo C 6,5%, Imposto Predial, Imposto de Selo", "Todos os contribuintes", "01/01/2026", "—", "https://kpmg.com/ao/pt/insights/tax-news/lei-orcamento-geral-estado-2026.html", VERIF, "POR VALIDAR (número/data a confirmar no DR)"),
    ("Decreto Presidencial", "71/25", "20/03/2025", "Vários", "Facturação", "Regime Jurídico das Facturas e Documentos Equivalentes: software validado AGT, facturação electrónica, comunicação, SAF-T, cópias de segurança", "Grandes Contribuintes e fornecedores do Estado desde 01/01/2026; regimes geral e simplificado de IVA desde 01/01/2027", "Faseado", "Revoga o regime anterior (confirmar)", "https://www.ey.com/pt_ao/technical/tax-alerts/facturacao-electronica-a-partir-de-1-de-janeiro-de-2026", VERIF, "CONFIRMADO (fonte secundária)"),
    ("Decreto Presidencial", "312/18", "—", "—", "Facturação", "Regime jurídico das facturas anterior", "—", "—", "Presumivelmente revogado pelo DP 71/25 — confirmar", "—", VERIF, "POR VALIDAR"),
    ("Código", "Imposto de Selo", "—", "Tabela anexa, verba 23.3", "Imposto de Selo", "Recibo de quitação — 1% (âmbito restrito)", "Ver parametrização IS_REC", "—", "—", "https://www.expansao.co.ao/gestao/detalhe/imposto-de-selo-do-recibo-regresso-ou-retrocesso-60218.html", VERIF, "POR VALIDAR"),
    ("Lei", "Código Geral Tributário", "—", "—", "Procedimento / infracções", "Obrigações acessórias, prazos, juros e multas", "Todos os contribuintes", "—", "—", "—", VERIF, "POR VALIDAR"),
    ("Decreto Presidencial", "Reintegrações e amortizações — a identificar", "—", "Tabelas de taxas", "Imposto Industrial", "Taxas máximas fiscalmente aceites de amortização", "Activos fixos", "—", "—", "—", VERIF, "POR VALIDAR"),
    ("Decreto Executivo", "SAF-T (AO) — a identificar", "—", "Estrutura XSD", "SAF-T", "Estrutura do ficheiro SAF-T (AO)", "Utilizadores de software de facturação/contabilidade", "—", "—", "Portal da AGT", VERIF, "POR VALIDAR"),
    ("Protecção social", "Diploma de contribuições INSS — a identificar", "—", "—", "Segurança Social", "Taxas contributivas 3% trabalhador / 8% empregador (parâmetro)", "Entidades empregadoras", "—", "—", "—", VERIF, "POR VALIDAR"),
]

TERCEIROS = [
    ("5000000001", "Cliente Alfa, Lda", "Cliente", "Angola", 30, 1_000_000, "N"),
    ("5000000002", "Fornecedor Beta, SA", "Fornecedor", "Angola", 30, 0, "N"),
    ("5000000003", "Papelaria Gama, Lda", "Fornecedor", "Angola", 0, 0, "N"),
    ("5000000004", "Delta Informática, Lda", "Fornecedor", "Angola", 0, 0, "N"),
    ("5000000005", "Epsilon Consultoria, SA", "Cliente", "Angola", 30, 5_000_000, "S"),
    ("5000000006", "Seguradora Zeta, SA", "Fornecedor", "Angola", 0, 0, "N"),
    ("EXT0000001", "Omega Software Ltd", "Fornecedor", "África do Sul", 30, 0, "N"),
    ("999999999", "Consumidor final", "Cliente", "Angola", 0, 0, "N"),
]

ARTIGOS = [
    ("A001", "Mercadoria A — artigo de revenda", "UN", "26.1", 200, 1500, 7, 50),
    ("A002", "Mercadoria B — artigo de revenda", "UN", "26.1", 50, 400, 10, 20),
]

ACTIVOS = [
    ("AF001", "Computadores portáteis (lote de 8)", "11.5.1", "18.1.5", "73.1", date(2026, 2, 1), 1_200_000, 4, "Linear (quotas constantes)", 0, "Sede — Administração", "Director Administrativo", "Em uso", None, None, "ADM", "PRJ01"),
]


def d(m, dd):
    return date(ANO, m, dd)


U1, U2 = "contab01", "dirfin01"
CERT = "000/AGT/2026 (fictício)"


def L(ID, dt, td, se, nd, ddoc, venc, nif, conta, desc, deb=0, cred=0, cc="", cr="", proj="", fonte="", nat="",
      codf="", base=None, ref=None, moeda="", camb=None, valme=None, forma="", art="", qtd=None, sup="", user=U1,
      val=U2, dtins=None, dtalt=None, estdoc="", hsh="", cert="", estagt="", dtcom=None, erro="", obs=""):
    return dict(ID=ID, Data=dt, TipoDoc=td, Serie=se, NumDoc=nd, DataDoc=ddoc, Venc=venc, NIF=nif, Conta=conta,
                Desc=desc, Deb=deb or None, Cred=cred or None, CC=cc, CR=cr, Proj=proj, Fonte=fonte, Nat=nat,
                CodF=codf, Base=base, Ref=ref, Moeda=moeda, Cambio=camb, ValME=valme, FormaPag=forma, Artigo=art,
                Qtd=qtd, Suporte=sup, User=user, Validador=val, DtIns=dtins or dt, DtAlt=dtalt, EstDoc=estdoc,
                Hash=hsh, Cert=cert, EstAGT=estagt, DtCom=dtcom, ErroCom=erro, Obs=obs)


CMV3 = 104_386  # custo médio ponderado móvel: 100 un × (1 190 000 / 1 140)
II_EST = 402_153.50  # 25% × RAI 1 608 614 (validado em tests/verify.py)

JOURNAL = [
    # 01 — Abertura
    L(1, d(1, 1), "ABE", "2026", 1, d(1, 1), None, "", "43.1.1", "Saldo de abertura — Banco A", deb=5_000_000, nat="Abertura", sup="Balanço de fecho 2025", obs="TESTE 00 — Abertura"),
    L(1, d(1, 1), "ABE", "2026", 1, d(1, 1), None, "", "45.1", "Saldo de abertura — Caixa", deb=200_000, nat="Abertura", sup="Balanço de fecho 2025"),
    L(1, d(1, 1), "ABE", "2026", 1, d(1, 1), None, "", "26.1", "Saldo de abertura — Mercadoria A (1 000 un)", deb=1_000_000, nat="Abertura", art="A001", qtd=1000, sup="Inventário 31/12/2025"),
    L(1, d(1, 1), "ABE", "2026", 1, d(1, 1), None, "", "51.1", "Saldo de abertura — Capital social", cred=5_000_000, nat="Abertura", sup="Balanço de fecho 2025"),
    L(1, d(1, 1), "ABE", "2026", 1, d(1, 1), None, "", "81.1", "Saldo de abertura — Resultados transitados", cred=1_200_000, nat="Abertura", sup="Balanço de fecho 2025"),
    # 02 — Venda a dinheiro (FR)
    L(2, d(1, 5), "FR", "A", 1, d(1, 5), d(1, 5), "999999999", "45.1", "FR A/1 — venda a dinheiro", deb=114_000, nat="Venda", forma="Numerário", sup="FR A/1", estdoc="Normal", hsh="Xk3p", cert=CERT, estagt="Comunicado", dtcom=d(1, 5), obs="TESTE 01 — Venda a dinheiro"),
    L(2, d(1, 5), "FR", "A", 1, d(1, 5), None, "", "61.1", "FR A/1 — vendas mercadoria A", cred=100_000, cc="COM", nat="Venda", sup="FR A/1"),
    L(2, d(1, 5), "FR", "A", 1, d(1, 5), None, "", "34.5.3", "FR A/1 — IVA liquidado 14%", cred=14_000, nat="Venda", codf="IVA_GER", base=100_000, sup="FR A/1"),
    L(2, d(1, 5), "FR", "A", 1, d(1, 5), None, "", "71.1", "FR A/1 — custo das mercadorias (60 un)", deb=60_000, cc="COM", nat="Venda", sup="FR A/1"),
    L(2, d(1, 5), "FR", "A", 1, d(1, 5), None, "", "26.1", "FR A/1 — saída de armazém (60 un)", cred=60_000, nat="Venda", art="A001", qtd=-60, sup="FR A/1"),
    # 03 — Venda a crédito (FT)
    L(3, d(1, 10), "FT", "A", 1, d(1, 10), d(2, 9), "5000000001", "31.1.1", "FT A/1 — Cliente Alfa", deb=570_000, nat="Venda", sup="FT A/1", estdoc="Normal", hsh="Pq7Z", cert=CERT, estagt="Comunicado", dtcom=d(1, 10), obs="TESTE 02 — Venda a crédito / TESTE 12 — Operação sujeita a IVA"),
    L(3, d(1, 10), "FT", "A", 1, d(1, 10), None, "", "61.1", "FT A/1 — vendas mercadoria A", cred=500_000, cc="COM", nat="Venda", sup="FT A/1"),
    L(3, d(1, 10), "FT", "A", 1, d(1, 10), None, "", "34.5.3", "FT A/1 — IVA liquidado 14%", cred=70_000, nat="Venda", codf="IVA_GER", base=500_000, sup="FT A/1"),
    L(3, d(1, 10), "FT", "A", 1, d(1, 10), None, "", "71.1", "FT A/1 — custo das mercadorias (300 un)", deb=300_000, cc="COM", nat="Venda", sup="FT A/1"),
    L(3, d(1, 10), "FT", "A", 1, d(1, 10), None, "", "26.1", "FT A/1 — saída de armazém (300 un)", cred=300_000, nat="Venda", art="A001", qtd=-300, sup="FT A/1"),
    # 04 — Compra a crédito
    L(4, d(1, 12), "FC", "B", 889, d(1, 12), d(2, 11), "5000000002", "26.1", "FC B/889 — compra mercadoria A (500 un)", deb=550_000, nat="Compra", art="A001", qtd=500, sup="FC B/889", obs="TESTE 03 — Compra a crédito"),
    L(4, d(1, 12), "FC", "B", 889, d(1, 12), None, "5000000002", "34.5.2", "FC B/889 — IVA dedutível 14%", deb=77_000, nat="Compra", codf="IVA_GER", base=550_000, sup="FC B/889"),
    L(4, d(1, 12), "FC", "B", 889, d(1, 12), d(2, 11), "5000000002", "32.1.1", "FC B/889 — Fornecedor Beta", cred=627_000, nat="Compra", sup="FC B/889"),
    # 05 — Compra a pronto
    L(5, d(1, 15), "FRF", "G", 1502, d(1, 15), d(1, 15), "5000000003", "75.2.1", "FRF G/1502 — material de escritório", deb=50_000, cc="ADM", nat="Compra", sup="FRF G/1502", obs="TESTE 04 — Compra a pronto"),
    L(5, d(1, 15), "FRF", "G", 1502, d(1, 15), None, "5000000003", "34.5.2", "FRF G/1502 — IVA dedutível 14%", deb=7_000, nat="Compra", codf="IVA_GER", base=50_000, sup="FRF G/1502"),
    L(5, d(1, 15), "FRF", "G", 1502, d(1, 15), None, "5000000003", "45.1", "FRF G/1502 — pagamento em numerário", cred=57_000, nat="Compra", forma="Numerário", sup="FRF G/1502"),
    # 06 — Processamento salarial
    L(6, d(1, 28), "FS", "2026", 1, d(1, 28), None, "", "72.2", "Salários Jan/2026 — remunerações brutas", deb=400_000, cc="ADM", nat="Processamento salarial", sup="Folha salarial 01/2026", obs="TESTE 07 — Pagamento de salário (processamento)"),
    L(6, d(1, 28), "FS", "2026", 1, d(1, 28), None, "", "72.5", "Salários Jan/2026 — INSS entidade empregadora (8%)", deb=32_000, cc="ADM", nat="Processamento salarial", sup="Folha salarial 01/2026"),
    L(6, d(1, 28), "FS", "2026", 1, d(1, 28), None, "", "36.1.1", "Salários Jan/2026 — líquido a pagar", cred=348_000, nat="Processamento salarial", sup="Folha salarial 01/2026"),
    L(6, d(1, 28), "FS", "2026", 1, d(1, 28), None, "", "34.3.1", "Salários Jan/2026 — IRT retido", cred=40_000, nat="Processamento salarial", sup="Folha salarial 01/2026", obs="Valor ILUSTRATIVO — calcular com a tabela IRT oficial validada"),
    L(6, d(1, 28), "FS", "2026", 1, d(1, 28), None, "", "34.9.1", "Salários Jan/2026 — INSS (3% + 8%)", cred=44_000, nat="Processamento salarial", sup="Folha salarial 01/2026"),
    # 07 — Pagamento de salários
    L(7, d(1, 30), "EXT", "BA", 130, d(1, 30), None, "", "36.1.1", "Pagamento salários Jan/2026", deb=348_000, nat="Pagamento ao pessoal", sup="Extracto Banco A 30/01", obs="TESTE 07 — Pagamento de salário"),
    L(7, d(1, 30), "EXT", "BA", 130, d(1, 30), None, "", "43.1.1", "Pagamento salários Jan/2026", cred=348_000, nat="Pagamento ao pessoal", forma="Transferência", sup="Extracto Banco A 30/01"),
    # 28 — Apuramento do IVA de Janeiro
    L(28, d(1, 31), "DI", "IVA", 1, d(1, 31), None, "", "34.5.3", "Apuramento IVA 01/2026 — transferência do liquidado", deb=84_000, nat="Apuramento de IVA", sup="Mapa 12_IVA 01/2026", obs="Apuramento mensal do IVA (34.5.2/34.5.3 → 34.5.6/34.5.7)"),
    L(28, d(1, 31), "DI", "IVA", 1, d(1, 31), None, "", "34.5.2", "Apuramento IVA 01/2026 — transferência do dedutível", cred=84_000, nat="Apuramento de IVA", sup="Mapa 12_IVA 01/2026"),
    # 08 — Aquisição de activo fixo
    L(8, d(2, 1), "FRF", "D", 77, d(2, 1), d(2, 1), "5000000004", "11.5.1", "FRF D/77 — computadores portáteis (AF001)", deb=1_200_000, cc="ADM", proj="PRJ01", nat="Aquisição de imobilizado", sup="FRF D/77", obs="TESTE 08 — Aquisição de activo"),
    L(8, d(2, 1), "FRF", "D", 77, d(2, 1), None, "5000000004", "34.5.2", "FRF D/77 — IVA dedutível 14%", deb=168_000, nat="Aquisição de imobilizado", codf="IVA_GER", base=1_200_000, sup="FRF D/77"),
    L(8, d(2, 1), "FRF", "D", 77, d(2, 1), None, "5000000004", "43.1.1", "FRF D/77 — pagamento por transferência", cred=1_368_000, proj="PRJ01", nat="Aquisição de imobilizado", forma="Transferência", sup="FRF D/77"),
    # 09 — Empréstimo bancário
    L(9, d(2, 1), "EXT", "BA", 201, d(2, 1), None, "", "43.1.1", "Desembolso empréstimo Banco A (36 meses)", deb=3_000_000, nat="Empréstimo obtido", fonte="Banco A", sup="Contrato de mútuo n.º 12/2026", obs="TESTE 10 — Empréstimo bancário / TESTE 17 — Financiamento"),
    L(9, d(2, 1), "EXT", "BA", 201, d(2, 1), None, "", "33.1.1", "Empréstimo Banco A — médio/longo prazo", cred=3_000_000, nat="Empréstimo obtido", fonte="Banco A", sup="Contrato de mútuo n.º 12/2026"),
    # 10 — Pagamento parcial a fornecedor
    L(10, d(2, 5), "RCF", "B", 55, d(2, 5), None, "5000000002", "32.1.1", "Pagamento parcial FC B/889", deb=400_000, nat="Pagamento a fornecedor", ref=4, sup="Comprovativo transf. 05/02", obs="TESTE 05 — Pagamento de fornecedor"),
    L(10, d(2, 5), "RCF", "B", 55, d(2, 5), None, "", "43.1.1", "Pagamento parcial FC B/889", cred=400_000, nat="Pagamento a fornecedor", forma="Transferência", sup="Comprovativo transf. 05/02"),
    # 11 — Recebimento parcial de cliente
    L(11, d(2, 8), "RC", "A", 1, d(2, 8), None, "5000000001", "43.1.1", "RC A/1 — recebimento parcial FT A/1", deb=300_000, nat="Recebimento de cliente", forma="Transferência", sup="RC A/1", estdoc="Normal", hsh="Rt5c", cert=CERT, estagt="Comunicado", dtcom=d(2, 8), obs="TESTE 06 — Recebimento de cliente"),
    L(11, d(2, 8), "RC", "A", 1, d(2, 8), None, "5000000001", "31.1.1", "RC A/1 — Cliente Alfa", cred=300_000, nat="Recebimento de cliente", ref=3, sup="RC A/1"),
    # 29 — Pagamento de IRT e INSS de Janeiro
    L(29, d(2, 20), "DLI", "AGT", 1, d(2, 20), None, "", "34.3.1", "Entrega IRT retido 01/2026", deb=40_000, nat="Pagamento de impostos", sup="Guia/comprovativo AGT 01/2026", obs="Pagamento ao Estado (calendário fiscal)"),
    L(29, d(2, 20), "DLI", "AGT", 1, d(2, 20), None, "", "34.9.1", "Entrega INSS 01/2026", deb=44_000, nat="Pagamento de impostos", sup="Guia INSS 01/2026"),
    L(29, d(2, 20), "DLI", "AGT", 1, d(2, 20), None, "", "43.1.1", "Pagamento IRT + INSS 01/2026", cred=84_000, nat="Pagamento de impostos", forma="Transferência", sup="Guia/comprovativo AGT 01/2026"),
    # 12 — Prestação de serviços
    L(12, d(2, 20), "FT", "A", 2, d(2, 20), d(3, 21), "5000000005", "31.1.1", "FT A/2 — Epsilon — consultoria", deb=3_420_000, proj="PRJ02", nat="Venda", sup="FT A/2", estdoc="Normal", hsh="Mn8w", cert=CERT, estagt="Comunicado", dtcom=d(2, 20), obs="TESTE 12 — Operação sujeita a IVA (serviços)"),
    L(12, d(2, 20), "FT", "A", 2, d(2, 20), None, "", "62.1", "FT A/2 — serviços de consultoria", cred=3_000_000, cc="OPS", proj="PRJ02", nat="Venda", sup="FT A/2"),
    L(12, d(2, 20), "FT", "A", 2, d(2, 20), None, "", "34.5.3", "FT A/2 — IVA liquidado 14%", cred=420_000, nat="Venda", codf="IVA_GER", base=3_000_000, sup="FT A/2"),
    # 13 — Venda isenta
    L(13, d(2, 25), "FT", "A", 3, d(2, 25), d(3, 27), "5000000001", "31.1.1", "FT A/3 — Cliente Alfa — venda isenta", deb=200_000, nat="Venda", sup="FT A/3", estdoc="Normal", hsh="Lq2e", cert=CERT, estagt="Pendente", obs="TESTE 13 — Operação isenta (fundamento legal a indicar)"),
    L(13, d(2, 25), "FT", "A", 3, d(2, 25), None, "", "61.1", "FT A/3 — vendas isentas", cred=200_000, cc="COM", nat="Venda", codf="IVA_ISE", base=200_000, sup="FT A/3"),
    L(13, d(2, 25), "FT", "A", 3, d(2, 25), None, "", "71.1", "FT A/3 — custo das mercadorias (100 un, CMP)", deb=CMV3, cc="COM", nat="Venda", sup="FT A/3"),
    L(13, d(2, 25), "FT", "A", 3, d(2, 25), None, "", "26.1", "FT A/3 — saída de armazém (100 un)", cred=CMV3, nat="Venda", art="A001", qtd=-100, sup="FT A/3"),
    # 14 — Nota de crédito
    L(14, d(2, 28), "NC", "A", 1, d(2, 28), None, "5000000001", "31.1.1", "NC A/1 — desconto s/ FT A/1", cred=57_000, nat="Venda", ref=3, sup="NC A/1", estdoc="Normal", hsh="Vb4y", cert=CERT, estagt="Comunicado", dtcom=d(2, 28), obs="TESTE 14 — Nota de crédito"),
    L(14, d(2, 28), "NC", "A", 1, d(2, 28), None, "", "61.8", "NC A/1 — desconto comercial", deb=50_000, cc="COM", nat="Venda", sup="NC A/1"),
    L(14, d(2, 28), "NC", "A", 1, d(2, 28), None, "", "34.5.4.1", "NC A/1 — regularização IVA a favor", deb=7_000, nat="Venda", codf="IVA_GER", base=50_000, sup="NC A/1"),
    # 15 — Depreciação Fevereiro
    L(15, d(2, 28), "DI", "AMT", 2, d(2, 28), None, "", "73.1", "Amortização Fev/2026 — AF001", deb=25_000, cc="ADM", nat="Depreciação", sup="Mapa de amortizações 02/2026", obs="TESTE 09 — Depreciação"),
    L(15, d(2, 28), "DI", "AMT", 2, d(2, 28), None, "", "18.1.5", "Amortização Fev/2026 — AF001", cred=25_000, nat="Depreciação", sup="Mapa de amortizações 02/2026"),
    # 16 — Juros
    L(16, d(2, 28), "EXT", "BA", 228, d(2, 28), None, "", "76.1", "Juros empréstimo Banco A — Fev/2026", deb=45_000, nat="Juros pagos", fonte="Banco A", sup="Aviso de débito 28/02", obs="TESTE 11 — Pagamento de juros"),
    L(16, d(2, 28), "EXT", "BA", 228, d(2, 28), None, "", "43.1.1", "Juros empréstimo Banco A — Fev/2026", cred=45_000, nat="Juros pagos", forma="Débito directo", sup="Aviso de débito 28/02"),
    # 30 — Apuramento do IVA de Fevereiro
    L(30, d(2, 28), "DI", "IVA", 2, d(2, 28), None, "", "34.5.3", "Apuramento IVA 02/2026 — liquidado", deb=420_000, nat="Apuramento de IVA", sup="Mapa 12_IVA 02/2026"),
    L(30, d(2, 28), "DI", "IVA", 2, d(2, 28), None, "", "34.5.2", "Apuramento IVA 02/2026 — dedutível", cred=168_000, nat="Apuramento de IVA", sup="Mapa 12_IVA 02/2026"),
    L(30, d(2, 28), "DI", "IVA", 2, d(2, 28), None, "", "34.5.4.1", "Apuramento IVA 02/2026 — regularizações a favor", cred=7_000, nat="Apuramento de IVA", sup="Mapa 12_IVA 02/2026"),
    L(30, d(2, 28), "DI", "IVA", 2, d(2, 28), None, "", "34.5.6", "Apuramento IVA 02/2026 — IVA a pagar", cred=245_000, nat="Apuramento de IVA", sup="Mapa 12_IVA 02/2026"),
    # 17 — Factura em moeda estrangeira
    L(17, d(3, 1), "FC", "OM", 3301, d(3, 1), d(3, 31), "EXT0000001", "75.2.2", "Licença de software — USD 1 000 @ 900", deb=900_000, cc="OPS", nat="Compra", moeda="USD", camb=900, valme=1000, sup="Invoice OM-3301", obs="TESTE 15 — Operação cambial. Enquadramento IVA (serviço de não residente) POR VALIDAR"),
    L(17, d(3, 1), "FC", "OM", 3301, d(3, 1), d(3, 31), "EXT0000001", "32.1.2", "Omega Software — USD 1 000 @ 900", cred=900_000, nat="Compra", moeda="USD", camb=900, valme=1000, sup="Invoice OM-3301"),
    # 18 — Despesa antecipada
    L(18, d(3, 1), "FRF", "Z", 45, d(3, 1), d(3, 1), "5000000006", "37.4.1", "Seguro multirriscos Mar/2026–Fev/2027", deb=1_200_000, nat="Outros pagamentos operacionais", sup="Apólice Z-45", obs="TESTE 18 — Despesa antecipada"),
    L(18, d(3, 1), "FRF", "Z", 45, d(3, 1), None, "5000000006", "43.1.1", "Pagamento prémio de seguro anual", cred=1_200_000, nat="Outros pagamentos operacionais", forma="Transferência", sup="Apólice Z-45"),
    # 19 — Investimento financeiro
    L(19, d(3, 10), "EXT", "BA", 310, d(3, 10), None, "", "42.1", "Constituição depósito a prazo 180 dias", deb=1_000_000, nat="Investimento financeiro", sup="Contrato DP 310", obs="TESTE 16 — Investimento"),
    L(19, d(3, 10), "EXT", "BA", 310, d(3, 10), None, "", "43.1.1", "Constituição depósito a prazo 180 dias", cred=1_000_000, nat="Investimento financeiro", forma="Transferência", sup="Contrato DP 310"),
    # 20 — Recebimento com retenção na fonte
    L(20, d(3, 15), "RC", "A", 2, d(3, 15), None, "5000000005", "43.1.1", "RC A/2 — recebimento FT A/2 (líquido de retenção)", deb=3_225_000, proj="PRJ02", nat="Recebimento de cliente", forma="Transferência", sup="RC A/2", estdoc="Normal", hsh="Hy6d", cert=CERT, estagt="Comunicado", dtcom=d(3, 15), obs="TESTE 06 — Recebimento com retenção na fonte"),
    L(20, d(3, 15), "RC", "A", 2, d(3, 15), None, "", "34.1.2", "RC A/2 — retenção na fonte sofrida 6,5%", deb=195_000, nat="Recebimento de cliente", codf="RET_SERV", base=3_000_000, sup="RC A/2"),
    L(20, d(3, 15), "RC", "A", 2, d(3, 15), None, "5000000005", "31.1.1", "RC A/2 — Epsilon", cred=3_420_000, nat="Recebimento de cliente", ref=12, sup="RC A/2"),
    # 21 — Receita antecipada (adiantamento)
    L(21, d(3, 15), "FR", "A", 2, d(3, 15), d(3, 15), "5000000005", "43.1.1", "FR A/2 — adiantamento Epsilon (serviço Abril)", deb=684_000, proj="PRJ02", nat="Recebimento de cliente", forma="Transferência", sup="FR A/2", estdoc="Normal", hsh="Ws1k", cert=CERT, estagt="Erro", erro="Timeout no envio — reenviar", obs="TESTE 19 — Receita antecipada. Exigibilidade do IVA no adiantamento: confirmar artigo do CIVA"),
    L(21, d(3, 15), "FR", "A", 2, d(3, 15), None, "", "37.6.1", "FR A/2 — proveito diferido", cred=600_000, proj="PRJ02", nat="Recebimento de cliente", sup="FR A/2"),
    L(21, d(3, 15), "FR", "A", 2, d(3, 15), None, "", "34.5.3", "FR A/2 — IVA liquidado 14% (adiantamento)", cred=84_000, nat="Recebimento de cliente", codf="IVA_GER", base=600_000, sup="FR A/2"),
    # 22 — Aumento de capital
    L(22, d(3, 20), "DI", "CAP", 1, d(3, 20), None, "", "43.1.1", "Realização de aumento de capital", deb=2_000_000, nat="Aumento de capital", fonte="Sócios", sup="Acta AG 01/2026 + escritura", obs="TESTE 17 — Financiamento por capital"),
    L(22, d(3, 20), "DI", "CAP", 1, d(3, 20), None, "", "51.1", "Aumento de capital social", cred=2_000_000, nat="Aumento de capital", fonte="Sócios", sup="Acta AG 01/2026 + escritura"),
    # 31 — Pagamento do IVA de Fevereiro
    L(31, d(3, 20), "DLI", "AGT", 2, d(3, 20), None, "", "34.5.6", "Pagamento IVA 02/2026", deb=245_000, nat="Pagamento de impostos", sup="Declaração periódica IVA 02/2026 + comprovativo", obs="Pagamento ao Estado (calendário fiscal)"),
    L(31, d(3, 20), "DLI", "AGT", 2, d(3, 20), None, "", "43.1.1", "Pagamento IVA 02/2026", cred=245_000, nat="Pagamento de impostos", forma="Transferência", sup="Declaração periódica IVA 02/2026 + comprovativo"),
    # 23 — Pagamento em moeda estrangeira com diferença de câmbio
    L(23, d(3, 25), "RCF", "OM", 3301, d(3, 25), None, "EXT0000001", "32.1.2", "Pagamento Omega USD 1 000 (câmbio histórico 900)", deb=900_000, nat="Pagamento a fornecedor", ref=17, moeda="USD", camb=900, valme=1000, sup="Swift 25/03", obs="TESTE 15 — Operação cambial (liquidação)"),
    L(23, d(3, 25), "RCF", "OM", 3301, d(3, 25), None, "", "76.5", "Diferença de câmbio desfavorável (920 − 900)", deb=20_000, nat="Diferença de câmbio", sup="Swift 25/03"),
    L(23, d(3, 25), "RCF", "OM", 3301, d(3, 25), None, "", "43.1.1", "Pagamento Omega USD 1 000 @ 920", cred=920_000, nat="Pagamento a fornecedor", moeda="USD", camb=920, valme=1000, forma="Transferência", sup="Swift 25/03"),
    # 24 — Depreciação Março
    L(24, d(3, 31), "DI", "AMT", 3, d(3, 31), None, "", "73.1", "Amortização Mar/2026 — AF001", deb=25_000, cc="ADM", nat="Depreciação", sup="Mapa de amortizações 03/2026", obs="TESTE 09 — Depreciação"),
    L(24, d(3, 31), "DI", "AMT", 3, d(3, 31), None, "", "18.1.5", "Amortização Mar/2026 — AF001", cred=25_000, nat="Depreciação", sup="Mapa de amortizações 03/2026"),
    # 25 — Diferimento (reconhecimento do seguro)
    L(25, d(3, 31), "DI", "DIF", 3, d(3, 31), None, "", "75.2.3", "Seguro — custo de Março (1/12)", deb=100_000, cc="ADM", nat="Diferimento", sup="Mapa de diferimentos 03/2026", obs="TESTE 18 — Despesa antecipada (reconhecimento)"),
    L(25, d(3, 31), "DI", "DIF", 3, d(3, 31), None, "", "37.4.1", "Seguro — custo de Março (1/12)", cred=100_000, nat="Diferimento", sup="Mapa de diferimentos 03/2026"),
    # 26 — Acréscimo de custos
    L(26, d(3, 31), "DI", "ACR", 3, d(3, 31), None, "", "75.2.4", "Electricidade Março — estimativa", deb=80_000, cc="OPS", nat="Acréscimo", sup="Leitura contador 31/03", obs="Acréscimo de custos"),
    L(26, d(3, 31), "DI", "ACR", 3, d(3, 31), None, "", "37.5.1", "Electricidade Março — encargo a pagar", cred=80_000, nat="Acréscimo", sup="Leitura contador 31/03"),
    # 32 — Apuramento do IVA de Março
    L(32, d(3, 31), "DI", "IVA", 3, d(3, 31), None, "", "34.5.3", "Apuramento IVA 03/2026 — liquidado", deb=84_000, nat="Apuramento de IVA", sup="Mapa 12_IVA 03/2026"),
    L(32, d(3, 31), "DI", "IVA", 3, d(3, 31), None, "", "34.5.6", "Apuramento IVA 03/2026 — IVA a pagar", cred=84_000, nat="Apuramento de IVA", sup="Mapa 12_IVA 03/2026"),
    # 27 — Estimativa de Imposto Industrial
    L(27, d(3, 31), "DI", "IMP", 3, d(3, 31), None, "", "87.1", "Estimativa Imposto Industrial — 1.º trimestre", deb=II_EST, nat="Imposto sobre lucros (estimativa)", codf="II_GER", sup="Mapa 15_IMPOSTO_INDUSTRIAL", obs="Valor = matéria colectável × taxa (ver 15_IMPOSTO_INDUSTRIAL)"),
    L(27, d(3, 31), "DI", "IMP", 3, d(3, 31), None, "", "34.1.1", "Estimativa Imposto Industrial — 1.º trimestre", cred=II_EST, nat="Imposto sobre lucros (estimativa)", sup="Mapa 15_IMPOSTO_INDUSTRIAL"),
]
