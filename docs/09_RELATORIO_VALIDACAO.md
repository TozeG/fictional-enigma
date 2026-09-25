# 09 — Relatório de Validação

Gerado automaticamente por `tests/verify.py` em 2026-09-25.

Método: a matriz é gerada com os casos de teste, recalculada com o LibreOffice Calc (motor independente do Excel) e cada valor
é comparado com um modelo contabilístico independente escrito em Python a partir dos mesmos lançamentos. Os testes negativos
injectam erros no Diário e confirmam que o sistema os detecta.

**Resultado: 164 / 164 verificações aprovadas.**

| Área | Verificação | Obtido | Esperado | Resultado |
|---|---|---|---|---|
| Recálculo | 111349 fórmulas, erros = 0 | 0.00 | 0.00 | ✅ |
| DR mensal | DR01 mês 1 | 600,000.00 | 600,000.00 | ✅ |
| DR mensal | DR01 mês 2 | 150,000.00 | 150,000.00 | ✅ |
| DR mensal | DR02 mês 2 | 3,000,000.00 | 3,000,000.00 | ✅ |
| DR mensal | DR04 mês 1 | -360,000.00 | -360,000.00 | ✅ |
| DR mensal | DR04 mês 2 | -104,386.00 | -104,386.00 | ✅ |
| DR mensal | DR05 mês 1 | -50,000.00 | -50,000.00 | ✅ |
| DR mensal | DR05 mês 3 | -1,080,000.00 | -1,080,000.00 | ✅ |
| DR mensal | DR06 mês 1 | -432,000.00 | -432,000.00 | ✅ |
| DR mensal | DR07 mês 2 | -25,000.00 | -25,000.00 | ✅ |
| DR mensal | DR07 mês 3 | -25,000.00 | -25,000.00 | ✅ |
| DR mensal | DR10 mês 2 | -45,000.00 | -45,000.00 | ✅ |
| DR mensal | DR10 mês 3 | -20,000.00 | -20,000.00 | ✅ |
| DR mensal | DR13 mês 3 | -402,153.50 | -402,153.50 | ✅ |
| DR | Resultado antes de impostos (acum.) | 1,608,614.00 | 1,608,614.00 | ✅ |
| DR | Resultado líquido (acum.) | 1,206,460.50 | 1,206,460.50 | ✅ |
| Balanço | BA_IMOB_CORP | 1,150,000.00 | 1,150,000.00 | ✅ |
| Balanço | BA_IMOB_INC | 0.00 | 0.00 | ✅ |
| Balanço | BA_INV_FIN | 0.00 | 0.00 | ✅ |
| Balanço | BA_EXIST | 1,085,614.00 | 1,085,614.00 | ✅ |
| Balanço | BA_CLIENTES | 413,000.00 | 413,000.00 | ✅ |
| Balanço | BA_ESTADO | 195,000.00 | 195,000.00 | ✅ |
| Balanço | BA_OUTROS_REC | 0.00 | 0.00 | ✅ |
| Balanço | BA_ACRESC | 1,100,000.00 | 1,100,000.00 | ✅ |
| Balanço | BA_APLIC | 1,000,000.00 | 1,000,000.00 | ✅ |
| Balanço | BA_DISP | 8,856,000.00 | 8,856,000.00 | ✅ |
| Balanço | BCP_CAPITAL | 7,000,000.00 | 7,000,000.00 | ✅ |
| Balanço | BCP_RESERVAS | 0.00 | 0.00 | ✅ |
| Balanço | BCP_RT | 1,200,000.00 | 1,200,000.00 | ✅ |
| Balanço | BCP_RL | 1,206,460.50 | 1,206,460.50 | ✅ |
| Balanço | BPNC_EMP | 3,000,000.00 | 3,000,000.00 | ✅ |
| Balanço | BPNC_PROV | 0.00 | 0.00 | ✅ |
| Balanço | BPC_FORN | 227,000.00 | 227,000.00 | ✅ |
| Balanço | BPC_EMP | 0.00 | 0.00 | ✅ |
| Balanço | BPC_ESTADO | 486,153.50 | 486,153.50 | ✅ |
| Balanço | BPC_OUTROS | 0.00 | 0.00 | ✅ |
| Balanço | BPC_ACRESC | 680,000.00 | 680,000.00 | ✅ |
| Balanço | Activo = CP + Passivo | 🟢 Balanço equilibrado | 🟢 | ✅ |
| Balanço | Activo total | 13,799,614.00 | 13,799,614.00 | ✅ |
| Razão/Plano | saldo 11.5.1 | 1,200,000.00 | 1,200,000.00 | ✅ |
| Razão/Plano | saldo 18.1.5 | -50,000.00 | -50,000.00 | ✅ |
| Razão/Plano | saldo 26.1 | 1,085,614.00 | 1,085,614.00 | ✅ |
| Razão/Plano | saldo 31.1.1 | 413,000.00 | 413,000.00 | ✅ |
| Razão/Plano | saldo 32.1.1 | -227,000.00 | -227,000.00 | ✅ |
| Razão/Plano | saldo 32.1.2 | 0.00 | 0.00 | ✅ |
| Razão/Plano | saldo 33.1.1 | -3,000,000.00 | -3,000,000.00 | ✅ |
| Razão/Plano | saldo 34.1.1 | -402,153.50 | -402,153.50 | ✅ |
| Razão/Plano | saldo 34.1.2 | 195,000.00 | 195,000.00 | ✅ |
| Razão/Plano | saldo 34.3.1 | 0.00 | 0.00 | ✅ |
| Razão/Plano | saldo 34.5.2 | 0.00 | 0.00 | ✅ |
| Razão/Plano | saldo 34.5.3 | 0.00 | 0.00 | ✅ |
| Razão/Plano | saldo 34.5.4.1 | 0.00 | 0.00 | ✅ |
| Razão/Plano | saldo 34.5.6 | -84,000.00 | -84,000.00 | ✅ |
| Razão/Plano | saldo 34.9.1 | 0.00 | 0.00 | ✅ |
| Razão/Plano | saldo 36.1.1 | 0.00 | 0.00 | ✅ |
| Razão/Plano | saldo 37.4.1 | 1,100,000.00 | 1,100,000.00 | ✅ |
| Razão/Plano | saldo 37.5.1 | -80,000.00 | -80,000.00 | ✅ |
| Razão/Plano | saldo 37.6.1 | -600,000.00 | -600,000.00 | ✅ |
| Razão/Plano | saldo 42.1 | 1,000,000.00 | 1,000,000.00 | ✅ |
| Razão/Plano | saldo 43.1.1 | 8,599,000.00 | 8,599,000.00 | ✅ |
| Razão/Plano | saldo 45.1 | 257,000.00 | 257,000.00 | ✅ |
| Razão/Plano | saldo 51.1 | -7,000,000.00 | -7,000,000.00 | ✅ |
| Razão/Plano | saldo 61.1 | -800,000.00 | -800,000.00 | ✅ |
| Razão/Plano | saldo 61.8 | 50,000.00 | 50,000.00 | ✅ |
| Razão/Plano | saldo 62.1 | -3,000,000.00 | -3,000,000.00 | ✅ |
| Razão/Plano | saldo 71.1 | 464,386.00 | 464,386.00 | ✅ |
| Razão/Plano | saldo 72.2 | 400,000.00 | 400,000.00 | ✅ |
| Razão/Plano | saldo 72.5 | 32,000.00 | 32,000.00 | ✅ |
| Razão/Plano | saldo 73.1 | 50,000.00 | 50,000.00 | ✅ |
| Razão/Plano | saldo 75.2.1 | 50,000.00 | 50,000.00 | ✅ |
| Razão/Plano | saldo 75.2.2 | 900,000.00 | 900,000.00 | ✅ |
| Razão/Plano | saldo 75.2.3 | 100,000.00 | 100,000.00 | ✅ |
| Razão/Plano | saldo 75.2.4 | 80,000.00 | 80,000.00 | ✅ |
| Razão/Plano | saldo 76.1 | 45,000.00 | 45,000.00 | ✅ |
| Razão/Plano | saldo 76.5 | 20,000.00 | 20,000.00 | ✅ |
| Razão/Plano | saldo 81.1 | -1,200,000.00 | -1,200,000.00 | ✅ |
| Razão/Plano | saldo 87.1 | 402,153.50 | 402,153.50 | ✅ |
| IVA mensal | DED mês 1 | 84,000.00 | 84,000.00 | ✅ |
| IVA mensal | DED mês 2 | 168,000.00 | 168,000.00 | ✅ |
| IVA mensal | LIQ mês 1 | 84,000.00 | 84,000.00 | ✅ |
| IVA mensal | LIQ mês 2 | 420,000.00 | 420,000.00 | ✅ |
| IVA mensal | LIQ mês 3 | 84,000.00 | 84,000.00 | ✅ |
| IVA mensal | REGSP mês 2 | 7,000.00 | 7,000.00 | ✅ |
| IVA | IVA a pagar acumulado | 329,000.00 | 329,000.00 | ✅ |
| IVA | Conciliação contabilidade × mapa | 🟢 IVA conciliado | 🟢 | ✅ |
| DFC | Recebimentos de clientes | 4,323,000.00 | 4,323,000.00 | ✅ |
| DFC | Pagamentos a fornecedores | -1,377,000.00 | -1,377,000.00 | ✅ |
| DFC | Pagamentos ao pessoal | -322,030.00 | -322,030.00 | ✅ |
| DFC | Pagamentos de imobilizações | -1,368,000.00 | -1,368,000.00 | ✅ |
| DFC | Empréstimos obtidos | 3,000,000.00 | 3,000,000.00 | ✅ |
| DFC | Pagamentos/recebimentos de impostos | -354,970.00 | -354,970.00 | ✅ |
| DFC | Juros e custos similares pagos | -45,000.00 | -45,000.00 | ✅ |
| DFC | Outros recebimentos/pagamentos operacionais | -1,200,000.00 | -1,200,000.00 | ✅ |
| DFC | Aplicações e investimentos financeiros | -1,000,000.00 | -1,000,000.00 | ✅ |
| DFC | Aumentos de capital | 2,000,000.00 | 2,000,000.00 | ✅ |
| DFC | Caixa no fim do período | 8,856,000.00 | 8,856,000.00 | ✅ |
| DFC | DFC = saldo das contas de meios monetários | 🟢 DFC conciliada com o Balanço/Razão | 🟢 | ✅ |
| Clientes | saldo em aberto doc ID 3 | 213,000.00 | 213,000.00 | ✅ |
| Clientes | saldo em aberto doc ID 12 | 0.00 | 0.00 | ✅ |
| Clientes | saldo em aberto doc ID 13 | 200,000.00 | 200,000.00 | ✅ |
| Clientes | Auxiliar = Razão (conta 31) | 🟢 Clientes conciliados | 🟢 | ✅ |
| Fornecedores | saldo em aberto doc ID 4 | 227,000.00 | 227,000.00 | ✅ |
| Fornecedores | saldo em aberto doc ID 17 | 0.00 | 0.00 | ✅ |
| Fornecedores | Auxiliar = Razão (conta 32) | 🟢 Fornecedores conciliados | 🟢 | ✅ |
| Inventário | A001 quantidade final | 1,040.00 | 1,040.00 | ✅ |
| Inventário | A001 valor | 1,085,614.00 | 1,085,614.00 | ✅ |
| Inventário | Kardex: saídas ao custo médio ponderado | 0.00 | 0.00 | ✅ |
| Activos | AF001 depreciação acumulada 31/03 | 50,000.00 | 50,000.00 | ✅ |
| Activos | AF001 VLC | 1,150,000.00 | 1,150,000.00 | ✅ |
| Activos | Registo = contabilidade | 🟢 Activos conciliados | 🟢 | ✅ |
| Imposto Industrial | Matéria colectável | 1,608,614.00 | 1,608,614.00 | ✅ |
| Imposto Industrial | Imposto estimado (25%) | 402,153.50 | 402,153.50 | ✅ |
| Imposto Industrial | A pagar após retenções (195 000) | 207,153.50 | 207,153.50 | ✅ |
| Imposto Industrial | Contabilizado = estimado | 🟢 Fiscalidade conciliada | 🟢 | ✅ |
| Caixa | Saldo 45.1 | 257,000.00 | 257,000.00 | ✅ |
| Bancos | Saldo contabilístico 43 | 8,599,000.00 | 8,599,000.00 | ✅ |
| Bancos | Diferença de reconciliação | 0.00 | 0.00 | ✅ |
| Bancos | Item pendente detectado (despesa 2 500 não contabilizada) | 1.00 | 1.00 | ✅ |
| Retenções | 6,5% sobre 3 000 000 | 195,000.00 | 195,000.00 | ✅ |
| Facturação | 8 documentos emitidos no registo | 8.00 | 8.00 | ✅ |
| Facturação | Erro de comunicação AGT detectado (FR A/2) | 🟢 Conforme/🟢 Conforme/🟢 Conforme/🟢 Conforme/🟡 Comunicação pendente/🟢 C | 🔴 Erro de comunicação | ✅ |
| Facturação | Comunicação pendente detectada (FT A/3) | 🟢 Conforme/🟢 Conforme/🟢 Conforme/🟢 Conforme/🟡 Comunicação pendente/🟢 C | 🟡 Comunicação pendente | ✅ |
| Reconciliação global | Diário = Razão (Σ débitos do Diário vs Σ débitos das contas de movimento) | 🟢 Provado | 🟢 Provado | ✅ |
| Reconciliação global | Razão = Balancete (Σ saldos devedores − credores = 0) | 🟢 Provado | 🟢 Provado | ✅ |
| Reconciliação global | Balancete = Demonstrações (Activo vs CP + Passivo) | 🟢 Provado | 🟢 Provado | ✅ |
| Reconciliação global | Resultado no Balanço = Resultado na DR | 🟢 Provado | 🟢 Provado | ✅ |
| Reconciliação global | Caixa contabilístico = movimento de caixa (05_CAIXA) | 🟢 Provado | 🟢 Provado | ✅ |
| Reconciliação global | Bancos contabilísticos = reconciliação bancária (extracto ajustado) | 🟢 Provado | 🟢 Provado | ✅ |
| Reconciliação global | IVA contabilístico (saldo 34.5) = mapa fiscal de IVA (apuramento acumulado) | 🟢 Provado | 🟢 Provado | ✅ |
| Reconciliação global | Resultado contabilístico → fiscal → imposto (estimado vs contabilizado) | 🟢 Provado | 🟢 Provado | ✅ |
| Reconciliação global | Fluxos contabilísticos → DFC (saldo final DFC vs contas de meios monetários) | 🟢 Provado | 🟢 Provado | ✅ |
| Reconciliação global | Orçamento: Σ mapa por rubrica = Σ orçamentos parciais (RL orçado) | 🟢 Provado | 🟢 Provado | ✅ |
| Integridade (críticas) | Diário equilibrado? | 🟢 Diário equilibrado | 🟢 | ✅ |
| Integridade (críticas) | Lançamentos sem erros de validação? | 🟢 Sem erros | 🟢 | ✅ |
| Integridade (críticas) | Razão reconciliado com o Diário? | 🟢 Provado | 🟢 | ✅ |
| Integridade (críticas) | Balancete equilibrado? | 🟢 Balancete equilibrado / 🟢 Diário = Balancete | 🟢 | ✅ |
| Integridade (críticas) | Balanço equilibrado? | 🟢 Balanço equilibrado | 🟢 | ✅ |
| Integridade (críticas) | Plano de contas íntegro? | 🟢 Plano íntegro | 🟢 | ✅ |
| Integridade (críticas) | Períodos encerrados sem bloqueio? | 🟢 OK | 🟢 | ✅ |
| Sistema | Estado global (esperado: pendências intencionais, sem bloqueio) | 🟡 SISTEMA COM PENDÊNCIAS | 🟡 SISTEMA COM PENDÊNCIAS | ✅ |
| Investimentos | Grelha de sensibilidade reproduz o VAL do modelo | 🟢 Modelo de sensibilidade consistente | 🟢 | ✅ |
| Encerramento | Apuramento proposto equilibrado | 🟢 Apuramento equilibrado | 🟢 | ✅ |
| Encerramento | Resultado apurado = RL da DR | 1,206,460.50 | 1,206,460.50 | ✅ |
| Encerramento | Abertura N+1 equilibrada | 🟢 Abertura equilibrada | 🟢 | ✅ |
| Teste negativo | Lançamento desequilibrado (FR A/1 crédito alterado) → erro detectado no Diário | ERRO — LANÇAMENTO NÃO EQUILIBRADO;  / ERRO — LANÇAMENTO NÃO EQUILIBRAD | LANÇAMENTO NÃO EQUILIBRADO | ✅ |
| Teste negativo | Lançamento desequilibrado (FR A/1 crédito alterado) → estado do sistema | 🔴 SISTEMA BLOQUEADO | 🔴 SISTEMA BLOQUEADO | ✅ |
| Teste negativo | Factura de fornecedor lançada em duplicado → erro detectado no Diário | Documento duplicado;  / Documento duplicado;  / Documento duplicado;  | Documento duplicado | ✅ |
| Teste negativo | Factura de fornecedor lançada em duplicado → estado do sistema | 🔴 SISTEMA BLOQUEADO | 🔴 SISTEMA BLOQUEADO | ✅ |
| Teste negativo | Conta inexistente → erro detectado no Diário | Conta inexistente;  | Conta inexistente | ✅ |
| Teste negativo | Conta inexistente → estado do sistema | 🔴 SISTEMA BLOQUEADO | 🔴 SISTEMA BLOQUEADO | ✅ |
| Teste negativo | Movimento em conta de agregação → erro detectado no Diário | Conta não movimentável;  | Conta não movimentável | ✅ |
| Teste negativo | Movimento em conta de agregação → estado do sistema | 🔴 SISTEMA BLOQUEADO | 🔴 SISTEMA BLOQUEADO | ✅ |
| Teste negativo | Alteração em Janeiro após o fecho (10/02) → erro detectado no Diário | Alteração em período encerrado;  | Alteração em período encerrado | ✅ |
| Teste negativo | Alteração em Janeiro após o fecho (10/02) → estado do sistema | 🔴 SISTEMA BLOQUEADO | 🔴 SISTEMA BLOQUEADO | ✅ |
| Teste negativo | IVA com taxa incompatível (15 000 em vez de 14 000) → erro detectado no Diário | Taxa fiscal incompatível;  | Taxa fiscal incompatível | ✅ |
| Teste negativo | IVA com taxa incompatível (15 000 em vez de 14 000) → estado do sistema | 🔴 SISTEMA BLOQUEADO | 🔴 SISTEMA BLOQUEADO | ✅ |
| Teste negativo | Venda a crédito sem NIF do cliente → erro detectado no Diário | NIF inválido/não registado;  | NIF inválido | ✅ |
| Teste negativo | Venda a crédito sem NIF do cliente → estado do sistema | 🔴 SISTEMA BLOQUEADO | 🔴 SISTEMA BLOQUEADO | ✅ |
| Teste negativo | Lançamento sem documento de suporte → erro detectado no Diário | Sem documento de suporte;  | Sem documento de suporte | ✅ |
| Teste negativo | Lançamento sem documento de suporte → estado do sistema | 🔴 SISTEMA BLOQUEADO | 🔴 SISTEMA BLOQUEADO | ✅ |
| Teste negativo | Lançamento fora do exercício → erro detectado no Diário | Fora do exercício;  / Fora do exercício;  / Fora do exercício;  | Fora do exercício | ✅ |
| Teste negativo | Lançamento fora do exercício → estado do sistema | 🔴 SISTEMA BLOQUEADO | 🔴 SISTEMA BLOQUEADO | ✅ |
| Teste negativo | Câmbio inconsistente (valor ME × câmbio ≠ Kz) → erro detectado no Diário | Câmbio inconsistente;  | Câmbio inconsistente | ✅ |
| Teste negativo | Câmbio inconsistente (valor ME × câmbio ≠ Kz) → estado do sistema | 🔴 SISTEMA BLOQUEADO | 🔴 SISTEMA BLOQUEADO | ✅ |
