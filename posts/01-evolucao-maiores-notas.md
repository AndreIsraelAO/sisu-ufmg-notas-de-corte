# As maiores notas de corte da UFMG subiram, e Medicina segue isolada no topo

**Resumo.** Entre as ofertas de Belo Horizonte com série longa, as 10 com maior nota de corte em 2024–2026 são, em geral, as mesmas engenharias e cursos de prestígio. 10 das 10 tiveram em 2026 nota maior que em 2014 (mediana de 29,0 pontos). **Medicina – Integral** lidera com média de 814,6 pontos em 2024–2026.

## Pergunta

Como evoluiu, de 2014 a 2026, a nota de corte das ofertas com as maiores notas da UFMG em Belo Horizonte?

## Dados usados

- `data/notas_corte.csv`, filtrado em: chamada regular (menor chamada da edição), cota `AC` (ampla concorrência), campus Belo Horizonte.
- Unidade: **oferta** = curso (`curso_id`) × turno. Cada turno tem nota de corte própria.
- Ofertas elegíveis: presentes em 2024, 2025 e 2026 **e** em pelo menos 13 das 15 edições (58 de 110 ofertas). Isso deixa de fora cursos novos, como Ciência de Dados e Engenharia de Computação, que aparecem no post 02.

## Método

1. Para cada oferta, calculamos a média da nota de corte em 2024-1, 2025-1 e 2026-1.
2. As 10 maiores médias formam o grupo analisado.
3. Mostramos a série completa por edição (2014 e 2015 têm duas edições cada) e a variação simples `nota(2026-1) − nota(2014-1)`.

## Resultados

**Tabela 1 – Nota de corte (AC, chamada regular) em edições selecionadas.**

| oferta | 2014-1 | 2018-1 | 2022-1 | 2026-1 | média 2024–26 | variação 2014-1→2026-1 |
|---|---|---|---|---|---|---|
| Medicina – Integral | 795,22 | 796,18 | 811,06 | 818,50 | 814,59 | 23,28 |
| Engenharia Aeroespacial – Matutino | 774,28 | 768,04 | 782,30 | 794,44 | 790,19 | 20,16 |
| Direito – Matutino | 750,70 | 764,56 | 769,68 | 783,14 | 775,21 | 32,44 |
| Engenharia Química – Matutino | 771,74 | 768,12 | 767,06 | 779,90 | 770,64 | 8,16 |
| Engenharia Mecânica – Matutino | 751,66 | 756,62 | 757,18 | 781,34 | 767,71 | 29,68 |
| Ciências Econômicas – Matutino | 717,28 | 747,06 | 754,28 | 780,92 | 767,13 | 63,64 |
| Psicologia – Matutino | 714,12 | 740,24 | 756,58 | 771,06 | 763,78 | 56,94 |
| Biomedicina – Noturno | 720,10 | 747,34 | 764,44 | 769,24 | 763,26 | 49,14 |
| Direito – Noturno | 743,48 | 753,56 | 755,18 | 771,80 | 762,21 | 28,32 |
| Engenharia Elétrica – Matutino | 753,44 | 753,54 | 745,50 | 771,22 | 761,79 | 17,78 |

![Evolução das maiores notas](../figuras/01_evolucao_top10.png)

*Figura 1 – Nota de corte por edição das 10 ofertas com maior média em 2024–2026. Linhas tracejadas apenas distinguem as últimas séries. Fonte: SISU/UFMG; elaboração própria.*

## Interpretação

- As 10 ofertas ficaram mais próximas entre si: a distância entre a maior e a menor nota do grupo era de 81,1 pontos em 2014-1 e de 49,3 pontos em 2026-1.
- O grupo do topo é estável: Medicina, engenharias tradicionais (Aeroespacial, Química, Mecânica), Direito e Economia estão perto do teto ao longo de toda a série.
- A segunda edição de 2014 e de 2015 (`2014-2`, `2015-2`) costuma ter notas menores que a primeira. Isso é associado à edição, não a uma queda do curso. Por isso as edições nunca são juntadas por ano.
- A alta observada em 2026 em várias ofertas é uma **diferença observada**. Não dá para dizer, só com esta base, se ela vem de mais candidatos, de menos vagas ou de mudança na escala do ENEM.

## Limitações e ressalvas

- Nota de corte é a nota do último classificado. Ela depende de quantas pessoas se inscreveram, de suas notas e do número de vagas; não mede a qualidade do curso. A base não traz o número de candidatos, então "mais concorrido" aqui significa "maior nota de corte".
- As notas do ENEM são padronizadas a cada edição, e o número de vagas, as regras de cota e o perfil dos candidatos mudam de um ano para outro. Diferenças entre anos mostram o que foi observado, não uma mudança na "dificuldade" do curso.
- Ciência da Computação (Matutino) deixa de existir em 2025 com esse nome. O curso combinado "Ciência da Computação e Sistemas de Informação" é tratado como outro curso (veja o post 20).
- 2016 e 2017 usam a chamada 11 e 10, que é a chamada regular única dessas edições.

## Como reproduzir

```bash
python scripts/01_evolucao_top10.py
```
