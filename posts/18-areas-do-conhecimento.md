# Ciências Exatas e Engenharias e Ciências da Saúde no topo, Ciências Biológicas e Agrárias embaixo, mas as áreas se sobrepõem muito

**Resumo.** Em 2024–2026, a área com maior nota de corte mediana (ampla concorrência, chamada regular) foi **Ciências Exatas e Engenharias** (736,7 pontos) e a menor foi **Ciências Biológicas e Agrárias** (669,8). A diferença entre as medianas extremas é de 66,9 pontos, menor que a variação dentro de várias áreas.

## Pergunta

Há diferença de nota de corte entre as áreas do conhecimento?

## Dados usados

- `data/notas_corte.csv`: chamada regular, cota `AC`, dois campi.
- `data/areas_conhecimento.csv`: **tabela de mapeamento criada para este projeto**, que liga cada um dos 88 `curso_id` a uma de seis áreas, com uma coluna de observação para os casos discutíveis.

### Como as áreas foram definidas

O mapeamento parte das grandes áreas do CNPq, com duas simplificações: Exatas e da Terra junto com Engenharias, e Biológicas junto com Agrárias. Os casos de fronteira estão documentados no CSV (coluna `observacao`). Exemplos: Biomedicina foi para Saúde (no CNPq fica em Biológicas); Ciências Atuariais foi para Sociais Aplicadas; Engenharias Florestal, Agrícola e de Alimentos foram para Agrárias, como no CNPq. Quem discordar pode editar o CSV e rodar o script de novo.

**Tabela 1 – Cursos por área no mapeamento.**

| Área | curso_id |
|---|---|
| Ciências Biológicas e Agrárias | agronomia-bach, aquacultura-bach, ciencias-biologicas-bach, ciencias-biologicas-lic, engenharia-agricola-e-ambiental-bach, engenharia-de-alimentos-bach, engenharia-florestal-bach, medicina-veterinaria-bach, zootecnia-bach |
| Ciências Exatas e Engenharias | ciencia-da-computacao-bach, ciencia-da-computacao-e-sistemas-de-informacao-bach, ciencia-de-dados-bach, ciencias-da-natureza-e-matematica-lic, engenharia-aeroespacial-bach, engenharia-ambiental-bach, engenharia-civil-bach, engenharia-de-computacao-bach, engenharia-de-controle-e-automacao-bach, engenharia-de-minas-bach, engenharia-de-producao-bach, engenharia-de-sistemas-bach, engenharia-eletrica-bach, engenharia-mecanica-bach, engenharia-metalurgica-bach, engenharia-metalurgica-e-engenharia-de-materiais-bach, engenharia-quimica-bach, estatistica-bach, fisica-bach, fisica-lic, geologia-bach, matematica-bach, matematica-computacional-bach, matematica-lic, quimica-bach, quimica-lic, quimica-tecnologica-bach, sistemas-de-informacao-bach |
| Ciências Humanas | antropologia-bach, antropologia-e-arqueologia-bach, ciencias-sociais-bach, ciencias-socioambientais-bach, filosofia-bach, geografia-bach, geografia-lic, historia-bach, historia-lic, pedagogia-bach, psicologia-bach |
| Ciências Sociais Aplicadas | administracao-bach, arquitetura-e-urbanismo-bach, arquivologia-bach, biblioteconomia-bach, ciencias-atuariais-bach, ciencias-contabeis-bach, ciencias-do-estado-bach, ciencias-economicas-bach, comunicacao-social-jornalismo-e-relacoes-publicas-bach, comunicacao-social-jornalismo-ou-relacoes-publicas-bach, comunicacao-social-publicidade-bach, controladoria-e-financas-bach, design-bach, direito-bach, gestao-publica-bach, jornalismo-bach, museologia-bach, publicidade-e-propaganda-bach, relacoes-economicas-internacionais-bach, relacoes-publicas-bach, turismo-bach |
| Ciências da Saúde | biomedicina-bach, educacao-fisica-bach, educacao-fisica-lic, enfermagem-bach, farmacia-bach, fisioterapia-bach, fonoaudiologia-bach, gestao-de-servicos-de-saude-bach, medicina-bach, nutricao-bach, odontologia-bach, radiologia-bach, terapia-ocupacional-bach |
| Linguística, Letras e Artes | conservacao-e-restauracao-de-bens-culturais-moveis-bach, letras-bach, letras-lic, letras-sem-modalidade-pre-2018-lic, teatro-bach, teatro-lic |

## Método

1. Média da nota de corte de 2024–2026 por oferta (curso × campus × turno).
2. Resumo por área: número de ofertas, média, mediana, mínimo e máximo.
3. Série histórica: mediana das ofertas da área em cada edição.

## Resultados

**Tabela 2 – Nota de corte por área, 2024–2026 (média por oferta).**

| Área | Ofertas | Média | Mediana | Mínimo | Máximo | Cursos no mapeamento (todas as edições) |
|---|---|---|---|---|---|---|
| Ciências Exatas e Engenharias | 31 | 736,4 | 736,7 | 619,7 | 790,2 | 28 |
| Ciências da Saúde | 18 | 725,1 | 728,8 | 653,2 | 814,6 | 13 |
| Ciências Sociais Aplicadas | 24 | 715,5 | 727,9 | 634,6 | 775,2 | 21 |
| Ciências Humanas | 13 | 698,3 | 693,1 | 656,4 | 763,8 | 11 |
| Linguística, Letras e Artes | 7 | 686,1 | 684,6 | 668,3 | 704,7 | 6 |
| Ciências Biológicas e Agrárias | 10 | 685,2 | 669,8 | 634,0 | 752,2 | 9 |

![Áreas](../figuras/18_areas_conhecimento.png)

*Figura 1 – Esquerda: distribuição das notas de corte por área (2024–2026). Direita: mediana por área ao longo das edições. Fonte: SISU/UFMG; elaboração própria.*

## Interpretação

- As caixas se sobrepõem bastante. Saber a área de um curso diz pouco sobre a nota de corte: há cursos de exatas com nota baixa e cursos de humanas com nota alta.
- Ciências Biológicas e Agrárias aparece embaixo em parte porque inclui os cursos de Montes Claros, que têm notas de corte menores (post 06).
- A ordem das áreas é parecida ao longo das edições (painel direito), o que combina com a estabilidade do ranking (post 16).

## Limitações e ressalvas

- O mapeamento de áreas é uma **decisão do autor**, não uma classificação oficial da UFMG.
- Áreas com poucas ofertas (Letras e Artes) têm resumos instáveis.
- Nota de corte é a nota do último classificado. Ela depende de quantas pessoas se inscreveram, de suas notas e do número de vagas; não mede a qualidade do curso. A base não traz o número de candidatos, então "mais concorrido" aqui significa "maior nota de corte".
- As notas do ENEM são padronizadas a cada edição, e o número de vagas, as regras de cota e o perfil dos candidatos mudam de um ano para outro. Diferenças entre anos mostram o que foi observado, não uma mudança na "dificuldade" do curso.

## Como reproduzir

```bash
python scripts/18_areas_conhecimento.py
```
