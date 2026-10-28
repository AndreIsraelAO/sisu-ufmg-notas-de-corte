# Mapa de calor: 84 ofertas de BH em 15 edições, numa só imagem

**Resumo.** O mapa mostra a nota de corte de 84 ofertas de Belo Horizonte (ampla concorrência, chamada regular) em 15 edições. As ofertas estão ordenadas pela distância média à mediana de cada edição. No topo está **Medicina – Integral**, 100,1 pontos acima da mediana em média; na base está **Biblioteconomia – Matutino**, 79,2 pontos abaixo. As faixas verticais mais claras ou mais escuras indicam edições em que quase todas as notas subiram ou caíram juntas.

## Pergunta

Como se distribuem as notas de corte de todas as ofertas ao longo das edições, vistas de uma vez?

## Dados usados

- `data/notas_corte.csv`: chamada regular, cota `AC`, campus Belo Horizonte.
- Ofertas presentes em pelo menos 8 das 15 edições (84 ofertas). Ofertas recentes ou extintas cedo ficam de fora para o mapa não ficar vazio.

## Método

- Cada célula é a nota de corte da oferta na edição. Cinza claro = oferta inexistente naquela edição.
- **Ordenação:** primeiro subtraímos de cada nota a mediana da sua edição (`nota − mediana da edição`). Depois ordenamos pela média dessa diferença. Isso evita que uma oferta pareça "alta" só por existir em anos de notas altas.
- Escala de cor *viridis*, legível por pessoas com daltonismo e em impressão em tons de cinza.

## Resultados

![Mapa de calor](../figuras/14_mapa_calor.png)

*Figura 1 – Nota de corte por oferta e edição, BH, AC, chamada regular. Fonte: SISU/UFMG; elaboração própria.*

**Tabela 1 – As 10 primeiras e as 10 últimas do ordenamento.**

| oferta | Edições | Média | Mínima | Máxima | Distância média à mediana da edição |
|---|---|---|---|---|---|
| Medicina – Integral | 15,0 | 802,4 | 782,5 | 818,5 | 100,1 |
| Engenharia Química – Matutino | 15,0 | 769,2 | 750,7 | 788,4 | 66,8 |
| Engenharia Aeroespacial – Matutino | 15,0 | 768,4 | 720,0 | 794,4 | 66,0 |
| Direito – Matutino | 15,0 | 757,2 | 710,7 | 783,1 | 54,8 |
| Engenharia Mecânica – Matutino | 15,0 | 754,7 | 705,3 | 781,3 | 52,4 |
| Ciência da Computação – Matutino | 13,0 | 747,5 | 685,0 | 789,1 | 47,9 |
| Direito – Noturno | 15,0 | 749,0 | 721,1 | 771,8 | 46,6 |
| Engenharia Elétrica – Matutino | 15,0 | 748,3 | 724,6 | 771,2 | 46,0 |
| Arquitetura e Urbanismo – Matutino | 15,0 | 746,3 | 719,2 | 766,7 | 44,0 |
| Engenharia de Produção – Matutino | 15,0 | 741,1 | 721,2 | 762,1 | 38,8 |

| oferta | Edições | Média | Mínima | Máxima | Distância média à mediana da edição |
|---|---|---|---|---|---|
| Pedagogia – Matutino | 13,0 | 648,6 | 575,6 | 683,9 | -55,4 |
| Geografia – Noturno | 12,0 | 649,2 | 614,0 | 673,9 | -57,0 |
| Gestão de Serviços de Saúde – Noturno | 15,0 | 641,5 | 604,5 | 664,8 | -60,8 |
| Radiologia – Noturno | 15,0 | 638,4 | 572,3 | 671,8 | -63,9 |
| Turismo – Matutino | 15,0 | 635,1 | 529,9 | 677,0 | -67,2 |
| Museologia – Matutino | 13,0 | 635,9 | 590,8 | 666,2 | -68,0 |
| Aquacultura – Matutino | 15,0 | 628,4 | 589,4 | 662,7 | -74,0 |
| Biblioteconomia – Noturno | 13,0 | 629,0 | 595,1 | 660,4 | -76,7 |
| Arquivologia – Noturno | 13,0 | 628,1 | 586,2 | 651,3 | -77,6 |
| Biblioteconomia – Matutino | 15,0 | 623,2 | 574,0 | 665,7 | -79,2 |

## Interpretação

- O mapa mostra mais estabilidade de posição (linhas com cor parecida de ponta a ponta) do que mudança. O post 16 mede isso com a correlação de Spearman.
- As colunas `2014-2` e `2015-2` são mais escuras para quase todas as ofertas: as segundas edições tiveram notas menores, o que é associado à edição e não aos cursos.

## Limitações e ressalvas

- As notas do ENEM são padronizadas a cada edição, e o número de vagas, as regras de cota e o perfil dos candidatos mudam de um ano para outro. Diferenças entre anos mostram o que foi observado, não uma mudança na "dificuldade" do curso.
- A cor mostra a nota bruta. Comparar cores entre colunas diferentes mistura a mudança do curso com a mudança geral daquela edição.

## Como reproduzir

```bash
python scripts/14_mapa_calor.py
```
