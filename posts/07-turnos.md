# O noturno tem nota de corte menor que o turno diurno em 85% das comparações

**Resumo.** Comparando o mesmo curso, edição e campus (ampla concorrência, chamada regular), o Noturno teve nota de corte menor que o turno diurno em 85% dos 241 pares, com diferença mediana de -13,4 pontos. As maiores diferenças estão em Geografia, Ciências Biológicas, Letras (Lic.), Letras. Só em Letras (sem modalidade, pré-2018) (Lic.) e Biblioteconomia o noturno teve, em média, nota um pouco maior.

## Pergunta

Nos cursos com mais de um turno, existe diferença de nota de corte entre Matutino, Vespertino, Noturno e Integral?

## Dados usados

- `data/notas_corte.csv`: chamada regular, cota `AC`, dois campi, 15 edições.
- Cursos que, na **mesma edição e campus**, têm o turno Noturno e um turno diurno.

**Achado de dados que mudou a análise:** Matutino, Vespertino e Integral **nunca coexistem** no mesmo curso e edição (o script verifica isso). A única comparação possível é **Noturno × turno diurno**. Além disso, em 2025 o turno diurno de 7 cursos mudou de nome:

| Curso | Campus | Turno em 2024-1 | Turno em 2025-1 |
|---|---|---|---|
| Fisioterapia | Belo Horizonte | Matutino | Integral |
| Fonoaudiologia | Belo Horizonte | Matutino | Integral |
| Física | Belo Horizonte | Matutino | Vespertino |
| História | Belo Horizonte | Matutino | Vespertino |
| Matemática Computacional | Belo Horizonte | Matutino | Vespertino |
| Medicina Veterinária | Belo Horizonte | Matutino | Integral |
| Odontologia | Belo Horizonte | Matutino | Integral |

Essas mudanças podem refletir reorganização de horários, e não um curso novo. Uma comparação "Integral × Matutino" do mesmo curso seria, na prática, uma comparação 2024 × 2025.

## Método

Para cada curso, campus e edição: `diferença = nota(Noturno) − nota(turno diurno)`. Resumimos pela mediana, pela média e pela % de pares em que o noturno teve nota menor.

## Resultados

**Tabela 1 – Resumo por turno diurno de referência.**

| Turno diurno | Pares (curso × edição) | Cursos | Diferença mediana | Diferença média | % com Noturno menor |
|---|---|---|---|---|---|
| Matutino | 237 | 20 | -13,2 | -12,3 | 85,2 |
| Vespertino | 4 | 2 | -21,1 | -20,8 | 100,0 |
| Todos | 241 | 20 | -13,4 | -12,4 | 85,5 |

**Tabela 2 – Diferença por curso (Noturno − diurno).**

| curso | Edições | Diferença média | Mínima | Máxima | % com Noturno menor |
|---|---|---|---|---|---|
| Geografia | 11 | -28,5 | -40,3 | -20,2 | 100,0 |
| Ciências Biológicas | 13 | -27,5 | -43,9 | -20,2 | 100,0 |
| Letras (Lic.) | 9 | -27,1 | -36,3 | -14,0 | 100,0 |
| Letras | 9 | -25,0 | -35,6 | -14,8 | 100,0 |
| Química | 11 | -23,7 | -36,3 | -6,5 | 100,0 |
| História | 11 | -20,2 | -43,0 | -9,0 | 100,0 |
| Engenharia Mecânica | 15 | -18,3 | -38,6 | 25,6 | 93,3 |
| Física | 12 | -16,6 | -27,7 | 21,2 | 91,7 |
| Arquitetura e Urbanismo | 15 | -12,4 | -23,2 | 10,7 | 86,7 |
| Jornalismo | 11 | -12,2 | -31,3 | 33,6 | 90,9 |
| Direito | 15 | -8,2 | -15,4 | 16,1 | 80,0 |
| Engenharia de Controle e Automação | 15 | -8,0 | -32,3 | 18,8 | 86,7 |
| Administração | 11 | -7,6 | -20,5 | 13,2 | 81,8 |
| Matemática | 12 | -7,2 | -23,8 | 14,7 | 83,3 |
| Filosofia | 13 | -5,6 | -30,1 | 27,4 | 69,2 |
| Pedagogia | 11 | -4,8 | -14,0 | 14,9 | 81,8 |
| Educação Física | 13 | -1,6 | -20,8 | 23,1 | 76,9 |
| Farmácia | 15 | -1,5 | -29,4 | 59,4 | 80,0 |
| Letras (sem modalidade, pré-2018) (Lic.) | 6 | 0,0 | -25,3 | 26,0 | 50,0 |
| Biblioteconomia | 13 | 0,6 | -15,9 | 23,2 | 53,8 |

![Turnos](../figuras/07_turnos.png)

*Figura 1 – Diferença média entre a nota de corte do Noturno e a do turno diurno, por curso. Fonte: SISU/UFMG; elaboração própria.*

## Interpretação

- O padrão dominante é o noturno com nota de corte menor. Nos quatro cursos com maior diferença ela fica entre 25,0 e 28,5 pontos em média.
- Em cursos como Direito, Farmácia e Biblioteconomia a diferença média é pequena e muda de sinal entre edições.
- A diferença observada é compatível com menor procura pelo noturno entre candidatos de nota alta. A base não tem dados de procura nem de vagas para confirmar.

## Limitações e ressalvas

- Nota de corte é a nota do último classificado. Ela depende de quantas pessoas se inscreveram, de suas notas e do número de vagas; não mede a qualidade do curso. A base não traz o número de candidatos, então "mais concorrido" aqui significa "maior nota de corte".
- As notas do ENEM são padronizadas a cada edição, e o número de vagas, as regras de cota e o perfil dos candidatos mudam de um ano para outro. Diferenças entre anos mostram o que foi observado, não uma mudança na "dificuldade" do curso.
- Turnos do mesmo curso podem ter número de vagas e currículo diferentes. A diferença não é só efeito do horário.
- Em 2014 os rótulos "Diurno" e "Tarde" foram convertidos para Matutino e Vespertino na construção da base (post 20).

## Como reproduzir

```bash
python scripts/07_turnos.py
```
