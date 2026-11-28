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

## Execuções 2 e 3: 28 de Novembro de 2026

**Condições:** gabarito v1.1 fixado antes das execuções. Instruções com as fronteiras de âmbito (`CLAUDE.md` §3-A). Agentes nativos com o modelo definido em cada um. Projectos isolados e teste cego, sem acesso a `calibracao/` nem a outros projectos.

| Medida | Exec. 1 | Exec. 2 | Exec. 3 | Meta |
|---|---|---|---|---|
| Achados brutos | 58 | 33 | 36 | — |
| Validados pelo auditor | 26 | 27 | 31 | — |
| Cobertura (lote validado) | 16/16 | **16/16** | **16/16** | ≥ 80 % |
| Armadilhas violadas | 0 | **0** | **0** | 0 |
| Rejeição por mérito | 6,9 % | **3,0 %** | **2,8 %** | < 15 % |
| Duplicação | 48 % | **15,2 %** | **8,3 %** | < 20 % |
| Veredicto do auditor | Aprovado com reserva | Aprovado com reserva | Aprovado com reserva | — |

**Resultado: v0.2 CONCLUÍDA.** Três execuções seguidas cumprem o critério. As execuções 2 e 3 não dependeram de ajustes posteriores ao gabarito.

### Lições das execuções 2 e 3
1. **Correcção inconsciente do excerto.** O leitor crítico, que não tinha a ferramenta Grep, escreveu «a expansão» quando o original diz «expanção», nas duas execuções. O validador apanhou-o nas duas. → Protocolo §3-A (confirmação literal com Grep) e Grep acrescentado ao agente.
2. **Contradição nas instruções do leitor crítico.** As instruções do agente permitiam preservações, mas o §3-A não. → Harmonizado no `CLAUDE.md` §3-A.
3. **O validador invalidava lotes por achados já rejeitados.** → Os defeitos de achados `rejeitado-auditor` passam a aviso.
4. **Lacuna residual:** a mistura de «vinte» por extenso com «25» em algarismos não teve achado de forma. Só foi tratada como inconsistência factual. Fica para a calibração alargada (v1.x).

### Limites desta calibração (a ter em conta)
- O texto é **curto** (≈330 palavras), **institucional** e tem **16 erros**. A v0.3 (piloto real) e a v1.x (50 ou mais erros por género, incluindo ficção) são necessárias antes de generalizar.
- Os erros semeados foram escritos por quem desenhou o sistema, o que pode favorecer tipos de erro que o sistema já antecipa. O piloto real com revisão humana paralela corrige este viés.
