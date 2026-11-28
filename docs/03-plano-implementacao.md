# 3. Plano de Implementação

## 3.1 Roteiro por versões

| Versão | Duração indicativa | Entregáveis | Critério de aceitação (verificável) |
|---|---|---|---|
| **v0.1: Fundação** *(feito neste repositório)* | — | Norma PT-AO, protocolo de achados, 9 agentes, comando `/revisao-editorial`, validador, kit de calibração | `editorial.py` rejeita os 3 achados defeituosos do exemplo ✔ |
| **v0.2: Calibração** *(concluída, 28 de Novembro de 2026)* | — | 3 execuções, instruções ajustadas. Ver `calibracao/registo-calibracao.md` | 16/16 e 0 armadilhas nas 3 execuções ✔; duplicação de 48 % → 8,3 % |
| **v0.3: Piloto real** *(em curso: aguarda G1/G2 do autor)* | 28 de Novembro de 2026 → | Livro de ≈ 37 000 palavras: macro na obra completa, micro em 6400 palavras. 95 achados, 86 validados; rejeição por mérito 4,2 %; duplicação 5,3 %; 0 excertos não literais. Projecto mantido fora do Git por confidencialidade | — |
| *(critério original v0.3)* | Semanas 2 e 3 | Um capítulo ou artigo real (5000 a 10 000 palavras) com revisão humana paralela | Taxa de aceitação dos achados pelo autor ≥ 70 %; rejeição pelo auditor < 15 %; nenhum angolanismo alterado indevidamente |
| **v0.4: Integrações** | Semana 4 | LanguageTool `pt-AO` (servidor local), Pandoc `.docx`, Crossref | Pipeline `.docx → revisão → .docx` sem perda de estilos; DOI validados automaticamente |
| **v1.0: Operação** | Mês 2 | Primeira obra completa; folha de estilo madura; métricas por obra | Revisor de provas dá APTO; registo de alterações a 100 %; tempo e custo medidos |
| **v1.x: Especialização** | Contínuo | Perfis por género (académico, literário, institucional, jornalístico); calibração alargada (50 ou mais erros por género) | Métricas por género estáveis ou a melhorar |
| **v2.0: Escala** | Quando houver volume | Agent SDK/API, fila de obras, painel de métricas, segunda opinião de outro modelo | Definir quando o volume o justificar |

## 3.2 Primeiros passos práticos (hoje)

1. Abrir este repositório no Claude Code.
2. Testar o validador:
   ```bash
   python3 ferramentas/editorial.py validar calibracao/texto-teste.md calibracao/exemplo-achados.json
   ```
3. Correr a calibração: `/revisao-editorial calibracao/texto-teste.md` (responder «avance» ao brief). Depois avaliar o resultado:
   ```bash
   python3 ferramentas/editorial.py avaliar projectos/<obra>/achados/consolidado.json calibracao/gabarito.json
   ```
4. Ajustar as instruções do agente que falhar e repetir até cumprir o critério da v0.2.

## 3.3 Métricas de qualidade

| Métrica | Fórmula | Meta |
|---|---|---|
| Cobertura (recall) | erros semeados detectados ÷ total semeado | ≥ 80 % (v0.2), ≥ 90 % (v1.x) |
| Falsos positivos críticos | armadilhas "corrigidas" | 0 |
| Precisão percebida | achados aceites pelo autor ÷ achados apresentados | ≥ 70 % |
| Rejeição pelo auditor | rejeitados ÷ propostos, por agente | < 15 % |
| Rastreabilidade | alterações com id de achado ÷ alterações totais | 100 % |

## 3.4 Matriz de riscos

| Risco | Prob. | Impacto | Mitigação |
|---|---|---|---|
| Regras ou fontes inventadas pelo modelo | Média | Alto | Fonte obrigatória para `obrigatoria`; auditor; proibição explícita |
| "Europeização" ou "brasileirização" de angolanismos | Média | Alto | Tripla classificação; armadilhas na calibração; auditor focado |
| Perda da voz do autor | Média | Alto | Perfil de voz no estilista; reescritas só como `consulta-autor`; G2 |
| Grafia AO90 introduzida por hábito do modelo | Alta | Médio | Tabela de contrastes na norma; LanguageTool `pt-AO`; gabarito |
| Fuga de manuscrito confidencial | Baixa | Alto | Autorização no brief; LanguageTool local; sem serviços externos por defeito |
| Custo elevado em obras longas | Média | Médio | Sonnet e Haiku nas tarefas volumosas; Opus só onde o erro custa mais |
| Mudança de estatuto do AO90 em Angola | Baixa | Médio | Reconfirmar anualmente; a norma de projecto já é parametrizável no brief |
| Dependência de uma só plataforma | Baixa | Médio | Agentes em Markdown simples, portáveis para qualquer API |

## 3.5 Responsabilidades (RACI simplificada)

| Actividade | Autor | Editor humano | Editor-chefe (IA) | Especialistas (IA) | Auditor (IA) |
|---|---|---|---|---|---|
| Brief | A | R | C | — | — |
| Decisões estruturais (G1) | **A** | C | R | C | — |
| Produção de achados | — | I | A | **R** | — |
| Validação de achados | — | C | A | — | **R** |
| Aceitação (G2) | **A** | R | C | — | I |
| Aprovação final para publicação | **A** | **R** | C | — | C |

R = executa · A = decide e responde · C = consultado · I = informado
