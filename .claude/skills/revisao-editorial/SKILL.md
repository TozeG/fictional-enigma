---
name: revisao-editorial
description: Executa o ciclo completo de revisão e produção editorial do SIE-AO (Português de Angola, ortografia de 1945) sobre um manuscrito, coordenando os agentes especializados com gates de decisão humana. Usar quando o utilizador pedir para rever, editar, preparar para publicação ou diagnosticar um texto, livro, artigo, tese ou relatório.
---

# Revisão Editorial SIE-AO

Argumento: caminho do manuscrito (`.md` ou `.txt`; `.docx` converte-se primeiro com `pandoc -t gfm`).

## Passo 0: Preparação
1. Se não existir `projectos/<obra>/`, copia `projectos/_modelo/` e coloca o manuscrito em `original/`.
2. Lê `CLAUDE.md`, `normas/norma-pt-ao.md` e `normas/protocolo-achados.md`.
3. Preenche o `brief.md` com o utilizador. Sem tipo de obra, público, nível de intervenção e norma não se avança. Quando o utilizador disser «avance», usa os valores por defeito do modelo e declara-os.

## Passo 1: Macro (em paralelo)
Lança `analista-estrutural` e `leitor-critico` sobre a obra completa.
→ **Gate G1:** apresenta só as decisões estruturais, com opções. Espera pela resposta.

## Passo 2: Micro (em paralelo, por segmento)
Para cada segmento, lança `revisor-linguistico`, `estilista`, `verificador-factual` (só em não ficção ou com dados) e `normalizador`. Cada um grava `achados/<agente>-<segmento>.json`.

## Passo 3: Consolidação e auditoria
```bash
python3 -c "import json,glob; a=[x for f in sorted(glob.glob('projectos/<obra>/achados/*-*.json')) for x in json.load(open(f))]; json.dump(a, open('projectos/<obra>/achados/consolidado.json','w'), ensure_ascii=False, indent=1)"
python3 ferramentas/editorial.py validar projectos/<obra>/original/<ficheiro> projectos/<obra>/achados/consolidado.json
```
Lança depois `auditor-qualidade`. Se o veredicto for DEVOLVER, reenvia ao agente indicado com o padrão de erro e repete o passo. No máximo há 2 ciclos. A partir daí, o achado passa a `consulta-autor`.

## Passo 4: Gate G2
Apresenta ao autor:
- uma tabela-resumo por severidade e tipo;
- os achados `obrigatoria` e `critica`/`alta` um a um (excerto → proposta → fundamento);
- os `recomendada` agrupados;
- os `opcional` só como contagem, que o autor pode abrir se quiser.

## Passo 5: Aplicação e provas
O `editor-chefe` aplica os aceites e grava `versoes/vN.md` e `relatorios/registo-alteracoes.md`. Depois o `revisor-provas` corre sobre a versão final e o `editor-chefe` escreve `relatorios/relatorio-editorial.md`.

## Critério de conclusão
O script valida sem erros, o auditor dá APROVADO, o revisor de provas dá APTO e existe registo de todas as alterações. Se algum destes faltar, diz ao utilizador exactamente qual e porquê.
