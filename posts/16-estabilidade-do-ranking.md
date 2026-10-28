# O ranking de notas de corte quase não muda de um ano para o outro (ρ entre 0,91 e 0,99)

**Resumo.** Entre edições consecutivas, a correlação de Spearman entre os rankings de nota de corte (BH, ampla concorrência, chamada regular) ficou entre 0,91 e 0,99. A menor foi em 2016-1→2017-1. Mesmo entre 2014-1 e 2026-1, doze anos depois, a correlação é 0,82.

## Pergunta

O ranking das ofertas pela nota de corte é estável de uma edição para a seguinte?

## Dados usados

- `data/notas_corte.csv`: chamada regular, cota `AC`, campus Belo Horizonte.
- Em cada par de edições entram só as ofertas presentes nas duas.

## Método

A **correlação de Spearman** (ρ) compara as posições de cada oferta nos dois rankings. ρ = 1 significa ranking idêntico; ρ = 0, nenhuma relação. A fórmula, sem empates, é `ρ = 1 − 6·Σd² / (n·(n² − 1))`, em que `d` é a diferença de posição de cada oferta e `n` o número de ofertas. Também mostramos dois pares de longo prazo (2014-1→2026-1 e 2018-1→2026-1).

## Resultados

**Tabela 1 – Correlação de Spearman entre rankings.**

| De | Para | ofertas em comum | rho | p-valor | Tipo |
|---|---|---|---|---|---|
| 2014-1 | 2014-2 | 48 | 0,957 | 2,2e-26 | consecutivas |
| 2014-2 | 2015-1 | 47 | 0,951 | 1,4e-24 | consecutivas |
| 2015-1 | 2015-2 | 48 | 0,977 | 2,5e-32 | consecutivas |
| 2015-2 | 2016-1 | 55 | 0,933 | 3,8e-25 | consecutivas |
| 2016-1 | 2017-1 | 81 | 0,911 | 3,6e-32 | consecutivas |
| 2017-1 | 2018-1 | 79 | 0,924 | 6,6e-34 | consecutivas |
| 2018-1 | 2019-1 | 84 | 0,980 | 3,0e-59 | consecutivas |
| 2019-1 | 2020-1 | 84 | 0,987 | 1,0e-66 | consecutivas |
| 2020-1 | 2021-1 | 84 | 0,982 | 2,4e-61 | consecutivas |
| 2021-1 | 2022-1 | 84 | 0,982 | 3,7e-61 | consecutivas |
| 2022-1 | 2023-1 | 84 | 0,990 | 1,0e-70 | consecutivas |
| 2023-1 | 2024-1 | 82 | 0,984 | 3,3e-62 | consecutivas |
| 2024-1 | 2025-1 | 76 | 0,985 | 1,6e-58 | consecutivas |
| 2025-1 | 2026-1 | 85 | 0,985 | 1,3e-65 | consecutivas |
| 2014-1 | 2026-1 | 53 | 0,815 | 1,1e-13 | longo prazo |
| 2018-1 | 2026-1 | 73 | 0,966 | 3,0e-43 | longo prazo |

![Estabilidade](../figuras/16_estabilidade_ranking.png)

*Figura 1 – Correlação de Spearman entre edições consecutivas; linhas tracejadas = pares de longo prazo. Fonte: SISU/UFMG; elaboração própria.*

## Interpretação

- O ranking é muito estável. Saber a posição de um curso num ano dá uma ótima ideia da posição no ano seguinte, mas não da nota exata, que muda com o ENEM.
- As menores correlações estão entre 2015-2 e 2018-1, período que inclui as edições de chamada única (2016 e 2017) e a troca de códigos de cota em 2018. De 2018 em diante, ρ é sempre de pelo menos 0,98.
- O par 2024-1→2025-1 tem menos ofertas em comum (76) porque vários cursos trocaram o turno Matutino por Integral ou Vespertino em 2025 (post 07).

## Limitações e ressalvas

- O p-valor testa só se ρ é diferente de zero, o que aqui é óbvio. Ele não mede se a estabilidade é "alta".
- O ρ não usa o número de vagas nem de candidatos, que a base não tem.
- Ofertas que existem em uma só das edições do par ficam de fora.

## Como reproduzir

```bash
python scripts/16_estabilidade_ranking.py
```
