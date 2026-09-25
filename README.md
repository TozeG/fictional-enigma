# MATRIZ PRO MASTER — Contabilidade, Fiscalidade, Gestão Financeira e Planeamento (Angola)

Sistema integrado de informação contabilístico-financeira em **Microsoft Excel**, gerado por código (auditável e reprodutível).

**UMA ÚNICA FONTE DE DADOS → MÚLTIPLAS VISÕES.** Funciona como aplicação: cada operação (venda, compra, recebimento, pagamento, salários, impostos…) é registada uma vez em `02A_OPERAÇÕES`, em linguagem de gestão; o motor `02B_MOTOR` gera as partidas dobradas no `02_DIÁRIO_LANÇAMENTOS` (que também aceita lançamentos manuais especiais); Diário Geral, Razão, Caixa, Bancos, Clientes, Fornecedores, Inventários, Activos, IVA, Imposto Industrial, Balancete, Balanço, DR, DFC, Orçamento, Tesouraria, KPI, Risco, Dashboard, Relatórios, Alertas e Controlo são calculados por fórmula.

> Estruturado para conformidade com o quadro legal identificado e sujeito à validação contabilística, fiscal e técnica antes da utilização oficial. A folha de cálculo **não** é software de facturação validado pela AGT.

## Entregáveis

| # | Entregável | Local |
|---|---|---|
| A | Ficheiro Excel principal (44 folhas, ~179 000 fórmulas, 563 nomes, 4 Tabelas Excel) | [`dist/MATRIZ_PRO_MASTER_CONTABILIDADE_ANGOLA.xlsx`](dist/MATRIZ_PRO_MASTER_CONTABILIDADE_ANGOLA.xlsx) |
| B | Manual de utilização | [`docs/01_MANUAL_UTILIZACAO.md`](docs/01_MANUAL_UTILIZACAO.md) |
| C | Manual contabilístico | [`docs/02_MANUAL_CONTABILISTICO.md`](docs/02_MANUAL_CONTABILISTICO.md) |
| D | Manual fiscal | [`docs/03_MANUAL_FISCAL.md`](docs/03_MANUAL_FISCAL.md) |
| E | Dicionário de dados (gerado) | [`docs/04_DICIONARIO_DADOS.md`](docs/04_DICIONARIO_DADOS.md) |
| F | Mapa de dependências (extraído das fórmulas) | [`docs/05_MAPA_DEPENDENCIAS.md`](docs/05_MAPA_DEPENDENCIAS.md) |
| G | Matriz de legislação | [`docs/06_MATRIZ_LEGISLACAO.md`](docs/06_MATRIZ_LEGISLACAO.md) |
| H | Checklist de conformidade | [`docs/07_CHECKLIST_CONFORMIDADE.md`](docs/07_CHECKLIST_CONFORMIDADE.md) |
| I | Casos de teste | [`docs/08_CASOS_TESTE.md`](docs/08_CASOS_TESTE.md) |
| J | Relatório de validação (gerado) | [`docs/09_RELATORIO_VALIDACAO.md`](docs/09_RELATORIO_VALIDACAO.md) |
| + | Evolução Power Query / Power Pivot / Power BI | [`docs/10_ROADMAP_POWER_BI.md`](docs/10_ROADMAP_POWER_BI.md) |
| + | Matriz vazia para produção (sem dados fictícios) | [`dist/MATRIZ_PRO_MASTER_VAZIA.xlsx`](dist/MATRIZ_PRO_MASTER_VAZIA.xlsx) |
| + | **Guia de arranque** (empresa sem sistema anterior) | [`docs/11_GUIA_DE_ARRANQUE.md`](docs/11_GUIA_DE_ARRANQUE.md) |
| + | Modelo de importação (carga inicial em massa, opcional) | [`dist/MODELO_IMPORTACAO.xlsx`](dist/MODELO_IMPORTACAO.xlsx) |

## Arquitectura

| Camada | Folhas |
|---|---|
| 1 — INPUT | 00_CONFIGURAÇÃO, 01_PLANO_CONTAS, 01A_TABELAS, 01B_TERCEIROS, **02_DIÁRIO_LANÇAMENTOS**, 10 (registo), 11 (parâmetros fiscais), 16 (orçamento), pressupostos de 17/24/25/26 |
| 2 — PROCESSAMENTO | 48 colunas calculadas do Diário, saldos do plano, 12_IVA, 15_IMPOSTO_INDUSTRIAL, depreciações |
| 3 — OUTPUT | 03–09, 13, 14, 18–39, 99 |

Validações por linha: contas inexistentes/de agregação, lançamento desequilibrado, datas inválidas e fora do exercício, documentos duplicados, NIF inválido/não registado, valores negativos, períodos encerrados, taxa fiscal incompatível, falta de suporte, câmbio inconsistente, natureza/fluxo não classificado, segregação de funções.

Motor de consistência (`99_CONTROLO_SISTEMA`): **SISTEMA CONFORME / COM PENDÊNCIAS / BLOQUEADO**, com provas matemáticas Diário = Razão = Balancete = Demonstrações, Caixa, Bancos, IVA, Imposto, DFC e Orçamento.

## Validação

`python tests/verify.py` → **164/164 verificações aprovadas**: comparação com um modelo contabilístico independente em Python (DR mensal, balanço por rubrica, saldos de todas as contas, IVA mensal, DFC, auxiliares, inventário, activos, imposto) e 10 testes negativos (injecção de erros → detecção e bloqueio). Recalculado com LibreOffice Calc: 0 erros de fórmula.

## Gerar / regenerar

```bash
pip install openpyxl
python src/build.py            # dist/MATRIZ_PRO_MASTER_CONTABILIDADE_ANGOLA.xlsx
python tests/verify.py         # requer LibreOffice Calc (libreoffice-calc)
python src/gen_docs.py         # docs 04, 05, 06, 08
MATRIZ_LINHAS=10000 python src/build.py   # Diário com mais capacidade
MATRIZ_MODO=producao python src/build.py dist/MATRIZ_PRO_MASTER_VAZIA.xlsx   # sem dados fictícios
python src/importar.py modelo                              # modelo de importação
python src/importar.py carregar modelo.xlsx --saida dist/MATRIZ_X.xlsx      # valida, gera e compara com o sistema actual
python tests/test_importar.py                              # teste de ponta a ponta do importador
python tests/test_operacoes.py                             # operações = lançamentos manuais (54/54)
python tests/test_irt.py                                   # IRT 2024/2025/2026 (17/17)
```

| Código | Conteúdo |
|---|---|
| `src/data.py` | Plano de contas PGC, parametrização fiscal com fontes, base legal, terceiros, activos e lançamentos de teste |
| `src/sheets_base.py` | Configuração, plano, tabelas, terceiros e o Diário (motor de validação) |
| `src/sheets_ledgers.py` | Diário geral, razão, caixa, bancos, clientes, fornecedores, inventários, activos |
| `src/sheets_fiscal.py` | Fiscalidade AGT, IVA, facturação, SAF-T, Imposto Industrial, calendário, base legal |
| `src/sheets_reports.py` | Balancete, Balanço, DR, fluxo de caixa, DFC, orçamento, tesouraria, budget vs actual |
| `src/sheets_analytics.py` | KPI, sustentabilidade, dashboard, planeamento/cenários, projectos, investimentos, risco, break-even |
| `src/sheets_ops.py` | Modo aplicação: 02A_OPERAÇÕES, 02B_MOTOR e modelos de lançamento |
| `src/importar.py` | Importação de dados reais, validação prévia e comparação com o balancete do sistema actual |
| `src/sheets_mgmt.py` | LEIA-ME, controlo interno, auditoria, fecho, encerramento, relatório de gestão, alertas, motor de consistência |

## Pontos que exigem validação antes do uso oficial

Escalões do IRT 2026 (isenção de 150 000 Kz já aplicada; limites e parcelas fixas por carregar), número/data da Lei do OGE 2026, retenção de 6,5% sobre serviços, codificação 34.5.x do IVA, prazos do calendário fiscal, taxas de amortização fiscais, exigibilidade do IVA em adiantamentos e autoliquidação de serviços de não residentes, XSD do SAF-T. Detalhe em `docs/06_MATRIZ_LEGISLACAO.md`.
