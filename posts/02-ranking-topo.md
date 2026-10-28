# Medicina liderou todas as edições; só 3 ofertas ficaram sempre no top 10

**Resumo.** Em 15 edições do SISU/UFMG (2014–2026), 25 ofertas diferentes entraram ao menos uma vez no top 10 de nota de corte (ampla concorrência, chamada regular, BH). Só 3 estiveram lá em todas: Medicina – Integral, Engenharia Aeroespacial – Matutino, Engenharia Química – Matutino. **Medicina – Integral** teve a maior nota em 15 das 15 edições.

## Pergunta

Quais ofertas aparecem no topo do ranking de nota de corte de forma estável, e quais entram e saem?

## Dados usados

- `data/notas_corte.csv`: chamada regular, cota `AC`, campus Belo Horizonte.
- Unidade: oferta = curso × turno, em cada uma das 15 edições (`edicao_chave`).

## Método

Em cada edição, as ofertas são ordenadas pela nota de corte, da maior para a menor (posição 1 = maior nota; empates recebem a mesma posição). Para cada oferta, contamos quantas vezes ela ficou entre as 10 primeiras e anotamos a melhor posição e a mediana das posições nessas vezes. A coluna "edições existentes" mostra em quantas edições a oferta existia, porque um curso novo não pode ter aparecido antes de existir.

## Resultados

**Tabela 1 – Ofertas que entraram no top 10 ao menos uma vez.**

| Oferta | Vezes no top 10 | Melhor posição | Mediana da posição (no top 10) | Edições existentes |
|---|---|---|---|---|
| Medicina – Integral | 15 | 1 | 1,0 | 15 |
| Engenharia Aeroespacial – Matutino | 15 | 2 | 2,0 | 15 |
| Engenharia Química – Matutino | 15 | 2 | 3,0 | 15 |
| Direito – Matutino | 14 | 4 | 4,0 | 15 |
| Engenharia Mecânica – Matutino | 13 | 3 | 5,0 | 15 |
| Direito – Noturno | 11 | 5 | 8,0 | 15 |
| Engenharia Elétrica – Matutino | 8 | 4 | 5,5 | 15 |
| Ciência da Computação – Matutino | 7 | 3 | 3,0 | 13 |
| Biomedicina – Noturno | 7 | 6 | 9,0 | 15 |
| Ciências Econômicas – Matutino | 7 | 6 | 9,0 | 15 |
| Arquitetura e Urbanismo – Matutino | 6 | 5 | 6,5 | 15 |
| Engenharia Civil – Matutino | 5 | 5 | 7,0 | 15 |
| Engenharia de Produção – Matutino | 5 | 6 | 8,0 | 15 |
| Engenharia Mecânica – Noturno | 3 | 8 | 9,0 | 15 |
| Odontologia – Matutino | 3 | 8 | 9,0 | 13 |
| Engenharia de Computação – Vespertino | 2 | 3 | 3,0 | 2 |
| Ciência da Computação e Sistemas de Informação – Vespertino | 2 | 5 | 6,0 | 2 |
| Ciência de Dados – Vespertino | 2 | 4 | 6,5 | 3 |
| Sistemas de Informação – Noturno | 2 | 7 | 7,0 | 13 |
| Psicologia – Matutino | 2 | 8 | 8,0 | 15 |
| Arquitetura e Urbanismo – Noturno | 2 | 10 | 10,0 | 15 |
| Jornalismo – Matutino | 1 | 7 | 7,0 | 11 |
| Matemática Computacional – Matutino | 1 | 8 | 8,0 | 11 |
| Engenharia Metalúrgica – Matutino | 1 | 10 | 10,0 | 12 |
| Engenharia de Minas – Matutino | 1 | 10 | 10,0 | 15 |

![Vezes no top 10](../figuras/02_ranking_top10.png)

*Figura 1 – Número de edições em que cada oferta ficou entre as 10 maiores notas de corte. Fonte: SISU/UFMG; elaboração própria.*

**Tabela 2 – Maior nota de corte de cada edição.**

| Edição | Oferta | Nota de corte |
|---|---|---|
| 2014-1 | Medicina – Integral | 795,22 |
| 2014-2 | Medicina – Integral | 782,50 |
| 2015-1 | Medicina – Integral | 798,50 |
| 2015-2 | Medicina – Integral | 787,28 |
| 2016-1 | Medicina – Integral | 795,22 |
| 2017-1 | Medicina – Integral | 802,74 |
| 2018-1 | Medicina – Integral | 796,18 |
| 2019-1 | Medicina – Integral | 810,46 |
| 2020-1 | Medicina – Integral | 794,52 |
| 2021-1 | Medicina – Integral | 813,76 |
| 2022-1 | Medicina – Integral | 811,06 |
| 2023-1 | Medicina – Integral | 805,42 |
| 2024-1 | Medicina – Integral | 812,80 |
| 2025-1 | Medicina – Integral | 812,48 |
| 2026-1 | Medicina – Integral | 818,50 |

**Tabela 3 – Posição no ranking das 12 ofertas mais frequentes, por edição** (vazio = oferta não existia na edição).

| Oferta | 2014-1 | 2014-2 | 2015-1 | 2015-2 | 2016-1 | 2017-1 | 2018-1 | 2019-1 | 2020-1 | 2021-1 | 2022-1 | 2023-1 | 2024-1 | 2025-1 | 2026-1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Medicina – Integral | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Engenharia Aeroespacial – Matutino | 2 | 9 | 7 | 4 | 3 | 8 | 3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| Engenharia Química – Matutino | 3 | 2 | 2 | 2 | 2 | 2 | 2 | 3 | 3 | 4 | 5 | 5 | 6 | 6 | 8 |
| Direito – Matutino | 6 | 13 | 9 | 5 | 6 | 4 | 4 | 4 | 4 | 5 | 4 | 4 | 5 | 4 | 4 |
| Engenharia Mecânica – Matutino | 5 | 3 | 3 | 3 | 22 | 3 | 5 | 5 | 7 | 11 | 7 | 9 | 8 | 10 | 5 |
| Direito – Noturno | 8 | 5 | 8 | 12 | 5 | 6 | 6 | 8 | 8 | 10 | 10 | 13 | 14 | 13 | 9 |
| Engenharia Elétrica – Matutino | 4 | 4 | 4 | 9 | 4 | 14 | 7 | 11 | 9 | 14 | 17 | 18 | 13 | 15 | 10 |
| Ciência da Computação – Matutino | 18 | 23 | 15 | 14 | 13 | 7 | 12 | 6 | 5 | 3 | 3 | 3 | 3 | – | – |
| Biomedicina – Noturno | 21 | 33 | 22 | 23 | 31 | 32 | 10 | 10 | 10 | 6 | 6 | 6 | 9 | 11 | 12 |
| Ciências Econômicas – Matutino | 22 | 20 | 17 | 18 | 36 | 9 | 11 | 9 | 6 | 9 | 11 | 10 | 12 | 7 | 6 |
| Arquitetura e Urbanismo – Matutino | 11 | 6 | 12 | 6 | 16 | 5 | 8 | 7 | 13 | 13 | 13 | 12 | 10 | 14 | 13 |
| Engenharia Civil – Matutino | 7 | 7 | 5 | 7 | 7 | 13 | 15 | 19 | 28 | 28 | 34 | 31 | 37 | 32 | 32 |

## Interpretação

- O topo é dominado por um mesmo grupo de cursos. A rotatividade acontece sobretudo nas últimas posições do top 10, onde as diferenças de nota são de poucos pontos.
- Cursos criados recentemente (Ciência de Dados em 2024; Engenharia de Computação e o curso combinado de Ciência da Computação e Sistemas de Informação em 2025) entram direto no topo. Eles aparecem poucas vezes na tabela só porque existem há pouco tempo.
- Estar no top 10 está associado a cursos de alta procura, mas a posição também depende do número de vagas da oferta.

## Limitações e ressalvas

- Nota de corte é a nota do último classificado. Ela depende de quantas pessoas se inscreveram, de suas notas e do número de vagas; não mede a qualidade do curso. A base não traz o número de candidatos, então "mais concorrido" aqui significa "maior nota de corte".
- As notas do ENEM são padronizadas a cada edição, e o número de vagas, as regras de cota e o perfil dos candidatos mudam de um ano para outro. Diferenças entre anos mostram o que foi observado, não uma mudança na "dificuldade" do curso.
- O número de ofertas por edição varia (77 em 2014-1, 56 em 2014-2, 94 em 2026-1). A posição 10 numa edição pequena não equivale exatamente à posição 10 numa edição grande.

## Como reproduzir

```bash
python scripts/02_ranking_topo.py
```
