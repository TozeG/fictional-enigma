# Relatório de Auditoria de Qualidade: calibracao-v02 (S01)

- **Manuscrito:** `original/relatorio-leitura-luanda.md` (título e 7 parágrafos)
- **Lote de entrada:** `achados/consolidado.json`, 58 achados de 6 agentes
- **Lote de saída (Gate G2):** `achados/auditado.json`
- **Auditor:** auditor-qualidade · 28 de Novembro de 2026

## 1. Veredicto

**APROVADO** para o Gate G2.

- Taxa de rejeição por falta de mérito: **4 / 58 = 6,9 %**, abaixo do limiar de 15 %.
- Nenhum achado `obrigatoria` inválido ficou por resolver. Os 14 `obrigatoria` do lote foram todos verificados: 10 seguem validados e 4 (NOR-0001, NOR-0003, NOR-0004, NOR-0009) foram fundidos como duplicados de um `obrigatoria` validado.
- Nenhuma variante angolana foi normalizada. *zungueira* e *candongueiros* não foram tocados, a fala «A gente agora lemos juntos» foi preservada e «Iremos reunir-nos» (que está correcto) não foi assinalado.

A aprovação leva **duas reservas**, que se enviam como devolução dirigida, sem bloquear o lote:
1. **estilista:** 3 rejeições em 7 achados (43 %). Padrão descrito no §5.
2. **leitor-critico e normalizador:** sobreposição de âmbito muito alta (80 % e 78 % dos achados eram duplicados). Ver §5.

> **Nota sobre a métrica.** O campo `estado` regista como `rejeitado-auditor` tanto os falsos positivos como os duplicados fundidos (32 / 58 no total). O veredicto conta apenas as rejeições por mérito. O duplicado de um achado correcto não é um erro de juízo, é uma sobreposição de âmbito, e por isso é medido à parte (§2) e tratado como problema de coordenação.

## 2. Métricas por agente

| Agente | Total | Validados | Rejeitados por mérito | Fundidos (duplicados) | Taxa de rejeição por mérito | Taxa de duplicação |
|---|---:|---:|---:|---:|---:|---:|
| analista-estrutural (EST) | 11 | 6 | 0 | 5 | 0 % | 45 % |
| estilista (ESTL) | 7 | 2 | 3 | 2 | **43 %** | 29 % |
| leitor-critico (LEI) | 15 | 2 | 1 | 12 | 7 % | **80 %** |
| normalizador (NOR) | 9 | 2 | 0 | 7 | 0 % | **78 %** |
| revisor-linguistico (LIN) | 8 | 8 | 0 | 0 | 0 % | 0 % |
| verificador-factual (FAC) | 8 | 6 | 0 | 2 | 0 % | 25 % |
| **Total** | **58** | **26** | **4** | **28** | **6,9 %** | 48 % |

Por tipo de intervenção, os 26 achados validados repartem-se assim: `obrigatoria` 10, `recomendada` 6, `opcional` 1 e `consulta-autor` 9.

**Validação mecânica.** `editorial.py validar` sobre o consolidado e sobre o auditado deu VÁLIDO, com 0 erros e 0 avisos. Os 12 conflitos continuam a aparecer na saída do script porque o script não lê o campo `estado`. Estão todos resolvidos no §3.

**Validação substantiva.** Revi 58 / 58 achados (100 %, acima da amostra mínima de 30 %). Corrigi duas localizações erradas (FAC-0002: §7 → §6; FAC-0008: §8 → §7) e registei a correcção na `nota`. Nenhum `excerto` foi alterado.

## 3. Conflitos assinalados pelo script e decisões

| # | Excerto | Ids | Natureza | Decisão |
|---|---|---|---|---|
| 1 | «o projecto demonstra … sem dificuldades» | EST-0001, LEI-0013 (+ NOR-0007, FAC-0007) | Duplicado: contradição entre a conclusão e o corpo | Mantém-se **EST-0001** (`consulta-autor`, crítica, com opções). As alternativas de FAC-0007 e LEI-0013 passam para a nota. Precedência: coerência/facto; a redacção cabe ao autor. |
| 2 | «o que representa um aumento de 15%» | EST-0003, ESTL-0003, LEI-0009, FAC-0001 (+ NOR-0004) | Duplicado: pontos percentuais e variação relativa | Mantém-se **FAC-0001** (`obrigatoria`, cálculo verificado). Precedência: exactidão factual. |
| 3 | «ou seja, cerca de metade do previsto» | EST-0004, ESTL-0004, LEI-0012, FAC-0002 (+ NOR-0006) | Conflito real: FAC corrige o número; ESTL-0004 corrige só a repetição e conserva «cerca de metade» | Mantém-se **FAC-0002**. **ESTL-0004 é rejeitado**: exactidão factual prevalece sobre estilo. EST-0004, LEI-0012 e NOR-0006 são fundidos. |
| 4 | «A taxa de leitura regular subiu de 20% para 35%» | EST-0005, LEI-0008, FAC-0006 | Duplicado: indicador sem definição nem método | Mantém-se **EST-0005**, o mais completo (inclui o juízo «Os resultados foram ótimos» e dá opções de método). |
| 5 | «Segundo o director, 85% …» | EST-0006, FAC-0005 (+ LEI-0005, ESTL-0002) | Duplicado: fonte e método do dado; ambiguidade de «o director» | Mantém-se **FAC-0005**, que cobre a fonte e a ambiguidade. |
| 6 | Título | EST-0008, LEI-0001 | Duplicado: estrutura de relatório e título | Mantém-se **EST-0008** (`recomendada`, com opções concretas). |
| 7 | «Os próximos passos incluem a expanção …» | EST-0010, LEI-0014 | Duplicado: expansão sem fundamentação | Mantém-se **EST-0010**. A grafia «expanção» segue em LIN-0007, que trata outra matéria e não conflitua. |
| 8 | «Iremos reunir-nos com o ministério em janeiro de 2025.» | EST-0011, LEI-0015, FAC-0008 | Parcialmente duplicados: voz e destinatário (EST) contra data e actualidade (FAC) | Mantêm-se **EST-0011** e **FAC-0008**, que tratam matérias complementares. LEI-0015 é fundido nos dois. |
| 9 | «iniciou um projeto de leitura em vinte escolas» | LEI-0002, LIN-0001 | Falso conflito: matérias diferentes (grafia e número de escolas) | LIN-0001 é validado. LEI-0002 é fundido em FAC-0003 (número de escolas). |
| 10 | «me disseram que os alunos gostam de ler» | LEI-0004, LIN-0003 | Falso conflito: colocação pronominal e voz enunciativa | LIN-0003 é validado (voz do relator, não discurso directo). LEI-0004 é fundido em EST-0011. |
| 11 | «A biblioteca móvel percorreu as 25 escolas …» | LEI-0006, FAC-0004 (+ EST-0007) | Duplicado: logística implausível | Mantém-se **FAC-0004** (cálculo de 40–50 h). |
| 12 | «as 25 escolas participantes» | NOR-0002, FAC-0003 (+ EST-0002, LEI-0002) | Duplicado: 20 ou 25 escolas | Mantém-se **FAC-0003** (cita os dois excertos). |

**Duplicados não assinalados pelo script** (os excertos diferem mas a correcção é a mesma): NOR-0001 → LIN-0001 (*projecto*); NOR-0003 → LIN-0005 (*óptimos*); NOR-0009 → LIN-0008 (*Janeiro*); LEI-0007 → ESTL-0001 (repetição de «cada sessão»). Nos três primeiros pares fica o achado do revisor linguístico, que cita a fonte primária (AO 1945 e a entrada do DLPC).

**Sobreposições compatíveis, ambas validadas:**
- LIN-0006 (vírgula depois de «Apesar disso») é compatível com a manutenção do conector.
- NOR-0008 (maiúscula em «Ministério da Educação») inclui «Janeiro», que coincide com LIN-0008 sem contradição.

## 4. Rejeições por mérito e tipos de falso positivo

| Id | Motivo | Tipo de falso positivo |
|---|---|---|
| ESTL-0004 | A proposta «cerca de metade desse valor» conserva a imprecisão factual (3/5 = 60 %). | Proposta de estilo que mantém um erro de facto |
| ESTL-0005 | «Apesar disso» tem antecedente lógico válido: concede o problema de financiamento contra o balanço positivo dos §§ 4–5. Trocá-lo por «Porém» é preferência pessoal contra a voz do autor, e a regra invocada («sem relação lógica») é falsa. | Fundamento incorrecto e intervenção na voz do autor |
| ESTL-0006 | «Em suma» é o marcador adequado de uma conclusão. O defeito está no conteúdo (EST-0001), não no conector. | Problema de conteúdo atribuído à forma |
| LEI-0011 | Não propõe intervenção: pede que se preserve um excerto que a norma (§2) já protege. Classificado como `recomendada` sobre discurso directo, pode ser lido no G2 como alteração da fala. O pedido de contexto duplica LEI-0010. | Pseudo-achado («achado de preservação») |

**Tipos de falso positivo no lote:**
1. **Estilo contra facto:** a proposta de estilo ignora a precedência e conserva o erro factual (1 caso).
2. **Erro de forma diagnosticado onde o erro é de conteúdo** (conectores): 2 casos, ambos do estilista.
3. **Pseudo-achados de preservação** classificados com tipo de intervenção activa: 1 caso.
4. **Não houve** normalização de angolanismos, de oralidade em discurso directo nem de ortografia de 1945 para AO90. A armadilha principal do texto foi respeitada por todos os agentes.

**Defeitos menores, sem rejeição:**
- O verificador-factual errou a numeração dos últimos parágrafos em três achados (FAC-0002, FAC-0007, FAC-0008); FAC-0007 cita ainda o «§7» para o financiamento, que está no §6. As localizações dos achados mantidos foram corrigidas.
- NOR-0004 (duplicado) classifica como `facto-verificado` o que é uma regra da norma. A classificação está correcta, mas o achado era redundante.

## 5. Devolução dirigida aos agentes

- **estilista:** em 3 de 7 achados, propôs mudar conectores ou repetições sem verificar se a forma do autor era funcional ou se a proposta preservava erros de outra natureza. Antes de propor, o estilista deve (a) confirmar que o defeito é de forma e não de conteúdo e (b) não propor redacção sobre um excerto em que há erro factual demonstrado. Nesse caso remete para o verificador-factual.
- **leitor-critico:** 12 de 15 achados repetem matérias do analista-estrutural e do verificador-factual (número de escolas, 15 %, 60 %, indicador, fonte do director). A experiência de leitura é útil, mas deve entrar como nota no achado do agente competente e não como achado autónomo com excerto e proposta próprios. Não usar `recomendada` para «achados de preservação».
- **normalizador:** 7 de 9 achados duplicam os do revisor linguístico (*projecto*, *óptimo*, *Janeiro*) ou do verificador-factual (15 %, 60 %, 20/25 escolas, «sem dificuldades»). O âmbito do normalizador é a convenção tipográfica e a consistência de forma; a ortografia é do revisor linguístico.
- **analista-estrutural:** 5 duplicados por invasão do âmbito factual (EST-0003, EST-0004, EST-0002, EST-0006, EST-0007). Os próprios achados o reconhecem nas notas. É preferível remeter em nota do que criar achado.
- **verificador-factual:** confirmar a numeração de parágrafos contra o manuscrito antes de entregar.
- **revisor-linguistico:** sem reparos.

## 6. Achados validados para o G2 (26)

- **Obrigatórias (10):** LIN-0001 (*projecto*), LIN-0002 (*Houve*), LIN-0003 (*disseram-me*), LIN-0004 (*às sessões*), LIN-0005 (*óptimos*), LIN-0007 (*expansão*), LIN-0008 (*Janeiro*), NOR-0005 (*5 000 000 Kz*), FAC-0001 (*15 pontos percentuais*), FAC-0002 (*60 % do previsto*).
- **Recomendadas (6):** LIN-0006, NOR-0008, EST-0008, ESTL-0001, LEI-0003, LEI-0010.
- **Opcional (1):** ESTL-0007.
- **Consulta ao autor (9):** EST-0001, EST-0005, EST-0009, EST-0010, EST-0011, FAC-0003, FAC-0004, FAC-0005, FAC-0008.

## 7. Contagem verificada

Contagem feita por script sobre `auditado.json`:
- 26 validados e 32 `rejeitado-auditor` (28 fundidos e 4 por mérito).
- `obrigatoria` no lote: 14 (LIN 7, NOR 5, FAC 2). Validados: 10. Fundidos: 4 (NOR-0001, NOR-0003, NOR-0004, NOR-0009). Inválidos: 0.
- Validação final: `python3 ferramentas/editorial.py validar original/relatorio-leitura-luanda.md achados/auditado.json` → VÁLIDO (0 erros, 0 avisos; os 12 conflitos listados estão resolvidos no §3).
