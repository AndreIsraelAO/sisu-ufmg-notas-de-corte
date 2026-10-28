# A distância entre ampla concorrência e escola pública subiu até 2016-1, caiu até 2020 e está estável desde então

**Resumo.** Na cota de escola pública independente de renda (LI_EP), a distância mediana para a ampla concorrência foi de 11,9 pontos em média em 2014–2017 e de 10,3 pontos em 2024–2026. Na cota de escola pública com renda baixa (LB_EP), os valores foram 33,4 e 34,8 pontos. A série não é uma linha reta: na LI_EP a distância saiu de valores negativos em 2014, chegou a 30,7 pontos em 2016-1 e voltou para cerca de 10 pontos a partir de 2020. Por isso a tendência linear do período todo é quase nula (0,04 ponto/ano).

## Pergunta

A diferença de nota de corte entre a ampla concorrência e as cotas de escola pública diminuiu ao longo do tempo?

## Dados usados

- `data/notas_corte.csv`: chamada regular, 15 edições, dois campi.
- Cotas: `LI_EP` (escola pública, qualquer renda) e `LB_EP` (escola pública, renda baixa). Nas três eras de códigos, as duas têm equivalência de confiança **média** (2014–2023) ou **alta** (2024+). Os códigos originais eram 4 / 4.2 / LI_EP e 2 / 2.2 / LB_EP.
- Cada cota é comparada com a AC da mesma oferta e edição.

## Método

1. `diferença = nota(AC) − nota(cota)` por oferta e edição. Resumo por edição: mediana e faixa p25–p75.
2. Tendência: regressão linear simples da mediana contra o tempo (`mediana = a + b × ano`, com as segundas edições em ano + 0,5). `b` é a variação média por ano. O intervalo de confiança aproximado é `b ± 1,96 × erro padrão`. Como a série claramente não é linear, também ajustamos a reta só para 2018–2026 (mesma era de códigos até 2023 e mesmo desenho de cotas). Com tão poucos pontos e mudanças de regra no meio da série, isso é uma descrição, não um teste forte.

## Resultados

**Tabela 1 – Diferença mediana AC − cota, por edição.**

| Edição | Escola pública, renda baixa (LB_EP) | Escola pública, qualquer renda (LI_EP) | % cota > AC – LB_EP | % cota > AC – LI_EP |
|---|---|---|---|---|
| 2014-1 | 26,9 | -1,7 | 20,8 | 53,3 |
| 2014-2 | 6,6 | -5,6 | 41,1 | 58,2 |
| 2015-1 | 39,8 | 6,2 | 16,7 | 43,6 |
| 2015-2 | 38,5 | 18,5 | 3,6 | 30,4 |
| 2016-1 | 47,9 | 30,7 | 3,4 | 16,1 |
| 2017-1 | 41,1 | 23,2 | 5,7 | 11,5 |
| 2018-1 | 34,9 | 17,3 | 0,0 | 3,3 |
| 2019-1 | 33,7 | 12,6 | 0,0 | 2,2 |
| 2020-1 | 30,0 | 9,5 | 3,3 | 12,2 |
| 2021-1 | 27,7 | 9,0 | 0,0 | 14,4 |
| 2022-1 | 31,9 | 7,7 | 0,0 | 18,9 |
| 2023-1 | 29,5 | 10,1 | 0,0 | 11,1 |
| 2024-1 | 34,5 | 10,1 | 0,0 | 0,0 |
| 2025-1 | 33,8 | 10,6 | 0,0 | 0,0 |
| 2026-1 | 36,2 | 10,1 | 0,0 | 0,0 |

**Tabela 2 – Tendência linear da mediana.**

| Cota | Inclinação (pontos/ano) | IC 95% aproximado | R² | p-valor |
|---|---|---|---|---|
| LI_EP | 0,04 | -1,17 a 1,24 | 0,00 | 0,953 |
| LB_EP | 0,20 | -1,03 a 1,43 | 0,01 | 0,755 |
| LI_EP, só 2018–2026 | -0,54 | -1,18 a 0,09 | 0,29 | 0,138 |
| LB_EP, só 2018–2026 | 0,27 | -0,48 a 1,02 | 0,07 | 0,499 |

![AC x escola pública](../figuras/10_ac_escola_publica.png)

*Figura 1 – Diferença mediana (linha) e faixa interquartil (sombra) entre AC e cotas de escola pública. Linhas pontilhadas marcam as mudanças de código de cota. Fonte: SISU/UFMG; elaboração própria.*

## Interpretação

- **Cota acima da AC.** Em 53% das ofertas de 2014-1, a nota de corte da LI_EP foi **maior** que a da AC. Essa fração caiu ao longo do tempo e é **zero de 2024 em diante**, nas duas cotas. Isso é compatível com regras de seleção em que quem tem nota para a AC entra por ela, deixando a cota para as notas menores. A base não contém as regras, então isso é uma hipótese.
- A subida até 2016 coincide com a implantação gradual da Lei de Cotas (Lei 12.711/2012), que dava às universidades até 2016 para reservar 50% das vagas. A base não tem o número de vagas por cota, então essa associação não pode ser testada aqui.
- O padrão observado também deve ser lido junto com as mudanças de regra posteriores: em 2018 entrou o recorte PCD separado e em 2024 o limite de renda da LB caiu de 1,5 para 1 salário mínimo. A série LI_EP é a mais limpa, porque não depende de renda.
- Uma distância menor indica que o último aprovado na cota ficou mais próximo do último aprovado na AC. Isso pode estar associado a mudanças no perfil dos candidatos, nas vagas ou nas regras de migração entre listas. A base não permite separar esses fatores.

## Limitações e ressalvas

- As notas do ENEM são padronizadas a cada edição, e o número de vagas, as regras de cota e o perfil dos candidatos mudam de um ano para outro. Diferenças entre anos mostram o que foi observado, não uma mudança na "dificuldade" do curso.
- A equivalência de códigos entre eras é de confiança **média**, inferida das legendas dos PDFs, sem confirmação no edital.
- O limite de renda da LB_EP mudou em 2024. A comparação da LB_EP antes e depois de 2024 não é exatamente do mesmo grupo.
- A regressão linear ignora a dependência entre anos e as mudanças de regra. O intervalo de confiança é só indicativo.

## Como reproduzir

```bash
python scripts/10_ac_escola_publica.py
```
