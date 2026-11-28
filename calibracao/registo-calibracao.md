# Registo de Calibração (v0.2)

Critério da v0.2: cobertura ≥ 80 % e 0 armadilhas violadas no lote que chega ao autor, em **3 execuções seguidas**.

## Execução 1: 28 de Novembro de 2026

**Condições:** teste cego. Os agentes não tinham acesso a `calibracao/` e o manuscrito foi renomeado. Gabarito v1.0. Fase macro e micro em paralelo, auditoria depois.

| Fase | Achados | Observação |
|---|---|---|
| Especialistas (6 agentes) | 58 | Todos válidos no validador (0 erros) |
| Depois do auditor | 26 validados / 32 rejeitados (28 duplicados + 4 por mérito) | Veredicto: APROVADO, com reserva de coordenação |

| Medida | Resultado | Meta |
|---|---|---|
| Cobertura (lote validado) | **16/16 (100 %)** | ≥ 80 % |
| Armadilhas violadas (lote validado) | **0** | 0 |
| Rejeição por mérito | 4/58 (6,9 %) | < 15 % |
| Duplicação | 28/58 (48 %) | sem meta na v1.0; a meta é < 20 % na execução 2 |

**Resultado: APROVADA (1 de 3).**

### Defeitos do instrumento encontrados e corrigidos
1. G16 só aceitava uma das duas pontas da incoerência temporal. → Gabarito v1.1 com `chaves` alternativas e `requer_tipo`.
2. O avaliador contava os achados de *preservação* como correcções (LEI-0011). → Convenção `categoria: "preservacao"` (protocolo §4) e avaliação só do lote não rejeitado.
3. O validador listava conflitos já resolvidos pelo auditor. → Passa a respeitar o `estado`.

*Ressalva de rigor:* as correcções 1 e 2 foram feitas depois de ver os resultados. O resultado bruto, com o gabarito v1.0 e os 58 achados, foi de 15/16 e 1 falso alarme. As execuções 2 e 3 correm com o gabarito v1.1 já fixado, o que elimina esse viés.

### Defeitos dos agentes e correcções às instruções
| Agente | Problema observado | Correcção |
|---|---|---|
| leitor-critico | 80 % de duplicação: invade números e estrutura | Achados JSON só sobre a experiência do leitor-alvo |
| normalizador | 78 % de duplicação: invade a ortografia de 1945 | Âmbito limitado à forma uniforme |
| analista-estrutural | 45 % de duplicação em cálculos | Números só quando quebram o argumento |
| estilista | 43 % de rejeição por mérito; uma reescrita conservava o erro «cerca de metade» | Proibido reformular frases com erro factual ou normativo |
| verificador-factual | Numeração de parágrafos trocada em 3 achados | Regra de contagem no `CLAUDE.md` §3-A |
| todos | Sobreposição de âmbito | Tabela «um problema, um dono» (`CLAUDE.md` §3-A) |

## Execução 2: pendente
## Execução 3: pendente
