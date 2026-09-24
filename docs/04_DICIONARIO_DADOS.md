# 04 — Dicionário de Dados

Gerado por `src/gen_docs.py` a partir de `src/sheets_base.py` (fonte única).

## 02_DIÁRIO_LANÇAMENTOS — campos de INPUT

| Coluna | Campo | Tipo | Descrição | Validação |
|---|---|---|---|---|
| A | ID_Lançamento | Inteiro | Identificador único do lançamento. Todas as linhas da mesma operação partilham o ID. | Obrigatório; Σ Débito = Σ Crédito por ID. |
| B | Data | Data | Data contabilística do lançamento. | Data válida, dentro do exercício (00_CONFIGURAÇÃO). |
| C | Tipo_Documento | Texto (lista) | Tipo de documento (FT, FR, NC, ND, RC, FC, FRF, NCF, RCF, DU, EXT, FS, DI, DLI, ABE). | Lista 01A_TABELAS. |
| D | Série | Texto | Série do documento. | — |
| E | Nº_Documento | Inteiro | Número do documento na série. | Duplicados detectados (tipo+série+nº+NIF); sequência validada em 13_FACTURAÇÃO_FISCAL. |
| F | Data_Documento | Data | Data do documento de suporte. | — |
| G | Data_Vencimento | Data | Data de vencimento (conta corrente). | Usada no aging e na tesouraria de 13 semanas. |
| H | NIF_Terceiro | Texto (lista) | NIF do terceiro (clientes, fornecedores). | Obrigatório em contas correntes (31/32); formato 10 dígitos (colectivas) ou 14 caracteres (BI); deve existir em 01B_TERCEIROS. |
| I | Conta | Texto (lista) | Conta do PGC (apenas contas de Movimento). | Existe no plano; não pode ser conta de agregação. |
| J | Descrição | Texto | Descrição da linha. | — |
| K | Débito | Número | Valor a débito (Kz). | ≥ 0; exclusivo com Crédito. |
| L | Crédito | Número | Valor a crédito (Kz). | ≥ 0; exclusivo com Débito. |
| M | Centro_Custo | Texto (lista) | Centro de custo. | Lista 01A_TABELAS. |
| N | Centro_Responsabilidade | Texto | Centro de responsabilidade. | — |
| O | Projecto | Texto | Código do projecto (liga a 24_GESTÃO_DE_PROJECTOS). | — |
| P | Fonte_Financiamento | Texto | Fonte de financiamento. | — |
| Q | Natureza_Operação | Texto (lista) | Natureza da operação — determina a classificação na DFC e a inclusão na DR. | Obrigatória; parametrizada em 01A_TABELAS. |
| R | Código_Fiscal | Texto (lista) | Código fiscal (IVA_GER, IVA_ISE, RET_SERV, …). | Obrigatório nas linhas de IVA; taxa × base = valor (tolerância CFG_Tol). |
| S | Base_Tributável | Número | Base tributável associada ao código fiscal. | Usada no mapa de IVA e retenções. |
| T | Ref_Origem_ID | Inteiro | ID do documento de origem liquidado/regularizado (recibos, pagamentos, NC). | Tem de existir no Diário. |
| U | Moeda | Texto (lista) | Moeda da operação (vazio = AOA). | Se ≠ AOA: câmbio e valor em ME obrigatórios. |
| V | Taxa_Câmbio | Número | Taxa de câmbio aplicada. | Valor ME × câmbio = valor em Kz. |
| W | Valor_Moeda_Origem | Número | Valor na moeda de origem. | — |
| X | Forma_Pagamento | Texto (lista) | Forma de pagamento/recebimento. | — |
| Y | Artigo | Texto | Código do artigo (linhas da classe 2). | Alimenta 09_INVENTÁRIOS e o kardex. |
| Z | Quantidade | Número | Quantidade (+ entrada, − saída). | — |
| AA | Documento_Suporte | Texto | Referência do documento de suporte / arquivo. | Obrigatório. |
| AB | Utilizador | Texto | Utilizador que registou. | Rastreabilidade. |
| AC | Validado_Por | Texto | Utilizador que validou. | Diferente do Utilizador (segregação de funções). |
| AD | Data_Inserção | Data | Data de inserção. | Comparada com a data de fecho do mês. |
| AE | Data_Alteração | Data | Data da última alteração. | Alteração após fecho = erro. |
| AF | Estado_Documento | Texto (lista) | Normal / Anulado / Rectificado. | — |
| AG | Hash_AGT | Texto | Hash/assinatura do documento emitido (software validado). | Obrigatório em documentos emitidos. |
| AH | Nº_Certificado_Software | Texto | Nº do certificado/validação do software de facturação. | Obrigatório em documentos emitidos. |
| AI | Estado_Comunicação_AGT | Texto (lista) | Estado da comunicação electrónica à AGT. | Erro/Pendente geram alertas. |
| AJ | Data_Comunicação | Data | Data de comunicação à AGT. | — |
| AK | Erro_Comunicação | Texto | Mensagem de erro da comunicação. | — |
| AL | Observação | Texto | Observação. | — |

## 02_DIÁRIO_LANÇAMENTOS — campos CALCULADOS (camada de processamento)

| Coluna | Campo | Nome definido | Fórmula (linha 6) |
|---|---|---|---|
| AM | Exercício | `J_Ano` | `=IF(A6="","",IF(ISNUMBER(B6),YEAR(B6),""))` |
| AN | Mês | `J_Mes` | `=IF(A6="","",IF(ISNUMBER(B6),MONTH(B6),""))` |
| AO | Trimestre | `J_Trim` | `=IF(AN6="","",ROUNDUP(AN6/3,0))` |
| AP | Semestre | `J_Sem` | `=IF(AN6="","",IF(AN6<=6,1,2))` |
| AQ | Classe | `J_Classe` | `=IF(A6="","",LEFT(I6,1))` |
| AR | Conta_2D | `J_G2` | `=IF(A6="","",LEFT(I6,2))` |
| AS | Designação_Conta | `J_NomeConta` | `=IF(A6="","",IFERROR(INDEX(PC_Desig,MATCH(I6,PC_Cod,0)),"#CONTA INEXISTENTE"))` |
| AT | Conta_Existe | `J_ContaOK` | `=IF(A6="","",IF(ISNUMBER(MATCH(I6,PC_Cod,0)),1,0))` |
| AU | Conta_Movimento | `J_ContaMov` | `=IF(A6="","",IF(AT6=1,IF(INDEX(PC_Tipo,MATCH(I6,PC_Cod,0))="Movimento",1,0),0))` |
| AV | Conta_Corrente | `J_ContaCorr` | `=IF(A6="","",IF(AT6=1,INDEX(PC_CCorr,MATCH(I6,PC_Cod,0))&"","N"))` |
| AW | Nome_Terceiro | `J_Terceiro` | `=IF(OR(A6="",H6=""),"",IFERROR(INDEX(T_Nome,MATCH(H6,T_NIF,0)),"#NIF NÃO REGISTADO"))` |
| AX | Tipo_Terceiro | `J_TipoTerc` | `=IF(OR(A6="",H6=""),"",IFERROR(INDEX(T_Tipo,MATCH(H6,T_NIF,0)),""))` |
| AY | NIF_Formato_OK | `J_NIFfmt` | `=IF(OR(A6="",H6=""),"",IF(IFERROR(INDEX(T_Pais,MATCH(H6,T_NIF,0)),"Angola")<>"Angola",1,IF(OR(H6=CFG_NIFCF,AND(LEN(H6)=10,ISNUMBER(-H6)),AND(LEN(H6)=14,ISNUMBER(-LEFT(H6,9)),ISN…` |
| AZ | Valor_D_menos_C | `J_DC` | `=N(K6)-N(L6)` |
| BA | Montante_Linha | `J_Montante` | `=N(K6)+N(L6)` |
| BB | Saldo_Lançamento | `J_SaldoID` | `=IF(A6="","",IF(A6=A5,BB5,SUMIF(J_ID,A6,J_DC)))` |
| BC | Chave_Documento | `J_ChaveDoc` | `=IF(OR(A6="",E6=""),"",C6&"¦"&D6&"¦"&E6&"¦"&H6)` |
| BD | Documento_Duplicado | `J_Dup` | `=IF(BC6="",0,IF(INDEX(J_ID,MATCH(BC6,J_ChaveDoc,0))<>A6,1,0))` |
| BE | É_Abertura | `J_IsAbe` | `=IF(A6="","",IF(Q6="Abertura",1,0))` |
| BF | Inclui_DR | `J_IncDR` | `=IF(A6="","",IF(IFERROR(INDEX(NAT_IncDR,MATCH(Q6,NAT_Nome,0)),"S")="S",1,0))` |
| BG | Rubrica_DR | `J_RubDR` | `=IF(A6="","",IFERROR(INDEX(PC_RubDR,MATCH(I6,PC_Cod,0))&"",""))` |
| BH | Meio_Monetário | `J_Caixa` | `=IF(A6="","",IF(ISNUMBER(MATCH(AR6,L_CaixaPref,0)),1,0))` |
| BI | Fluxo_Caixa | `J_Fluxo` | `=IF(A6="","",IF(BH6<>1,"",IF(BE6=1,"Abertura",IFERROR(INDEX(NAT_Fluxo,MATCH(Q6,NAT_Nome,0)),"NÃO CLASSIFICADO"))))` |
| BJ | Linha_DFC | `J_LinhaDFC` | `=IF(A6="","",IF(OR(BH6<>1,BE6=1),"",IFERROR(INDEX(NAT_DFC,MATCH(Q6,NAT_Nome,0)),"NÃO CLASSIFICADO")))` |
| BK | Taxa_Fiscal | `J_TaxaF` | `=IF(OR(A6="",R6=""),"",IFERROR(INDEX(TX_Taxa,MATCH(R6,TX_Cod,0)),"#CÓDIGO"))` |
| BL | Estado_Taxa | `J_TaxaEst` | `=IF(OR(A6="",R6=""),"",IFERROR(INDEX(TX_Estado,MATCH(R6,TX_Cod,0)),""))` |
| BM | Tipo_IVA | `J_TipoIVA` | `=IF(OR(A6="",LEFT(R6,3)<>"IVA"),"",IF(LEFT(I6,6)="34.5.3","Liquidado",IF(LEFT(I6,6)="34.5.2","Dedutível",IF(LEFT(I6,6)="34.5.4","Regularização",IF(AQ6="6","Base — venda s/ IVA",…` |
| BN | IVA_Calculado | `J_IVACalc` | `=IF(OR(A6="",BM6=""),"",IF(ISNUMBER(BK6),ROUND(N(S6)*BK6,2),""))` |
| BO | Erro_Taxa | `J_ErrTaxa` | `=IF(A6="","",IF(OR(BM6="Liquidado",BM6="Dedutível",BM6="Regularização",R6="RET_SERV"),IF(ISNUMBER(BK6),IF(ABS(BA6-N(S6)*BK6)>CFG_Tol,1,0),1),IF(BK6="#CÓDIGO",1,0)))` |
| BP | Mês_Encerrado | `J_MesFech` | `=IF(A6="","",IF(AND(ISNUMBER(AN6),AM6=CFG_Ano),IF(INDEX(FECHO_Estado,AN6)="S",1,0),0))` |
| BQ | Alteração_Período_Encerrado | `J_ErrPer` | `=IF(A6="","",IF(BP6=1,IF(OR(N(AD6)>INDEX(FECHO_Data,AN6),N(AE6)>INDEX(FECHO_Data,AN6)),1,0),0))` |
| BR | Segregação | `J_Segreg` | `=IF(A6="","",IF(AC6="","Pendente",IF(AC6=AB6,"Violação","OK")))` |
| BS | Parte_Relacionada | `J_ParteRel` | `=IF(OR(A6="",H6=""),0,IF(IFERROR(INDEX(T_PR,MATCH(H6,T_NIF,0)),"N")="S",1,0))` |
| BT | Desvio²_Montante | `J_Mont2` | `=IF(OR(A6="",BE6=1),0,(BA6-AUD_Media)^2)` |
| BU | Valor_Anómalo | `J_Anomalo` | `=IF(OR(A6="",BE6=1),0,IF(BA6>AUD_Limite,1,0))` |
| BV | Erros_Detectados | `J_Erros` | `=IF(A6="","",IF(NOT(ISNUMBER(B6)),"Data inválida; ","")&IF(AND(ISNUMBER(B6),AM6<>CFG_Ano),"Fora do exercício; ","")&IF(AT6=0,"Conta inexistente; ","")&IF(AND(AT6=1,AU6=0),"Conta…` |
| BW | Tem_Erro | `J_ErrFlag` | `=IF(A6="",0,IF(BV6="",0,1))` |
| BX | Estado_Validação | `J_EstVal` | `=IF(A6="","",IF(BW6=1,"🔴 ERRO",IF(BR6="OK","🟢 Validado",IF(BR6="Violação","🟡 Segregação","🟡 Por aprovar"))))` |
| BY | Estado_Fiscal | `J_EstFisc` | `=IF(OR(A6="",R6=""),"",IF(BO6=1,"🔴 Inconsistente",IF(ISNUMBER(SEARCH("VALIDAR",BL6)),"🟡 Taxa por validar","🟢 Conforme parametrização")))` |
| BZ | Primeira_Linha_ID | `J_Primeira` | `=IF(A6="",0,IF(MATCH(A6,J_ID,0)=ROW()-5,1,0))` |
| CA | Documento_Emitido | `J_EmitDoc` | `=IF(A6="","",IFERROR(INDEX(TD_Emit,MATCH(C6,TD_Cod,0)),"N"))` |
| CB | Seq_Facturação | `J_SeqFact` | `=IF(AND(BZ6=1,CA6="S"),1,0)+N(CB5)` |
| CC | Seq_Clientes | `J_SeqCli` | `=IF(AND(A6<>"",AR6="31",N(K6)>0,N(T6)=0,N(B6)<=CFG_DataRef),1,0)+N(CC5)` |
| CD | Seq_Fornecedores | `J_SeqForn` | `=IF(AND(A6<>"",AR6="32",N(L6)>0,N(T6)=0,N(B6)<=CFG_DataRef),1,0)+N(CD5)` |
| CE | Seq_Caixa | `J_SeqCaixa` | `=IF(AND(A6<>"",AR6="45",AM6=CFG_Ano,N(B6)<=CFG_DataRef),1,0)+N(CE5)` |
| CF | Seq_Diário_Geral | `J_SeqDG` | `=IF(AND(A6<>"",AM6=CFG_Ano,N(AN6)>=DG_MesIni,N(AN6)<=DG_MesFim,OR(DG_Conta="",LEFT(I6,LEN(DG_Conta))=DG_Conta&""),OR(DG_NIF="",H6=DG_NIF&""),OR(DG_CC="",M6=DG_CC&""),OR(DG_Proj=…` |
| CG | Seq_Razão | `J_SeqRZ` | `=IF(AND(A6<>"",AM6=CFG_Ano,BE6=0,N(AN6)>=RZ_MesIni,N(AN6)<=RZ_MesFim,OR(I6=RZ_Conta&"",LEFT(I6,LEN(RZ_Conta)+1)=RZ_Conta&".",AND(LEN(RZ_Conta)=1,AQ6=RZ_Conta&"")),OR(RZ_NIF="",H…` |
| CH | Seq_Kardex | `J_SeqArt` | `=IF(AND(A6<>"",AQ6="2",Y6=INV_ArtSel&"",N(Z6)<>0),1,0)+N(CH5)` |

## 01_PLANO_CONTAS

| Campo | Descrição |
|---|---|
| Código | Código PGC (texto, com pontos). |
| Tipo | Movimento (recebe lançamentos) ou Agregação (soma as filhas). |
| Rubrica balanço (saldo devedor/credor) | Rubrica do Balanço consoante o sinal do saldo (ex.: 43 devedor → Disponibilidades; credor → Empréstimos de curto prazo). |
| Rubrica DR | Linha da Demonstração de Resultados (classes 6, 7 e 87). |
| Conta corrente | S = exige NIF (31, 32). |
| Reconciliação | S = conta sujeita a reconciliação/alerta de ausência de movimento. |
| Saldos | Débito, crédito, saldo, abertura — calculados. |

## Nomes definidos (interface entre folhas)

Os mapas comunicam por **nomes definidos** (ex.: `DR_RL`, `BS_AT`, `IVA_Estado`). A lista completa com a folha de origem está em `05_MAPA_DEPENDENCIAS.md`.
