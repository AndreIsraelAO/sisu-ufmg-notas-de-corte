# Antes de tudo: como esta base funciona e onde ela engana

**Resumo.** A base tem 52.144 linhas e 15 edições do SISU/UFMG (2014–2026). Todas as 15 de 15 validações automáticas passaram. Os maiores riscos não são erros nos números, e sim armadilhas de uso: 2014 e 2015 têm duas edições, a nota de corte cai a cada chamada da lista de espera e os códigos de cota mudaram duas vezes.

## Pergunta

Os dados são confiáveis e quais regras evitam conclusões erradas nas outras 19 análises?

## Dados usados

- `data/notas_corte.csv`: base longa, uma linha por edição × curso × campus × turno × chamada × cota.
- `data/notas_corte_final.csv`: só a maior chamada de cada chave (`is_final == True`).
- `data/de_para_cursos.csv` e `data/de_para_cotas.csv`: tabelas de equivalência.
- Nenhum filtro: este post olha a base inteira.

## Método

O script `scripts/20_guia_qualidade.py` refaz, a partir dos CSVs prontos, as checagens que importam para as análises. Exemplos: a chave é única, `nota_min ≤ nota_max`, a nota mínima nunca sobe de uma chamada para a seguinte e `notas_corte_final.csv` é igual às linhas `is_final` da base longa. Se alguma falhar, o script para com erro. A conferência contra os PDFs oficiais foi feita na construção da base e está em [`docs/relatorio_qualidade_base.md`](../docs/relatorio_qualidade_base.md).

## Resultados

**Tabela 1 – Validações automáticas.**

| Validação | Resultado | Detalhe |
|---|---|---|
| Linhas da base longa | PASSOU | 52144 (esperado 52.144) |
| Linhas da base final | PASSOU | 8405 (esperado 8.405) |
| Chave única (edição × curso × campus × turno × chamada × cota) | PASSOU | 0 duplicatas |
| Final = uma linha por chave sem chamada | PASSOU | 8405 chaves |
| is_final marca a maior chamada da chave | PASSOU | comparado linha a linha |
| notas_corte_final.csv = linhas is_final da base longa | PASSOU | 8405 linhas casadas |
| nota_min ≤ nota_max | PASSOU | 0 violações |
| 0 < nota ≤ 1000 | PASSOU | mín 263.76, máx 863.9 |
| nota_min nunca sobe entre chamadas | PASSOU | 0 subidas |
| nota_max constante entre chamadas | PASSOU | 0 chaves com nota_max variável |
| Uma chamada regular por edição | PASSOU | 0 em todas, exceto 11 (2016) e 10 (2017) |
| Todo curso_id está em de_para_cursos.csv | PASSOU | 0 sem mapeamento |
| Confiança baixa só nos códigos legados PPI+PCD | PASSOU | LB_PPI_PCD, LI_PPI_PCD |
| 2024 sem cota quilombola na base (só no PDF) | PASSOU | 0 linhas |
| Toda oferta da chamada regular tem linha AC | PASSOU | ofertas comparadas |

**Tabela 2 – Cobertura por edição.** "Ofertas" = combinações curso × campus × turno.

| Edição | Linhas | Linhas (regular) | Linhas (final) | Ofertas | Cursos | Cotas | Chamadas presentes |
|---|---|---|---|---|---|---|---|
| 2014-1 | 382 | 382 | 382 | 77 | 68 | 5 | 0 |
| 2014-2 | 278 | 278 | 278 | 56 | 49 | 5 | 0 |
| 2015-1 | 390 | 390 | 390 | 78 | 66 | 5 | 0 |
| 2015-2 | 280 | 280 | 280 | 56 | 48 | 5 | 0 |
| 2016-1 | 435 | 435 | 435 | 87 | 68 | 5 | 11 |
| 2017-1 | 435 | 435 | 435 | 87 | 68 | 5 | 10 |
| 2018-1 | 792 | 792 | 792 | 90 | 70 | 9 | 0 |
| 2019-1 | 714 | 714 | 714 | 90 | 70 | 9 | 0 |
| 2020-1 | 699 | 699 | 699 | 90 | 70 | 9 | 0 |
| 2021-1 | 684 | 684 | 684 | 90 | 70 | 9 | 0 |
| 2022-1 | 3230 | 646 | 646 | 90 | 70 | 9 | 0, 4, 5, 10, 12 |
| 2023-1 | 11101 | 653 | 653 | 90 | 70 | 9 | 0, 1, 3, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19 |
| 2024-1 | 10710 | 595 | 595 | 91 | 71 | 7 | 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17 |
| 2025-1 | 10944 | 684 | 684 | 92 | 72 | 9 | 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 |
| 2026-1 | 11070 | 738 | 738 | 94 | 74 | 9 | 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14 |

![Linhas e chamadas por edição](../figuras/20_linhas_e_chamadas.png)

*Figura 1 – À esquerda, linhas por edição, separando chamada regular e listas de espera. À direita, quais chamadas existem em cada edição. Fonte: SISU/UFMG; elaboração própria.*

**Tabela 3 – Eras de cota e confiança da equivalência.**

| Era | Confiança | Códigos padronizados |
|---|---|---|
| E1_2014-2017 | alta | AC |
| E1_2014-2017 | media | LB_EP, LB_PPI, LI_EP, LI_PPI |
| E2_2018-2023 | alta | AC |
| E2_2018-2023 | baixa | LB_PPI_PCD, LI_PPI_PCD |
| E2_2018-2023 | media | LB_EP, LB_PCD, LB_PPI, LI_EP, LI_PCD, LI_PPI |
| E3_2024+ | alta | AC, LB_EP, LB_PCD, LB_PPI, LB_Q, LI_EP, LI_PCD, LI_PPI, LI_Q |

## Interpretação: as regras usadas em todo o projeto

1. **Edição, não ano.** 2014 e 2015 tiveram duas edições (`2014-1`, `2014-2`...). A segunda edição oferece menos cursos (56 ofertas em 2014-2 contra 77 em 2014-1). Todas as análises agrupam por `edicao_chave`.
2. **Chamada regular para séries longas.** De 2014 a 2021 só existe a chamada regular. A partir de 2022 aparecem as listas de espera, e a nota mínima cai a cada chamada. Misturar as duas coisas criaria uma "queda" artificial. Por isso as séries 2014–2026 usam a **chamada regular**, definida como a menor chamada da edição: 0 em quase todas, mas **11 em 2016 e 10 em 2017**, que tiveram um único PDF de chamada regular.
3. **Nota "final"** (`is_final`) só é usada quando a pergunta envolve a lista de espera (posts 04 e 15). Ela é a maior chamada *presente nos dados*: **2022 só tem as chamadas 0, 4, 5, 10, 12** e 2023 não tem as chamadas 2, 4 e 6.
4. **Cotas entre eras.** E1 (2014–2017) usava códigos 1–4, E2 (2018–2023) usava 1.1–4.2 e E3 (2024+) usa LB/LI. Comparações entre eras usam só equivalências de confiança alta ou média. Os códigos `LB_PPI_PCD` e `LI_PPI_PCD` (confiança baixa) nunca são comparados com outras eras. O limite de renda das cotas "LB" passou de 1,5 para 1 salário mínimo em 2024. As cotas "LI" (independentes de renda) não sofrem essa mudança e são as preferidas para séries longas.
5. **Quilombolas.** Em 2024 a lista de quilombolas existe só no PDF e não está na base. LB_Q e LI_Q aparecem a partir de 2025.
6. **Cursos renomeados.** O `curso_id` é estável, mas a base **não** uniu renomeações prováveis, como Antropologia → Antropologia e Arqueologia (2024) e Engenharia Metalúrgica → Metalúrgica e de Materiais (2024). Também não uniu Ciência da Computação e Sistemas de Informação → curso combinado (2025). Este projeto mantém essa decisão: cada nome é tratado como curso próprio.
7. **Turno 2014.** Os PDFs de 2014 dizem "Diurno" e "Tarde". A base converte para Matutino e Vespertino com base na correspondência com 2015 (`turno_ajustado`).

## Limitações e ressalvas

- A conferência contra os PDFs foi amostral (5 linhas por ano) mais uma reconciliação de valores para 2015+. Não houve releitura célula a célula.
- A base não tem número de vagas nem de candidatos. "Concorrência" é sempre inferida pela nota de corte.
- Grupos de cota com uma ou duas vagas (sobretudo PCD) podem ter notas de corte muito baixas ou muito altas por causa de um único candidato.
- As notas do ENEM e as vagas mudam a cada ano. Comparações no tempo descrevem o que foi observado, sem explicar a causa.
- A base é agregada por curso, campus, turno e cota e não contém dados pessoais.

## Como reproduzir

```bash
python scripts/20_guia_qualidade.py
```

Para rodar tudo: `python scripts/run_all.py`.
