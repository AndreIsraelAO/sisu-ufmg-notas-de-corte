"""14 — Mapa de calor oferta × edição (BH, AC, chamada regular), ordenado pela nota média."""
import matplotlib.pyplot as plt
import numpy as np

from comum import RESSALVA_TEMPO, escrever_post, md, num, regular_ac, salvar

MIN_EDICOES = 8


def calcular():
    r = regular_ac()
    p = r.pivot_table(index="oferta", columns="edicao_chave", values="nota_min")
    p = p[p.notna().sum(axis=1) >= MIN_EDICOES]
    # Ordena pela média das notas centralizadas por edição, para não favorecer ofertas que só existem em anos de nota alta.
    centr = p - p.median()
    p = p.loc[centr.mean(axis=1).sort_values(ascending=False).index]
    return {"r": r, "p": p, "centr": centr.loc[p.index]}


def figura(res):
    p = res["p"]
    fig, ax = plt.subplots(figsize=(10, 0.2 * len(p) + 2))
    im = ax.imshow(p.values, aspect="auto", cmap="viridis", interpolation="nearest")
    ax.set_xticks(np.arange(p.shape[1]), p.columns, rotation=60)
    ax.set_yticks(np.arange(len(p)), p.index, fontsize=6.5)
    ax.set_xlabel("Edição do SISU")
    ax.set_ylabel("Oferta (curso – turno), da maior para a menor nota relativa")
    ax.set_title("Nota de corte por oferta e edição\n(Belo Horizonte, ampla concorrência, chamada regular; cinza claro = oferta inexistente)")
    ax.set_facecolor("#eeeeee")
    ax.grid(False)
    cb = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    cb.set_label("Nota de corte (pontos)")
    return salvar(fig, "14_mapa_calor")


def post(res, fig):
    p, c = res["p"], res["centr"]
    resumo = p.agg(["count", "mean", "min", "max"], axis=1)
    resumo["acima da mediana da edição (média)"] = c.mean(axis=1)
    resumo.columns = ["Edições", "Média", "Mínima", "Máxima", "Distância média à mediana da edição"]
    escrever_post("14-mapa-de-calor", f"""
# Mapa de calor: {len(p)} ofertas de BH em 15 edições, numa só imagem

**Resumo.** O mapa mostra a nota de corte de {len(p)} ofertas de Belo Horizonte (ampla concorrência, chamada regular) em 15 edições. As ofertas estão ordenadas pela distância média à mediana de cada edição. No topo está **{p.index[0]}**, {num(c.iloc[0].mean())} pontos acima da mediana em média; na base está **{p.index[-1]}**, {num(-c.iloc[-1].mean())} pontos abaixo. As faixas verticais mais claras ou mais escuras indicam edições em que quase todas as notas subiram ou caíram juntas.

## Pergunta

Como se distribuem as notas de corte de todas as ofertas ao longo das edições, vistas de uma vez?

## Dados usados

- `data/notas_corte.csv`: chamada regular, cota `AC`, campus Belo Horizonte.
- Ofertas presentes em pelo menos {MIN_EDICOES} das 15 edições ({len(p)} ofertas). Ofertas recentes ou extintas cedo ficam de fora para o mapa não ficar vazio.

## Método

- Cada célula é a nota de corte da oferta na edição. Cinza claro = oferta inexistente naquela edição.
- **Ordenação:** primeiro subtraímos de cada nota a mediana da sua edição (`nota − mediana da edição`). Depois ordenamos pela média dessa diferença. Isso evita que uma oferta pareça "alta" só por existir em anos de notas altas.
- Escala de cor *viridis*, legível por pessoas com daltonismo e em impressão em tons de cinza.

## Resultados

![Mapa de calor]({fig})

*Figura 1 – Nota de corte por oferta e edição, BH, AC, chamada regular. Fonte: SISU/UFMG; elaboração própria.*

**Tabela 1 – As 10 primeiras e as 10 últimas do ordenamento.**

{md(resumo.head(10), index=True, decimais=1)}

{md(resumo.tail(10), index=True, decimais=1)}

## Interpretação

- O mapa mostra mais estabilidade de posição (linhas com cor parecida de ponta a ponta) do que mudança. O post 16 mede isso com a correlação de Spearman.
- As colunas `2014-2` e `2015-2` são mais escuras para quase todas as ofertas: as segundas edições tiveram notas menores, o que é associado à edição e não aos cursos.

## Limitações e ressalvas

- {RESSALVA_TEMPO}
- A cor mostra a nota bruta. Comparar cores entre colunas diferentes mistura a mudança do curso com a mudança geral daquela edição.

## Como reproduzir

```bash
python scripts/14_mapa_calor.py
```
""")


def checar(res):
    r, p = res["r"], res["p"]
    v = r[(r["oferta"] == p.index[0]) & (r["edicao_chave"] == "2026-1")]["nota_min"]
    assert len(v) == 1 and v.iat[0] == p.loc[p.index[0], "2026-1"]
    assert (p.notna().sum(axis=1) >= MIN_EDICOES).all()


def main():
    res = calcular()
    checar(res)
    post(res, figura(res))


if __name__ == "__main__":
    main()
