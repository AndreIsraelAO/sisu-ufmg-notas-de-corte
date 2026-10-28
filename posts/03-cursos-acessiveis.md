# As menores notas de corte estão em cursos de nicho e em Montes Claros, e ficaram relativamente mais baixas

**Resumo.** Das 10 ofertas com menor nota de corte em 2024–2026 (ampla concorrência, chamada regular), 2 são do campus Montes Claros. A menor média é a de **Engenharia Florestal – Matutino, MOC** (634,0 pontos). Das 8 que já existiam em 2014-1, 8 ocupam em 2026-1 um percentil mais baixo, ou seja, ficaram relativamente mais acessíveis.

## Pergunta

Quais ofertas da UFMG têm as menores notas de corte e como a posição delas mudou ao longo do tempo?

## Dados usados

- `data/notas_corte.csv`: chamada regular, cota `AC`, **os dois campi** (Montes Claros entra porque concentra parte das menores notas).
- Ofertas com nota em 2024, 2025 e 2026.

## Método

1. Selecionamos as 10 ofertas com menor média de nota de corte em 2024-1, 2025-1 e 2026-1.
2. Como o número de ofertas e a escala do ENEM mudam de edição para edição, a comparação no tempo usa o **percentil** da oferta dentro da edição: `percentil = posição da nota (da menor para a maior) / nº de ofertas × 100`. O valor 10 quer dizer que só 10% das ofertas daquela edição tinham nota de corte menor ou igual.

## Resultados

**Tabela 1 – As 10 ofertas com menor nota de corte em 2024–2026.**

| oferta | 2014-1 | 2018-1 | 2026-1 | média 2024–26 | percentil 2014-1 | percentil 2026-1 |
|---|---|---|---|---|---|---|
| Engenharia Florestal – Matutino, MOC | 570,8 | 656,4 | 642,0 | 634,0 | 5,2 | 2,1 |
| Arquivologia – Noturno | 629,5 | 644,8 | 651,3 | 634,6 | 14,3 | 4,3 |
| Aquacultura – Matutino | 622,3 | 662,7 | 647,5 | 640,7 | 10,4 | 3,2 |
| Biblioteconomia – Noturno | 623,6 | 646,9 | 660,4 | 641,2 | 13,0 | 7,4 |
| Engenharia Agrícola e Ambiental – Matutino, MOC | 573,9 | 657,7 | 651,4 | 645,8 | 6,5 | 5,3 |
| Biblioteconomia – Matutino | 639,5 | 643,6 | 665,7 | 649,0 | 19,5 | 10,6 |
| Museologia – Matutino | – | 653,8 | 655,7 | 649,2 | – | 6,4 |
| Turismo – Matutino | 639,3 | 677,0 | 663,3 | 650,3 | 18,2 | 8,5 |
| Gestão de Serviços de Saúde – Noturno | 652,9 | 662,1 | 664,8 | 653,2 | 28,6 | 9,6 |
| Geografia – Noturno | – | 672,3 | 669,9 | 656,4 | – | 13,8 |

![Percentil das ofertas mais acessíveis](../figuras/03_cursos_acessiveis.png)

*Figura 1 – Percentil da nota de corte na edição, para as 10 ofertas com menor nota em 2024–2026. Linha interrompida = oferta ausente na edição. Fonte: SISU/UFMG; elaboração própria.*

**Tabela 2 – Menor nota de corte (AC) de cada edição.**

| Edição | Oferta | Nota de corte |
|---|---|---|
| 2014-1 | Engenharia de Alimentos – Matutino, MOC | 536,94 |
| 2014-2 | Turismo – Matutino | 529,94 |
| 2015-1 | Zootecnia – Matutino, MOC | 522,12 |
| 2015-2 | Radiologia – Noturno | 586,62 |
| 2016-1 | Zootecnia – Matutino, MOC | 541,82 |
| 2017-1 | Engenharia de Alimentos – Matutino, MOC | 520,08 |
| 2018-1 | Biblioteconomia – Matutino | 643,62 |
| 2019-1 | Arquivologia – Noturno | 642,46 |
| 2020-1 | Engenharia Florestal – Matutino, MOC | 628,86 |
| 2021-1 | Biblioteconomia – Matutino | 615,96 |
| 2022-1 | Aquacultura – Matutino | 620,92 |
| 2023-1 | Arquivologia – Noturno | 614,86 |
| 2024-1 | Arquivologia – Noturno | 624,52 |
| 2025-1 | Ciências da Natureza e Matemática (Lic.) – Noturno, MOC | 604,86 |
| 2026-1 | Ciências da Natureza e Matemática (Lic.) – Noturno, MOC | 634,46 |

## Interpretação

- As menores notas de corte estão em cursos de nicho de Belo Horizonte (Arquivologia, Biblioteconomia, Museologia, Aquacultura, Turismo) e em dois cursos de Montes Claros.
- Em 2014-1 essas ofertas já estavam abaixo do percentil 29. Em 2026-1 todas estão abaixo do percentil 14. A maior mudança é a de Gestão de Serviços de Saúde – Noturno.
- Nenhuma das 10 ofertas subiu mais de 15 pontos percentuais entre 2014-1 e 2026-1.
- Nota de corte menor indica que o último aprovado teve nota menor, o que é associado a menos procura ou a mais vagas. Não diz nada sobre a qualidade do curso.

## Limitações e ressalvas

- Nota de corte é a nota do último classificado. Ela depende de quantas pessoas se inscreveram, de suas notas e do número de vagas; não mede a qualidade do curso. A base não traz o número de candidatos, então "mais concorrido" aqui significa "maior nota de corte".
- As notas do ENEM são padronizadas a cada edição, e o número de vagas, as regras de cota e o perfil dos candidatos mudam de um ano para outro. Diferenças entre anos mostram o que foi observado, não uma mudança na "dificuldade" do curso.
- Os percentis dependem de quantas ofertas existem em cada edição. Em 2014-2 e 2015-2 há cerca de 56 ofertas, contra 94 em 2026-1.
- **Efeito de seleção:** as 10 ofertas foram escolhidas por estarem no fundo em 2024–2026. É de se esperar que estivessem um pouco mais acima em anos anteriores (regressão à média), então parte da "queda de percentil" vem do próprio critério de escolha.
- Montes Claros tem poucos cursos (7 ofertas em 2026), o que pesa na lista.

## Como reproduzir

```bash
python scripts/03_cursos_acessiveis.py
```
