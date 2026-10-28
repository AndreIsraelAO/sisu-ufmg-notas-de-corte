"""16 — Estabilidade do ranking: correlação de Spearman entre edições consecutivas."""
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import spearmanr

from comum import escrever_post, md, num, regular_ac, salvar


def calcular():
    r = regular_ac()
    p = r.pivot_table(index="oferta", columns="edicao_chave", values="nota_min")
    eds = list(p.columns)
    linhas = []
    for a, b in list(zip(eds, eds[1:])) + [("2014-1", "2026-1"), ("2018-1", "2026-1")]:
        par = p[[a, b]].dropna()
        rho, pv = spearmanr(par[a], par[b])
        linhas.append({"de": a, "para": b, "ofertas em comum": len(par), "rho": rho, "p-valor": pv,
                       "tipo": "consecutivas" if eds.index(b) - eds.index(a) == 1 else "longo prazo"})
    return {"p": p, "tab": pd.DataFrame(linhas)}


def figura(res):
    t = res["tab"]
    c = t[t["tipo"] == "consecutivas"]
    fig, ax = plt.subplots(figsize=(10, 5))
    rot = c["de"] + "→" + c["para"]
    ax.plot(rot, c["rho"], marker="o", color="#0072B2", label="Edições consecutivas")
    for _, row in t[t["tipo"] == "longo prazo"].iterrows():
        ax.axhline(row["rho"], ls="--", lw=1, color="#D55E00" if row["de"] == "2014-1" else "#009E73",
                   label=f"{row['de']}→{row['para']} (ρ = {row['rho']:.2f})".replace(".", ","))
    ax.set_ylim(0, 1)
    ax.set_xlabel("Par de edições")
    ax.set_ylabel("Correlação de Spearman (ρ)")
    ax.set_title("Quanto o ranking de notas de corte se repete de uma edição para a seguinte\n(BH, ampla concorrência, chamada regular)")
    ax.tick_params(axis="x", rotation=60)
    ax.legend(loc="lower right")
    return salvar(fig, "16_estabilidade_ranking")


def post(res, fig):
    t = res["tab"]
    c = t[t["tipo"] == "consecutivas"]
    lp = t[t["tipo"] == "longo prazo"].set_index("de")
    menor = c.loc[c["rho"].idxmin()]
    escrever_post("16-estabilidade-do-ranking", f"""
# O ranking de notas de corte quase não muda de um ano para o outro (ρ entre {num(c['rho'].min(), 2)} e {num(c['rho'].max(), 2)})

**Resumo.** Entre edições consecutivas, a correlação de Spearman entre os rankings de nota de corte (BH, ampla concorrência, chamada regular) ficou entre {num(c['rho'].min(), 2)} e {num(c['rho'].max(), 2)}. A menor foi em {menor['de']}→{menor['para']}. Mesmo entre 2014-1 e 2026-1, doze anos depois, a correlação é {num(lp.loc['2014-1', 'rho'], 2)}.

## Pergunta

O ranking das ofertas pela nota de corte é estável de uma edição para a seguinte?

## Dados usados

- `data/notas_corte.csv`: chamada regular, cota `AC`, campus Belo Horizonte.
- Em cada par de edições entram só as ofertas presentes nas duas.

## Método

A **correlação de Spearman** (ρ) compara as posições de cada oferta nos dois rankings. ρ = 1 significa ranking idêntico; ρ = 0, nenhuma relação. A fórmula, sem empates, é `ρ = 1 − 6·Σd² / (n·(n² − 1))`, em que `d` é a diferença de posição de cada oferta e `n` o número de ofertas. Também mostramos dois pares de longo prazo (2014-1→2026-1 e 2018-1→2026-1).

## Resultados

**Tabela 1 – Correlação de Spearman entre rankings.**

{md(t.rename(columns={'de': 'De', 'para': 'Para', 'tipo': 'Tipo'}).assign(**{'p-valor': t['p-valor'].map(lambda v: f'{v:.1e}'.replace('.', ','))}), decimais=3)}

![Estabilidade]({fig})

*Figura 1 – Correlação de Spearman entre edições consecutivas; linhas tracejadas = pares de longo prazo. Fonte: SISU/UFMG; elaboração própria.*

## Interpretação

- O ranking é muito estável. Saber a posição de um curso num ano dá uma ótima ideia da posição no ano seguinte, mas não da nota exata, que muda com o ENEM.
- As menores correlações estão entre 2015-2 e 2018-1, período que inclui as edições de chamada única (2016 e 2017) e a troca de códigos de cota em 2018. De 2018 em diante, ρ é sempre de pelo menos {num(c[c['de'] >= '2018-1']['rho'].min(), 2)}.
- O par 2024-1→2025-1 tem menos ofertas em comum ({c.set_index('de').loc['2024-1', 'ofertas em comum']}) porque vários cursos trocaram o turno Matutino por Integral ou Vespertino em 2025 (post 07).

## Limitações e ressalvas

- O p-valor testa só se ρ é diferente de zero, o que aqui é óbvio. Ele não mede se a estabilidade é "alta".
- O ρ não usa o número de vagas nem de candidatos, que a base não tem.
- Ofertas que existem em uma só das edições do par ficam de fora.

## Como reproduzir

```bash
python scripts/16_estabilidade_ranking.py
```
""")


def checar(res):
    p, t = res["p"], res["tab"]
    par = p[["2025-1", "2026-1"]].dropna()
    # Conferência independente: Spearman = Pearson dos postos.
    rho = par.rank().corr().iloc[0, 1]
    assert abs(rho - t[(t["de"] == "2025-1") & (t["para"] == "2026-1")]["rho"].iat[0]) < 1e-9


def main():
    res = calcular()
    checar(res)
    post(res, figura(res))


if __name__ == "__main__":
    main()
