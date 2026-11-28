# Protocolo de Achados Verificáveis (v1.0)

Um achado é a unidade mínima de trabalho de todos os agentes. Tem de poder ser **verificado por um terceiro sem consultar o agente que o produziu**.

## 1. Campos obrigatórios

```json
{
  "id": "LIN-0007",
  "agente": "revisor-linguistico",
  "categoria": "sintaxe",
  "subcategoria": "colocacao-pronominal",
  "localizacao": {"seccao": "Cap. 2", "paragrafo": 3},
  "excerto": "me disseram que os alunos",
  "proposta": "disseram-me que os alunos",
  "tipo_intervencao": "obrigatoria",
  "severidade": "media",
  "fundamento": {
    "regra": "Ênclise por defeito em texto formal; não há atractor de próclise.",
    "fonte": "Cunha & Cintra, Nova Gramática do Português Contemporâneo — colocação dos pronomes átonos",
    "estatuto": "facto-normativo"
  },
  "confianca": "alta",
  "nota": "Fora do discurso directo. Em fala de personagem seria preservado."
}
```

## 2. Vocabulário controlado

| Campo | Valores |
|---|---|
| `agente` | `analista-estrutural`, `revisor-linguistico`, `estilista`, `verificador-factual`, `normalizador`, `leitor-critico`, `revisor-provas` |
| `tipo_intervencao` | `obrigatoria`, `recomendada`, `opcional`, `consulta-autor` |
| `severidade` | `critica` (compromete sentido, verdade ou risco legal), `alta`, `media`, `baixa` |
| `fundamento.estatuto` | `facto-normativo`, `facto-verificado`, `interpretacao`, `hipotese`, `preferencia-estilo` |
| `confianca` | `alta`, `media`, `baixa` |

Prefixos de `id`: EST (estrutural), LIN (linguístico), ESTL (estilo), FAC (factual), NOR (normalização), LEI (leitor), PRV (provas).

## 3. Regras de validade (verificadas pelo `ferramentas/editorial.py validar`)

1. O `excerto` existe **literalmente** no manuscrito.
2. A `proposta` é diferente do `excerto`. Excepção: `consulta-autor` e achados estruturais podem trazer a proposta em prosa.
3. Um achado `obrigatoria` exige `fundamento.fonte` não vazia e estatuto `facto-normativo` ou `facto-verificado`.
4. Um estatuto `preferencia-estilo` nunca pode ser `obrigatoria`.
5. Os `id` são únicos.
6. Dois agentes com propostas diferentes para o mesmo excerto geram **conflito**, que o auditor resolve pela regra de precedência do `CLAUDE.md`.

### 3-A. Confirmação literal obrigatória

Antes de gravar um achado, confirma o `excerto` com a ferramenta Grep (pesquisa literal) sobre o manuscrito. **Copia o erro tal como está, mesmo quando é gritante.** Na calibração, um agente escreveu «a expansão» onde o original diz «expanção», corrigindo sem dar por isso o texto que devia citar. Um excerto corrigido deixa de ser verificável e esconde o próprio erro.

## 4. Achados de preservação

Quando um agente quer **proteger** um excerto de alterações (um angolanismo, uma fala de personagem, um trecho forte), usa `categoria: "preservacao"`, `tipo_intervencao: "opcional"` e uma `proposta` que começa por «Preservar». Assim, nem os outros agentes nem o avaliador confundem uma protecção com uma correcção.

## 5. Proibições

- Achados vagos («melhorar a fluidez») sem excerto nem proposta.
- Reescrever parágrafos inteiros sob a capa de «correcção». Uma reescrita é `recomendada` ou `consulta-autor`, com justificação.
- Inventar fontes, páginas, estatísticas ou regras.
- Normalizar angolanismos, oralidade em discurso directo ou opções de voz do autor.
