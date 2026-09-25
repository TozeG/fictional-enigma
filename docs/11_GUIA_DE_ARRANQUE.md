# 11 — Guia de Arranque (empresa sem sistema anterior)

A matriz **é** o sistema de contabilidade, fiscalidade e gestão financeira. Não há migração nem execução em paralelo: arranca-se com o balanço de abertura e, a partir daí, registam-se as operações do dia-a-dia.

Ficheiro de trabalho: `dist/MATRIZ_PRO_MASTER_VAZIA.xlsx` (sem dados fictícios; capacidade: 1 000 operações + 500 lançamentos manuais por exercício).
Ficheiro de aprendizagem: `dist/MATRIZ_PRO_MASTER_CONTABILIDADE_ANGOLA.xlsx` (mesma matriz com um trimestre de exemplo já registado).

## Semana 1 — Preparação (uma vez)

| # | Onde | O quê |
|---|---|---|
| 1 | `00_CONFIGURAÇÃO` | Nome, NIF, exercício, regime de IVA e de Imposto Industrial, Grande Contribuinte (S/N), reserva mínima de liquidez, limites de alerta |
| 2 | `01_PLANO_CONTAS` | Rever o PGC; acrescentar contas próprias (ex.: um banco por conta 43.1.x) — manter as colunas |
| 3 | `01A_TABELAS` | Se criou novas contas bancárias, acrescentá-las à lista **Pago / recebido por** |
| 4 | `01B_TERCEIROS` | Clientes e fornecedores com NIF, prazo e limite de crédito |
| 5 | `09_INVENTÁRIOS` | Artigos (código, descrição, stock mínimo/máximo) — se vende mercadorias |
| 6 | `10_ACTIVOS_FIXOS` | Bens do imobilizado (valor, data, vida útil) |
| 7 | `16_ORÇAMENTO_EMPRESARIAL` | Orçamento do ano (opcional, mas activa o Budget vs Actual) |

## Dia 1 — Abertura

Em `02_DIÁRIO_LANÇAMENTOS` (zona manual), um único lançamento com natureza **Abertura** e data 01/01: saldos de caixa, bancos, stock (com artigo e quantidade), clientes e fornecedores em aberto (com NIF), imobilizado, empréstimos, capital e resultados transitados. Σ Débito = Σ Crédito. Empresa nova: basta a entrada de capital (pode ser feita como operação "Entrada de capital").

## Todos os dias — `02A_OPERAÇÕES`

Uma linha por acontecimento. Escolhe-se o **Tipo de operação** e preenchem-se data, NIF, descrição, valor sem IVA, código IVA e **Pago / recebido por** ("A crédito" ou a caixa/banco). A matriz gera os lançamentos e a coluna **Estado** confirma 🟢.

| Aconteceu… | Tipo de operação | Notas |
|---|---|---|
| Vendi mercadoria | Venda de mercadorias | Artigo + quantidade → custo automático |
| Prestei um serviço | Prestação de serviços | |
| Recebi de um cliente | Recebimento de cliente | Ref. = nº da operação da venda |
| Comprei mercadoria | Compra de mercadorias | Artigo + quantidade |
| Paguei uma despesa (luz, renda, material…) | Despesa / fornecimento de serviços | Conta específica = conta de custo |
| Comprei equipamento | Aquisição de imobilizado | + registar em 10_ACTIVOS_FIXOS |
| Paguei a um fornecedor | Pagamento a fornecedor | Ref. = nº da operação da compra |
| Paguei salários | Salários (processar e pagar) | INSS 3%/8% e IRT automáticos (tabela oficial do ano) |
| Paguei impostos à AGT | Pagamento de impostos | Conta específica = 34.5.6 IVA, 34.3.1 IRT, 34.9.1 INSS… |
| Movimentei dinheiro entre contas | Transferência entre contas | |
| Recebi / reembolsei um empréstimo; paguei juros | Empréstimo recebido / Reembolso / Juros | |
| Sócios entraram com capital | Entrada de capital | |
| Fim do mês | Depreciação do mês | Valor vazio = cálculo de 10_ACTIVOS_FIXOS |

Situações especiais (notas de crédito, moeda estrangeira, retenções na fonte sofridas, adiantamentos, acréscimos e diferimentos, apuramento do IVA, estimativa de imposto) lançam-se no `02_DIÁRIO` (zona manual) — os exemplos estão na matriz de aprendizagem.

**A matriz não emite facturas.** As facturas continuam a ser emitidas por software validado pela AGT (obrigatório para Grandes Contribuintes desde 01/01/2026 e para os regimes geral e simplificado do IVA a partir de 01/01/2027 — DP n.º 71/25); na matriz regista-se a operação com o número, a série e o hash do documento.

## Todos os meses — fecho (`33_FECHO_MENSAL`)

1. Contagem de caixa (`05_CAIXA`) e extractos bancários (`06_BANCOS`).
2. Operação **Depreciação do mês**; acréscimos/diferimentos se houver.
3. Apuramento do IVA (`12_IVA`) → lançamento de apuramento → declaração e pagamento (operação **Pagamento de impostos**).
4. `99_CONTROLO_SISTEMA` sem 🔴 → marcar o mês como encerrado (S + data).
5. Ler `29_DASHBOARD_EXECUTIVO` e `38_RELATÓRIO_GESTÃO`.

## Critérios de "está a funcionar"

| Critério | Onde |
|---|---|
| Todas as operações 🟢 | `02A_OPERAÇÕES`, coluna Estado |
| Caixa = contagem; bancos = extracto | `05`, `06` |
| Saldos de clientes/fornecedores confirmados com os próprios | `07`, `08` |
| IVA do mapa = declaração entregue | `12_IVA` |
| Sistema sem bloqueio | `99_CONTROLO_SISTEMA` |
| Contabilista certificado validou o 1.º trimestre | parecer |

## Capacidade e desempenho

| Versão | Operações | Lançamentos manuais | Fórmulas | Recálculo completo (LibreOffice) |
|---|---|---|---|---|
| Aprendizagem | 300 | 2 000 | ~440 000 | ~45 s |
| Produção (vazia) | 1 000 | 500 | ~0,9 M | ~1,5 min |

Recálculo completo só acontece ao abrir; ao registar uma operação o Excel recalcula apenas o dependente. Se a actividade exceder a capacidade: regenerar com mais linhas (`MATRIZ_OPERACOES=3000 MATRIZ_MODO=producao python src/build.py …`) ou usar um ficheiro por semestre. Para volumes elevados, evoluir para Power Query/Power Pivot (`10_ROADMAP_POWER_BI.md`).

## Validação desta funcionalidade

`python tests/test_operacoes.py` — o trimestre de exemplo registado por 18 operações reproduz o mesmo trimestre lançado à mão: resultado, balanço por rubrica, IVA, clientes, fornecedores, DFC, caixa, bancos e imposto coincidem (diferença máxima 0,04 Kz, do arredondamento do custo médio); 54/54 verificações.
