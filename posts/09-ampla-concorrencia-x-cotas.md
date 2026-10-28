# Em 2024–2026, nenhuma cota teve nota de corte acima da ampla concorrência, e a distância vai de 10 a 160 pontos

**Resumo.** Em 2024–2026, no mesmo curso, turno e edição, a nota de corte da ampla concorrência ficou acima da nota da cota em 100% dos 1738 pares. A menor distância mediana é a da cota LI_EP (10,2 pontos) e a maior é a da LB_Q (159,3 pontos).

## Pergunta

Qual a diferença de nota de corte entre a ampla concorrência e cada modalidade de cota, curso a curso?

## Dados usados

- `data/notas_corte.csv`: chamada regular. Cada cota é comparada com a AC da mesma oferta (curso × campus × turno) e edição.
- Período principal: 2024–2026, quando todos os códigos são da era E3 (confiança **alta**). Os códigos `LB_PPI_PCD`/`LI_PPI_PCD` (confiança baixa) estão excluídos. `LI_Q` tem só 2 linhas e também foi excluída.
- Séries anteriores a 2024 aparecem nos posts 10 e 12, que tratam da comparação entre eras.

## Método

`diferença = nota(AC) − nota(cota)` em cada par. Valor positivo indica que a cota teve nota de corte menor. Resumimos pela mediana, pelo intervalo interquartil (p25–p75, onde fica a metade central dos pares) e pela % de pares em que a cota teve nota maior que a AC.

Siglas: **LB** = escola pública e renda baixa (até 1 salário mínimo per capita em 2024+); **LI** = escola pública, qualquer renda; **PPI** = pretos, pardos e indígenas; **EP** = só escola pública; **PCD** = pessoa com deficiência; **Q** = quilombola.

## Resultados

**Tabela 1 – Diferença AC − cota, 2024–2026.**

| Cota | Descrição | Pares | Mediana | Média | p25 | p75 | % cota > AC |
|---|---|---|---|---|---|---|---|
| LI_EP | Escola pública (qualquer renda) | 277 | 10,2 | 11,1 | 6,8 | 14,8 | 0,0 |
| LB_EP | Escola pública, renda baixa | 277 | 34,6 | 35,5 | 26,0 | 44,2 | 0,0 |
| LI_PPI | Escola pública, PPI (qualquer renda) | 277 | 57,0 | 57,7 | 45,9 | 68,6 | 0,0 |
| LB_PPI | Escola pública, renda baixa, PPI | 277 | 91,1 | 94,7 | 77,5 | 110,2 | 0,0 |
| LI_PCD | Escola pública, PCD (qualquer renda) | 255 | 92,6 | 101,1 | 67,1 | 123,1 | 0,0 |
| LB_PCD | Escola pública, renda baixa, PCD | 227 | 157,0 | 170,6 | 125,3 | 205,4 | 0,0 |
| LB_Q | Escola pública, renda baixa, quilombola | 148 | 159,3 | 163,7 | 114,7 | 208,7 | 0,0 |

![AC x cotas](../figuras/09_ac_cotas.png)

*Figura 1 – Distribuição da diferença AC − cota por modalidade, 2024–2026. Fonte: SISU/UFMG; elaboração própria.*

**Tabela 2 – Cota LB_PPI: ofertas com menor e maior distância média para a AC (2024–2026).**

| Menor distância | AC − LB_PPI |
|---|---|
| Zootecnia – Matutino, MOC | 59,1 |
| Radiologia – Noturno | 60,4 |
| Ciências da Natureza e Matemática (Lic.) – Noturno, MOC | 63,5 |
| Enfermagem – Matutino | 63,7 |
| Pedagogia – Noturno | 65,4 |

| Maior distância | AC − LB_PPI |
|---|---|
| Física – Vespertino | 148,3 |
| Física – Matutino | 147,3 |
| Estatística – Matutino | 139,3 |
| Engenharia Química – Matutino | 136,7 |
| Engenharia Metalúrgica e Engenharia de Materiais – Matutino | 135,6 |

## Interpretação

- A ordem é clara: LI_EP < LB_EP < LI_PPI < LB_PPI < cotas PCD e quilombola. Cada recorte adicional (renda, raça, deficiência) está associado a uma distância maior. A distância está associada ao grupo de candidatos de cada modalidade e ao número de vagas de cada uma, não a "quanto mais fácil" é entrar.
- Em cotas com poucas vagas (PCD, quilombola), a dispersão é enorme: um único candidato define a nota de corte.
- Nenhum par de 2024–2026 teve cota com nota acima da AC. Isso é compatível com a regra em que o candidato cotista concorre primeiro na ampla concorrência: quem tem nota para a AC entra por ela, e a cota fica com as notas menores. Antes de 2024 isso acontecia em parte das ofertas (post 10).

## Limitações e ressalvas

- Nota de corte é a nota do último classificado. Ela depende de quantas pessoas se inscreveram, de suas notas e do número de vagas; não mede a qualidade do curso. A base não traz o número de candidatos, então "mais concorrido" aqui significa "maior nota de corte".
- Só 2024–2026. Comparar com eras anteriores exige as equivalências de confiança média (post 12).
- A base não informa vagas por modalidade.

## Como reproduzir

```bash
python scripts/09_ac_cotas.py
```
