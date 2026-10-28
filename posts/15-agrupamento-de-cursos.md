# Agrupando as ofertas pelo perfil de nota: 4 grupos

**Resumo.** Usando quatro medidas de 2024–2026 (nota de corte da AC, amplitude, distância para a cota LB_PPI e queda na lista de espera), o k-means separou 82 ofertas em 4 grupos. O número de grupos foi escolhido pelo maior coeficiente de silhueta (0,351). O grupo 1 reúne as 25 ofertas com nota de corte média de 745,5 pontos.

## Pergunta

As ofertas da UFMG formam grupos com perfis de nota parecidos?

## Dados usados

- `data/notas_corte.csv` (chamada regular) e `data/notas_corte_final.csv` (última chamada), edições 2024-1 a 2026-1 (era de cotas E3, confiança alta), dois campi.
- Só ofertas com as quatro medidas nas três edições (82 ofertas).

## Método

1. Para cada oferta, média de 2024–2026 de: Nota de corte AC; Amplitude AC (máx − mín); Distância AC − LB_PPI; Queda AC na lista de espera.
2. **Padronização** (z-score: subtrai a média e divide pelo desvio-padrão), para que nenhuma variável domine por ter escala maior.
3. **k-means** com k de 2 a 8 (`random_state=20260101`, 50 inicializações). O k-means junta ofertas cujas medidas estão próximas umas das outras.
4. **Escolha de k pela silhueta.** Para cada oferta, a silhueta compara a distância média ao próprio grupo (a) com a distância média ao grupo vizinho mais próximo (b): `s = (b − a) / max(a, b)`. Vai de −1 a 1; quanto maior a média, mais bem separados os grupos. A inércia ("cotovelo") aparece como apoio.

## Resultados

**Tabela 1 – Avaliação de k.**

| k | silhueta | inércia |
|---|---|---|
| 2 | 0,299 | 224,532 |
| 3 | 0,325 | 162,031 |
| 4 | 0,351 | 113,911 |
| 5 | 0,310 | 97,385 |
| 6 | 0,276 | 86,721 |
| 7 | 0,269 | 78,769 |
| 8 | 0,260 | 71,131 |

**Tabela 2 – Perfil médio de cada grupo (pontos).**

| Grupo | Ofertas | Nota de corte AC | Amplitude AC (máx − mín) | Distância AC − LB_PPI | Queda AC na lista de espera |
|---|---|---|---|---|---|
| 1 | 25 | 745,5 | 40,0 | 86,7 | 22,0 |
| 2 | 27 | 722,5 | 61,7 | 118,6 | 30,7 |
| 3 | 24 | 674,9 | 66,0 | 82,3 | 31,2 |
| 4 | 6 | 663,3 | 55,7 | 74,0 | 177,2 |

![Agrupamento](../figuras/15_agrupamento.png)

*Figura 1 – Esquerda: silhueta e inércia para cada k. Direita: ofertas coloridas por grupo, em duas das quatro variáveis. Fonte: SISU/UFMG; elaboração própria.*

**Membros de cada grupo:**

- **Grupo 1** (25): Administração – Matutino, Administração – Noturno, Arquitetura e Urbanismo – Noturno, Biomedicina – Noturno, Ciência de Dados – Vespertino, Direito – Matutino, Direito – Noturno, Educação Física – Noturno, Enfermagem – Matutino, Engenharia Aeroespacial – Matutino, Engenharia Mecânica – Noturno, Engenharia de Controle e Automação – Noturno, Engenharia de Sistemas – Noturno, Farmácia – Matutino, Farmácia – Noturno, História – Noturno, Jornalismo – Matutino, Jornalismo – Noturno, Medicina – Integral, Nutrição – Matutino, Psicologia – Matutino, Publicidade e Propaganda – Matutino, Relações Econômicas Internacionais – Noturno, Relações Públicas – Matutino, Terapia Ocupacional – Matutino
- **Grupo 2** (27): Arquitetura e Urbanismo – Matutino, Ciências Atuariais – Matutino, Ciências Biológicas – Matutino, Ciências Econômicas – Matutino, Ciências do Estado – Vespertino, Conservação e Restauração de Bens Culturais Móveis – Matutino, Controladoria e Finanças – Matutino, Engenharia Ambiental – Matutino, Engenharia Civil – Matutino, Engenharia Elétrica – Matutino, Engenharia Mecânica – Matutino, Engenharia Metalúrgica e Engenharia de Materiais – Matutino, Engenharia Química – Matutino, Engenharia de Controle e Automação – Matutino, Engenharia de Minas – Matutino, Engenharia de Produção – Matutino, Estatística – Matutino, Filosofia – Matutino, Física – Noturno, Geografia – Matutino, Geologia – Matutino, Letras (Lic.) – Matutino, Letras – Matutino, Matemática – Matutino, Matemática – Noturno, Química Tecnológica – Noturno, Química – Matutino
- **Grupo 3** (24): Antropologia e Arqueologia – Noturno, Aquacultura – Matutino, Arquivologia – Noturno, Biblioteconomia – Matutino, Biblioteconomia – Noturno, Ciências Biológicas – Noturno, Ciências Contábeis – Noturno, Ciências Sociais – Matutino, Ciências Socioambientais – Noturno, Design – Noturno, Educação Física (Lic.) – Matutino, Educação Física – Matutino, Filosofia – Noturno, Geografia – Noturno, Gestão Pública – Noturno, Gestão de Serviços de Saúde – Noturno, Letras (Lic.) – Noturno, Letras – Noturno, Museologia – Matutino, Pedagogia – Matutino, Pedagogia – Noturno, Química – Noturno, Radiologia – Noturno, Turismo – Matutino
- **Grupo 4** (6): Administração – Noturno, MOC, Agronomia – Matutino, MOC, Engenharia Agrícola e Ambiental – Matutino, MOC, Engenharia Florestal – Matutino, MOC, Engenharia de Alimentos – Matutino, MOC, Zootecnia – Matutino, MOC

## Interpretação

- **Grupo 1:** nota de corte alta, amplitude estreita e distância moderada para a LB_PPI (86,7 pontos). Reúne Medicina, Direito, cursos de saúde, comunicação e algumas engenharias noturnas.
- **Grupo 2:** nota um pouco menor que o grupo 1, mas com a **maior distância para a LB_PPI** (118,6 pontos). É formado quase só por engenharias diurnas e cursos de exatas (Estatística, Matemática, Física, Química, Economia). Ou seja, o agrupamento não é só uma ordenação por nota: a distância AC − cota separa exatas de saúde e humanas com nota parecida.
- **Grupo 3:** notas de corte menores, com cursos de humanidades, licenciaturas e cursos de nicho de BH.
- **Grupo 4:** as 6 ofertas de **Montes Claros**, marcadas sobretudo pela queda muito grande na lista de espera (177,2 pontos em média, contra 22,0–31,2 nos outros grupos).
- Uma silhueta média de 0,35 indica uma estrutura de grupos razoável. As fronteiras são graduais, não há "tipos" de curso bem separados.
- Os grupos descrevem perfis de nota. Não dizem nada sobre qualidade ou área do curso (post 18).

## Limitações e ressalvas

- O resultado depende das variáveis escolhidas e da padronização. Outras medidas dariam outros grupos.
- Só três edições, com ENEM e vagas diferentes em cada uma.
- O k-means supõe grupos aproximadamente "redondos" e de tamanho parecido.

## Como reproduzir

```bash
python scripts/15_agrupamento.py
```
