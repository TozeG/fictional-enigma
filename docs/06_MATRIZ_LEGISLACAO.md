# 06 — Matriz de Legislação

> Pesquisa efectuada em 24/09/2026 com base em fontes secundárias (MINFIN, consultoras, imprensa especializada). **Nenhuma regra deve ser usada oficialmente sem confirmação no Diário da República.**

## Diplomas

| Diploma | Número | Data | Artigo | Matéria | Regra | Aplicabilidade | Vigor | Revogação | Fonte | Estado |
|---|---|---|---|---|---|---|---|---|---|---|
| Decreto | 82/01 | 16/11/2001 | — | Contabilidade | Aprova o Plano Geral de Contabilidade (PGC) | Entidades abrangidas pelo PGC (confirmar normativo aplicável: IFRS para certas entidades, planos sectoriais BNA/ARSEG) | 2001 | — | Diário da República | POR VALIDAR data exacta |
| Lei | 14/23 | 28/12/2023 | Vários | IVA | Altera e republica o Código do IVA (taxas 14% / 7% / 5% / 1%; dedução até 12 meses; reembolso mínimo 700 000 Kz) | Sujeitos passivos de IVA | 28/12/2023 | — | https://cms.law/pt/prt/publication/angola-alteracoes-ao-codigo-do-imposto-sobre-o-valor-acrescentado | CONFIRMADO (fonte secundária) |
| Regulamentação IVA / PGC | Instrutivo/Decreto Executivo — a identificar | — | — | IVA / Contabilidade | Cria as contas de IVA no PGC (34.5.x) | Sujeitos passivos de IVA | — | — | — | POR VALIDAR |
| Lei | 26/20 | 20/07/2020 | Vários | Imposto Industrial | Altera o Código do Imposto Industrial (taxa geral 25%) | Pessoas colectivas e singulares com actividade comercial/industrial | 20/07/2020 | — | https://lex.ao/docs/assembleia-nacional/2020/lei-n-o-26-20-de-20-de-julho/ | CONFIRMADO (fonte secundária) |
| Lei | 28/20 | 22/07/2020 | Tabela | IRT | Altera o Código do IRT | Rendimentos do trabalho | 01/09/2020 | Alterada pela Lei do OGE 2026 | https://www.ucm.minfin.gov.ao/cs/groups/public/documents/document/aw4x/mjm3/~edisp/minfin1237855.pdf | CONFIRMADO (fonte secundária) |
| Lei | 14/25 | 30/12/2025 | Várias | OGE 2026 | Lei do OGE 2026: alterações ao IRT (isenção e escalões), IRT Grupo C 6,5%, Imposto Predial, Imposto de Selo | Todos os contribuintes | 01/01/2026 | — | https://kpmg.com/ao/pt/insights/tax-news/lei-orcamento-geral-estado-2026.html | POR VALIDAR (número/data a confirmar no DR) |
| Decreto Presidencial | 71/25 | 20/03/2025 | Vários | Facturação | Regime Jurídico das Facturas e Documentos Equivalentes: software validado AGT, facturação electrónica, comunicação, SAF-T, cópias de segurança | Grandes Contribuintes e fornecedores do Estado desde 01/01/2026; regimes geral e simplificado de IVA desde 01/01/2027 | Faseado | Revoga o regime anterior (confirmar) | https://www.ey.com/pt_ao/technical/tax-alerts/facturacao-electronica-a-partir-de-1-de-janeiro-de-2026 | CONFIRMADO (fonte secundária) |
| Decreto Presidencial | 312/18 | — | — | Facturação | Regime jurídico das facturas anterior | — | — | Presumivelmente revogado pelo DP 71/25 — confirmar | — | POR VALIDAR |
| Código | Imposto de Selo | — | Tabela anexa, verba 23.3 | Imposto de Selo | Recibo de quitação — 1% (âmbito restrito) | Ver parametrização IS_REC | — | — | https://www.expansao.co.ao/gestao/detalhe/imposto-de-selo-do-recibo-regresso-ou-retrocesso-60218.html | POR VALIDAR |
| Lei | Código Geral Tributário | — | — | Procedimento / infracções | Obrigações acessórias, prazos, juros e multas | Todos os contribuintes | — | — | — | POR VALIDAR |
| Decreto Presidencial | Reintegrações e amortizações — a identificar | — | Tabelas de taxas | Imposto Industrial | Taxas máximas fiscalmente aceites de amortização | Activos fixos | — | — | — | POR VALIDAR |
| Decreto Executivo | SAF-T (AO) — a identificar | — | Estrutura XSD | SAF-T | Estrutura do ficheiro SAF-T (AO) | Utilizadores de software de facturação/contabilidade | — | — | Portal da AGT | POR VALIDAR |
| Protecção social | Diploma de contribuições INSS — a identificar | — | — | Segurança Social | Taxas contributivas 3% trabalhador / 8% empregador (parâmetro) | Entidades empregadoras | — | — | — | POR VALIDAR |

## Parametrização fiscal (11_FISCALIDADE_AGT)

| Código | Imposto | Descrição | Taxa | Natureza | Diploma | Artigo | Vigência | Estado | Observação |
|---|---|---|---|---|---|---|---|---|---|
| IVA_GER | IVA | Taxa geral | 14.0% | Regra legal | Código do IVA, republicado pela Lei n.º 14/23, de 28 de Dezembro | Artigo das taxas — confirmar no DR | 2023-12-28 | CONFIRMADO (fonte secundária) | Confirmar no Diário da República antes do uso oficial. |
| IVA_HOT | IVA | Taxa — serviços de hotelaria e restauração | 7.0% | Regra legal | Código do IVA (Lei n.º 14/23) | Confirmar | — | POR VALIDAR | Vigência e âmbito a confirmar. |
| IVA_ALI | IVA | Taxa — bens alimentares de amplo consumo e insumos agrícolas (lista legal) | 5.0% | Regra legal | Código do IVA (Lei n.º 14/23) e lista anexa | Confirmar | 2024-01-01 | CONFIRMADO (fonte secundária) | Aplicável apenas aos bens da lista legal. |
| IVA_CAB | IVA | Taxa — regime especial da Província de Cabinda | 1.0% | Regra legal | Código do IVA (Lei n.º 14/23) | Confirmar | — | POR VALIDAR | Âmbito objectivo e subjectivo a confirmar. |
| IVA_ISE | IVA | Operação isenta sem direito à dedução | 0.0% | Regra legal | Código do IVA — isenções | Confirmar artigo da isenção concreta | — | POR VALIDAR | Indicar o fundamento legal de cada isenção no documento. |
| IVA_EXP | IVA | Exportação / isenção com direito à dedução | 0.0% | Regra legal | Código do IVA — isenções nas exportações | Confirmar | — | POR VALIDAR |  |
| IVA_NSUJ | IVA | Operação não sujeita | 0.0% | Regra legal | Código do IVA — incidência | Confirmar | — | POR VALIDAR |  |
| II_GER | Imposto Industrial | Taxa geral do Imposto Industrial | 25.0% | Regra legal | Código do Imposto Industrial, alterado pela Lei n.º 26/20, de 20 de Julho | Artigo da taxa — confirmar no DR | 2020-07-20 | CONFIRMADO (fonte secundária) | Existem taxas especiais por sector (ex.: banca, seguros, telecomunicações, agricultura) — parametrizar se aplicável. |
| RET_SERV | Imposto Industrial | Retenção na fonte sobre prestações de serviços | 6.5% | Parâmetro do modelo | Código do Imposto Industrial (Lei n.º 26/20) | Confirmar artigo, incidência e dispensas | — | POR VALIDAR | Taxa usada no teste. Confirmar incidência e excepções antes do uso oficial. |
| IS_REC | Imposto de Selo | Recibo de quitação (verba 23.3 da Tabela) | 1.0% | Regra legal | Código do Imposto de Selo — Tabela anexa, verba 23.3 | Verba 23.3 | — | POR VALIDAR | Aplicação limitada (ex.: sujeitos passivos com operações isentas sem direito à dedução). Confirmar. |
| INSS_TRAB | Segurança Social | Contribuição do trabalhador | 3.0% | Parâmetro do modelo | Regime jurídico de protecção social obrigatória (confirmar diploma vigente) | Confirmar | — | POR VALIDAR |  |
| INSS_EMP | Segurança Social | Contribuição da entidade empregadora | 8.0% | Parâmetro do modelo | Regime jurídico de protecção social obrigatória (confirmar diploma vigente) | Confirmar | — | POR VALIDAR |  |
| IRT_A | IRT | IRT Grupo A — ver tabela de escalões | — (não parametrizada) | Regra legal | Código do IRT, alterado pela Lei n.º 28/20 e pela Lei do OGE 2026 (Lei n.º 14/25) | Tabela anexa | 2026-01-01 | POR VALIDAR | Fontes secundárias divergem no limite de isenção (100 000 vs 150 000 Kz). Carregar a tabela oficial do DR. |
| IRT_C | IRT | IRT Grupo C — taxa sobre vendas/serviços não sujeitos a retenção (volume 2025 ≥ 10 M Kz) | 6.5% | Regra legal | Lei do OGE 2026 (Lei n.º 14/25) | Confirmar | 2026-01-01 | CONFIRMADO (fonte secundária) |  |
| IAC | Imposto sobre a Aplicação de Capitais | Taxas por tipo de rendimento | — (não parametrizada) | Regra legal | Código do IAC (confirmar diploma e alterações) | Confirmar | — | POR VALIDAR | Não parametrizado: carregar taxas oficiais. |
| IP | Imposto Predial | Taxas e isenções (OGE 2026: isenção transmissões habitacionais ≤ 40 M Kz) | — (não parametrizada) | Regra legal | Código do Imposto Predial e Lei do OGE 2026 | Confirmar | 2026-01-01 | POR VALIDAR | Não parametrizado: carregar taxas oficiais. |

## Pontos em aberto (validação obrigatória)

1. **Tabela do IRT 2026 (Grupo A)** — fontes secundárias divergem quanto ao limite de isenção (100 000 vs 150 000 Kz). A tabela na matriz está vazia de propósito; carregar a tabela oficial da Lei do OGE 2026.
2. **Número e data da Lei do OGE 2026** — referida como Lei n.º 14/25, de 30 de Dezembro, em fontes secundárias; confirmar.
3. **Retenção na fonte de 6,5% sobre serviços (Imposto Industrial)** — usada nos testes; confirmar artigo, incidência e dispensas.
4. **Contas de IVA no PGC (34.5.x)** — codificação analítica usada é a sugerida; confirmar com o instrutivo/decreto executivo que as criou.
5. **Prazos declarativos (IVA, IRT, INSS, retenções, Imposto de Selo, Modelo 1)** — parametrizados como 'último dia do mês seguinte' e '31/05'; validar cada um.
6. **Taxas de amortização fiscalmente aceites** — diploma a identificar; vida útil actual = política contabilística.
7. **Exigibilidade do IVA em adiantamentos** e **autoliquidação em serviços de não residentes** — confirmar artigos do CIVA.
8. **Estrutura XSD do SAF-T (AO)** vigente e requisitos de comunicação electrónica (DP 71/25 e regulamentação).
