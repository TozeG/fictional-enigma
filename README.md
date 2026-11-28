# SIE-AO: Sistema de Inteligência Editorial

Sistema de revisão e produção editorial com agentes de IA especializados que trabalham de forma coordenada, para **Português de Angola** (ortografia de 1945, gramática de referência europeia), construído sobre o **Claude** e integrável com outras plataformas.

## O que faz
Recebe um manuscrito e devolve:
1. o diagnóstico estrutural e a leitura crítica (decisão do autor no Gate G1);
2. os achados de linha **verificáveis**: excerto literal, proposta, fundamento citado e grau de confiança;
3. a auditoria independente desses achados;
4. a versão revista com o registo de cada alteração;
5. o veredicto de provas e o relatório editorial.

## Equipa de agentes
| Agente | Função | Modelo |
|---|---|---|
| `editor-chefe` | Orquestra, arbitra, aplica e reporta | Opus |
| `analista-estrutural` | Estrutura, argumento, narrativa | Opus |
| `leitor-critico` | Experiência do leitor-alvo | Sonnet |
| `revisor-linguistico` | Norma PT-AO: ortografia, gramática, sintaxe | Opus |
| `estilista` | Clareza, concisão e ritmo, sem apagar a voz do autor | Sonnet |
| `verificador-factual` | Factos, números, citações, risco editorial | Opus |
| `normalizador` | Consistência, folha de estilo, referências | Sonnet |
| `auditor-qualidade` | Valida achados, elimina falsos positivos, resolve conflitos | Opus |
| `revisor-provas` | Gralhas e erros introduzidos pela revisão | Sonnet |

## Como usar
```bash
# 1. Verificar o validador
python3 ferramentas/editorial.py validar calibracao/texto-teste.md calibracao/exemplo-achados.json
```
2. No Claude Code: `/revisao-editorial caminho/do/manuscrito.md`

## Documentação
- [Modelos e ferramentas](docs/01-modelos-e-ferramentas.md)
- [Arquitectura técnica](docs/02-arquitectura-tecnica.md)
- [Plano de implementação](docs/03-plano-implementacao.md)
- [Norma PT-AO](normas/norma-pt-ao.md) · [Protocolo de achados](normas/protocolo-achados.md)
