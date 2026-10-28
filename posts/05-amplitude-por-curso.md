# Ofertas com nota de corte mais alta têm turmas mais "apertadas"

**Resumo.** Em 2024–2026, a distância entre a maior e a menor nota dos aprovados na ampla concorrência (chamada regular) variou de 19,9 pontos (Biomedicina – Noturno) a 98,0 pontos (Matemática – Matutino). Quanto maior a nota de corte, menor tende a ser a amplitude (correlação de Spearman ρ = -0,54).

## Pergunta

Em quais ofertas a diferença entre o primeiro e o último aprovado é maior?

## Dados usados

- `data/notas_corte.csv`: chamada regular, cota `AC`, dois campi, edições 2024-1, 2025-1 e 2026-1.
- Só ofertas presentes nas três edições (82 ofertas).

## Método

- `amplitude = nota_max − nota_min`, em cada oferta e edição, depois a média das três edições. `nota_max` é a maior nota entre os aprovados do grupo e não muda entre chamadas. Usamos a chamada regular para não inflar a amplitude com as quedas da lista de espera (post 04).
- A associação entre nota de corte e amplitude é medida pela **correlação de Spearman** (ρ), que compara as posições (rankings) das duas variáveis. Vai de −1 a 1; valores negativos indicam que uma cresce quando a outra cai. p-valor = 1.9e-07.

## Resultados

**Tabela 1 – As 10 maiores amplitudes.**

| oferta | Edições | Nota mín. (corte) | Nota máx. | Amplitude |
|---|---|---|---|---|
| Matemática – Matutino | 3 | 707,4 | 805,4 | 98,0 |
| Conservação e Restauração de Bens Culturais Móveis – Matutino | 3 | 677,7 | 764,5 | 86,8 |
| Letras (Lic.) – Matutino | 3 | 695,8 | 779,0 | 83,1 |
| Turismo – Matutino | 3 | 650,3 | 729,9 | 79,7 |
| Geografia – Noturno | 3 | 656,4 | 734,4 | 78,0 |
| Aquacultura – Matutino | 3 | 640,7 | 718,6 | 77,9 |
| Letras (Lic.) – Noturno | 3 | 668,3 | 745,0 | 76,7 |
| Engenharia de Produção – Matutino | 3 | 751,4 | 825,2 | 73,9 |
| Gestão de Serviços de Saúde – Noturno | 3 | 653,2 | 726,8 | 73,6 |
| Ciências Socioambientais – Noturno | 3 | 666,5 | 739,2 | 72,7 |

**Tabela 2 – As 10 menores amplitudes.**

| oferta | Edições | Nota mín. (corte) | Nota máx. | Amplitude |
|---|---|---|---|---|
| Biomedicina – Noturno | 3 | 763,3 | 783,1 | 19,9 |
| Arquitetura e Urbanismo – Noturno | 3 | 741,2 | 767,2 | 26,0 |
| Engenharia Aeroespacial – Matutino | 3 | 790,2 | 817,3 | 27,1 |
| Engenharia de Controle e Automação – Noturno | 3 | 736,7 | 767,6 | 30,9 |
| Ciência de Dados – Vespertino | 3 | 764,9 | 798,1 | 33,2 |
| Engenharia de Sistemas – Noturno | 3 | 749,7 | 783,0 | 33,3 |
| Educação Física – Noturno | 3 | 697,8 | 731,5 | 33,6 |
| Ciências do Estado – Vespertino | 3 | 702,9 | 740,0 | 37,2 |
| Arquivologia – Noturno | 3 | 634,6 | 672,8 | 38,2 |
| Jornalismo – Noturno | 3 | 730,0 | 768,6 | 38,6 |

![Amplitude](../figuras/05_amplitude.png)

*Figura 1 – Esquerda: faixa entre a nota mínima e a máxima dos aprovados nas 10 maiores e 10 menores amplitudes. Direita: relação entre nota de corte e amplitude para todas as ofertas. Fonte: SISU/UFMG; elaboração própria.*

## Interpretação

- Há um efeito de "teto": a nota máxima do ENEM é limitada, então ofertas com nota de corte muito alta têm pouco espaço entre o último e o primeiro aprovado.
- A amplitude também está associada ao **número de vagas**, que a base não informa: mais vagas na AC tendem a abrir mais espaço entre o primeiro e o último aprovado. Por isso amplitude não deve ser lida como "diversidade" da turma.

## Limitações e ressalvas

- Nota de corte é a nota do último classificado. Ela depende de quantas pessoas se inscreveram, de suas notas e do número de vagas; não mede a qualidade do curso. A base não traz o número de candidatos, então "mais concorrido" aqui significa "maior nota de corte".
- A amplitude depende do número de vagas e de um único candidato com nota muito alta. Ela não descreve a distribuição completa das notas.
- Análise restrita a 2024–2026 e à ampla concorrência. Nas cotas há grupos com uma vaga, em que a amplitude é zero.

## Como reproduzir

```bash
python scripts/05_amplitude.py
```
