# 08 — Casos de Teste (teste de integridade)

Os lançamentos de teste estão em `src/data.py` (lista `JOURNAL`) e são carregados no Diário da matriz entregue. Valores fictícios; entidade fictícia.
Resultados automáticos em `09_RELATORIO_VALIDACAO.md`.

| Teste | Operação | IDs | Reflexos verificados |
|---|---|---|---|
| TESTE 00 | Abertura | 1 | Saldos iniciais em 01_PLANO_CONTAS (abertura), 21_BALANÇO (coluna abertura), 05_CAIXA, 19/23 (saldo inicial), kardex A001 (1 000 un). |
| TESTE 01 | Venda a dinheiro (FR A/1) | 2 | 05_CAIXA (+114 000), 22_DRE Jan (vendas 100 000; CMV −60 000), 12_IVA Jan (liquidado 14 000), 13_FACTURAÇÃO (FR A/1), 19/23 (recebimentos de clientes), 09_INVENTÁRIOS (−60 un). |
| TESTE 02 | Venda a crédito (FT A/1) | 3 | 07_CLIENTES (doc ID 3), 22_DRE, 12_IVA, 13_FACTURAÇÃO, aging, KPI PMR. |
| TESTE 03 | Compra a crédito (FC B/889) | 4 | 08_FORNECEDORES (doc ID 4), 12_IVA dedutível 77 000, 09_INVENTÁRIOS (+500 un a 1 100), CMP móvel. |
| TESTE 04 | Compra a pronto (FRF G/1502) | 5 | 05_CAIXA (−57 000), 22_DRE FSE, 12_IVA dedutível 7 000, DFC pagamentos a fornecedores. |
| TESTE 05 | Pagamento a fornecedor | 10 | 08_FORNECEDORES (doc 4 em aberto 227 000), 06_BANCOS, 19/23. |
| TESTE 06 | Recebimento de cliente (parcial + com retenção) | 11, 20 | 07_CLIENTES (doc 3: 213 000; doc 12: 0), 11_FISCALIDADE retenções 195 000, 15_IMPOSTO_INDUSTRIAL (dedução à colecta), 19/23. |
| TESTE 07 | Salários (processamento + pagamento) | 6, 7 | 22_DRE pessoal 432 000, 11_FISCALIDADE (IRT/INSS), 34_CALENDÁRIO, DFC pagamentos ao pessoal. |
| TESTE 08 | Aquisição de activo (AF001) | 8 | 10_ACTIVOS_FIXOS, 21_BALANÇO imobilizado, 23_DFC investimento, 24_PROJECTOS (PRJ01), 12_IVA dedutível 168 000. |
| TESTE 09 | Depreciação (Fev + Mar) | 15, 24 | 10_ACTIVOS (estado 'Processada' por mês), 22_DRE amortizações 50 000, 33_FECHO_MENSAL, EBITDA. |
| TESTE 10 | Empréstimo bancário | 9 | 21_BALANÇO passivo não corrente 3 000 000, 23_DFC financiamento, KPI Dívida/EBITDA, 26_RISCO. |
| TESTE 11 | Pagamento de juros | 16 | 22_DRE custos financeiros, 23_DFC financiamento (juros pagos), cobertura de juros. |
| TESTE 12 | Operação sujeita a IVA (serviços FT A/2) | 12, 3 | 12_IVA liquidado 420 000, 22_DRE serviços 3 000 000, 24_PROJECTOS PRJ02. |
| TESTE 13 | Operação isenta (FT A/3) | 13 | 12_IVA base isenta 200 000 (IVA_ISE), checklist AGT (motivo de isenção), comunicação pendente → 🟡. |
| TESTE 14 | Nota de crédito (NC A/1) | 14 | 12_IVA regularização a favor 7 000, 22_DRE vendas −50 000, 07_CLIENTES (reduz doc 3), 13_FACTURAÇÃO. |
| TESTE 15 | Operação cambial (USD) | 17, 23 | Validação câmbio × valor ME, 08_FORNECEDORES estrangeiro, diferença de câmbio 20 000 em 22_DRE, 39_ALERTAS risco cambial. |
| TESTE 16 | Investimento financeiro (depósito a prazo) | 19 | 21_BALANÇO aplicações 1 000 000, 23_DFC investimento (não é equivalente de caixa). |
| TESTE 17 | Financiamento (empréstimo + aumento de capital) | 22, 9 | 21_BALANÇO capital 7 000 000, 23_DFC financiamento 4 955 000. |
| TESTE 18 | Despesa antecipada (seguro anual) | 18, 25 | 37.4.1 diferimento 1 100 000 no activo, 22_DRE seguros 100 000 (1/12). |
| TESTE 19 | Receita antecipada (adiantamento FR A/2) | 21 | 37.6.1 proveito diferido 600 000, IVA liquidado 84 000, 13_FACTURAÇÃO erro de comunicação → 🔴 (detecção). |
| TESTE 20 | Operação de encerramento | (proposta 37) | 37_ENCERRAMENTO_EXERCÍCIO: apuramento proposto equilibrado; resultado apurado = RL da DR; abertura N+1 equilibrada. |

## Lançamentos adicionais do cenário

| ID | Operação |
|---|---|
| 26 | Acréscimo de custos (electricidade Março) |
| 27 | Estimativa de Imposto Industrial do 1.º trimestre |
| 28, 30, 32 | Apuramento mensal do IVA (34.5.2/34.5.3/34.5.4 → 34.5.6) |
| 29, 31 | Pagamentos ao Estado (IRT/INSS de Janeiro; IVA de Fevereiro) |

## Testes negativos (injecção de erros)

| Erro injectado | Resultado esperado |
|---|---|
| Lançamento desequilibrado | 'ERRO — LANÇAMENTO NÃO EQUILIBRADO' + SISTEMA BLOQUEADO |
| Documento duplicado | 'Documento duplicado' + bloqueio |
| Conta inexistente | 'Conta inexistente' + bloqueio |
| Conta de agregação | 'Conta não movimentável' + bloqueio |
| Alteração em mês encerrado | 'Alteração em período encerrado' + bloqueio |
| Taxa de IVA incompatível | 'Taxa fiscal incompatível' + bloqueio |
| Cliente sem NIF | 'NIF inválido/não registado' + bloqueio |
| Sem documento de suporte | 'Sem documento de suporte' + bloqueio |
| Fora do exercício | 'Fora do exercício' + bloqueio |
| Câmbio inconsistente | 'Câmbio inconsistente' + bloqueio |

## Valores de referência do cenário (31/03/2026)

| Indicador | Valor (Kz) |
|---|---|
| Receita (vendas + serviços) | 3 750 000,00 |
| Resultado operacional | 1 673 614,00 |
| Resultado antes de impostos | 1 608 614,00 |
| Imposto Industrial estimado (25%) | 402 153,50 |
| Resultado líquido | 1 206 460,50 |
| Activo total = CP + Passivo | 13 799 614,00 |
| Capital próprio | 9 406 460,50 |
| IVA apurado Jan–Mar | 329 000,00 (pago 245 000; a pagar 84 000) |
| Meios monetários | 8 856 000,00 |
| Clientes em aberto | 413 000,00 |
| Fornecedores em aberto | 227 000,00 |
| Existências (A001: 1 040 un) | 1 085 614,00 |
