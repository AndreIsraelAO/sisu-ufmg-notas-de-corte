# Entre 2018 e 2026, 69 de 79 ofertas subiram a nota de corte, e a maior alta foi de 37,7 pontos

**Resumo.** Comparando 2018-1 e 2026-1 (ampla concorrência, chamada regular), a nota de corte mediana das ofertas subiu 12,9 pontos. A maior alta foi de **Terapia Ocupacional – Matutino** (+37,7). A maior queda foi de **Aquacultura – Matutino** (-15,2).

## Pergunta

Quais ofertas tiveram as maiores altas e quedas de nota de corte entre 2018 e 2026?

## Dados usados

- `data/notas_corte.csv`: chamada regular, cota `AC`, dois campi.
- Ofertas presentes em 2018, 2019, 2025 e 2026 (79 ofertas). Cursos com turno renomeado em 2025 (post 07) ficam de fora.
- **Por que só AC:** 2018 está na era de cotas E2 (códigos 1.1–4.2) e 2026 na E3 (LB/LI). A ampla concorrência é o único grupo com mesmo código e mesma regra nas duas pontas (confiança alta). Comparar cotas entre 2018 e 2026 misturaria a mudança da nota com a mudança de regra (post 12).

## Método

- `variação = nota(2026-1) − nota(2018-1)`.
- `variação relativa = variação − mediana das variações de todas as ofertas`. Desconta o movimento geral das notas, que inclui as mudanças do ENEM.
- **Robustez:** a mesma conta com a média de dois anos em cada ponta (2018–2019 → 2025–2026), para reduzir o efeito de um ano atípico. A correlação de Spearman entre as duas versões é 0,91.

## Resultados

**Tabela 1 – As 10 maiores altas.**

| oferta | 2018 | 2026 | variação 2018→2026 | variação relativa | variação (média 2018–19 → 2025–26) |
|---|---|---|---|---|---|
| Terapia Ocupacional – Matutino | 678,2 | 715,9 | 37,7 | 24,8 | 26,2 |
| Estatística – Matutino | 708,7 | 743,4 | 34,7 | 21,9 | 24,3 |
| Ciências Econômicas – Matutino | 747,1 | 780,9 | 33,9 | 21,0 | 17,0 |
| Psicologia – Matutino | 740,2 | 771,1 | 30,8 | 17,9 | 18,0 |
| Educação Física (Lic.) – Matutino | 669,6 | 697,8 | 28,2 | 15,3 | 17,0 |
| Farmácia – Noturno | 708,2 | 735,8 | 27,6 | 14,7 | 14,4 |
| Nutrição – Matutino | 718,5 | 745,3 | 26,8 | 13,9 | 16,7 |
| Engenharia de Sistemas – Noturno | 725,3 | 752,0 | 26,7 | 13,8 | 22,0 |
| Engenharia Aeroespacial – Matutino | 768,0 | 794,4 | 26,4 | 13,5 | 14,9 |
| Farmácia – Matutino | 720,4 | 746,1 | 25,8 | 12,9 | 17,5 |

**Tabela 2 – As 10 menores variações.**

| oferta | 2018 | 2026 | variação 2018→2026 | variação relativa | variação (média 2018–19 → 2025–26) |
|---|---|---|---|---|---|
| Aquacultura – Matutino | 662,7 | 647,5 | -15,2 | -28,0 | -18,1 |
| Engenharia Florestal – Matutino, MOC | 656,4 | 642,0 | -14,5 | -27,3 | -18,3 |
| Turismo – Matutino | 677,0 | 663,3 | -13,7 | -26,5 | -22,0 |
| Química Tecnológica – Noturno | 706,1 | 697,8 | -8,3 | -21,1 | -11,2 |
| Engenharia Agrícola e Ambiental – Matutino, MOC | 657,7 | 651,4 | -6,3 | -19,1 | -6,1 |
| Ciências do Estado – Vespertino | 715,5 | 713,0 | -2,5 | -15,4 | -4,5 |
| Geografia – Noturno | 672,3 | 669,9 | -2,4 | -15,3 | -12,7 |
| Geologia – Matutino | 719,0 | 717,8 | -1,2 | -14,1 | 3,2 |
| Radiologia – Noturno | 670,6 | 669,6 | -1,0 | -13,9 | -2,4 |
| Engenharia de Alimentos – Matutino, MOC | 676,9 | 676,4 | -0,6 | -13,4 | -20,4 |

![Altas e quedas](../figuras/19_altas_quedas.png)

*Figura 1 – Variação da nota de corte entre 2018-1 e 2026-1 nas 10 ofertas que mais subiram e nas 10 que menos subiram (ou caíram). Fonte: SISU/UFMG; elaboração própria.*

## Interpretação

- A maior parte das ofertas subiu. A variação relativa (descontada a mediana) é a melhor forma de ver quem se destacou em relação às outras.
- Uma alta grande está associada a mais procura relativa ou a menos vagas. A base não tem nenhum dos dois, então não há como apontar o motivo.
- A versão com média de dois anos ordena as ofertas de forma muito parecida (ρ = 0,91). Isso indica que o resultado não depende de um único ano atípico.

## Limitações e ressalvas

- As notas do ENEM são padronizadas a cada edição, e o número de vagas, as regras de cota e o perfil dos candidatos mudam de um ano para outro. Diferenças entre anos mostram o que foi observado, não uma mudança na "dificuldade" do curso.
- Nota de corte é a nota do último classificado. Ela depende de quantas pessoas se inscreveram, de suas notas e do número de vagas; não mede a qualidade do curso. A base não traz o número de candidatos, então "mais concorrido" aqui significa "maior nota de corte".
- Comparação de duas pontas: não diz nada sobre o caminho entre elas (veja os posts 01 e 17).

## Como reproduzir

```bash
python scripts/19_altas_quedas.py
```
