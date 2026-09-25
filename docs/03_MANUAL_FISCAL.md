# 03 — Manual Fiscal

> Estruturado para conformidade com o quadro legal identificado e sujeito à validação contabilística, fiscal e técnica antes da utilização oficial. **Nada neste modelo é "100% conforme com a AGT"** até ser validado por técnico de contas / jurista com a legislação em vigor à data de uso.

## 1. Regra legal ≠ parametrização

Cada taxa em `11_FISCALIDADE_AGT` tem: diploma, artigo, vigência, data de verificação, fonte, **estado de validação** e natureza:

- **Regra legal** — conteúdo da lei (ex.: taxa geral do IVA 14%).
- **Parâmetro do modelo** — pressuposto técnico que precisa de confirmação (ex.: retenção de 6,5% sobre serviços usada nos testes).

Se uma taxa com estado **POR VALIDAR** for usada no Diário, a linha fica com Estado_Fiscal 🟡 e a taxa aparece nos alertas e no risco fiscal.

## 2. Protocolo antes de aplicar um imposto

1. Natureza da operação · 2. Sujeito passivo · 3. Regime fiscal · 4. Legislação vigente · 5. Isenção/não sujeição · 6. Taxa · 7. Base tributável.

## 3. IVA (12_IVA)

**Quadro legal identificado:** Código do IVA republicado pela **Lei n.º 14/23, de 28 de Dezembro** — taxas 14% (geral), 7% (hotelaria e restauração), 5% (bens alimentares de amplo consumo e insumos agrícolas, desde 01/01/2024), 1% (regime especial de Cabinda); dedução até 12 meses após a factura; reembolso mínimo 700 000 Kz (fontes: MINFIN, CMS).

**Mecânica no modelo**

| Operação | Conta | Código fiscal | Base |
|---|---|---|---|
| IVA liquidado em vendas/serviços/adiantamentos | 34.5.3 (crédito) | IVA_GER / IVA_HOT / IVA_ALI / IVA_CAB | na linha do IVA |
| IVA dedutível em compras/investimento/importações (DU) | 34.5.2 (débito) | idem | na linha do IVA |
| Notas de crédito emitidas | 34.5.4.1 (débito) | idem | idem |
| Notas de débito | 34.5.4.2 (crédito) | idem | idem |
| Operações isentas / exportações / não sujeitas | linha de proveito | IVA_ISE / IVA_EXP / IVA_NSUJ | na linha de proveito |
| Apuramento mensal | 34.5.3/34.5.2/34.5.4.x → 34.5.6 ou 34.5.7 | natureza `Apuramento de IVA` | — |
| Pagamento | D 34.5.6 / C 43 | natureza `Pagamento de impostos` | — |

**Mapa de apuramento:** IVA liquidado − IVA dedutível − regularizações a favor + regularizações a favor do Estado − crédito do período anterior = IVA a pagar / (a recuperar). O crédito é reportado automaticamente ao mês seguinte, deduzido de reembolsos pedidos.

**Controlos:** (i) cada linha de IVA: valor = base × taxa (tolerância `CFG_Tol`); (ii) IVA contabilístico = Σ base × taxa por mês; (iii) saldo das contas 34.5 = apuramento acumulado − pagamentos/reembolsos.

**Pontos a validar:** exigibilidade do IVA em adiantamentos (o teste liquida IVA no adiantamento — tratamento conservador); autoliquidação em serviços de não residentes (o teste 15 não aplica IVA e está assinalado); regime de caixa / regimes especiais.

## 4. Facturação e AGT (13_FACTURAÇÃO_FISCAL)

**Quadro legal identificado:** **Decreto Presidencial n.º 71/25, de 20 de Março** — regime jurídico das facturas: software validado pela AGT, integridade dos dados, cópias de segurança, facturação electrónica com comunicação à AGT, SAF-T. Faseamento (fontes EY/Cegid): **Grandes Contribuintes e fornecedores do Estado desde 01/01/2026**; **regimes geral e simplificado do IVA desde 01/01/2027**.

O registo de documentos emitidos é gerado a partir do Diário e controla: hash, certificado do software, sequência por série, NIF do adquirente, duplicados, estado e erros de comunicação. A **checklist de conformidade AGT** combina verificações automáticas e confirmações manuais.

> A folha Excel **não é software de facturação** e não emite documentos fiscais. Os documentos devem ser emitidos por software validado pela AGT; a matriz recebe os seus dados.

## 5. SAF-T (14_SAFT)

Mapeia as secções do SAF-T (AO) — Header, MasterFiles (GeneralLedgerAccounts, Customer, Supplier, Product, TaxTable), GeneralLedgerEntries, SourceDocuments (SalesInvoices, Payments, PurchaseInvoices, MovementOfGoods) — às fontes da matriz e valida completude/consistência (🟢 Conforme / 🟡 Incompleto / 🔴 Inconsistente). A estrutura XSD vigente deve ser confirmada no Portal da AGT.

## 6. Imposto Industrial (15_IMPOSTO_INDUSTRIAL)

**Quadro legal identificado:** Código do Imposto Industrial alterado pela **Lei n.º 26/20, de 20 de Julho** — taxa geral **25%** (existem taxas especiais sectoriais a parametrizar). O regime geral exige contabilidade organizada; a matéria colectável parte do resultado contabilístico.

**Mapa de reconciliação contabilístico-fiscal**

```
Resultado antes de impostos (DR)
+ acréscimos (gastos não dedutíveis do Quadro A + correcções manuais)
− deduções (rendimentos não tributáveis + correcções manuais)
= lucro tributável
− prejuízos fiscais reportáveis (prazo/limite POR VALIDAR)
= MATÉRIA COLECTÁVEL × taxa (II_GER)
= colecta estimada
− retenções na fonte sofridas (34.1.2) − liquidação provisória paga
= imposto a pagar / (a recuperar)
```

O Quadro A separa, por rubrica, gastos contabilísticos em dedutíveis e não dedutíveis (percentagem com fundamento a indicar). O Quadro C separa diferenças permanentes e temporárias e calcula a taxa efectiva. O imposto contabilizado (87) é comparado com o estimado.

## 7. IRT, INSS, Imposto de Selo e outros

- **IRT (Grupo A):** a tabela é escolhida pelo exercício (`00_CONFIGURAÇÃO`). **Até 2024** — Lei n.º 28/20 (13 escalões, isenção 70 000 Kz). **2025** — Lei n.º 18/24, art. 20.º n.º 3 e Anexo I (DR I Série n.º 247, 30/12/2024, p. 13798): isenção 100 000 Kz, 12 escalões, 13% a 25%, base = excesso sobre 100 001, 150 001, … tal como publicado. **2026** — Lei n.º 14/25, art. 21.º n.º 3 e Anexo I: isenção 150 000 Kz aplicada; **escalões por carregar** (separador IRT_ESCALOES do modelo). Matéria colectável = remuneração − INSS do trabalhador. Testes: `tests/test_irt.py` (14 casos).
- **IRT Grupo C:** OGE 2026 — 6,5% sobre vendas/serviços não sujeitos a retenção para volume 2025 ≥ 10 M Kz (fonte KPMG).
- **INSS:** 3% trabalhador / 8% entidade empregadora — parâmetro a validar.
- **Imposto de Selo:** recibo de quitação 1% (verba 23.3) com âmbito restrito — a validar.
- **Imposto Predial / IAC:** estrutura criada, taxas não parametrizadas (OGE 2026 alterou isenções do Predial).

## 8. Calendário fiscal (34_CALENDÁRIO_FISCAL_AGT)

Prazos gerados por regra **parametrizada** (por omissão "último dia do mês seguinte" para as obrigações mensais e 31/05 para a declaração Modelo 1). **Todos marcados POR VALIDAR.** O estado (entregue / por entregar), data de entrega e comprovativo são input; os alertas (prazo ultrapassado, a vencer ≤ 10 dias, entregue fora do prazo) são automáticos. Valores a entregar vêm do Diário/12_IVA.

## 9. Pontos em aberto

Ver secção final de `06_MATRIZ_LEGISLACAO.md`.
