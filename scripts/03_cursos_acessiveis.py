"""03 — Ofertas com as menores notas de corte e como a posição delas mudou."""
import matplotlib.pyplot as plt

from comum import RESSALVA_CORTE, RESSALVA_TEMPO, escrever_post, md, num, regular_ac, salvar

RECENTES = ["2024-1", "2025-1", "2026-1"]


def calcular():
    r = regular_ac(campus=None)  # inclui Montes Claros: é onde estão várias das menores notas
    # Percentil na edição: 0 = menor nota de corte, 100 = maior.
    r["percentil"] = (r.groupby("edicao_chave")["nota_min"].rank(pct=True, method="average") * 100)
    p = r.pivot_table(index="oferta", columns="edicao_chave", values="nota_min")
    pct = r.pivot_table(index="oferta", columns="edicao_chave", values="percentil")
    ok = p[RECENTES].notna().all(axis=1)
    base10 = p[ok][RECENTES].mean(axis=1).sort_values().head(10).index
    tab = p.loc[base10, ["2014-1", "2018-1", "2026-1"]].copy()
    tab["média 2024–26"] = p.loc[base10, RECENTES].mean(axis=1)
    tab["percentil 2014-1"] = pct.loc[base10, "2014-1"]
    tab["percentil 2026-1"] = pct.loc[base10, "2026-1"]
    menor = r.loc[r.groupby("edicao_chave")["nota_min"].idxmin(), ["edicao_chave", "oferta", "nota_min"]]
    return {"r": r, "tab": tab, "pct": pct.loc[base10], "menor": menor}


def figura(res):
    pct = res["pct"]
    fig, ax = plt.subplots(figsize=(11, 6))
    for i, (nome, linha) in enumerate(pct.iterrows()):
        ax.plot(pct.columns, linha.values, marker="o", ms=3.5, ls=["-", "--"][i // 8], label=nome)
    ax.set_ylim(0, 100)
    ax.set_title("Posição relativa das 10 ofertas com menor nota de corte em 2024–2026\n(percentil na edição: 0 = menor nota, 100 = maior; AC, chamada regular, BH e Montes Claros)")
    ax.set_xlabel("Edição do SISU")
    ax.set_ylabel("Percentil da nota de corte na edição")
    ax.tick_params(axis="x", rotation=60)
    ax.legend(fontsize=8, loc="center left", bbox_to_anchor=(1, 0.5), title="Oferta")
    return salvar(fig, "03_cursos_acessiveis")


def post(res, fig):
    t = res["tab"]
    moc = sum(", MOC" in o for o in t.index)
    subiu = t[t["percentil 2026-1"] - t["percentil 2014-1"] > 15].index.tolist()
    caiu = t[t["percentil 2026-1"] < t["percentil 2014-1"]]
    com2014 = t["percentil 2014-1"].notna().sum()
    escrever_post("03-cursos-acessiveis", f"""
# As menores notas de corte estão em cursos de nicho e em Montes Claros, e ficaram relativamente mais baixas

**Resumo.** Das 10 ofertas com menor nota de corte em 2024–2026 (ampla concorrência, chamada regular), {moc} são do campus Montes Claros. A menor média é a de **{t.index[0]}** ({num(t.iloc[0]['média 2024–26'])} pontos). Das {com2014} que já existiam em 2014-1, {len(caiu)} ocupam em 2026-1 um percentil mais baixo, ou seja, ficaram relativamente mais acessíveis.

## Pergunta

Quais ofertas da UFMG têm as menores notas de corte e como a posição delas mudou ao longo do tempo?

## Dados usados

- `data/notas_corte.csv`: chamada regular, cota `AC`, **os dois campi** (Montes Claros entra porque concentra parte das menores notas).
- Ofertas com nota em 2024, 2025 e 2026.

## Método

1. Selecionamos as 10 ofertas com menor média de nota de corte em 2024-1, 2025-1 e 2026-1.
2. Como o número de ofertas e a escala do ENEM mudam de edição para edição, a comparação no tempo usa o **percentil** da oferta dentro da edição: `percentil = posição da nota (da menor para a maior) / nº de ofertas × 100`. O valor 10 quer dizer que só 10% das ofertas daquela edição tinham nota de corte menor ou igual.

## Resultados

**Tabela 1 – As 10 ofertas com menor nota de corte em 2024–2026.**

{md(t, index=True, decimais=1)}

![Percentil das ofertas mais acessíveis]({fig})

*Figura 1 – Percentil da nota de corte na edição, para as 10 ofertas com menor nota em 2024–2026. Linha interrompida = oferta ausente na edição. Fonte: SISU/UFMG; elaboração própria.*

**Tabela 2 – Menor nota de corte (AC) de cada edição.**

{md(res['menor'].rename(columns={'edicao_chave': 'Edição', 'oferta': 'Oferta', 'nota_min': 'Nota de corte'}))}

## Interpretação

- As menores notas de corte estão em cursos de nicho de Belo Horizonte (Arquivologia, Biblioteconomia, Museologia, Aquacultura, Turismo) e em dois cursos de Montes Claros.
- Em 2014-1 essas ofertas já estavam abaixo do percentil {num(t['percentil 2014-1'].max(), 0)}. Em 2026-1 todas estão abaixo do percentil {num(t['percentil 2026-1'].max(), 0)}. A maior mudança é a de {caiu.assign(dif=caiu['percentil 2026-1'] - caiu['percentil 2014-1']).sort_values('dif').index[0]}.
- {"Ofertas como " + ", ".join(subiu) + " subiram mais de 15 pontos percentuais entre 2014-1 e 2026-1, ou seja, ficaram relativamente menos acessíveis." if subiu else "Nenhuma das 10 ofertas subiu mais de 15 pontos percentuais entre 2014-1 e 2026-1."}
- Nota de corte menor indica que o último aprovado teve nota menor, o que é associado a menos procura ou a mais vagas. Não diz nada sobre a qualidade do curso.

## Limitações e ressalvas

- {RESSALVA_CORTE}
- {RESSALVA_TEMPO}
- Os percentis dependem de quantas ofertas existem em cada edição. Em 2014-2 e 2015-2 há cerca de 56 ofertas, contra 94 em 2026-1.
- **Efeito de seleção:** as 10 ofertas foram escolhidas por estarem no fundo em 2024–2026. É de se esperar que estivessem um pouco mais acima em anos anteriores (regressão à média), então parte da "queda de percentil" vem do próprio critério de escolha.
- Montes Claros tem poucos cursos (7 ofertas em 2026), o que pesa na lista.

## Como reproduzir

```bash
python scripts/03_cursos_acessiveis.py
```
""")


def checar(res):
    r = res["r"]
    m = r[r["edicao_chave"] == "2026-1"]["nota_min"].min()
    assert m == res["menor"].set_index("edicao_chave").loc["2026-1", "nota_min"]
    assert res["tab"]["média 2024–26"].is_monotonic_increasing


def main():
    res = calcular()
    checar(res)
    post(res, figura(res))


if __name__ == "__main__":
    main()
