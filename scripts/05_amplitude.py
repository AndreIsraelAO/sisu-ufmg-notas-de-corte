"""05 — Amplitude (nota_max − nota_min) por oferta: onde a turma é mais heterogênea?"""
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import spearmanr

from comum import RESSALVA_CORTE, escrever_post, md, num, regular_ac, salvar

ANOS = [2024, 2025, 2026]


def calcular():
    r = regular_ac(campus=None)
    r = r[r["ano"].isin(ANOS)].copy()
    r["amplitude"] = r["nota_max"] - r["nota_min"]
    g = r.groupby("oferta").agg(edicoes=("ano", "nunique"), nota_min=("nota_min", "mean"),
                                nota_max=("nota_max", "mean"), amplitude=("amplitude", "mean"))
    g = g[g["edicoes"] == len(ANOS)].sort_values("amplitude", ascending=False)
    rho, p = spearmanr(g["nota_min"], g["amplitude"])
    return {"r": r, "g": g, "rho": rho, "p": p}


def figura(res):
    g = res["g"]
    top, bot = g.head(10), g.tail(10)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 6.5), gridspec_kw={"width_ratios": [1.4, 1]})
    linhas = list(bot.index[::-1]) + [""] + list(top.index[::-1])
    y = {n: i for i, n in enumerate(linhas) if n}
    for nome, row in pd.concat([bot, top]).iterrows():
        cor = "#0072B2" if nome in top.index else "#E69F00"
        a1.plot([row["nota_min"], row["nota_max"]], [y[nome]] * 2, color=cor, lw=3)
        a1.plot(row["nota_min"], y[nome], "o", color=cor)
        a1.plot(row["nota_max"], y[nome], "D", color=cor, ms=4)
    a1.set_yticks(list(y.values()), list(y.keys()), fontsize=8)
    a1.set_xlabel("Nota (média 2024–2026)  ● mínima   ◆ máxima")
    a1.set_title("Maiores (azul) e menores (laranja) amplitudes\nentre aprovados na AC, chamada regular")
    a2.scatter(g["nota_min"], g["amplitude"], s=18, color="#009E73")
    a2.set_xlabel("Nota de corte média 2024–2026 (pontos)")
    a2.set_ylabel("Amplitude média (máx − mín, pontos)")
    a2.set_title(f"Nota de corte × amplitude\n(Spearman ρ = {res['rho']:.2f})".replace(".", ","))
    return salvar(fig, "05_amplitude")


def post(res, fig):
    g = res["g"]
    cols = {"edicoes": "Edições", "nota_min": "Nota mín. (corte)", "nota_max": "Nota máx.", "amplitude": "Amplitude"}
    escrever_post("05-amplitude-por-curso", f"""
# Ofertas com nota de corte mais alta têm turmas mais "apertadas"

**Resumo.** Em 2024–2026, a distância entre a maior e a menor nota dos aprovados na ampla concorrência (chamada regular) variou de {num(g['amplitude'].min())} pontos ({g.index[-1]}) a {num(g['amplitude'].max())} pontos ({g.index[0]}). Quanto maior a nota de corte, menor tende a ser a amplitude (correlação de Spearman ρ = {num(res['rho'], 2)}).

## Pergunta

Em quais ofertas a diferença entre o primeiro e o último aprovado é maior?

## Dados usados

- `data/notas_corte.csv`: chamada regular, cota `AC`, dois campi, edições 2024-1, 2025-1 e 2026-1.
- Só ofertas presentes nas três edições ({len(g)} ofertas).

## Método

- `amplitude = nota_max − nota_min`, em cada oferta e edição, depois a média das três edições. `nota_max` é a maior nota entre os aprovados do grupo e não muda entre chamadas. Usamos a chamada regular para não inflar a amplitude com as quedas da lista de espera (post 04).
- A associação entre nota de corte e amplitude é medida pela **correlação de Spearman** (ρ), que compara as posições (rankings) das duas variáveis. Vai de −1 a 1; valores negativos indicam que uma cresce quando a outra cai. p-valor = {res['p']:.1e}.

## Resultados

**Tabela 1 – As 10 maiores amplitudes.**

{md(g.head(10).rename(columns=cols), index=True, decimais=1)}

**Tabela 2 – As 10 menores amplitudes.**

{md(g.tail(10).iloc[::-1].rename(columns=cols), index=True, decimais=1)}

![Amplitude]({fig})

*Figura 1 – Esquerda: faixa entre a nota mínima e a máxima dos aprovados nas 10 maiores e 10 menores amplitudes. Direita: relação entre nota de corte e amplitude para todas as ofertas. Fonte: SISU/UFMG; elaboração própria.*

## Interpretação

- Há um efeito de "teto": a nota máxima do ENEM é limitada, então ofertas com nota de corte muito alta têm pouco espaço entre o último e o primeiro aprovado.
- A amplitude também está associada ao **número de vagas**, que a base não informa: mais vagas na AC tendem a abrir mais espaço entre o primeiro e o último aprovado. Por isso amplitude não deve ser lida como "diversidade" da turma.

## Limitações e ressalvas

- {RESSALVA_CORTE}
- A amplitude depende do número de vagas e de um único candidato com nota muito alta. Ela não descreve a distribuição completa das notas.
- Análise restrita a 2024–2026 e à ampla concorrência. Nas cotas há grupos com uma vaga, em que a amplitude é zero.

## Como reproduzir

```bash
python scripts/05_amplitude.py
```
""")


def checar(res):
    r = res["r"]
    x = r[r["oferta"] == res["g"].index[0]]
    assert abs((x["nota_max"] - x["nota_min"]).mean() - res["g"]["amplitude"].iat[0]) < 1e-9
    assert (res["g"]["amplitude"] >= 0).all()


def main():
    res = calcular()
    checar(res)
    post(res, figura(res))


if __name__ == "__main__":
    main()
