# Auditoria de qualidade: S01 (Relatório: A Leitura nas Escolas de Luanda)

- Entrada: `achados/consolidado.json` (33 achados, 6 agentes)
- Saída: `achados/auditado.json` (27 `validado`, 6 `rejeitado-auditor`)
- Amostra substantiva: 100 % (os 10 `obrigatoria` e os 23 restantes, acima dos 30 % mínimos)

## 1. Validação mecânica

| Achado | Resultado | Decisão |
|---|---|---|
| LEI-0003 | Excerto não literal: o achado escreve «expansão» e o manuscrito tem «expanção» (o agente corrigiu o texto quando o copiou) | `rejeitado-auditor` (mérito). Era também duplicado de EST-0002 |

Nenhum `obrigatoria` tem a fonte vazia ou um estatuto incompatível.

## 2. Validação substantiva dos `obrigatoria` (10/10 validados)

| Achado | Verificação |
|---|---|
| LIN-0001 projeto → projecto | Grafia de 1945. O próprio texto usa «projecto» nos outros parágrafos |
| LIN-0002 Houveram → Houve | *Haver* existencial é impessoal (norma §4) |
| LIN-0003 me disseram → disseram-me | Está fora do discurso directo e o «que» pertence à relativa intercalada, por isso não atrai o pronome. A vírgula anterior fica correcta |
| LIN-0004 assistiram as → às | *Assistir* no sentido de presenciar rege a preposição *a* |
| LIN-0005 ótimos → óptimos | Grafia de 1945 |
| LIN-0008 expanção → expansão | Erro ortográfico. A forma «expanção» não existe |
| LIN-0009 janeiro → Janeiro | Maiúscula nos meses (1945). O texto tem «Março» no 1.º parágrafo |
| NOR-0001 5.000.000 → 5 000 000 Kz | A folha de estilo fixa o espaço como separador de milhares, e «3 000 000 Kz» aparece no mesmo parágrafo |
| FAC-0001 aumento de 15% → 15 pontos percentuais | 35 − 20 = 15 p.p. e 15/20 = 75 %. A correcção obrigatória é «pontos percentuais»; o parêntese com os 75 % é um acréscimo opcional |
| FAC-0002 cerca de metade → 60% | 3 000 000 / 5 000 000 = 60 %. A conta depende de o valor previsto estar certo |

Nenhuma das propostas introduz um erro novo de concordância ou de pontuação. Nenhuma toca no discurso directo nem nos angolanismos.

## 3. Restantes achados (23/23 revistos)

- Foram validados os achados que se seguem. Estruturais: EST-0001, EST-0002, EST-0004, EST-0005 e EST-0006. De estilo: ESTL-0001 (a proposta mantém a concordância e a enumeração) e ESTL-0003. Do revisor: LIN-0006, LIN-0007 (`recomendada`, vírgula facultativa) e LIN-0010 (`consulta-autor`). Factuais: FAC-0003 a FAC-0007; em FAC-0007 confirmei os 22 meses entre Janeiro de 2025 e Novembro de 2026. Do leitor: LEI-0001 e LEI-0002 (`consulta-autor` sobre a explicação de termos para financiadores estrangeiros, sem alterar o termo nem contrariar o «sem marca» do brief).
- A variação angolana foi respeitada em todo o lote: «a gente lemos» (em discurso directo), «zungueira» e «candongueiros» estão preservados e nenhum achado os normaliza.

## 4. Conflitos

| Excerto | Achados | Decisão |
|---|---|---|
| «A taxa de leitura regular subiu de 20% para 35%» | EST-0003 e FAC-0006 | É o mesmo pedido (definição, instrumento, amostra e datas). Pela precedência, a **exactidão factual** prevalece sobre a coerência: fica FAC-0006 e EST-0003 é fundido nele. A parte própria do analista (moderar a conclusão) passou para a nota de FAC-0006 |
| «Os candongueiros da zona chegaram a transportar caixas de livros sem cobrar.» | EST-0006 e ESTL-0003 | Não há incompatibilidade: os dois achados preservam o trecho, um como evidência estrutural e o outro pelo léxico sem marca. **Ficam os dois.** O validador continua a assinalar o par porque as propostas têm textos diferentes. Esse aviso fica resolvido por esta decisão |

## 5. Duplicados fundidos

| Rejeitado | Mantido | Problema |
|---|---|---|
| EST-0003 (analista-estrutural) | FAC-0006 | Método e fonte da medição |
| ESTL-0002 (estilista) | LIN-0006 | Preservação da concordância em discurso directo |
| LEI-0004 (leitor-critico) | LIN-0006 | Idem |
| LEI-0005 (leitor-critico) | EST-0006 | Preservação do contributo dos candongueiros |
| LEI-0003 (leitor-critico) | EST-0002 | Fundamentação da expansão (já rejeitado por mérito, ver §1) |

Fora de âmbito sem duplicado: LEI-0006. O leitor-critico criou um achado `opcional` de preservação, e a §3-A só lhe permite relatório e `consulta-autor`. A observação já está em `relatorios/leitura-critica.md`, por isso a rejeição não faz perder conteúdo. Este achado não conta para nenhuma das duas taxas.

## 6. Métricas por agente

O LEI-0003 conta nas duas taxas, porque tem os dois defeitos: excerto inválido e problema já tratado pelo dono.

| Agente | Achados | Validados | Rejeição por mérito | Duplicação | Fora de âmbito |
|---|---|---|---|---|---|
| analista-estrutural | 6 | 5 | 0 (0 %) | 1 (16,7 %) | 0 |
| estilista | 3 | 2 | 0 (0 %) | 1 (33,3 %) | 0 |
| leitor-critico | 6 | 2 | 1 (16,7 %) | 3 (50,0 %) | 1 |
| normalizador | 1 | 1 | 0 (0 %) | 0 (0 %) | 0 |
| revisor-linguistico | 10 | 10 | 0 (0 %) | 0 (0 %) | 0 |
| verificador-factual | 7 | 7 | 0 (0 %) | 0 (0 %) | 0 |
| **Lote** | **33** | **27** | **1 (3,0 %)** | **5 (15,2 %)** | **1** |

**Tipos de falso positivo:**
1. Excerto corrigido em vez de copiado (LEI-0003). É o único achado rejeitado por mérito.

**Problemas de coordenação:**
1. Preservação do mesmo trecho por vários agentes. O discurso directo foi preservado 3 vezes (LIN, ESTL, LEI) e a frase dos candongueiros 3 vezes (EST, ESTL, LEI).
2. Sobreposição entre «evidência insuficiente» (analista) e «fonte e método» (verificador) no mesmo resultado.
3. O leitor-critico criou achados de um tipo que não lhe é permitido (`opcional`).

## 7. Veredicto

**APROVADO COM RESERVA DE COORDENAÇÃO**

- A rejeição por mérito do lote é de 3,0 % (abaixo de 15 %) e não fica por resolver nenhum `obrigatoria` inválido: os 10 foram verificados e validados.
- Reserva: o **leitor-critico** tem 50 % de duplicação e mais um achado fora de âmbito. Invadiu três áreas:
  - a estrutura e o argumento (LEI-0003 repete EST-0002);
  - a preservação de gramática em discurso directo (LEI-0004 repete LIN-0006);
  - os pontos fortes estruturais (LEI-0005 repete EST-0006).

  Instrução: deixar os trechos a preservar e os juízos sobre a estrutura apenas no relatório, criar só achados `consulta-autor` e copiar o excerto sem o corrigir.
- Nota secundária para o analista-estrutural: um pedido de dados de método é do verificador-factual. Basta mencioná-lo em «Fora do meu âmbito».

## 8. Validação final de `auditado.json`

O validador devolve `INVÁLIDO` por um único erro: o excerto de LEI-0003. O script verifica os excertos de todos os achados, incluindo os `rejeitado-auditor`, e o excerto não pode ser alterado. Esse achado está rejeitado e não chega ao autor.

O único conflito que resta (EST-0006 e ESTL-0003) foi decidido na §4.

Sugere-se que `ferramentas/editorial.py` passe a ignorar os achados `rejeitado-auditor` também na verificação do excerto.
