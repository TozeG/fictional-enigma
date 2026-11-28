# SIE-AO — Sistema de Inteligência Editorial (Português de Angola)

Este repositório é um sistema de revisão e produção editorial com agentes especializados que trabalham de forma coordenada. Qualquer sessão do Claude Code aberta aqui deve cumprir estas regras.

## 1. Norma linguística (vinculativa)

- **Padrão:** Português de Angola, com referência à norma europeia.
- **Ortografia:** norma de 1945, a grafia pré-Acordo de 1990 (*acção, direcção, óptimo, projecto, Janeiro, hei-de*). Angola assinou o AO90 mas não o ratificou. Se o cliente pedir AO90, isso fica registado no `brief.md` da obra e prevalece.
- **Referência completa:** `normas/norma-pt-ao.md`. Nenhum agente pode "corrigir" uma variante angolana legítima para a forma europeia ou brasileira.

## 2. Princípio de evidência (vinculativo)

Todo achado segue `normas/protocolo-achados.md` e o esquema `normas/esquema-achados.json`:

1. **Excerto literal** copiado do texto, sem paráfrase.
2. **Fundamento**: a regra, a fonte e o tipo de evidência (facto normativo, interpretação ou preferência de estilo).
3. **Tipo de intervenção**: `obrigatoria` (erro face à norma), `recomendada`, `opcional` (estilo) ou `consulta-autor`.
4. **Confiança** declarada. Sem fonte não há achado `obrigatoria`.

Antes de entregar ao autor, todos os achados passam por `python3 ferramentas/editorial.py validar`.

## 3. Precedência em conflitos

Quando dois agentes divergem sobre o mesmo excerto, decide-se por esta ordem:
**norma > exactidão factual > clareza > coerência interna > estilo**.
A voz do autor e a variação angolana legítima só cedem perante erro normativo ou factual demonstrado.

## 4. Decisões humanas

- **G1:** o autor aprova as alterações estruturais.
- **G2:** o autor aceita ou rejeita os achados.

Nenhum agente aplica alterações estruturais ou de conteúdo sem aprovação. Correcções `obrigatoria` com confiança alta podem ser pré-aplicadas, sempre com registo.

## 5. Organização de uma obra

`projectos/<obra>/` contém `brief.md`, `folha-de-estilo.md`, `original/`, `achados/`, `versoes/` e `relatorios/`. O ponto de partida é a cópia de `projectos/_modelo/`.

## 6. Comando principal

`/revisao-editorial <caminho-do-manuscrito>` executa o fluxo completo descrito em `docs/02-arquitectura-tecnica.md`.
