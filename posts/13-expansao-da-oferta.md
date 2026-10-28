# A oferta no SISU/UFMG passou de 77 para 94 ofertas, mas o salto de linhas vem das listas de espera

**Resumo.** O número de cursos na chamada regular foi de 68 (2014-1) para 74 (2026-1), e o de ofertas (curso × campus × turno) de 77 para 94. Os dois campi aparecem em todas as primeiras edições. O número de linhas da base passa de algumas centenas para mais de 10 mil a partir de 2023, efeito da publicação das listas de espera e das novas modalidades de cota, não da criação de cursos.

## Pergunta

Como mudou o tamanho da oferta da UFMG no SISU entre 2014 e 2026?

## Dados usados

- `data/notas_corte.csv`: chamada regular para contar cursos e ofertas; todas as chamadas para contar linhas.
- **Não há dado de vagas** na base. "Oferta" aqui é uma combinação curso × campus × turno que aparece no PDF, não o número de vagas.

## Método

Contagens distintas por edição. Para entradas e saídas de cursos, comparamos cada edição com a anterior, pulando as segundas edições de 2014 e 2015, que oferecem só parte dos cursos.

## Resultados

**Tabela 1 – Tamanho da oferta por edição.**

| Edição | Cursos | Ofertas | Campi | Códigos de cota | Linhas (regular) | Ofertas BH | Ofertas MOC | Linhas (todas) | Chamadas |
|---|---|---|---|---|---|---|---|---|---|
| 2014-1 | 68 | 77 | 2 | 5 | 382 | 71 | 6,00 | 382 | 1 |
| 2014-2 | 49 | 56 | 1 | 5 | 278 | 56 | – | 278 | 1 |
| 2015-1 | 66 | 78 | 2 | 5 | 390 | 72 | 6,00 | 390 | 1 |
| 2015-2 | 48 | 56 | 1 | 5 | 280 | 56 | – | 280 | 1 |
| 2016-1 | 68 | 87 | 2 | 5 | 435 | 81 | 6,00 | 435 | 1 |
| 2017-1 | 68 | 87 | 2 | 5 | 435 | 81 | 6,00 | 435 | 1 |
| 2018-1 | 70 | 90 | 2 | 9 | 792 | 84 | 6,00 | 792 | 1 |
| 2019-1 | 70 | 90 | 2 | 9 | 714 | 84 | 6,00 | 714 | 1 |
| 2020-1 | 70 | 90 | 2 | 9 | 699 | 84 | 6,00 | 699 | 1 |
| 2021-1 | 70 | 90 | 2 | 9 | 684 | 84 | 6,00 | 684 | 1 |
| 2022-1 | 70 | 90 | 2 | 9 | 646 | 84 | 6,00 | 3230 | 5 |
| 2023-1 | 70 | 90 | 2 | 9 | 653 | 84 | 6,00 | 11101 | 17 |
| 2024-1 | 71 | 91 | 2 | 7 | 595 | 85 | 6,00 | 10710 | 18 |
| 2025-1 | 72 | 92 | 2 | 9 | 684 | 85 | 7,00 | 10944 | 16 |
| 2026-1 | 74 | 94 | 2 | 9 | 738 | 87 | 7,00 | 11070 | 15 |

![Expansão](../figuras/13_expansao_oferta.png)

*Figura 1 – Esquerda: cursos e ofertas por edição. Direita: total de linhas por edição. Fonte: SISU/UFMG; elaboração própria.*

**Tabela 2 – Cursos que entram e saem (pelo `curso_id`).**

| Edição | Entram | Saem |
|---|---|---|
| 2015-1 | Comunicação Social - Jornalismo e Relações Públicas; Conservação e Restauração de Bens Culturais Móveis | Ciências Biológicas (Lic.); Comunicação Social - Jornalismo ou Relações Públicas; Física (Lic.); Matemática (Lic.) |
| 2016-1 | Jornalismo; Museologia; Publicidade e Propaganda; Relações Públicas | Comunicação Social - Jornalismo e Relações Públicas; Comunicação Social - Publicidade |
| 2018-1 | Design; Letras; Letras (Lic.) | Letras (sem modalidade, pré-2018) (Lic.) |
| 2024-1 | Antropologia e Arqueologia; Ciência de Dados; Engenharia Metalúrgica e Engenharia de Materiais | Antropologia; Engenharia Metalúrgica |
| 2025-1 | Ciência da Computação e Sistemas de Informação; Ciências da Natureza e Matemática (Lic.); Engenharia de Computação | Ciência da Computação; Sistemas de Informação |
| 2026-1 | Teatro; Teatro (Lic.) | — |

## Interpretação

- O crescimento de cursos e ofertas é modesto e concentrado em 2016 e em 2024–2026.
- Várias "entradas" e "saídas" são **renomeações**, não cursos novos. Exemplos: Comunicação Social → Jornalismo, Relações Públicas e Publicidade (2016); Antropologia → Antropologia e Arqueologia (2024); Engenharia Metalúrgica → Metalúrgica e de Materiais (2024); Ciência da Computação + Sistemas de Informação → curso combinado (2025). A base mantém `curso_id` separados nesses casos (post 20).
- O número de linhas não mede expansão da universidade. Ele cresce porque a base passa a ter listas de espera (2022+) e mais modalidades de cota (2018+, 2025+).

## Limitações e ressalvas

- Sem dado de vagas, não é possível medir a expansão real de oferta.
- As notas do ENEM e as vagas mudam a cada ano; esta análise só conta o que aparece nos PDFs.

## Como reproduzir

```bash
python scripts/13_expansao_oferta.py
```
