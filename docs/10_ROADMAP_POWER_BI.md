# 10 — Evolução: Excel → Power Query → Power Pivot → Power BI → ERP/API

A matriz foi desenhada para esta evolução: uma tabela de factos (`tbl_Diario`) e tabelas de dimensão (`tbl_PlanoContas`, `tbl_Terceiros`, `tbl_Activos`, tabelas de 01A) já existem como **Tabelas Excel** nomeadas.

## Fase 1 — Power Query (volume > 2 000 linhas, múltiplas fontes)

Carregar o Diário (ou exportações do ERP/software de facturação) e limpar:

```m
let
    Origem = Excel.CurrentWorkbook(){[Name="tbl_Diario"]}[Content],
    Tipos = Table.TransformColumnTypes(Origem, {
        {"ID_Lançamento", Int64.Type}, {"Data", type date}, {"Conta", type text},
        {"Débito", type number}, {"Crédito", type number}, {"NIF_Terceiro", type text},
        {"Natureza_Operação", type text}, {"Código_Fiscal", type text}, {"Base_Tributável", type number}}),
    SoLinhas = Table.SelectRows(Tipos, each [ID_Lançamento] <> null),
    Valor = Table.AddColumn(SoLinhas, "Valor_DC", each ([Débito] ?? 0) - ([Crédito] ?? 0), type number),
    Classe = Table.AddColumn(Valor, "Classe", each Text.Start([Conta], 1), type text)
in
    Classe
```

FIFO por lotes: agrupar entradas por artigo (`Table.Group`) e consumir saídas por ordem de data numa função recursiva — substitui o CMP do kardex quando a política for FIFO.

## Fase 2 — Power Pivot (modelo em estrela)

```
            DimData ─┐
     DimPlanoContas ─┤
       DimTerceiros ─┼── FactLancamentos (tbl_Diario)
        DimProjecto ─┤
    DimNaturezaDFC ──┘
```

Medidas DAX equivalentes às fórmulas da matriz:

```dax
Saldo := SUM ( FactLancamentos[Valor_DC] )
Saldo Acumulado := CALCULATE ( [Saldo], FILTER ( ALL ( DimData ), DimData[Data] <= MAX ( DimData[Data] ) ) )
Proveitos := - CALCULATE ( [Saldo], DimPlanoContas[Classe] = "6", FactLancamentos[Inclui_DR] = 1 )
Custos := - CALCULATE ( [Saldo], DimPlanoContas[Classe] = "7", FactLancamentos[Inclui_DR] = 1 )
Resultado Liquido := - CALCULATE ( [Saldo], DimPlanoContas[Rubrica_DR] <> BLANK (), FactLancamentos[Inclui_DR] = 1 )
EBITDA := [Resultado Operacional] - CALCULATE ( - [Saldo], DimPlanoContas[Rubrica_DR] = "DR07" )
IVA Liquidado := - CALCULATE ( [Saldo], DimPlanoContas[Codigo] = "34.5.3", FactLancamentos[Natureza] <> "Apuramento de IVA" )
Liquidez Geral := DIVIDE ( [Activo Corrente], [Passivo Corrente] )
ROE Anualizado := DIVIDE ( [Resultado Liquido] * 12 / MAX ( DimData[Mes] ), [Capital Proprio] )
```

## Fase 3 — Power BI

Publicar o modelo; páginas equivalentes a 29_DASHBOARD (KPI com semáforos por medidas de limite), 22_DRE (matriz por mês), 18_TESOURARIA, 07_CLIENTES (aging), 26_RISCO. Segurança a nível de linha por centro de custo/projecto.

## Fase 4 — ERP / API / AGT

- Importar documentos do software de facturação validado (ficheiro SAF-T AO ou API) para a tabela de factos — elimina a digitação.
- A comunicação electrónica à AGT continua a ser feita pelo software validado, nunca pela folha de cálculo.
- A matriz mantém-se como camada de controlo, reconciliação e gestão.
