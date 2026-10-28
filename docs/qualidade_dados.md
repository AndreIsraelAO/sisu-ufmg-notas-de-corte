# Qualidade dos dados: validações e decisões de limpeza

Resumo para quem vai usar a base. O relatório completo da construção (incluindo a amostragem contra os PDFs) está em [`relatorio_qualidade_base.md`](relatorio_qualidade_base.md). As validações refeitas a cada execução estão no [post 20](../posts/20-guia-uso-e-qualidade.md).

## Origem

1. PDFs oficiais de notas máximas e mínimas por chamada, SISU/UFMG 2014–2026.
2. Transcrição para CSV (`UFMG_notasCorte_completo.csv`, 52.144 linhas; não incluído neste repositório).
3. Limpeza com `build.py` (não incluído, porque tem caminho fixo da máquina original), que gerou os CSVs de `data/`.

O projeto usa **apenas** os CSVs prontos de `data/`. Para reconstruir a base a partir do bruto seria preciso ajustar o caminho fixo `BASE` no `build.py` original.

## Validações feitas na construção da base

| Validação | Resultado |
|---|---|
| Linhas do CSV completo = soma dos CSVs por ano | 52.144 = 52.144 |
| Chave bruta e chave padronizada sem duplicatas | 0 duplicatas |
| Sem nulos; 0 < nota ≤ 1000; `nota_min ≤ nota_max` | 0 violações |
| Todo código de cota e todo nome de curso têm de-para | 0 sem mapeamento |
| `nota_min` nunca sobe entre chamadas; `nota_max` constante | 0 exceções em 8.405 chaves |
| Amostra aleatória contra os PDFs (5 por ano, seed 20260101) | 65 OK, 0 divergentes |
| Reconciliação de todas as linhas 2015+ com o texto dos PDFs | 0 linhas com valor ausente do PDF |

## Decisões de limpeza (herdadas da base)

| Decisão | Efeito |
|---|---|
| `Diurno` → Matutino e `Tarde` → Vespertino em 2014 | Inferido da correspondência com 2015; `turno_raw` preservado |
| Códigos de cota padronizados em LB/LI com sufixos | Equivalência entre eras com confiança alta, média ou baixa |
| 1.1 e 3.1 (PPI + PCD, 2018–2023) → `LB_PPI_PCD`, `LI_PPI_PCD` | Sem equivalente em 2024+; confiança baixa |
| Cursos renomeados **não** unidos | Antropologia, Eng. Metalúrgica, Ciência da Computação/Sistemas de Informação, Comunicação Social, Letras pré-2018 ficam com `curso_id` próprios |
| `is_final` = maior chamada presente nos dados | Em 2022 e 2023 há lacunas de chamada |

## Decisões tomadas neste projeto

| Decisão | Motivo | Onde |
|---|---|---|
| "Chamada regular" = menor chamada da edição | 2016 e 2017 têm só a chamada 11 e 10 (chamada única) | `scripts/comum.py` |
| Unidade = oferta (curso × campus × turno) | Cada turno tem nota de corte própria | Todos |
| Séries históricas só com chamada regular | 2014–2021 não têm listas de espera | 01, 02, 03, 10, 14, 16, 17, 19 |
| Comparações entre eras de cota só com confiança alta/média | Equivalências inferidas das legendas, sem edital | 09–12, 19 |
| Mapeamento de áreas próprio (`data/areas_conhecimento.csv`) | Não há classificação oficial na base | 18 |
| Edições 2014-2 e 2015-2 mantidas | São edições reais, com menos cursos; nunca juntadas com a 1ª | Todos |

## Limitações conhecidas

- Sem número de **vagas** e de **candidatos**: "concorrência" é sempre inferida pela nota de corte.
- Quilombolas de 2024 só no PDF (fora da base); LI_Q tem 2 linhas.
- Equivalência de cotas entre eras inferida das legendas dos PDFs, não dos editais.
- Notas do ENEM, vagas e regras mudam a cada ano.
