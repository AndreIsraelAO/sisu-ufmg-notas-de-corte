# A lista de espera derruba a nota de corte, sobretudo nas cotas para pessoas pretas, pardas e indígenas

**Resumo.** Entre a chamada regular e a última chamada presente na base, a nota de corte mediana da ampla concorrência caiu de 23,7 a 42,2 pontos, dependendo da edição (2022–2026). Em 2024–2026, as cotas PPI de renda baixa (LB_PPI) tiveram a maior queda mediana (69,9 pontos). Já as cotas PCD e quilombola quase não se mexem na mediana.

## Pergunta

Quanto a nota de corte cai entre a chamada regular (chamada 0) e a última chamada da lista de espera? Isso mudou entre 2022 e 2026?

## Dados usados

- `data/notas_corte.csv`, chamada regular de 2022-1 a 2026-1.
- `data/notas_corte_final.csv` (`is_final == True`): a última chamada **presente na base** para cada chave.
- Chave = edição × curso × campus × turno × cota. As duas tabelas casam 1 para 1 (nenhuma chave perdida).
- Antes de 2022 a base só tem a chamada regular, por isso o período começa em 2022.

## Método

Para cada chave, `queda = nota_min(chamada regular) − nota_min(última chamada)`. Como `nota_min` é acumulada, a queda nunca é negativa (validado no post 20). Resumimos pela mediana, que é menos sensível a grupos com uma só vaga do que a média. O painel da esquerda da figura mostra a queda mediana acumulada da AC em cada chamada intermediária.

## Resultados

**Tabela 1 – Queda da nota de corte por edição.**

| Edição | Chaves | Última chamada na base | Queda mediana AC | Queda mediana cotas | Queda média (todas) | % sem queda |
|---|---|---|---|---|---|---|
| 2022-1 | 646 | 12 | 42,2 | 41,6 | 58,0 | 25,2 |
| 2023-1 | 653 | 19 | 35,4 | 31,6 | 50,6 | 27,0 |
| 2024-1 | 595 | 17 | 23,7 | 34,6 | 49,4 | 18,2 |
| 2025-1 | 684 | 15 | 27,5 | 27,9 | 45,2 | 24,9 |
| 2026-1 | 738 | 14 | 26,2 | 31,7 | 50,4 | 22,1 |

![Queda entre chamadas](../figuras/04_queda_chamadas.png)

*Figura 1 – Esquerda: queda mediana acumulada (AC) a cada chamada; em 2022 e 2023 faltam chamadas na base, então as linhas ligam só as chamadas existentes. Direita: distribuição da queda total por edição, AC × cotas. Fonte: SISU/UFMG; elaboração própria.*

**Tabela 2 – Queda por modalidade de cota, 2024–2026 (mesmo sistema de códigos).**

| Cota | Chaves | Mediana | Média |
|---|---|---|---|
| LB_PPI | 277 | 69,9 | 87,7 |
| LI_PPI | 277 | 43,3 | 53,6 |
| LB_EP | 277 | 31,5 | 55,5 |
| AC | 277 | 25,9 | 40,8 |
| LI_EP | 277 | 17,7 | 31,5 |
| LI_PCD | 255 | 6,4 | 47,0 |
| LB_PCD | 227 | 0,0 | 34,5 |
| LB_Q | 148 | 0,0 | 21,4 |
| LI_Q | 2 | 0,0 | 0,0 |

## Interpretação

- A maior parte da queda acontece nas primeiras chamadas da lista de espera. Depois a curva achata.
- Agregando todas as cotas, a queda mediana fica perto da AC (Tabela 1). Separando por modalidade (Tabela 2), aparecem dois padrões: as cotas PPI e LB_EP caem **mais** que a AC, e as cotas PCD e quilombola têm mediana zero. Nestas há poucas vagas e muitas vezes nenhuma troca do último classificado ao longo das chamadas.
- Em 18,2% a 27,0% das chaves a nota não caiu nada entre a regular e a última chamada.
- Para quem consulta a nota de corte: a nota da chamada regular é bem mais alta que a nota com que a última pessoa entrou. Comparar a sua nota só com a chamada regular superestima a nota necessária.

## Limitações e ressalvas

- **2022 e 2023 têm lacunas de chamada** (2022 só tem as chamadas 0, 4, 5, 10 e 12; 2023 não tem as chamadas 2, 4 e 6). A "última chamada" é a última presente nos dados, não necessariamente a última que existiu.
- O número de chamadas difere entre edições (última chamada: 2022-1: 12, 2023-1: 19, 2024-1: 17, 2025-1: 15, 2026-1: 14). Mais chamadas tendem a produzir quedas maiores, então as edições não são comparáveis em pé de igualdade.
- Até 2023 os códigos de cota eram outros (era E2). A Tabela 2 usa só 2024–2026 para não misturar eras.
- As notas do ENEM e as vagas mudam a cada ano.

## Como reproduzir

```bash
python scripts/04_queda_chamadas.py
```
