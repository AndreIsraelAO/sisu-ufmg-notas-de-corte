# Relatório de qualidade — notas de corte SISU/UFMG

Gerado por `build.py` (seed=20260101). Linhas: 52144. Cursos brutos: 92 -> 88 curso_id (curso x modelo).

## 1. Validações

| Validação | Resultado | Detalhe |
|---|---|---|
| Linhas no CSV completo | PASSOU | 52144 (esperado 52144) |
| Toda cota_raw (por era) tem de-para | PASSOU | sem mapeamento: nenhum |
| Cotas do de-para sem uso nos dados | PASSOU | nenhuma |
| curso_raw único no de-para | PASSOU | 92 nomes brutos |
| Todo curso_raw tem de-para | PASSOU | 0 sem mapeamento |
| Sem duplicatas na chave bruta | PASSOU | 0 duplicatas |
| Sem duplicatas na chave padronizada (pós de-para) | PASSOU | 0 duplicatas |
| Sem nulos/vazios | PASSOU | 0 |
| nota_min <= nota_max | PASSOU | 0 violações |
| 0 < nota <= 1000 | PASSOU | 0 fora do intervalo (nota==1000 aceita: 0) |
| Todo curso_id/cota_padrao preenchido | PASSOU | 0 sem mapeamento |
| Linhas por ano = csv_por_ano | PASSOU | limpo={2014: 660, 2015: 670, 2016: 435, 2017: 435, 2018: 792, 2019: 714, 2020: 699, 2021: 684, 2022: 3230, 2023: 11101, 2024: 10710, 2025: 10944, 2026: 11070} / csv_por_ano={2014: 660, 2015: 670, 2016: 435, 2017: 435, 2018: 792, 2019: 714, 2020: 699, 2021: 684, 2022: 3230, 2023: 11101, 2024: 10710, 2025: 10944, 2026: 11070} |
| Conteúdo csv_por_ano == csv completo | PASSOU | idêntico |
| Total de linhas limpo == entrada | PASSOU | 52144 |
| nota_min não crescente com a chamada (por chave) | PASSOU | 0 subidas em 0 de 8405 chaves |
| nota_max constante entre chamadas (por chave) | PASSOU | 0 chaves com nota_max variável |
| notas_corte.parquet | PASSOU | gerado |
| notas_corte_final: 1 linha por (chave sem chamada) | PASSOU | 8405 linhas = 8405 chaves |
| Amostragem contra PDFs (5/ano, seed=20260101) | PASSOU | 65 OK (52 com rótulo confirmado), 0 divergentes, 0 não verificáveis de 65 |
| Reconciliação CSV x PDF (2015+, todas as linhas) | PASSOU | 49377 no bloco curso+turno; 2107 fora do bloco mas com mín e máx em outro ponto do PDF (layout); 0 com mín ou máx ausente do PDF (linhas_fora_do_bloco_pdf.csv) |
| Toda chamada do CSV (2018+) tem PDF | PASSOU | sem PDF: nenhuma |
| PDFs (2018+) sem linhas no CSV | PASSOU | nenhum |

Legenda: FALHOU = interrompe o build (assert). ATENÇÃO = verificação informativa que não passou.

## 2. Linhas, PDFs e chamadas por ano

| ano | linhas csv_por_ano | linhas limpo | nº PDFs | chamadas no CSV |
|---|---|---|---|---|
| 2014 | 660 | 660 | 3 | 0 |
| 2015 | 670 | 670 | 2 | 0 |
| 2016 | 435 | 435 | 1 | 11 |
| 2017 | 435 | 435 | 1 | 10 |
| 2018 | 792 | 792 | 1 | 0 |
| 2019 | 714 | 714 | 1 | 0 |
| 2020 | 699 | 699 | 1 | 0 |
| 2021 | 684 | 684 | 1 | 0 |
| 2022 | 3230 | 3230 | 5 | 0,4,5,10,12 |
| 2023 | 11101 | 11101 | 17 | 0,1,3,5,7,8,9,10,11,12,13,14,15,16,17,18,19 |
| 2024 | 10710 | 10710 | 18 | 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17 |
| 2025 | 10944 | 10944 | 16 | 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 |
| 2026 | 11070 | 11070 | 15 | 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14 |

- O enunciado dizia '2014 tem 3 PDFs, 2015 tem 2, os demais 1'. Real: 2016-2021 têm 1; 2022 tem 5; 2023 tem 17; 2024 tem 18; 2025 tem 16; 2026 tem 15 (chamada regular + listas de espera).
- 2016 e 2017: um único PDF 'chamada regular', mas o CSV tem chamada=11 e 10 (tratado como chamada única; `chamada_raw` preservada).
- 2022 e 2023 têm lacunas de chamada no CSV (2022: 0,4,5,10,12; 2023 sem 2, 4 e 6) e há PDFs sem linhas no CSV (ver validação acima). `is_final` usa a maior chamada **presente nos dados**.

## 3. Cotas

Divergências entre o enunciado e os dados/PDFs:

- **2023 usa a era 2 (1.1…4.2, AC), não a era 3.** Confirmado na legenda do PDF de 2023. Era 3 começa em 2024.
- **LB_Q e LI_Q aparecem em 2025 e 2026** (não só 2026). 2024 não tem LB_Q/LI_Q; no PDF de 2024 há uma lista 'QUILOMBOLA' separada (curso/turno/mín/máx, sem modalidade) que **não está no CSV**.
- 2024 tem LI_PCD/LB_PCD só em parte dos cursos (1368 e 1152 linhas contra 1638 das demais).

| cota_raw | era | cota_padrao | confiança |
|---|---|---|---|
| 1 | E1_2014-2017 | LB_PPI | media |
| 2 | E1_2014-2017 | LB_EP | media |
| 3 | E1_2014-2017 | LI_PPI | media |
| 4 | E1_2014-2017 | LI_EP | media |
| AC | E1_2014-2017 | AC | alta |
| 1.1 | E2_2018-2023 | LB_PPI_PCD | baixa |
| 1.2 | E2_2018-2023 | LB_PPI | media |
| 2.1 | E2_2018-2023 | LB_PCD | media |
| 2.2 | E2_2018-2023 | LB_EP | media |
| 3.1 | E2_2018-2023 | LI_PPI_PCD | baixa |
| 3.2 | E2_2018-2023 | LI_PPI | media |
| 4.1 | E2_2018-2023 | LI_PCD | media |
| 4.2 | E2_2018-2023 | LI_EP | media |
| AC | E2_2018-2023 | AC | alta |
| LB_PPI | E3_2024+ | LB_PPI | alta |
| LB_Q | E3_2024+ | LB_Q | alta |
| LB_PCD | E3_2024+ | LB_PCD | alta |
| LB_EP | E3_2024+ | LB_EP | alta |
| LI_PPI | E3_2024+ | LI_PPI | alta |
| LI_Q | E3_2024+ | LI_Q | alta |
| LI_PCD | E3_2024+ | LI_PCD | alta |
| LI_EP | E3_2024+ | LI_EP | alta |
| AC | E3_2024+ | AC | alta |

Fontes e descrições completas em `de_para_cotas.csv`. Evidência: legendas dos PDFs oficiais (lidas). Os editais não foram lidos; nenhuma fonte oficial declara a correspondência entre eras (é inferida pela comparação das legendas). Dimensões que mudam entre eras: limiar de renda (1,5 SM -> 1 SM), PCD separado (2018+), quilombola (2025+).

Colisão evitada: 1.1 e 2.1 não podem ambos virar LB_PCD (violaria a unicidade da chave e misturaria populações diferentes), então 1.1 -> `LB_PPI_PCD` e 3.1 -> `LI_PPI_PCD` (códigos legados, confiança baixa).

## 4. Turno

- Os PDFs de 2014 usam literalmente `DIURNO` e `TARDE` (ex.: 'CIENCIAS DO ESTADO TARDE', 1ª ed. BH). Não são erro de scraping.
- Em 2015 os mesmos cursos aparecem como Matutino/Vespertino. Evidência (cursos 2014 com o rótulo que também existem em 2015):

| rótulo 2014 | alvo | cursos-campus em 2014 | presentes em 2015 | com o alvo em 2015 |
|---|---|---|---|---|
| Diurno | Matutino | 51 | 51 | 51 |
| Tarde | Vespertino | 1 | 1 | 1 |

- Aplicado em `turno`: Diurno -> Matutino (419 linhas), Tarde -> Vespertino (5 linhas). `turno_raw` e `turno_ajustado` preservam o original. Inferência por evidência indireta, **não confirmada pela UFMG** (ver decisões pendentes).

## 5. Cursos

Unificações automáticas (mesmo curso_id, nomes brutos diferentes):

| curso_id | curso_raw unificados |
|---|---|
| comunicacao-social-jornalismo-ou-relacoes-publicas-bach | COMUNICAÇÃO SOCIAL (JORNALISMO OU RELAÇÕES PÚBLICAS) ; COMUNICAÇÃO SOCIAL - JORNALISMO OU RELAÇÕES PÚBLICAS |
| comunicacao-social-publicidade-bach | COMUNICAÇÃO SOCIAL (PUBLICIDADE) ; COMUNICAÇÃO SOCIAL - PUBLICIDADE |
| engenharia-metalurgica-e-engenharia-de-materiais-bach | ENG. METALÚRGICA E ENG. DE MATERIAIS ; ENGENHARIA METALÚRGICA E ENGENHARIA DE MATERIAIS |
| quimica-tecnologica-bach | QUÍMICA TECNOLÓGICA ; QUÍMICA TECNOLÓGICA (BACHARELADO) |

Casos em dúvida (não unidos, exceto quando indicado):

| caso | nomes brutos [anos] | tratamento |
|---|---|---|
| Comunicação Social 2014/2015 -> cursos separados 2016+ | COMUNICAÇÃO SOCIAL (JORNALISMO OU RELAÇÕES PÚBLICAS) [2014]; COMUNICAÇÃO SOCIAL (PUBLICIDADE) [2014]; COMUNICAÇÃO SOCIAL - JORNALISMO E RELAÇÕES PÚBLICAS [2015]; COMUNICAÇÃO SOCIAL - JORNALISMO OU RELAÇÕES PÚBLICAS [2015]; COMUNICAÇÃO SOCIAL - PUBLICIDADE [2015]; JORNALISMO [2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026]; RELAÇÕES PÚBLICAS [2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026]; PUBLICIDADE E PROPAGANDA [2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026] | Não unidos. 2015 tem 'Jornalismo E RP' (1ª ed.) e 'Jornalismo OU RP' (2ª ed.): pode ser erro de digitação ou mudança real. |
| Engenharia Metalúrgica -> Metalúrgica e de Materiais | ENGENHARIA METALÚRGICA [2014,2015,2016,2017,2018,2019,2020,2021,2022,2023]; ENGENHARIA METALÚRGICA E ENGENHARIA DE MATERIAIS [2024]; ENG. METALÚRGICA E ENG. DE MATERIAIS [2025,2026] | Só as duas últimas foram unidas (expansão de 'ENG.'). A primeira (2014-2023) não foi unida: provável renomeação. |
| Ciência da Computação -> '... e Sistemas de Informação' | CIÊNCIA DA COMPUTAÇÃO [2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024]; CIÊNCIA DA COMPUTAÇÃO E SISTEMAS DE INFORMAÇÃO [2025,2026]; SISTEMAS DE INFORMAÇÃO [2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024] | Não unidos. Sistemas de Informação some em 2025 quando surge o nome combinado: fusão ou novo curso? |
| Antropologia -> Antropologia e Arqueologia | ANTROPOLOGIA [2014,2015,2016,2017,2018,2019,2020,2021,2022,2023]; ANTROPOLOGIA E ARQUEOLOGIA [2024,2025,2026] | Não unidos: provável renomeação em 2024. |
| Letras sem modalidade (2014-2017) vs Letras Bacharelado/Licenciatura (2018+) | LETRAS [2014,2015,2016,2017]; LETRAS (BACHARELADO) [2018,2019,2020,2021,2022,2023,2024,2025,2026]; LETRAS (LICENCIATURA) [2018,2019,2020,2021,2022,2023,2024,2025,2026] | A coluna modelo marca 'LETRAS' como Licenciatura, mas é entrada única pré-2018; não unida a nenhuma das duas. |
| Química Tecnológica com e sem sufixo | QUÍMICA TECNOLÓGICA [2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026]; QUÍMICA TECNOLÓGICA (BACHARELADO) [2014] | UNIDOS pela regra (sufixo = modelo). Registrado aqui para revisão. |

## 6. Monotonicidade de nota_min

0 subidas em 0 de 8405 chaves (lista completa em `excecoes_monotonia.csv`). Por ano:

| ano | nº de subidas |
|---|---|

Primeiras 15:

| ano | edição | curso_id | campus | turno | cota | chamadas | nota_min |
|---|---|---|---|---|---|---|---|

## 7. Amostragem contra PDFs

5 linhas aleatórias por ano (pandas `sample(random_state=20260101)`). Critério: no texto do PDF (`pdftotext -layout`), curso (prefixo), turno, valores mín/máx e rótulo da modalidade aparecem juntos em linhas vizinhas. Em 2014 o rótulo da modalidade não é checado (o layout do PDF desloca os números das linhas 2-4; só curso, turno e par mín/máx). Não compara coluna a coluna.

Reconciliação de **todas** as linhas 2015+ (bloco = curso+turno; 'fora do bloco' = mín e máx existem no PDF, mas o texto os separa do nome do curso):

| ano | linhas | no bloco | fora do bloco (layout) | ausentes do PDF |
|---|---|---|---|---|
| 2015 | 670 | 481 | 189 | 0 |
| 2016 | 435 | 419 | 16 | 0 |
| 2017 | 435 | 419 | 16 | 0 |
| 2018 | 792 | 775 | 17 | 0 |
| 2019 | 714 | 683 | 31 | 0 |
| 2020 | 699 | 676 | 23 | 0 |
| 2021 | 684 | 672 | 12 | 0 |
| 2022 | 3230 | 3065 | 165 | 0 |
| 2023 | 11101 | 10812 | 289 | 0 |
| 2024 | 10710 | 10170 | 540 | 0 |
| 2025 | 10944 | 10460 | 484 | 0 |
| 2026 | 11070 | 10745 | 325 | 0 |

Amostra:

| ano | linha_raw | edição | curso_raw | campus | turno | chamada | cota | mín | máx | status | detalhe |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2014 | 93 | 2014-1 | COMUNICAÇÃO SOCIAL (JORNALISMO OU RELAÇÕES PÚBLICAS) | BELO HORIZONTE | Noturno | 0 | 3 | 696.52 | 737.58 | OK (valores no PDF; bloco não atribuível pelo texto) | 2014_maximas-e-minimas-em-belo-horizonte-1-edicao-do-sisu-ufmg-2014.pdf |
| 2014 | 643 | 2014-2 | RADIOLOGIA | BELO HORIZONTE | Noturno | 0 | 2 | 579.26 | 632.68 | OK (valores no PDF; bloco não atribuível pelo texto) | 2014_maximas-e-minimas-2-edicao-do-sisu-ufmg-2014.pdf |
| 2014 | 451 | 2014-2 | DIREITO | BELO HORIZONTE | Diurno | 0 | 4 | 679.84 | 746.1 | OK | 2014_maximas-e-minimas-2-edicao-do-sisu-ufmg-2014.pdf |
| 2014 | 232 | 2014-1 | FÍSICA | BELO HORIZONTE | Diurno | 0 | 2 | 600.28 | 780.94 | OK | 2014_maximas-e-minimas-em-belo-horizonte-1-edicao-do-sisu-ufmg-2014.pdf |
| 2014 | 517 | 2014-2 | ENGENHARIA DE SISTEMAS | BELO HORIZONTE | Noturno | 0 | AC | 707.94 | 752.72 | OK | 2014_maximas-e-minimas-2-edicao-do-sisu-ufmg-2014.pdf |
| 2015 | 1055 | 2015-2 | ADMINISTRAÇÃO | BELO HORIZONTE | Matutino | 0 | 4 | 645.72 | 724.4 | OK | 2015_maximas-e-minimas-2-edicao-do-sisu-ufmg-2015.pdf |
| 2015 | 745 | 2015-1 | CIÊNCIAS SOCIAIS | BELO HORIZONTE | Matutino | 0 | 4 | 658.28 | 711.9 | OK (valores no PDF; bloco não atribuível pelo texto) | 2015_maximas-e-minimas-1-edicao-do-sisu-ufmg-2015.pdf |
| 2015 | 1014 | 2015-1 | TERAPIA OCUPACIONAL | BELO HORIZONTE | Matutino | 0 | 3 | 657.1 | 674.3 | OK (valores no PDF; bloco não atribuível pelo texto) | 2015_maximas-e-minimas-1-edicao-do-sisu-ufmg-2015.pdf |
| 2015 | 1313 | 2015-2 | RADIOLOGIA | BELO HORIZONTE | Noturno | 0 | 2 | 580.08 | 666.24 | OK | 2015_maximas-e-minimas-2-edicao-do-sisu-ufmg-2015.pdf |
| 2015 | 1108 | 2015-2 | CIÊNCIAS SOCIAIS | BELO HORIZONTE | Matutino | 0 | 2 | 611.46 | 679.12 | OK | 2015_maximas-e-minimas-2-edicao-do-sisu-ufmg-2015.pdf |
| 2016 | 1465 | 2016-1 | ENFERMAGEM | BELO HORIZONTE | Matutino | 11 | 4 | 612.56 | 759.22 | OK | 2016_minimas-e-maximas-chamada-regular.pdf |
| 2016 | 1611 | 2016-1 | HISTÓRIA | BELO HORIZONTE | Noturno | 11 | AC | 662 | 747.6 | OK | 2016_minimas-e-maximas-chamada-regular.pdf |
| 2016 | 1434 | 2016-1 | CONTROLADORIA E FINANÇAS | BELO HORIZONTE | Matutino | 11 | 3 | 657.26 | 704.12 | OK (valores; rótulo inconclusivo) | 2016_minimas-e-maximas-chamada-regular.pdf |
| 2016 | 1334 | 2016-1 | ADMINISTRAÇÃO | BELO HORIZONTE | Matutino | 11 | 3 | 637.44 | 692.64 | OK | 2016_minimas-e-maximas-chamada-regular.pdf |
| 2016 | 1527 | 2016-1 | ENGENHARIA QUÍMICA | BELO HORIZONTE | Matutino | 11 | 1 | 713.58 | 757.96 | OK | 2016_minimas-e-maximas-chamada-regular.pdf |
| 2017 | 1900 | 2017-1 | ENFERMAGEM | BELO HORIZONTE | Matutino | 10 | 4 | 655.66 | 729.6 | OK | 2017_minimas-e-maximas-chamada-regular.pdf |
| 2017 | 2046 | 2017-1 | HISTÓRIA | BELO HORIZONTE | Noturno | 10 | AC | 684.18 | 756.46 | OK | 2017_minimas-e-maximas-chamada-regular.pdf |
| 2017 | 1869 | 2017-1 | CONTROLADORIA E FINANÇAS | BELO HORIZONTE | Matutino | 10 | 3 | 647.08 | 689.66 | OK (valores; rótulo inconclusivo) | 2017_minimas-e-maximas-chamada-regular.pdf |
| 2017 | 1769 | 2017-1 | ADMINISTRAÇÃO | BELO HORIZONTE | Matutino | 10 | 3 | 665.46 | 697.14 | OK | 2017_minimas-e-maximas-chamada-regular.pdf |
| 2017 | 1962 | 2017-1 | ENGENHARIA QUÍMICA | BELO HORIZONTE | Matutino | 10 | 1 | 707 | 750.44 | OK | 2017_minimas-e-maximas-chamada-regular.pdf |
| 2018 | 2886 | 2018-1 | QUÍMICA TECNOLÓGICA | BELO HORIZONTE | Noturno | 0 | 4.1 | 586.56 | 586.56 | OK | 2018_minimas-e-maximas-chamada-regular.pdf |
| 2018 | 2870 | 2018-1 | QUÍMICA | BELO HORIZONTE | Matutino | 0 | 3.2 | 673.14 | 716.04 | OK | 2018_minimas-e-maximas-chamada-regular.pdf |
| 2018 | 2625 | 2018-1 | FONOAUDIOLOGIA | BELO HORIZONTE | Matutino | 0 | 4.1 | 571.64 | 571.64 | OK | 2018_minimas-e-maximas-chamada-regular.pdf |
| 2018 | 2309 | 2018-1 | CIÊNCIAS BIOLÓGICAS | BELO HORIZONTE | Matutino | 0 | 2.1 | 556.4 | 557.86 | OK | 2018_minimas-e-maximas-chamada-regular.pdf |
| 2018 | 2978 | 2018-1 | ENGENHARIA FLORESTAL | MONTES CLAROS | Matutino | 0 | 2.1 | 534.96 | 534.96 | OK | 2018_minimas-e-maximas-chamada-regular.pdf |
| 2019 | 3223 | 2019-1 | ENGENHARIA AEROESPACIAL | BELO HORIZONTE | Matutino | 0 | 4.2 | 771.86 | 788.22 | OK | 2019_minimas-e-maximas-chamada-regular.pdf |
| 2019 | 3323 | 2019-1 | ENGENHARIA QUÍMICA | BELO HORIZONTE | Matutino | 0 | 3.2 | 726.98 | 760.98 | OK (valores; rótulo inconclusivo) | 2019_minimas-e-maximas-chamada-regular.pdf |
| 2019 | 3289 | 2019-1 | ENGENHARIA ELÉTRICA | BELO HORIZONTE | Matutino | 0 | 3.2 | 702.84 | 764.06 | OK | 2019_minimas-e-maximas-chamada-regular.pdf |
| 2019 | 3100 | 2019-1 | CIÊNCIAS BIOLÓGICAS | BELO HORIZONTE | Noturno | 0 | 3.2 | 665.5 | 748.64 | OK | 2019_minimas-e-maximas-chamada-regular.pdf |
| 2019 | 3042 | 2019-1 | ARQUIVOLOGIA | BELO HORIZONTE | Noturno | 0 | 1.1 | 551.98 | 551.98 | OK | 2019_minimas-e-maximas-chamada-regular.pdf |
| 2020 | 4038 | 2020-1 | ESTATÍSTICA | BELO HORIZONTE | Matutino | 0 | 1.2 | 645.94 | 677.06 | OK | 2020_minimas-e-maximas-chamada-regular.pdf |
| 2020 | 4261 | 2020-1 | ODONTOLOGIA | BELO HORIZONTE | Matutino | 0 | 2.2 | 719.08 | 738.68 | OK (valores; rótulo inconclusivo) | 2020_minimas-e-maximas-chamada-regular.pdf |
| 2020 | 4095 | 2020-1 | FÍSICA | BELO HORIZONTE | Matutino | 0 | 3.1 | 263.76 | 263.76 | OK | 2020_minimas-e-maximas-chamada-regular.pdf |
| 2020 | 4268 | 2020-1 | PEDAGOGIA | BELO HORIZONTE | Matutino | 0 | 1.2 | 620.64 | 646.76 | OK (valores; rótulo inconclusivo) | 2020_minimas-e-maximas-chamada-regular.pdf |
| 2020 | 3921 | 2020-1 | EDUCAÇÃO FÍSICA (LICENCIATURA) | BELO HORIZONTE | Matutino | 0 | AC | 680.72 | 734.92 | OK | 2020_minimas-e-maximas-chamada-regular.pdf |
| 2021 | 4763 | 2021-1 | FILOSOFIA | BELO HORIZONTE | Noturno | 0 | AC | 693.1 | 768.66 | OK | 2021_minimas-e-maximas-chamada-regular.pdf |
| 2021 | 4957 | 2021-1 | PEDAGOGIA | BELO HORIZONTE | Noturno | 0 | 1.1 | 489.82 | 489.82 | OK | 2021_minimas-e-maximas-chamada-regular.pdf |
| 2021 | 4818 | 2021-1 | GESTÃO DE SERVIÇOS DE SAÚDE | BELO HORIZONTE | Noturno | 0 | 3.2 | 612.78 | 635.24 | OK | 2021_minimas-e-maximas-chamada-regular.pdf |
| 2021 | 4835 | 2021-1 | HISTÓRIA | BELO HORIZONTE | Matutino | 0 | 4.2 | 728.46 | 762.32 | OK | 2021_minimas-e-maximas-chamada-regular.pdf |
| 2021 | 4981 | 2021-1 | PUBLICIDADE E PROPAGANDA | BELO HORIZONTE | Matutino | 0 | AC | 735.46 | 770.38 | OK | 2021_minimas-e-maximas-chamada-regular.pdf |
| 2022 | 6069 | 2022-1 | FILOSOFIA | BELO HORIZONTE | Noturno | 4 | 2.2 | 633.12 | 647.8 | OK | 2022_minimas-e-maximas-4-chamada.pdf |
| 2022 | 6338 | 2022-1 | TURISMO | BELO HORIZONTE | Matutino | 4 | 1.2 | 521.04 | 620.94 | OK | 2022_minimas-e-maximas-4-chamada.pdf |
| 2022 | 7759 | 2022-1 | CIÊNCIAS ATUARIAIS | BELO HORIZONTE | Matutino | 12 | 3.2 | 446.12 | 685.08 | OK (valores; rótulo inconclusivo) | 2022_minimas-e-maximas-12-chamada.pdf |
| 2022 | 5553 | 2022-1 | MATEMÁTICA | BELO HORIZONTE | Noturno | 0 | 1.2 | 610.96 | 640.74 | OK | 2022_minimas-e-maximas-chamada-regular.pdf |
| 2022 | 5945 | 2022-1 | ENFERMAGEM | BELO HORIZONTE | Matutino | 4 | 4.1 | 565.66 | 653.26 | OK | 2022_minimas-e-maximas-4-chamada.pdf |
| 2023 | 17153 | 2023-1 | FISIOTERAPIA | BELO HORIZONTE | Matutino | 16 | 4.1 | 624.62 | 624.62 | OK | 2023_minimas-e-maximas-16-chamada-da-lista-de-espera.pdf |
| 2023 | 17178 | 2023-1 | GEOGRAFIA | BELO HORIZONTE | Matutino | 16 | 1.2 | 577.8 | 645.62 | OK | 2023_minimas-e-maximas-16-chamada-da-lista-de-espera.pdf |
| 2023 | 18425 | 2023-1 | FARMÁCIA | BELO HORIZONTE | Matutino | 18 | 2.1 | 642.06 | 642.06 | OK | 2023_minimas-e-maximas-18-chamada-da-lista-de-espera.pdf |
| 2023 | 13174 | 2023-1 | ENGENHARIA MECÂNICA | BELO HORIZONTE | Noturno | 10 | 1.2 | 566.34 | 676.42 | OK | 2023_minimas-e-maximas-10-chamada-da-lista-de-espera.pdf |
| 2023 | 15181 | 2023-1 | FILOSOFIA | BELO HORIZONTE | Matutino | 13 | 4.2 | 591.68 | 728.98 | OK | 2023_minimas-e-maximas-13-chamada-da-lista-de-espera.pdf |
| 2024 | 23080 | 2024-1 | CIÊNCIAS BIOLÓGICAS | BELO HORIZONTE | Matutino | 6 | LI_EP | 696.22 | 723.84 | OK | 2024_minimas-e-maximas-6-chamada-da-lista-de-espera.pdf |
| 2024 | 19711 | 2024-1 | FARMÁCIA | BELO HORIZONTE | Noturno | 0 | LB_PCD | 464 | 570.22 | OK | 2024_minimas-e-maximas-chamada-regular.pdf |
| 2024 | 22981 | 2024-1 | ENGENHARIA FLORESTAL | MONTES CLAROS | Matutino | 5 | LB_EP | 491.1 | 617.58 | OK (valores; rótulo inconclusivo) | 2024_minimas-e-maximas-5-chamada-da-lista-de-espera.pdf |
| 2024 | 26707 | 2024-1 | DESIGN | BELO HORIZONTE | Noturno | 12 | LI_PCD | 680.22 | 681.86 | OK (valores; rótulo inconclusivo) | 2024_minimas-e-maximas-12-chamada-da-lista-de-espera.pdf |
| 2024 | 28877 | 2024-1 | RELAÇÕES PÚBLICAS | BELO HORIZONTE | Matutino | 15 | LB_EP | 680.76 | 690.84 | OK (valores; rótulo inconclusivo) | 2024_minimas-e-maximas-15-chamada-da-lista-de-espera.pdf |
| 2025 | 40171 | 2025-1 | LETRAS (BACHARELADO) | BELO HORIZONTE | Noturno | 14 | LI_EP | 654.92 | 673.14 | OK | 2025_minimas-e-maximas-14-chamada-da-lista-de-espera.pdf |
| 2025 | 39195 | 2025-1 | DIREITO | BELO HORIZONTE | Matutino | 13 | LI_PCD | 576.46 | 720.28 | OK | 2025_minimas-e-maximas-13-chamada-da-lista-de-espera.pdf |
| 2025 | 33557 | 2025-1 | ADMINISTRAÇÃO | BELO HORIZONTE | Matutino | 5 | LB_Q | 570.1 | 570.1 | OK | 2025_minimas-e-maximas-5-chamada-da-lista-de-espera.pdf |
| 2025 | 35035 | 2025-1 | CIÊNCIAS CONTÁBEIS | BELO HORIZONTE | Noturno | 7 | LB_Q | 588.3 | 588.3 | OK | 2025_minimas-e-maximas-7-chamada-da-lista-de-espera.pdf |
| 2025 | 33229 | 2025-1 | FISIOTERAPIA | BELO HORIZONTE | Integral | 4 | LB_Q | 654.26 | 654.26 | OK | 2025_minimas-e-maximas-4-chamada-da-lista-de-espera.pdf |
| 2026 | 41381 | 2026-1 | ENGENHARIA ELÉTRICA | BELO HORIZONTE | Matutino | 0 | LI_PPI | 705.94 | 754.18 | OK | 2026_minimas-e-maximas-chamada-regular.pdf |
| 2026 | 47301 | 2026-1 | ENGENHARIA MECÂNICA | BELO HORIZONTE | Noturno | 8 | LI_PPI | 686.36 | 738.34 | OK | 2026_minimas-e-maximas-8-chamada-da-lista-de-espera.pdf |
| 2026 | 51100 | 2026-1 | GESTÃO DE SERVIÇOS DE SAÚDE | BELO HORIZONTE | Noturno | 13 | LI_EP | 642.82 | 664.68 | OK | 2026_minimas-e-maximas-13-chamada-da-lista-de-espera.pdf |
| 2026 | 42625 | 2026-1 | BIOMEDICINA | BELO HORIZONTE | Noturno | 2 | LB_EP | 690.44 | 754.32 | OK | 2026_minimas-e-maximas-2-chamada-da-lista-de-espera-e-2-antecipacao-de-entrada.pdf |
| 2026 | 44227 | 2026-1 | EDUCAÇÃO FÍSICA (BACHARELADO) | BELO HORIZONTE | Matutino | 4 | LB_Q | 591.6 | 591.6 | OK | 2026_minimas-e-maximas-4-chamada-da-lista-de-espera-e-4-antecipacao-de-entrada.pdf |

## 8. Decisões pendentes

1. **Turno:** confirmar Diurno -> Matutino e Tarde -> Vespertino (ou manter 'Diurno' como categoria própria).
2. **Cotas 1.1 e 3.1:** definir se viram LB_PCD / LI_PCD (provável) ou ficam como códigos legados.
3. **Cotas entre eras:** aceitar a equivalência de confiança média (limiar de renda 1,5 -> 1 SM) para séries históricas ou comparar só dentro da era.
4. **Cursos:** decidir os casos da seção 5 (Comunicação Social, Metalúrgica, Ciência da Computação/Sist. de Informação, Antropologia, Letras).
5. **Quilombola 2024:** a lista separada do PDF de 2024 não está no CSV; incluir exige extração nova.
6. **Lacunas de chamada** (2022, 2023) e chamada 11/10 de 2016/2017: confirmar que são lacunas da fonte e não da coleta.

## 9. Não verificado

- Editais do SISU/UFMG (texto) não foram lidos; só as legendas dos PDFs e os índices do repositório.
- Conferência por PDF é amostral (ver seção 7), não exaustiva.
- Parquet: gerado.
