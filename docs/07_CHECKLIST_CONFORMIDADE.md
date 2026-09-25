# 07 — Checklist de Conformidade (antes da utilização oficial)

Estado actual: **estruturado para conformidade; validação técnica e jurídica pendente.** Marque cada item com evidência e responsável (a mesma checklist existe em `35_BASE_LEGAL` e `13_FACTURAÇÃO_FISCAL`).

## A. Legal e fiscal

| # | Verificação | Estado | Evidência exigida |
|---|---|---|---|
| 1 | Legislação angolana vigente pesquisada | 🟢 Pesquisa inicial (fontes secundárias, 24/09/2026) | 06_MATRIZ_LEGISLACAO |
| 2 | PGC / normativo contabilístico aplicável confirmado (PGC, IFRS, plano sectorial) | 🟡 | Parecer do contabilista certificado |
| 3 | Código do IVA (Lei 14/23 e alterações posteriores) confirmado | 🟡 | Texto do DR |
| 4 | Contas 34.5.x do PGC confirmadas com a regulamentação do IVA | 🟡 | Instrutivo / decreto executivo |
| 5 | Código do Imposto Industrial (Lei 26/20 e alterações) — taxa aplicável ao sector | 🟡 | DR + enquadramento AGT |
| 6 | Retenção na fonte sobre serviços (6,5%) — incidência e dispensas | 🟡 | Artigo do CII |
| 7 | Código do Imposto de Selo — verbas aplicáveis | 🟡 | Tabela anexa |
| 8 | Código do IRT + **tabela oficial 2026** carregada em 11_FISCALIDADE_AGT | 🟢 ≤ 2024 (Lei 28/20) e 2025 (Lei 18/24, DR 30/12/2024) carregadas e testadas · 🟡 2026: isenção 150 000 Kz aplicada; escalões do Anexo I da Lei 14/25 por carregar | Leis n.º 28/20, 18/24 e 14/25 |
| 9 | Contribuições INSS (taxas vigentes) | 🟡 | Diploma da protecção social |
| 10 | Regime de facturação (DP 71/25) e faseamento da facturação electrónica | 🟢 Identificado / 🟡 aplicação | DP 71/25 + regulamentação |
| 11 | Estrutura SAF-T (AO) vigente | 🟡 | XSD no Portal da AGT |
| 12 | Prazos declarativos e de pagamento (calendário) | 🟡 | CGT / códigos de cada imposto |
| 13 | Normas revogadas identificadas (ex.: DP 312/18) | 🟡 | DR |
| 14 | Normas transitórias identificadas | 🟡 | DR |
| 15 | Regras específicas por regime (geral, simplificado, exclusão, sectoriais) | 🟡 | Enquadramento da entidade na AGT |

## B. Técnica (modelo)

| # | Verificação | Estado |
|---|---|---|
| 1 | Zero erros de fórmula (179 087 fórmulas) | 🟢 |
| 2 | Diário = Razão = Balancete = Demonstrações (provas em 99_CONTROLO_SISTEMA) | 🟢 |
| 3 | Activo = Capital próprio + Passivo | 🟢 |
| 4 | IVA contabilístico = mapa fiscal | 🟢 |
| 5 | DFC = saldo das contas de meios monetários | 🟢 |
| 6 | Auxiliares = Razão (clientes, fornecedores, inventário, activos) | 🟢 |
| 7 | Testes negativos (10 tipos de erro detectados e bloqueados) | 🟢 |
| 8 | Protecção com palavra-passe e perfis de utilizador | 🟡 A definir na implementação |
| 9 | Cópias de segurança e controlo de versões do ficheiro | 🟡 A definir (DP 71/25 exige cópias de segurança) |
| 10 | Teste com dados reais de um mês completo, em paralelo com o sistema actual | 🟡 Recomendado antes do uso oficial |

## C. Facturação / AGT

A matriz **não substitui** software de facturação validado pela AGT. Confirmar: software validado; séries registadas; hash e certificado em todos os documentos; comunicação electrónica sem erros; menções obrigatórias (incl. motivo de isenção); anulações com motivo; arquivo e conservação pelo prazo legal.

## Formulação obrigatória

> "Estruturado para conformidade com o quadro legal identificado e sujeito à validação contabilística, fiscal e técnica antes da utilização oficial."
