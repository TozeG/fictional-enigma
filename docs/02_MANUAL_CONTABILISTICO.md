# 02 — Manual Contabilístico

> Base: Plano Geral de Contabilidade (PGC) aprovado pelo **Decreto n.º 82/01**. Nem todas as entidades angolanas usam exactamente este plano (entidades sob IFRS, planos sectoriais do BNA ou da ARSEG). A arquitectura permite substituir o plano sem destruir os mapas.

## 1. Estrutura do plano

| Classe | Conteúdo | Tratamento no modelo |
|---|---|---|
| 1 | Meios fixos e investimentos | Balanço (activo não corrente); 18 = amortizações acumuladas (subtraem à rubrica) |
| 2 | Existências | Balanço; movimentos com artigo/quantidade alimentam o kardex |
| 3 | Terceiros | Balanço; rubrica depende do **sinal do saldo** (ex.: cliente credor → outros passivos) |
| 4 | Meios monetários | Balanço; 43 e 45 = caixa e equivalentes para a DFC (parametrizável); 42 = aplicação (investimento) |
| 5 | Capital e reservas | Capital próprio |
| 6 | Proveitos por natureza | DR (rubricas DR01–DR03, DR09, DR11) |
| 7 | Custos por natureza | DR (DR04–DR08, DR10, DR12) |
| 8 | Resultados | 81 transitados; 82–86 apuramento; 87 imposto (DR13); 88 RL |

Hierarquia: Classe → Conta → Subconta → Sub-subconta → Analítica. As contas de **Agregação** somam as filhas; lançar numa agregação é erro.

Subcontas analíticas incluídas (ex.: 34.5.1–34.5.8 do IVA, 34.1.1/34.1.2, 37.4.1) são **sugestões** do modelo — validar com o plano da entidade e com a regulamentação do IVA que criou as contas 34.5.x.

## 2. Regra de construção do Balanço

Cada conta de movimento tem duas rubricas: uma usada se o saldo for **devedor**, outra se for **credor**.

- Activo: `Σ saldos devedores com rubrica X − Σ saldos credores com rubrica X`
- Capital próprio / Passivo: `Σ saldos credores com rubrica X − Σ saldos devedores com rubrica X`

Assim, um descoberto bancário (43 credor) aparece automaticamente em "Empréstimos de curto prazo", e o Estado aparece no activo ou no passivo conforme o saldo. **Teste automático: Activo = Capital próprio + Passivo.**

As contas das classes 6, 7 e 82–89 estão mapeadas para "Resultado líquido do exercício" — o Balanço fecha antes e depois do apuramento.

## 3. Demonstração de Resultados

- Por natureza, com proveitos positivos e custos negativos.
- Colunas: 12 meses, 4 trimestres, 2 semestres, acumulado até ao mês de reporte e ano.
- Lançamentos com natureza `Apuramento de resultados` / `Encerramento` são excluídos (para a DR não se anular após o apuramento).
- EBITDA = Resultado operacional − amortizações (DR07).

## 4. Demonstração dos Fluxos de Caixa (método directo)

A linha da DFC é determinada pela **natureza da operação** registada na linha de meios monetários (43/45):

| Natureza | Actividade | Linha |
|---|---|---|
| Venda / Recebimento de cliente | Operacional | Recebimentos de clientes |
| Compra / Pagamento a fornecedor | Operacional | Pagamentos a fornecedores |
| Pagamento ao pessoal | Operacional | Pagamentos ao pessoal |
| Pagamento de impostos | Operacional | Pagamentos/recebimentos de impostos |
| Aquisição / Alienação de imobilizado | Investimento | Pagamentos / recebimentos de imobilizações |
| Investimento financeiro | Investimento | Aplicações e investimentos financeiros |
| Empréstimo obtido / Reembolso | Financiamento | Empréstimos obtidos / reembolsos |
| Juros pagos | Financiamento (opção de política) | Juros pagos |
| Aumento de capital / Dividendos | Financiamento | — |
| Transferência interna | Excluído | (deve somar zero) |

Controlo: saldo inicial + fluxos = saldo final das contas 43/45 (prova em `99_CONTROLO_SISTEMA`).

## 5. Auxiliares e reconciliações

| Auxiliar | Chave | Reconciliação |
|---|---|---|
| Clientes / Fornecedores | Documento de origem (ID) + `Ref_Origem_ID` nas liquidações | Σ partidas em aberto = saldo da conta 31/32 |
| Caixa | Conta 45 | Contabilístico vs contagem física |
| Bancos | Cada conta 43 | Contabilístico vs extracto ajustado (trânsito, cheques, despesas, juros) |
| Inventário | Artigo | Σ valor por artigo = saldo da classe 2; saídas = CMP móvel (kardex) |
| Activos | Registo | Bruto vs 11/12/14; acumulada vs 18; exercício vs 73 |
| IVA | Contas 34.5 | Apuramento acumulado − pagamentos = saldo 34.5 |

## 6. Inventários — custo médio ponderado

O kardex (09_INVENTÁRIOS) recalcula, movimento a movimento, a quantidade, o valor e o CMP; cada saída lançada é comparada com `quantidade × CMP anterior` (tolerância `CFG_Tol`). Exemplo do teste: após a compra de 500 un a 1 100 Kz, CMP = 1 190 000 / 1 140 = 1 043,86 → saída de 100 un = 104 386 Kz.

FIFO: seleccionável como política mas **não implementado em fórmulas** (exige ordenação por lotes); previsto na camada Power Query.

## 7. Acréscimos e diferimentos

- Custos a reconhecer em períodos futuros → 37.4 (activo), reconhecidos mensalmente (natureza `Diferimento`).
- Custos incorridos não facturados → 37.5 (natureza `Acréscimo`).
- Adiantamentos de clientes / proveitos diferidos → 37.6.

## 8. Encerramento do exercício

1. Mês de reporte = 12; todos os meses encerrados sem erros.
2. `37_ENCERRAMENTO_EXERCÍCIO` gera: encerramento das contas de resultados contra 88; abertura das contas de balanço; RL → 81.1 (aplicação a deliberar em Assembleia Geral).
3. Copiar os lançamentos propostos **como valores**; controlo de diferenças automático (Σ D = Σ C).
4. O ficheiro do ano anterior é mantido intacto (histórico).

## 9. Limitações conhecidas

- Um documento de conta corrente deve ter **uma** linha na conta 31/32 (a chave do auxiliar é o ID).
- Os mapas trabalham com um exercício por ficheiro (os dados de outros anos são ignorados pelos filtros, não apagados).
- Consolidação de contas, contabilidade analítica (classe 9) e diferenças de câmbio não realizadas de fim de período (actualização cambial de saldos) não estão automatizadas — lançam-se manualmente.
