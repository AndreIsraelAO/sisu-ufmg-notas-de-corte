# Onde dá para comparar, o bacharelado teve nota de corte maior que a licenciatura

**Resumo.** Só há 4 pares bacharelado/licenciatura no mesmo curso, turno e edição: Educação Física – Matutino, Letras – Matutino, Letras – Noturno, Teatro – Matutino. O bacharelado teve nota de corte maior em 32 das 34 comparações, com diferença média por par entre 7,9 e 22,9 pontos.

## Pergunta

Nos cursos que oferecem as duas modalidades, o bacharelado e a licenciatura têm notas de corte diferentes?

## Dados usados

- `data/notas_corte.csv`: chamada regular, cota `AC`, dois campi.
- Pares formados pelo nome do curso sem o sufixo de modalidade (`curso_id` sem `-bach`/`-lic`), no **mesmo turno e edição**.
- Ficam de fora: "Letras (sem modalidade, pré-2018)", que não tem par; e licenciaturas que existiram só em 2014 (Física, Geografia, História, Matemática, Química, Ciências Biológicas), porque nessas edições o bacharelado do mesmo turno não aparece.
- **Atenção:** na base, Pedagogia está marcada como Bacharelado e não tem licenciatura correspondente, então não entra.

## Método

`diferença = nota(Bacharelado) − nota(Licenciatura)` por par e edição. Mostramos a média por par e quantas vezes o bacharelado teve a nota maior.

## Resultados

**Tabela 1 – Resumo por par.**

| Curso – turno | Edições | Bacharelado (média) | Licenciatura (média) | Diferença média (B − L) | Edições com B > L |
|---|---|---|---|---|---|
| Educação Física – Matutino | 15 | 681,2 | 658,3 | 22,9 | 15 |
| Letras – Matutino | 9 | 695,3 | 687,4 | 7,9 | 8 |
| Letras – Noturno | 9 | 670,2 | 660,3 | 10,0 | 8 |
| Teatro – Matutino | 1 | 704,7 | 684,6 | 20,1 | 1 |

**Tabela 2 – Todas as comparações.**

| Curso – turno | Edição | Bacharelado | Licenciatura | Diferença |
|---|---|---|---|---|
| Educação Física – Matutino | 2014-1 | 668,60 | 645,48 | 23,12 |
| Educação Física – Matutino | 2014-2 | 623,40 | 602,82 | 20,58 |
| Educação Física – Matutino | 2015-1 | 667,48 | 642,70 | 24,78 |
| Educação Física – Matutino | 2015-2 | 653,16 | 625,40 | 27,76 |
| Educação Física – Matutino | 2016-1 | 650,94 | 633,64 | 17,30 |
| Educação Física – Matutino | 2017-1 | 657,56 | 654,42 | 3,14 |
| Educação Física – Matutino | 2018-1 | 699,52 | 669,56 | 29,96 |
| Educação Física – Matutino | 2019-1 | 703,22 | 676,76 | 26,46 |
| Educação Física – Matutino | 2020-1 | 695,84 | 680,72 | 15,12 |
| Educação Física – Matutino | 2021-1 | 690,24 | 661,08 | 29,16 |
| Educação Física – Matutino | 2022-1 | 694,34 | 663,22 | 31,12 |
| Educação Física – Matutino | 2023-1 | 692,44 | 664,36 | 28,08 |
| Educação Física – Matutino | 2024-1 | 703,96 | 674,80 | 29,16 |
| Educação Física – Matutino | 2025-1 | 707,54 | 682,44 | 25,10 |
| Educação Física – Matutino | 2026-1 | 710,46 | 697,78 | 12,68 |
| Letras – Matutino | 2018-1 | 703,70 | 695,26 | 8,44 |
| Letras – Matutino | 2019-1 | 711,38 | 706,46 | 4,92 |
| Letras – Matutino | 2020-1 | 693,86 | 690,98 | 2,88 |
| Letras – Matutino | 2021-1 | 682,92 | 665,20 | 17,72 |
| Letras – Matutino | 2022-1 | 688,40 | 677,08 | 11,32 |
| Letras – Matutino | 2023-1 | 684,48 | 664,34 | 20,14 |
| Letras – Matutino | 2024-1 | 686,92 | 687,26 | -0,34 |
| Letras – Matutino | 2025-1 | 695,08 | 694,12 | 0,96 |
| Letras – Matutino | 2026-1 | 710,92 | 706,06 | 4,86 |
| Letras – Noturno | 2018-1 | 677,38 | 669,06 | 8,32 |
| Letras – Noturno | 2019-1 | 681,42 | 674,76 | 6,66 |
| Letras – Noturno | 2020-1 | 677,70 | 664,62 | 13,08 |
| Letras – Noturno | 2021-1 | 668,14 | 651,16 | 16,98 |
| Letras – Noturno | 2022-1 | 657,76 | 640,80 | 16,96 |
| Letras – Noturno | 2023-1 | 648,88 | 637,28 | 11,60 |
| Letras – Noturno | 2024-1 | 666,34 | 656,52 | 9,82 |
| Letras – Noturno | 2025-1 | 674,40 | 666,42 | 7,98 |
| Letras – Noturno | 2026-1 | 680,22 | 681,94 | -1,72 |
| Teatro – Matutino | 2026-1 | 704,70 | 684,60 | 20,10 |

![Bacharelado x Licenciatura](../figuras/08_bacharelado_licenciatura.png)

*Figura 1 – Nota de corte do bacharelado e da licenciatura nos pares com mais de uma edição. Fonte: SISU/UFMG; elaboração própria.*

## Interpretação

- Nos pares disponíveis o padrão é consistente: bacharelado acima. Mas são só três cursos, todos de Belo Horizonte, e não dá para generalizar para a universidade.
- Em Educação Física a série é longa (15 edições) e a diferença aparece em todas, com média de 22,9 pontos. Em Letras, as modalidades só aparecem separadas a partir de 2018.
- Diferenças de nota entre modalidades estão associadas a diferenças de procura e de vagas, que a base não informa.

## Limitações e ressalvas

- Poucos pares; a comparação é descritiva.
- Nota de corte é a nota do último classificado. Ela depende de quantas pessoas se inscreveram, de suas notas e do número de vagas; não mede a qualidade do curso. A base não traz o número de candidatos, então "mais concorrido" aqui significa "maior nota de corte".
- As notas do ENEM são padronizadas a cada edição, e o número de vagas, as regras de cota e o perfil dos candidatos mudam de um ano para outro. Diferenças entre anos mostram o que foi observado, não uma mudança na "dificuldade" do curso.

## Como reproduzir

```bash
python scripts/08_bacharelado_licenciatura.py
```
