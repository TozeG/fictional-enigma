# 1. Modelos, Agentes e Ferramentas para Escrita e Revisão

> **Aviso de evidência.** Não existe, que eu conheça, nenhum *benchmark* público e independente de revisão editorial em **português de Angola**. As recomendações abaixo são uma **interpretação** baseada no perfil de capacidades de cada ferramenta, não um resultado medido. A evidência real para o seu caso é produzida pelo kit de calibração (`calibracao/`), que mede a cobertura de erros e os falsos positivos. As versões de modelos mudam depressa e devem ser reconfirmadas antes de cada actualização do sistema (data desta versão: 28 de Novembro de 2026).

## 1.1 Modelos de linguagem (plataforma principal: Claude)

| Modelo | Perfil | Papel no SIE-AO | Justificação |
|---|---|---|---|
| **Claude Opus 5.5** | Raciocínio profundo, textos longos, julgamento fino | Editor-chefe, analista estrutural, revisor linguístico, verificador factual, auditor | São as funções onde um erro custa mais: arbitragem, norma e factos. |
| **Claude Sonnet 5.5** | Boa relação qualidade/custo/velocidade | Estilista, normalizador, leitor crítico, revisor de provas | Tarefas volumosas e repetitivas, com regras explícitas. |
| **Claude Haiku 5.5** | Rápido e económico | Pré-processamento: segmentação, extracção de números e citações, triagem | Operações mecânicas em lote. |
| **Claude Fable 5.2** | Sem dados verificados meus sobre o desempenho em revisão | A avaliar | Incluir no teste de calibração antes de lhe atribuir um papel. |

**Modelos de outras plataformas** (famílias GPT da OpenAI e Gemini da Google) podem servir como **segunda opinião independente** nos achados `critica`. Modelos diferentes tendem a errar de formas diferentes, o que ajuda a reduzir erros correlacionados. Não lhes atribuo versão nem posição relativa porque não as verifiquei. O critério de inclusão é o mesmo: passar no kit de calibração.

## 1.2 Ferramentas especializadas (não-LLM)

As ferramentas determinísticas complementam os LLM. Dão o mesmo resultado sempre e não "alucinam" regras.

| Ferramenta | Função | Integração | Estado da verificação |
|---|---|---|---|
| **LanguageTool** | Gramática e ortografia por regras | API HTTP ou servidor local (Docker), com o código de língua `pt-AO` | **Verificado:** suporta a variante «Portuguese (Angola preAO)». |
| **Priberam FLiP** | Corrector e dicionário de português europeu | Manual ou suplemento de Word | Confirmar a opção pré-AO na versão licenciada. |
| **Zotero** + **Crossref API** | Gestão de referências; validação de DOI | Exportação CSL-JSON; consulta `api.crossref.org/works/<DOI>` | Funcionalidade padrão. |
| **Pandoc** | Conversão `.docx` ↔ `.md` sem perder estrutura | Linha de comandos | Funcionalidade padrão. |
| **Git** | Versionamento, diferenças entre versões e auditoria das alterações | Este repositório | Em uso. |
| **Turnitin / iThenticate** | Originalidade e plágio (académico) | Licença institucional | Fora do âmbito dos LLM. |

**Não recomendado:** os detectores de "texto gerado por IA" como evidência. As taxas de erro são documentadamente elevadas e podem prejudicar autores injustamente.

## 1.3 Ferramentas de agentes já disponíveis nesta conta

O ambiente tem plugins de escrita instalados. Avaliei-os pela descrição e **não** os testei em PT-AO:

- **apodictic** (auditoria de manuscrito, copidesque, coach de revisão) e **ghost-writer** (escrita longa com perfil de voz): podem ser úteis para a escrita assistida do autor, uma fase anterior a este sistema. Os prompts estão orientados para inglês.
- **matematic-humanizer: humanizer-pt**: aplicável ao estilo, mas é preciso confirmar se respeita o português europeu e a grafia pré-AO.
- **Google Docs / Drive / Notion** (conectores MCP): ler manuscritos e devolver versões revistas sem copiar e colar à mão.

**Recomendação:** o SIE-AO não depende de nenhum destes. Todos os agentes vivem neste repositório, em português e sob uma só norma, o que garante coerência e controlo.

## 1.4 Critérios de selecção usados

1. **Exactidão normativa em PT-AO pré-AO**: o critério eliminatório.
2. **Taxa de falsos positivos**, sobretudo a normalização indevida de angolanismos: eliminatório.
3. Verificabilidade da saída, ou seja, se o modelo consegue citar o excerto literal e o fundamento.
4. Custo por 10 000 palavras revistas.
5. Capacidade de contexto longo, para manter a coerência numa obra inteira.
