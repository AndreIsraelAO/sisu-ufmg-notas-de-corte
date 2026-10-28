# Projetar a nota de corte de 2027 com uma reta: um exercício com margem de erro de dezenas de pontos

**Resumo.** Ajustamos uma reta à nota de corte de 2018 a 2026 de 79 ofertas (ampla concorrência, chamada regular) e projetamos 2027. O intervalo de predição de 95% tem largura mediana de 52,1 pontos. Num retroteste (projetar 2026 com dados até 2025), o erro médio da reta foi 19,5 pontos, contra 13,2 pontos de simplesmente repetir a nota do ano anterior. **Isto é um exercício, não uma previsão confiável.**

## Pergunta

Se a tendência de 2018–2026 continuasse, qual seria a nota de corte de 2027 e quão incerta é essa conta?

## Dados usados

- `data/notas_corte.csv`: chamada regular, cota `AC`, dois campi, **2018 a 2026** (uma edição por ano, chamada 0). 2014–2017 ficam de fora por terem duas edições por ano ou chamada única com outro formato.
- Ofertas com pelo menos 7 anos e presentes em 2026 (79 ofertas).

## Método

1. **Regressão linear simples** por oferta: `nota = a + b × ano`. `b` é a variação média por ano.
2. **Projeção** para 2027 com **intervalo de predição de 95%**: `ŷ ± t(0,975; n−2) · s · √(1 + 1/n + (2027 − x̄)² / Σ(x − x̄)²)`, em que `s` é o desvio-padrão dos resíduos. Esse intervalo inclui a incerteza da reta e a variação de um ano isolado.
3. **Retroteste:** refazemos a conta sem 2026, projetamos 2026 e comparamos com o valor real. Medimos a % de vezes em que o valor real caiu dentro do intervalo e o erro médio absoluto, contra uma regra ingênua (repetir a nota de 2025).

## Resultados

**Tabela 1 – Retroteste (projeção de 2026 com dados até 2025).**

| Medida | Valor |
|---|---|
| Ofertas testadas | 79 |
| % com valor real dentro do IP 95% | 68,4% |
| Erro médio absoluto da reta | 19,5 pontos |
| Erro médio absoluto da regra "repetir 2025" | 13,2 pontos |
| Erro médio (real − projetado) | 19,5 pontos |

**Tabela 2 – Projeções para 2027: as 10 maiores.**

| oferta | pontos | inclinação (pts/ano) | nota 2026 | projeção 2027 | IP95 inferior | IP95 superior | largura IP95 |
|---|---|---|---|---|---|---|---|
| Medicina – Integral | 9 | 2,1 | 818,5 | 818,6 | 800,3 | 837,0 | 36,6 |
| Engenharia Aeroespacial – Matutino | 9 | 2,8 | 794,4 | 795,5 | 780,1 | 810,8 | 30,8 |
| Direito – Matutino | 9 | 1,6 | 783,1 | 777,6 | 761,0 | 794,3 | 33,3 |
| Engenharia Química – Matutino | 9 | 0,5 | 779,9 | 771,2 | 753,0 | 789,4 | 36,5 |
| Ciências Econômicas – Matutino | 9 | 2,3 | 780,9 | 770,6 | 748,3 | 792,8 | 44,5 |
| Psicologia – Matutino | 9 | 2,8 | 771,1 | 769,1 | 753,2 | 785,1 | 31,9 |
| Engenharia Mecânica – Matutino | 9 | 1,5 | 781,3 | 768,4 | 743,3 | 793,6 | 50,3 |
| Biomedicina – Noturno | 9 | 1,8 | 769,2 | 767,9 | 748,9 | 787,0 | 38,0 |
| Direito – Noturno | 9 | 1,2 | 771,8 | 763,2 | 744,3 | 782,2 | 37,9 |
| Arquitetura e Urbanismo – Matutino | 9 | 1,4 | 766,7 | 761,8 | 740,2 | 783,3 | 43,1 |

**Tabela 3 – Projeções para 2027: as 10 menores.**

| oferta | pontos | inclinação (pts/ano) | nota 2026 | projeção 2027 | IP95 inferior | IP95 superior | largura IP95 |
|---|---|---|---|---|---|---|---|
| Biblioteconomia – Matutino | 9 | 1,3 | 665,7 | 646,2 | 604,7 | 687,7 | 83,0 |
| Gestão de Serviços de Saúde – Noturno | 9 | -1,0 | 664,8 | 645,7 | 610,3 | 681,0 | 70,7 |
| Geografia – Noturno | 9 | -2,5 | 669,9 | 645,1 | 602,5 | 687,6 | 85,1 |
| Museologia – Matutino | 9 | -1,3 | 655,7 | 643,5 | 618,5 | 668,5 | 50,0 |
| Engenharia Agrícola e Ambiental – Matutino, MOC | 9 | -0,9 | 651,4 | 642,0 | 618,4 | 665,6 | 47,1 |
| Turismo – Matutino | 9 | -3,2 | 663,3 | 642,0 | 613,2 | 670,8 | 57,6 |
| Biblioteconomia – Noturno | 9 | 0,2 | 660,4 | 638,7 | 601,3 | 676,2 | 74,9 |
| Aquacultura – Matutino | 9 | -2,7 | 647,5 | 628,4 | 591,4 | 665,3 | 73,9 |
| Arquivologia – Noturno | 9 | -1,1 | 651,3 | 627,2 | 585,7 | 668,7 | 83,0 |
| Engenharia Florestal – Matutino, MOC | 9 | -2,1 | 642,0 | 625,6 | 594,3 | 657,0 | 62,8 |

![Tendência](../figuras/17_tendencia_projecao.png)

*Figura 1 – Exemplos de ajuste linear e projeção 2027 com intervalo de predição de 95%: a maior projeção, a maior e a menor inclinação e a menor projeção. Fonte: SISU/UFMG; elaboração própria.*

## Interpretação

- Só 11 das 79 retas têm inclinação estatisticamente diferente de zero (p < 0,05). Na maioria das ofertas a variação ano a ano é grande perto da tendência.
- No retroteste, o valor real de 2026 ficou dentro do intervalo em 68% dos casos. O erro médio (real − projetado) de 19,5 pontos mostra que 2026 veio acima da tendência na maioria das ofertas. Um ano atípico afeta todas as ofertas juntas, e a reta não antecipa isso. Um intervalo que se diz de 95% e acerta 68% das vezes está **estreito demais**: a incerteza real é maior que a calculada pelo modelo.
- A reta não superou a regra ingênua de repetir o ano anterior. Para um candidato, a faixa do intervalo importa mais que o número central.

## Limitações e ressalvas

- **Não use estes números para decidir inscrição.** A nota de corte de 2027 depende de vagas, número de inscritos, notas do ENEM 2026 e regras do SISU 2027, e nada disso está no modelo.
- As notas do ENEM são padronizadas a cada edição, e o número de vagas, as regras de cota e o perfil dos candidatos mudam de um ano para outro. Diferenças entre anos mostram o que foi observado, não uma mudança na "dificuldade" do curso.
- Com 7 a 9 pontos por oferta, a reta é muito sensível a um único ano. O intervalo supõe resíduos independentes e com distribuição normal, o que é só uma aproximação.
- Mudanças de regra no meio da série (cotas em 2024) não são modeladas, embora afetem menos a AC.

## Como reproduzir

```bash
python scripts/17_tendencia_projecao.py
```
