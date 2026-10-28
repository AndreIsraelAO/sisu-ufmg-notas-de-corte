# Belo Horizonte × Montes Claros: a diferença caiu muito a partir de 2018

**Resumo.** Só um curso é oferecido nos dois campi: **Administração (Noturno)**. Nele, a nota de corte de BH superou a de Montes Claros em média 113,5 pontos de 2014 a 2017 e 29,9 pontos de 2018 a 2026. A mesma redução aparece na mediana geral dos campi, mas lá os cursos são diferentes.

## Pergunta

Para os cursos oferecidos nos dois campi, qual a diferença de nota de corte entre Belo Horizonte e Montes Claros?

## Dados usados

- `data/notas_corte.csv`: chamada regular, cota `AC`, dois campi.
- Cursos presentes nos dois campi na mesma edição, pelo `curso_id`: **administracao-bach**. Os dois são do turno Noturno.
- Edições em que os dois campi aparecem: 13 (Montes Claros não aparece nas segundas edições de 2014 e 2015).

## Método

- **Comparação pareada:** `diferença = nota(BH) − nota(MOC)` para o mesmo curso, turno, cota e edição.
- **Complemento:** mediana da nota de corte de todas as ofertas de cada campus. Essa comparação mistura cursos diferentes (Montes Claros tem Agronomia, Zootecnia e engenharias agrárias; BH tem quase todo o resto) e serve só de contexto.

## Resultados

**Tabela 1 – Administração – Noturno, nota de corte AC.**

| edicao_chave | Belo Horizonte | Montes Claros | diferença (BH − MOC) |
|---|---|---|---|
| 2014-1 | 702,14 | 594,98 | 107,16 |
| 2015-1 | 704,16 | 598,30 | 105,86 |
| 2016-1 | 698,30 | 580,90 | 117,40 |
| 2017-1 | 717,52 | 593,74 | 123,78 |
| 2018-1 | 728,68 | 693,04 | 35,64 |
| 2019-1 | 741,46 | 711,62 | 29,84 |
| 2020-1 | 723,42 | 691,32 | 32,10 |
| 2021-1 | 721,10 | 682,36 | 38,74 |
| 2022-1 | 722,34 | 691,06 | 31,28 |
| 2023-1 | 717,28 | 693,90 | 23,38 |
| 2024-1 | 724,26 | 696,32 | 27,94 |
| 2025-1 | 723,52 | 697,62 | 25,90 |
| 2026-1 | 739,90 | 715,80 | 24,10 |

**Tabela 2 – Mediana das notas de corte por campus (cursos diferentes).**

| edicao_chave | Belo Horizonte | Montes Claros | diferença das medianas | ofertas BH | ofertas MOC |
|---|---|---|---|---|---|
| 2014-1 | 690,7 | 559,4 | 131,3 | 71,0 | 6,0 |
| 2014-2 | 659,2 | – | – | 56,0 | – |
| 2015-1 | 692,0 | 556,6 | 135,5 | 72,0 | 6,0 |
| 2015-2 | 680,4 | – | – | 56,0 | – |
| 2016-1 | 677,7 | 553,8 | 123,9 | 81,0 | 6,0 |
| 2017-1 | 692,3 | 564,4 | 127,9 | 81,0 | 6,0 |
| 2018-1 | 714,0 | 663,6 | 50,4 | 84,0 | 6,0 |
| 2019-1 | 719,1 | 666,4 | 52,6 | 84,0 | 6,0 |
| 2020-1 | 711,2 | 650,2 | 61,0 | 84,0 | 6,0 |
| 2021-1 | 708,7 | 642,5 | 66,1 | 84,0 | 6,0 |
| 2022-1 | 706,8 | 640,8 | 66,0 | 84,0 | 6,0 |
| 2023-1 | 699,7 | 651,0 | 48,7 | 84,0 | 6,0 |
| 2024-1 | 718,0 | 655,8 | 62,2 | 85,0 | 6,0 |
| 2025-1 | 720,3 | 649,9 | 70,4 | 85,0 | 7,0 |
| 2026-1 | 730,8 | 665,8 | 64,9 | 87,0 | 7,0 |

![BH x Montes Claros](../figuras/06_bh_montes_claros.png)

*Figura 1 – Esquerda: Administração – Noturno nos dois campi. Direita: mediana das notas de corte de cada campus. Fonte: SISU/UFMG; elaboração própria.*

## Interpretação

- Com um único curso em comum, a comparação "mesmo curso, outro campus" é um estudo de caso, não uma regra geral.
- A diferença de Administração diminuiu de forma brusca entre 2017-1 e 2018-1 (123,8 → 35,6 pontos). Isso coincide com a mudança do sistema de cotas (era E2) e com outras mudanças no SISU, mas a base não permite atribuir uma causa.
- Mesmo depois de 2018, BH segue com nota de corte maior em todas as edições.

## Limitações e ressalvas

- **Esta análise foi ajustada:** a pergunta original pedia "os cursos oferecidos nos dois campi", mas a base só tem um. O complemento por campus inteiro não compara cursos iguais.
- Nota de corte é a nota do último classificado. Ela depende de quantas pessoas se inscreveram, de suas notas e do número de vagas; não mede a qualidade do curso. A base não traz o número de candidatos, então "mais concorrido" aqui significa "maior nota de corte".
- As notas do ENEM são padronizadas a cada edição, e o número de vagas, as regras de cota e o perfil dos candidatos mudam de um ano para outro. Diferenças entre anos mostram o que foi observado, não uma mudança na "dificuldade" do curso.
- O número de vagas de cada campus não está na base.

## Como reproduzir

```bash
python scripts/06_bh_montes_claros.py
```
