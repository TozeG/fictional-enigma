# Auditoria de qualidade: S01 «Relatório: A Leitura nas Escolas de Luanda»

- **Lote:** `achados/consolidado.json` (36 achados, 6 agentes). **Saída:** `achados/auditado.json`.
- **Cobertura:** foram revistos os 36 achados (100 %): os 10 `obrigatoria` e os 26 restantes, acima do mínimo de 30 %.
- **Resultado:** 31 `validado` e 5 `rejeitado-auditor` (1 por mérito, 3 duplicados, 1 fora de âmbito).

## 1. Validação mecânica
- O validador encontrou 1 erro. Em **LEI-0003**, o excerto não é literal: o agente «corrigiu» *expanção* para *expansão* dentro do próprio excerto. O achado passou a `rejeitado-auditor` por mérito.
- Os 10 `obrigatoria` (NOR-0001, LIN-0001, LIN-0002, LIN-0003, LIN-0004, LIN-0005, LIN-0010, LIN-0011, FAC-0001, FAC-0002) têm fonte, estatuto factual e confiança alta. **Nenhum `obrigatoria` é inválido.**
- Na revalidação de `auditado.json`, o erro de LEI-0003 continua a aparecer. A causa é que `editorial.py validar` só exclui os `rejeitado-auditor` no cálculo de conflitos (linha 107) e não na verificação de excertos (linhas 91-96). Os excertos não podem ser alterados, por isso o erro fica e diz respeito a um achado já rejeitado. Proposta à ferramenta: aplicar o mesmo filtro à verificação de excertos.

## 2. Validação substantiva (pontos relevantes)
- **Ortografia de 1945:** LIN-0001 (*projecto*), LIN-0005 (*óptimos*), LIN-0010 (*expansão*) e LIN-0011 (*Janeiro*) estão correctos. Nenhum agente aplicou o AO90 nem normalizou variação angolana.
- **Gramática:** LIN-0002 (*Houve*), LIN-0003 (ênclise; o *já* está na relativa e não atrai o pronome na principal) e LIN-0004 (*assistiram às*) estão correctos e nenhuma proposta introduz erro novo.
- **Discurso directo e angolanismos:** a fala da zungueira (LIN-0006) e os termos *zungueira* e *candongueiros* (LIN-0007, LIN-0008) foram preservados correctamente.
- **Factual:** os dois cálculos foram refeitos e confirmados. Em FAC-0001, a subida é de 15 p.p., ou 75 % relativos. Em FAC-0002, 3 000 000 / 5 000 000 = 60 %, o que não é «metade». FAC-0003 (20 contra 25 escolas) é uma contradição demonstrada.
- **Ressalvas sem rejeição:** LIN-0009 podia ser `opcional`, porque o próprio fundamento admite que a vírgula é facultativa. A subcategoria de LIN-0010 está imprecisa. FAC-0004 assenta numa leitura possível da frase, mas não na única, e está bem declarado como hipótese.

## 3. Conflitos (precedência: norma > exactidão factual > clareza > coerência > estilo)
| Excerto | Achados | Decisão |
|---|---|---|
| «A taxa de leitura regular subiu de 20% para 35%» | EST-0002 / FAC-0006 | Pela exactidão factual, FAC-0006 fica com a pergunta sobre o método e a fonte do indicador. EST-0002 mantém-se só para o grau das afirmações («demonstra», «ótimos»). São complementares. |
| «Os candongueiros da zona chegaram…» | EST-0007 / LEI-0007 | Não há divergência real (ambos dizem «Preservar»). LEI-0007 é fundido em EST-0007. |
| «Iremos reunir-nos com o ministério» | LEI-0004 / LIN-0012 | São complementares. A maiúscula (LIN-0012, consulta-autor) depende da identificação do ministério (LEI-0004, FAC-0007). Ao aplicar, combinar com LIN-0011. |
| «Uma zungueira do bairro contou» | LEI-0005 / LIN-0007 | Pela norma e pelo brief («sem marca»), LIN-0007 decide o texto: sem itálico. LEI-0005 fica como consulta-autor apenas sobre um glossário (norma §2). |

O validador continua a listar 3 conflitos porque não lê as resoluções. Todos estão decididos nas notas de `auditado.json`.

## 4. Duplicados e âmbito
- **LEI-0001** é duplicado de FAC-0006 (método do indicador).
- **LEI-0006** é duplicado de LIN-0006 (preservação da oralidade).
- **LEI-0007** é duplicado de EST-0007.
- **LEI-0003**, além de ter o excerto inválido, é duplicado substantivo de EST-0003.
- **LEI-0008** está fora de âmbito. O leitor-crítico só produz relatório e consulta-autor (§3-A), e este é um achado opcional de preservação. O conteúdo está correcto e deve ir para `leitura-critica.md`.

## 5. Métricas por agente
| Agente | Achados | Validados | Rejeição por mérito | Duplicação | Fora de âmbito |
|---|---|---|---|---|---|
| analista-estrutural | 7 | 7 | 0 (0 %) | 0 (0 %) | 0 |
| estilista | 1 | 1 | 0 (0 %) | 0 (0 %) | 0 |
| leitor-critico | 8 | 3 | 1 (12,5 %) | 3 (37,5 %); com LEI-0003, 4 (50 %) | 1 |
| normalizador | 1 | 1 | 0 (0 %) | 0 (0 %) | 0 |
| revisor-linguistico | 12 | 12 | 0 (0 %) | 0 (0 %) | 0 |
| verificador-factual | 7 | 7 | 0 (0 %) | 0 (0 %) | 0 |
| **Total** | **36** | **31** | **1 (2,8 %)** | **3 (8,3 %)** | **1 (2,8 %)** |

- **Tipos de falso positivo:** apenas 1, um excerto alterado e não literal (LEI-0003). Não há falsos positivos normativos (variação angolana, oralidade, gerúndio, AO90).
- **Lacunas observadas (não são achados do auditor):** nenhum achado trata a uniformização do formato «vinte» (por extenso) / «25» (em algarismos), que FAC-0003 remete ao normalizador. O estilista produziu um único achado.

## 6. Veredicto: APROVADO COM RESERVA DE COORDENAÇÃO
- A rejeição por mérito é de 2,8 % (abaixo de 15 %) e não há nenhum `obrigatoria` inválido por resolver.
- **Reserva: leitor-critico.** A duplicação estrita é de 37,5 %, mas sobe para 50 % se se contar LEI-0003, que é duplicado substantivo de EST-0003. Juntando a invasão de âmbito de LEI-0008, 5 dos 8 achados (62,5 %) entram no terreno de outros donos. Os problemas invadidos foram:
  - a preservação da oralidade e dos trechos fortes (revisor-linguistico, analista-estrutural);
  - a fundamentação da expansão (analista-estrutural);
  - o método do indicador (verificador-factual).
- **Correcção pedida ao leitor-critico:**
  - criar só achados `consulta-autor` sobre a experiência do leitor e registar os «trunfos» no relatório, não como achados de preservação;
  - nunca alterar o texto dentro do campo `excerto`.
