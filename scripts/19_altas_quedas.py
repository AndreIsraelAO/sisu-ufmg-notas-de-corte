"""19 — Maiores altas e quedas de nota de corte entre 2018 e 2026 (ampla concorrência)."""
import matplotlib.pyplot as plt
import pandas as pd

from comum import RESSALVA_CORTE, RESSALVA_TEMPO, escrever_post, md, num, regular_ac, salvar


def calcular():
    # Só AC: é o único código idêntico entre a era E2 (2018–2023) e a E3 (2024+). As cotas mudaram de código e de regra.
    r = regular_ac(campus=None)
    assert set(r["cota_confianca"]) == {"alta"}
    p = r.pivot_table(index="oferta", columns="ano", values="nota_min")
    p = p[[2018, 2019, 2025, 2026]].dropna()
    t = p[[2018, 2026]].copy()
    t["variação 2018→2026"] = p[2026] - p[2018]
    # Variação descontando a mudança mediana de todas as ofertas (efeito geral do ENEM/edição).
    t["variação relativa"] = t["variação 2018→2026"] - t["variação 2018→2026"].median()
    # Robustez: média de dois anos em cada ponta.
    t["variação (média 2018–19 → 2025–26)"] = p[[2025, 2026]].mean(axis=1) - p[[2018, 2019]].mean(axis=1)
    t = t.sort_values("variação 2018→2026", ascending=False)
    rho = t["variação 2018→2026"].corr(t["variação (média 2018–19 → 2025–26)"], method="spearman")
    return {"r": r, "t": t, "rho": rho}


def figura(res):
    t = res["t"]
    sel = pd.concat([t.head(10), t.tail(10)]).iloc[::-1]
    fig, ax = plt.subplots(figsize=(10, 7))
    cor = ["#0072B2" if v > 0 else "#D55E00" for v in sel["variação 2018→2026"]]
    ax.barh(sel.index, sel["variação 2018→2026"], color=cor)
    ax.axvline(t["variação 2018→2026"].median(), color="#444", ls="--", lw=1,
               label=f"Mediana de todas as ofertas ({num(t['variação 2018→2026'].median())})")
    ax.axvline(0, color="#000", lw=0.8)
    ax.set_xlabel("Variação da nota de corte, 2018-1 → 2026-1 (pontos)")
    ax.set_ylabel("Oferta")
    ax.set_title("As 10 maiores altas e as 10 maiores quedas da nota de corte\n(ampla concorrência, chamada regular)")
    ax.tick_params(axis="y", labelsize=8)
    ax.legend(loc="lower right")
    return salvar(fig, "19_altas_quedas")


def post(res, fig):
    t, rho = res["t"], res["rho"]
    caiu = (t["variação 2018→2026"] < 0).sum()
    escrever_post("19-maiores-altas-e-quedas", f"""
# Entre 2018 e 2026, {len(t) - caiu} de {len(t)} ofertas subiram a nota de corte, e a maior alta foi de {num(t['variação 2018→2026'].iat[0])} pontos

**Resumo.** Comparando 2018-1 e 2026-1 (ampla concorrência, chamada regular), a nota de corte mediana das ofertas subiu {num(t['variação 2018→2026'].median())} pontos. A maior alta foi de **{t.index[0]}** (+{num(t['variação 2018→2026'].iat[0])}). {'A maior queda foi de **' + t.index[-1] + '** (' + num(t['variação 2018→2026'].iat[-1]) + ')' if caiu else 'Nenhuma oferta caiu; a menor alta foi de **' + t.index[-1] + '** (+' + num(t['variação 2018→2026'].iat[-1]) + ')'}.

## Pergunta

Quais ofertas tiveram as maiores altas e quedas de nota de corte entre 2018 e 2026?

## Dados usados

- `data/notas_corte.csv`: chamada regular, cota `AC`, dois campi.
- Ofertas presentes em 2018, 2019, 2025 e 2026 ({len(t)} ofertas). Cursos com turno renomeado em 2025 (post 07) ficam de fora.
- **Por que só AC:** 2018 está na era de cotas E2 (códigos 1.1–4.2) e 2026 na E3 (LB/LI). A ampla concorrência é o único grupo com mesmo código e mesma regra nas duas pontas (confiança alta). Comparar cotas entre 2018 e 2026 misturaria a mudança da nota com a mudança de regra (post 12).

## Método

- `variação = nota(2026-1) − nota(2018-1)`.
- `variação relativa = variação − mediana das variações de todas as ofertas`. Desconta o movimento geral das notas, que inclui as mudanças do ENEM.
- **Robustez:** a mesma conta com a média de dois anos em cada ponta (2018–2019 → 2025–2026), para reduzir o efeito de um ano atípico. A correlação de Spearman entre as duas versões é {num(rho, 2)}.

## Resultados

**Tabela 1 – As 10 maiores altas.**

{md(t.head(10), index=True, decimais=1)}

**Tabela 2 – As 10 menores variações.**

{md(t.tail(10).iloc[::-1], index=True, decimais=1)}

![Altas e quedas]({fig})

*Figura 1 – Variação da nota de corte entre 2018-1 e 2026-1 nas 10 ofertas que mais subiram e nas 10 que menos subiram (ou caíram). Fonte: SISU/UFMG; elaboração própria.*

## Interpretação

- A maior parte das ofertas subiu. A variação relativa (descontada a mediana) é a melhor forma de ver quem se destacou em relação às outras.
- Uma alta grande está associada a mais procura relativa ou a menos vagas. A base não tem nenhum dos dois, então não há como apontar o motivo.
- A versão com média de dois anos ordena as ofertas de forma {'muito parecida' if rho > 0.8 else 'parecida' if rho > 0.6 else 'diferente'} (ρ = {num(rho, 2)}). Isso indica que o resultado {'não depende' if rho > 0.8 else 'depende em parte'} de um único ano atípico.

## Limitações e ressalvas

- {RESSALVA_TEMPO}
- {RESSALVA_CORTE}
- Comparação de duas pontas: não diz nada sobre o caminho entre elas (veja os posts 01 e 17).

## Como reproduzir

```bash
python scripts/19_altas_quedas.py
```
""")


def checar(res):
    r, t = res["r"], res["t"]
    o = t.index[0]
    v = r[(r["oferta"] == o) & (r["ano"] == 2026)]["nota_min"].iat[0] - r[(r["oferta"] == o) & (r["ano"] == 2018)]["nota_min"].iat[0]
    assert abs(v - t["variação 2018→2026"].iat[0]) < 1e-9


def main():
    res = calcular()
    checar(res)
    post(res, figura(res))


if __name__ == "__main__":
    main()
