# 2. Arquitectura Técnica do SIE-AO

## 2.1 Visão geral

```text
                         ┌───────────────────────────┐
   Manuscrito + Brief ──▶│       EDITOR-CHEFE        │◀── decisões do autor (G1, G2)
                         │ (orquestração · arbitragem)│
                         └─────────────┬─────────────┘
              ┌────────────────────────┼─────────────────────────┐
              ▼ FASE MACRO (obra)      │                         │
   ┌────────────────────┐ ┌────────────────────┐                 │
   │ Analista estrutural│ │   Leitor crítico   │                 │
   └─────────┬──────────┘ └─────────┬──────────┘                 │
             └──────────► GATE G1 (autor: estrutura) ◄───────────┘
                                   │
              ▼ FASE MICRO (por segmento, em paralelo)
   ┌──────────────┐ ┌──────────┐ ┌───────────────┐ ┌─────────────┐
   │Rev. linguíst.│ │ Estilista│ │ Verif. factual│ │ Normalizador│
   └──────┬───────┘ └────┬─────┘ └──────┬────────┘ └──────┬──────┘
          └──────────────┴──────┬───────┴─────────────────┘
                                ▼
            ferramentas/editorial.py validar   (verificação mecânica)
                                ▼
                     AUDITOR DE QUALIDADE      (verificação substantiva,
                                ▼                 conflitos, falsos positivos)
                     GATE G2 (autor: aceita/rejeita)
                                ▼
            Aplicação → versoes/vN.md + registo-alteracoes.md
                                ▼
                     REVISOR DE PROVAS → APTO / NÃO APTO
                                ▼
                     Relatório editorial final
```

## 2.2 Camadas

| Camada | Componentes | Ficheiros |
|---|---|---|
| **Governança** | Norma, protocolo de evidência, precedência, gates | `CLAUDE.md`, `normas/` |
| **Orquestração** | Editor-chefe e skill de fluxo | `.claude/agents/editor-chefe.md`, `.claude/skills/revisao-editorial/` |
| **Especialistas** | 7 agentes de produção de achados | `.claude/agents/*.md` |
| **Controlo** | Validador determinístico, auditor e gabarito de calibração | `ferramentas/editorial.py`, `auditor-qualidade.md`, `calibracao/` |
| **Memória da obra** | Brief, folha de estilo, achados, versões e relatórios | `projectos/<obra>/` |
| **Integração** | LanguageTool pt-AO, Zotero/Crossref, Google Docs, Pandoc | ver §2.6 |

## 2.3 Princípios de desenho (e porquê)

1. **Separação de funções.** Quem produz o achado não o aprova. A autocorrecção de um mesmo modelo é pouco fiável, e um auditor com outro mandato ("procurar o erro do achado") reduz os falsos positivos.
2. **Verificação mecânica antes da semântica.** Tudo o que se pode verificar com código, verifica-se com código: existência do excerto, campos obrigatórios, coerência entre a intervenção e a evidência, conflitos. O LLM fica só para o que exige julgamento.
3. **Excerto literal obrigatório.** Torna cada achado verificável por qualquer pessoa com `Ctrl+F` e impede achados vagos ou inventados.
4. **Tripla classificação erro / variação / estilo.** É a protecção central do português de Angola contra a "europeização" ou "brasileirização" automática do texto.
5. **Humano nos pontos de decisão.** A estrutura (G1) e a aceitação (G2) são sempre do autor. O sistema propõe e o autor decide.
6. **Memória explícita em ficheiros.** A folha de estilo garante consistência entre sessões e entre agentes sem depender da memória do modelo.

## 2.4 Fluxo de dados

1. `original/` → segmentos de 1500 a 3000 palavras (`relatorios/mapa.md`).
2. Cada agente lê o segmento, o `brief.md`, a `folha-de-estilo.md` e as normas, e escreve `achados/<agente>-<seg>.json`.
3. Consolidação → `consolidado.json` → validação → auditoria (cada achado recebe um `estado`).
4. Aceites → patch → `versoes/vN.md`. O Git guarda a diferença `vN-1 → vN`.

## 2.5 Regra de precedência em conflitos
**norma > exactidão factual > clareza > coerência interna > estilo**. Voz do autor e variação angolana só cedem perante erro normativo ou factual demonstrado.

## 2.6 Integração com outras plataformas

| Plataforma | Como integrar | Uso |
|---|---|---|
| **Claude Code** (principal) | Este repositório: agentes em `.claude/agents/` e comando `/revisao-editorial` | Fluxo completo e auditável |
| **Claude.ai (Projectos)** | Criar um Projecto, carregar `CLAUDE.md` e `normas/*` como conhecimento e colar a instrução de um agente como instruções do projecto | Uso individual por agente, sem terminal |
| **Claude API / Agent SDK** | Cada `.md` de agente é um *system prompt*. O orquestrador chama os especialistas e exige saída JSON validada pelo `editorial.py` | Automação em escala ou integração num sistema editorial próprio |
| **LanguageTool (pt-AO)** | `POST /v2/check` com `language=pt-AO`. Os resultados entram como achados `LIN-` com `fundamento.fonte = "LanguageTool regra <id>"` | Primeira passagem determinística, antes do revisor linguístico |
| **Google Docs / Word** | Conector Google Docs (leitura e escrita) ou Pandoc `.docx`↔`.md` | Entrada e saída no formato do autor |
| **Zotero / Crossref** | Exportar CSL-JSON e validar os DOI pela API Crossref | Normalizador bibliográfico |
| **Segundo modelo (GPT, Gemini)** | Revisão independente só dos achados `critica` | Reduzir erros correlacionados |

## 2.7 Segurança e confidencialidade

- Os manuscritos inéditos são confidenciais. Não se enviam para serviços externos (LanguageTool público, outros modelos) sem autorização expressa do autor, registada no `brief.md`. Para obras sensíveis, a alternativa é o servidor LanguageTool local.
- Os achados do verificador factual sobre risco jurídico (difamação, direitos de autor) são **triagem** e não parecer jurídico.
