# 01 — Manual de Utilização

**Ficheiro:** `dist/MATRIZ_PRO_MASTER_CONTABILIDADE_ANGOLA.xlsx` (44 folhas, ~179 000 fórmulas, 563 nomes definidos).

> Estruturado para conformidade com o quadro legal identificado e sujeito à validação contabilística, fiscal e técnica antes da utilização oficial.

## 1. Princípio de funcionamento

Uma operação é introduzida **uma única vez** em `02_DIÁRIO_LANÇAMENTOS`. Tudo o resto — Diário Geral, Razão, Caixa, Bancos, Clientes, Fornecedores, Inventários, IVA, Imposto Industrial, Balancete, Balanço, DR, DFC, KPI, Dashboard, Relatórios, Alertas — é calculado por fórmula. Não existe nenhum valor repetido manualmente noutra folha.

```
INPUT (azul)  ──►  PROCESSAMENTO (cinzento)  ──►  OUTPUT (mapas, semáforos)
00, 01, 01A, 01B, 02, 16, 11     colunas AM+ do Diário, 01 (saldos), 12, 15     03–10, 19–39, 99
```

## 2. Convenção de cores

| Cor | Significado |
|---|---|
| Texto azul / fundo azul-claro | Campo de entrada — o único sítio onde se escreve |
| Preto | Fórmula |
| Cinzento | Processamento / protegido |
| Verde 🟢 | Validado / conforme |
| Amarelo 🟡 | Atenção / pendente / por validar |
| Vermelho 🔴 | Erro / crítico / bloqueante |

Separadores: azul = input, cinzento = processamento, verde = output.

## 3. Arranque (primeira utilização)

1. **00_CONFIGURAÇÃO** — nome, NIF, regime fiscal e de IVA, exercício, **mês de reporte**, reserva mínima de liquidez, limites de alerta. Os campos marcados "POR VALIDAR" (salário mínimo, taxa BNA) devem ser preenchidos com os valores oficiais.
2. **01_PLANO_CONTAS** — adapte ao plano da entidade. Mantenha as colunas; só contas `Movimento` recebem lançamentos; cada conta de movimento precisa de rubrica de balanço (devedora e credora) e, nas classes 6/7/87, de rubrica DR. A coluna *Validação* indica problemas.
3. **01A_TABELAS** — naturezas de operação (determinam a DFC), tipos de documento, rubricas, listas.
4. **01B_TERCEIROS** — clientes e fornecedores (NIF, prazo, limite de crédito, parte relacionada).
5. **10_ACTIVOS_FIXOS** — registo do imobilizado existente.
6. **16_ORÇAMENTO_EMPRESARIAL** — pressupostos do orçamento.
7. **Apague os lançamentos de teste** do Diário (linhas 6 a 94 — 89 linhas, 32 lançamentos) e registe o lançamento de abertura (natureza `Abertura`) a partir do balanço de fecho do ano anterior.

## 4. Como registar operações (modo aplicação) — `02A_OPERAÇÕES`

Uma linha por operação: **Data · Tipo de operação · NIF · Descrição · Valor (sem IVA) · Código IVA · Pago/recebido por** ("A crédito" ou caixa/banco). Conforme o tipo: artigo e quantidade (mercadorias), conta específica (despesas, activos, impostos), referência da operação liquidada (recebimentos e pagamentos). O motor gera os lançamentos na zona automática do Diário (linhas verdes) e a coluna **Estado** indica 🟢 Registada / 🟡 por aprovar / 🔴 erro. Calcula automaticamente: IVA, custo das mercadorias vendidas (custo médio ponderado), INSS (3% + 8%) e IRT pela tabela oficial do exercício. Tipos disponíveis e guia rápido: `11_GUIA_DE_ARRANQUE.md`. Os modelos de lançamento de cada tipo estão em `01A_TABELAS` e são editáveis.

## 4.1 Lançamentos manuais (situações especiais) — `02_DIÁRIO_LANÇAMENTOS`

Cada operação = várias linhas com o **mesmo ID_Lançamento**, Σ Débito = Σ Crédito.

| Campo | Regra prática |
|---|---|
| Conta | Escolha da lista (texto, ex.: `43.1.1`) |
| NIF_Terceiro | Obrigatório nas linhas de clientes (31) e fornecedores (32); em documentos emitidos preencha também na 1.ª linha |
| Natureza_Operação | Obrigatória. Nas linhas de caixa/bancos define a linha da DFC |
| Código_Fiscal + Base_Tributável | Obrigatórios nas linhas de IVA (34.5.2, 34.5.3, 34.5.4.x) e retenções; nas vendas isentas, na linha de proveito |
| Ref_Origem_ID | Em recibos, pagamentos e notas de crédito: ID do documento que liquidam — é isto que alimenta o aging |
| Artigo + Quantidade | Nas linhas da classe 2 (entradas +, saídas −) |
| Moeda / Taxa_Câmbio / Valor_Moeda_Origem | Em operações em moeda estrangeira (validação ME × câmbio = Kz) |
| Documento_Suporte, Utilizador, Validado_Por, Data_Inserção | Obrigatórios para rastreabilidade; Validado_Por ≠ Utilizador |

A coluna **Erros_Detectados** explica qualquer problema; o **Estado_Validação** fica 🔴 até ser corrigido.

### Exemplos (ver lançamentos de teste)

| Operação | Linhas |
|---|---|
| Venda a crédito com IVA | D 31.1.1 (NIF) · C 61.1 · C 34.5.3 (IVA_GER, base) · D 71.1 / C 26.1 (custo, artigo, qtd −) |
| Recebimento | D 43.1.1 · C 31.1.1 (Ref_Origem = ID da factura) |
| Compra a crédito | D 26.1 (artigo, qtd +) · D 34.5.2 (IVA_GER, base) · C 32.1.1 (NIF) |
| Salários | D 72.2 · D 72.5 · C 36.1.1 · C 34.3.1 (IRT) · C 34.9.1 (INSS) |
| Apuramento mensal do IVA | natureza `Apuramento de IVA`: D 34.5.3 · C 34.5.2 · C 34.5.4.1 · C 34.5.6 (a pagar) |

## 5. Fecho mensal (33_FECHO_MENSAL)

1. Verifique `99_CONTROLO_SISTEMA` → deve estar 🟢 ou 🟡 apenas com pendências conhecidas.
2. Introduza a contagem física em `05_CAIXA` e o extracto em `06_BANCOS`.
3. Lance a depreciação do mês (10_ACTIVOS indica "Por processar"), acréscimos, diferimentos e o apuramento do IVA.
4. Confirme as tarefas manuais (✔) e coloque **S** + data de fecho. Se houver lançamentos inválidos no mês o período fica **🔴 BLOQUEADO**.
5. Qualquer lançamento inserido/alterado depois da data de fecho num mês encerrado é assinalado.

## 6. Relatórios

| Necessidade | Folha |
|---|---|
| Visão executiva | 29_DASHBOARD_EXECUTIVO |
| Relatório mensal/trimestral/semestral/anual + recomendações | 38_RELATÓRIO_GESTÃO (seleccione tipo e nº) |
| Demonstrações financeiras | 21_BALANÇO, 22_DRE, 23_DFC |
| Balancete de qualquer período | 20_BALANCETE |
| Extracto de conta | 04_RAZÃO |
| Tesouraria 13 semanas | 18_TESOURARIA |
| Cenários e choques (−10/−20/−30% vendas, câmbio, juros) | 17_PLANEAMENTO_FINANCEIRO |
| Investimentos (VAL, TIR, payback, WACC, sensibilidade) | 25_ANÁLISE_DE_INVESTIMENTOS |

## 7. Encerramento do exercício

Com mês de reporte = 12: `37_ENCERRAMENTO_EXERCÍCIO` propõe (i) o apuramento do resultado (classes 6/7 → 88) e (ii) os saldos de abertura do ano seguinte (RL → 81.1). Copie **como valores** para o Diário do novo ficheiro (natureza `Abertura`). **Nunca apague o ficheiro/histórico do ano anterior.**

## 8. Protecção

As folhas estão protegidas **sem palavra-passe** (Rever → Desproteger folha) para permitir adaptação. Numa implementação real, defina palavra-passe e distribua perfis (quem lança ≠ quem valida ≠ quem fecha).

## 9. Capacidade e desempenho

O Diário vem dimensionado para 2 000 linhas. Para mais volume:
- regenerar: `MATRIZ_LINHAS=10000 python src/build.py` (as fórmulas de sequência são O(n); o custo principal são os SUMIFS);
- ou evoluir a fonte de dados para Power Query / Power Pivot (ver `10_ROADMAP_POWER_BI.md`).

## 10. Regenerar a matriz a partir do código

```bash
pip install openpyxl
python src/build.py                 # gera dist/MATRIZ_PRO_MASTER_CONTABILIDADE_ANGOLA.xlsx
python tests/verify.py              # valida (requer LibreOffice Calc)
python src/gen_docs.py              # regenera dicionário, dependências, legislação, casos de teste
```
