# 2024 trocou os códigos de cota: algumas séries continuam, outras quebram

**Resumo.** Em 2024 a UFMG passou a usar os códigos LB/LI, que substituíram 1.1–4.2 (2018–2023) e 1–4 (2014–2017). Quatro cotas têm equivalência direta e podem ser seguidas no tempo: LB_PPI, LB_EP, LI_PPI e LI_EP. As cotas PCD perderam o recorte PPI, e as quilombolas só entram na base em 2025. Na passagem 2023→2024, a distância para a AC variou 13,9 pontos na LB_PPI e 0,0 na LI_EP. As cotas de renda baixa saltaram acima do normal; as de qualquer renda, não.

## Pergunta

O que muda com os códigos de cota de 2024, o que continua comparável com os anos anteriores e o que não continua?

## Dados usados

- `data/de_para_cotas.csv`: tabela de equivalência com a confiança de cada correspondência.
- `data/notas_corte.csv`: chamada regular, 2018–2026, cotas comparáveis (`LB_PPI`, `LB_EP`, `LI_PPI`, `LI_EP`) contra a AC da mesma oferta.

## Método

1. Tabela de equivalência e presença de cada código por era.
2. Para as quatro cotas comparáveis, a distância mediana `AC − cota` por ano. O "salto" 2023→2024 é comparado com a variação anual típica de 2018–2023 (média do valor absoluto das variações ano a ano). Um salto bem maior que o típico sugere efeito da troca de regra. Isso é uma comparação descritiva, não um teste causal.

## Resultados

**Tabela 1 – Equivalência de códigos (de `de_para_cotas.csv`).**

| Era | Código original | Código padronizado | Confiança |
|---|---|---|---|
| E1_2014-2017 | 1 | LB_PPI | media |
| E1_2014-2017 | 2 | LB_EP | media |
| E1_2014-2017 | 3 | LI_PPI | media |
| E1_2014-2017 | 4 | LI_EP | media |
| E1_2014-2017 | AC | AC | alta |
| E2_2018-2023 | 1.1 | LB_PPI_PCD | baixa |
| E2_2018-2023 | 1.2 | LB_PPI | media |
| E2_2018-2023 | 2.1 | LB_PCD | media |
| E2_2018-2023 | 2.2 | LB_EP | media |
| E2_2018-2023 | 3.1 | LI_PPI_PCD | baixa |
| E2_2018-2023 | 3.2 | LI_PPI | media |
| E2_2018-2023 | 4.1 | LI_PCD | media |
| E2_2018-2023 | 4.2 | LI_EP | media |
| E2_2018-2023 | AC | AC | alta |
| E3_2024+ | LB_PPI | LB_PPI | alta |
| E3_2024+ | LB_Q | LB_Q | alta |
| E3_2024+ | LB_PCD | LB_PCD | alta |
| E3_2024+ | LB_EP | LB_EP | alta |
| E3_2024+ | LI_PPI | LI_PPI | alta |
| E3_2024+ | LI_Q | LI_Q | alta |
| E3_2024+ | LI_PCD | LI_PCD | alta |
| E3_2024+ | LI_EP | LI_EP | alta |
| E3_2024+ | AC | AC | alta |

**Tabela 2 – Ofertas com cada código (chamada regular, soma das edições da era).**

| Código | E1_2014-2017 | E2_2018-2023 | E3_2024+ |
|---|---|---|---|
| AC | 97 | 90 | 103 |
| LB_EP | 97 | 90 | 103 |
| LB_PCD | 0 | 85 | 100 |
| LB_PPI | 97 | 90 | 103 |
| LB_PPI_PCD | 0 | 90 | 0 |
| LB_Q | 0 | 0 | 87 |
| LI_EP | 97 | 90 | 103 |
| LI_PCD | 0 | 83 | 102 |
| LI_PPI | 97 | 90 | 103 |
| LI_PPI_PCD | 0 | 90 | 0 |
| LI_Q | 0 | 0 | 1 |

**Tabela 3 – Salto da distância mediana AC − cota entre 2023 e 2024.**

| Cota | salto 2023→2024 | variação anual típica 2018–2023 | Renda |
|---|---|---|---|
| LB_EP | 5,1 | 2,8 | baixa (limite mudou) |
| LB_PPI | 13,9 | 4,9 | baixa (limite mudou) |
| LI_EP | 0,0 | 2,4 | qualquer (sem mudança) |
| LI_PPI | -2,3 | 5,9 | qualquer (sem mudança) |

![Regime 2024](../figuras/12_regime_2024.png)

*Figura 1 – Distância mediana entre AC e as quatro cotas comparáveis, 2018–2026. Fonte: SISU/UFMG; elaboração própria.*

## Interpretação: o que é comparável

| Item | Comparável entre eras? | Por quê |
|---|---|---|
| AC | Sim | Mesmo código e conceito |
| LI_EP, LI_PPI | Sim (confiança média) | Mesmo recorte; não depende de renda |
| LB_EP, LB_PPI | Com ressalva (média) | Limite de renda caiu de 1,5 para 1 salário mínimo per capita em 2024 |
| LB_PCD, LI_PCD | Com ressalva (média), só desde 2018 | Em 2018–2023 havia versões PCD com e sem PPI |
| LB_PPI_PCD, LI_PPI_PCD | **Não** (baixa) | Deixam de existir em 2024; não há código equivalente |
| LB_Q, LI_Q | **Não** antes de 2025 | Em 2024 a lista quilombola está só no PDF; LI_Q tem 2 linhas |

- Se a troca de regra tivesse efeito, a expectativa seria um salto maior nas cotas "LB", cujo limite de renda mudou, do que nas "LI". É o que se observa: LB_EP, LB_PPI saltaram mais que a variação típica de 2018–2023, e LI_EP, LI_PPI não. O padrão é **compatível** com a redução do limite de renda (de 1,5 para 1 salário mínimo), que deixa o grupo LB mais restrito. Mas é um único ano, sem controle para outras mudanças.
- Além do código, 2024 coincide com a mudança nas regras de concorrência: desde 2024 nenhuma cota teve nota acima da AC (post 10).

## Limitações e ressalvas

- A equivalência entre eras foi **inferida das legendas dos PDFs**. Os editais não foram lidos (veja `docs/relatorio_qualidade_base.md`).
- Um ano só (2024) de comparação imediata. Variações de ENEM e vagas no mesmo ano se confundem com a mudança de regra.
- Quilombolas de 2024 não estão na base.

## Como reproduzir

```bash
python scripts/12_regime_2024.py
```
