# 11 — Plano de Execução em Paralelo (piloto de 1 mês)

**Objectivo:** provar, com dados reais, que a matriz produz o mesmo balancete que o sistema actual — e que detecta o que o sistema actual não detecta — antes de a usar para reporte oficial.

**Regra de decisão:** a matriz só passa a sistema de reporte quando, num mês completo, (1) todas as contas do balancete coincidem (tolerância 1 Kz) ou as diferenças estão explicadas e documentadas, (2) `99_CONTROLO_SISTEMA` não está BLOQUEADO, e (3) o contabilista certificado valida a parametrização fiscal usada.

## Ferramentas

| Ficheiro | Para quê |
|---|---|
| `dist/MATRIZ_PRO_MASTER_VAZIA.xlsx` | Matriz sem dados fictícios (para lançar directamente no Excel) |
| `dist/MODELO_IMPORTACAO.xlsx` | Modelo para colar a exportação do sistema actual |
| `src/importar.py` | Valida o modelo, gera a matriz com os dados reais e compara com o balancete do sistema actual |

## Calendário (≈ 2 semanas após o fecho do mês piloto)

| Dia | Actividade | Responsável | Entregável |
|---|---|---|---|
| D1 | Escolher o mês piloto (recomendado: o mês mais recente já fechado no sistema actual) | Direcção Financeira | Decisão |
| D1 | Copiar os 12 escalões do IRT 2026 (Lei n.º 14/25, DR de 30/12/2025) para o separador IRT_ESCALOES do modelo | Técnico de contas | Separador preenchido |
| D1–D2 | Mapear o plano de contas actual → PGC da matriz (contas novas no separador PLANO_CONTAS) | Contabilista | Tabela de correspondência |
| D2 | Preencher ENTIDADE e TERCEIROS (exportação de clientes/fornecedores com NIF) | Contabilidade | Modelo |
| D3 | Lançamento de abertura (balanço de fecho do ano anterior, natureza `Abertura`) + lançamentos de Janeiro até ao mês piloto | Contabilidade | Separador LANÇAMENTOS |
| D3 | Colar o balancete do sistema actual (saldo final D−C) em BALANCETE_REFERÊNCIA | Contabilidade | Separador preenchido |
| D4 | `python src/importar.py carregar modelo.xlsx --saida dist/MATRIZ_<ENTIDADE>_<AAAA-MM>.xlsx` | Técnico | Relatório de importação |
| D4–D7 | Corrigir erros bloqueantes na origem e reimportar até ao relatório sem erros | Contabilidade | Relatório "0 erros" |
| D7–D9 | Explicar cada diferença de saldo (tabela do relatório) até ficarem todas 🟢 ou justificadas | Contabilista | Nota de reconciliação |
| D9 | Introduzir extractos bancários (06), contagem de caixa (05), registo de activos (10) | Tesouraria | 99 sem pendências por falta de input |
| D10 | Rever 12_IVA vs declaração entregue; 15_IMPOSTO_INDUSTRIAL; 34_CALENDÁRIO | Técnico de contas | Validação fiscal |
| D10 | Rever 29_DASHBOARD e 38_RELATÓRIO_GESTÃO com a Administração | Direcção Financeira | Parecer de utilidade |
| D11 | Decisão: adoptar / repetir piloto / ajustar | Administração | Acta |

## Como ler o relatório de importação

- **Erros bloqueantes** (🔴): a matriz não é gerada. Os mesmos testes do Diário (equilíbrio, conta, NIF, natureza, suporte, IVA = base × taxa, câmbio, duplicados, referência de origem).
- **Avisos** (🟡): segregação de funções / lançamentos por aprovar — não bloqueiam, mas aparecem no controlo interno.
- **Tabela de paralelo:** saldo da matriz × saldo do sistema actual, por conta (movimento ou agregação). Causas típicas de diferença:
  1. lançamentos em falta ou duplicados na exportação;
  2. contas mapeadas de forma diferente (ex.: IVA numa conta genérica 34);
  3. saldos de abertura diferentes;
  4. arredondamentos e câmbio;
  5. lançamentos de apuramento/encerramento feitos só num dos sistemas.

## Critérios de aceitação

| # | Critério | Onde verificar |
|---|---|---|
| 1 | 0 erros bloqueantes na importação | Relatório de importação |
| 2 | 100% das contas do balancete de referência 🟢 ou justificadas | Relatório de importação |
| 3 | Balanço equilibrado; DR = contas de resultados; DFC = caixa | 99_CONTROLO_SISTEMA |
| 4 | IVA do mês = declaração periódica entregue | 12_IVA |
| 5 | Bancos reconciliados com extracto real | 06_BANCOS |
| 6 | Parametrização fiscal usada validada por técnico de contas | 11_FISCALIDADE_AGT (estado CONFIRMADO) |
| 7 | Tempo de fecho ≤ ao do sistema actual | Registo do piloto |

## Validação automática desta ferramenta

`python tests/test_importar.py` — importa o cenário de teste pelo modelo, com uma diferença deliberada de 2 500 Kz no banco: a matriz gerada reproduz exactamente os valores de referência (RL 1 206 460,50; Activo 13 799 614), o relatório assinala só a conta 43.1.1, e um lançamento desequilibrado bloqueia a importação (12/12 verificações).
