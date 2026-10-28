# A cota PCD existe desde 2018 e tem as notas de corte mais dispersas da base

**Resumo.** As cotas para pessoas com deficiência (PCD) aparecem a partir de 2018. Em 2026-1 havia linha de LB_PCD em 98% e de LI_PCD em 100% das ofertas. Em 2024–2026, a nota de corte mediana da LI_PCD ficou 92,6 pontos abaixo da ampla concorrência do mesmo curso. Em 44% das linhas LB_PCD a nota mínima é igual à máxima, sinal de um único aprovado no grupo.

## Pergunta

Onde aparece a cota PCD, em quais cursos e com que nota de corte?

## Dados usados

- `data/notas_corte.csv`: chamada regular, dois campi.
- Cotas PCD: `LB_PCD` e `LI_PCD` (2018–2023 com confiança média; 2024+ alta) e os códigos legados `LB_PPI_PCD` e `LI_PPI_PCD` (2018–2023, PPI + PCD, confiança **baixa**). Os legados aparecem só na contagem de presença e **não** são comparados com 2024+.
- Comparação de notas restrita a 2024–2026 (era E3).

## Método

- **Presença:** % das ofertas (curso × campus × turno) da edição que têm uma linha da cota na chamada regular. Ausência de linha significa que o PDF não listou classificado naquela cota. Pode ser vaga não ofertada ou sem candidato aprovado; a base não diferencia.
- **Nota:** mediana, mínimo e máximo da nota de corte e a diferença para a AC da mesma oferta (`AC − PCD`).
- **Indício de vaga única:** `nota_min == nota_max`, ou seja, um só aprovado (ou empate).

## Resultados

**Tabela 1 – Presença das cotas PCD (% das ofertas da edição).**

| Edição | LB_PCD | LB_PPI_PCD | LI_PCD | LI_PPI_PCD |
|---|---|---|---|---|
| 2014-1 | – | – | – | – |
| 2014-2 | – | – | – | – |
| 2015-1 | – | – | – | – |
| 2015-2 | – | – | – | – |
| 2016-1 | – | – | – | – |
| 2017-1 | – | – | – | – |
| 2018-1 | 93,3 | 96,7 | 91,1 | 98,9 |
| 2019-1 | 64,4 | 88,9 | 51,1 | 88,9 |
| 2020-1 | 62,2 | 87,8 | 47,8 | 78,9 |
| 2021-1 | 55,6 | 80,0 | 47,8 | 76,7 |
| 2022-1 | 53,3 | 63,3 | 41,1 | 60,0 |
| 2023-1 | 48,9 | 67,8 | 46,7 | 62,2 |
| 2024-1 | 70,3 | – | 83,5 | – |
| 2025-1 | 77,2 | – | 92,4 | – |
| 2026-1 | 97,9 | – | 100,0 | – |

**Tabela 2 – Notas de corte das cotas PCD, 2024–2026.**

| Cota | Linhas | Ofertas | Nota mediana | Menor nota | Maior nota | AC − PCD (mediana) | % mín = máx |
|---|---|---|---|---|---|---|---|
| LB_PCD | 227 | 100 | 556,3 | 302,7 | 744,7 | 157,0 | 44,5 |
| LI_PCD | 255 | 102 | 621,4 | 386,9 | 784,0 | 92,6 | 38,4 |

![Cota PCD](../figuras/11_cota_pcd.png)

*Figura 1 – Esquerda: presença das cotas PCD por edição. Direita: distribuição das notas de corte PCD e da AC nas mesmas ofertas, 2024–2026. Fonte: SISU/UFMG; elaboração própria.*

**Tabela 3 – As 5 menores notas de corte PCD da série (2018–2026).**

| Edição | Oferta | Cota | Nota de corte | Nota máxima | Nota AC |
|---|---|---|---|---|---|
| 2020-1 | Física – Matutino | LI_PPI_PCD | 263,76 | 263,76 | 726,32 |
| 2023-1 | Geografia – Matutino | LB_PPI_PCD | 299,00 | 299,00 | 663,92 |
| 2022-1 | Engenharia Civil – Matutino | LB_PPI_PCD | 300,08 | 441,98 | 723,80 |
| 2025-1 | Ciências do Estado – Vespertino | LB_PCD | 302,74 | 302,74 | 699,22 |
| 2025-1 | Letras (Lic.) – Noturno | LB_PCD | 313,34 | 402,02 | 666,42 |

Ofertas da chamada regular de 2026-1 **sem** nenhuma linha PCD: nenhuma.

## Interpretação

- A presença da cota PCD caiu entre 2018 e 2023 e voltou a subir a partir de 2024, quando o sistema de códigos mudou. A base não permite dizer se isso reflete mais vagas ofertadas ou mais aprovados.
- As notas PCD são muito dispersas. Com uma ou duas vagas por grupo, um único candidato define a nota de corte, o que gera valores extremos (Tabela 3). A média da cota PCD de um curso não deve ser usada como referência de "nota necessária".

## Limitações e ressalvas

- A equivalência 2018–2023 → 2024+ é de confiança média (`LB_PCD`, `LI_PCD`) ou baixa (códigos PPI+PCD). Em 2018–2023 havia duas cotas PCD por faixa de renda (com e sem PPI), e em 2024+ só uma.
- Em 2024 a LB_PCD e a LI_PCD aparecem só em parte dos cursos (veja o relatório da base).
- As notas do ENEM e as vagas mudam a cada ano.

## Como reproduzir

```bash
python scripts/11_cota_pcd.py
```
