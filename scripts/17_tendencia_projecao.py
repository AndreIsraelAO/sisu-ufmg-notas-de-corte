"""17 — Tendência linear por oferta e projeção para 2027 (exercício, não previsão)."""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from comum import RESSALVA_TEMPO, escrever_post, md, num, regular_ac, salvar

ANOS = list(range(2018, 2027))  # uma edição por ano e mesma forma de publicação (chamada 0)
MIN_PONTOS = 7


def ajustar(x, y, x0):
    """Regressão linear simples e intervalo de predição de 95% em x0."""
    n = len(x)
    lr = stats.linregress(x, y)
    pred = lr.intercept + lr.slope * x0
    resid = y - (lr.intercept + lr.slope * x)
    s = np.sqrt((resid ** 2).sum() / (n - 2))
    se = s * np.sqrt(1 + 1 / n + (x0 - x.mean()) ** 2 / ((x - x.mean()) ** 2).sum())
    t = stats.t.ppf(0.975, n - 2)
    return lr.slope, lr.pvalue, pred, pred - t * se, pred + t * se


def calcular():
    r = regular_ac(campus=None)
    r = r[r["ano"].isin(ANOS)]
    linhas, teste = [], []
    for oferta, g in r.groupby("oferta"):
        if len(g) < MIN_PONTOS or 2026 not in set(g["ano"]):
            continue
        x, y = g["ano"].to_numpy(float), g["nota_min"].to_numpy()
        b, p, pred, lo, hi = ajustar(x, y, 2027)
        linhas.append({"oferta": oferta, "pontos": len(g), "inclinação (pts/ano)": b, "p-valor": p,
                       "nota 2026": y[x == 2026][0], "projeção 2027": pred, "IP95 inferior": lo, "IP95 superior": hi})
        # Retroteste: ajusta sem 2026 e confere se 2026 caiu dentro do intervalo.
        m = x < 2026
        if m.sum() >= MIN_PONTOS - 1:
            _, _, p26, lo26, hi26 = ajustar(x[m], y[m], 2026)
            real = y[~m][0]
            teste.append({"oferta": oferta, "real": real, "proj": p26, "dentro": lo26 <= real <= hi26,
                          "erro": real - p26, "ingenuo": real - y[m][-1]})
    tab = pd.DataFrame(linhas).set_index("oferta").sort_values("projeção 2027", ascending=False)
    tab["largura IP95"] = tab["IP95 superior"] - tab["IP95 inferior"]
    teste = pd.DataFrame(teste)
    return {"r": r, "tab": tab, "teste": teste}


def figura(res):
    tab, r = res["tab"], res["r"]
    ex = [tab.index[0], tab["inclinação (pts/ano)"].idxmax(), tab["inclinação (pts/ano)"].idxmin(), tab.index[-1]]
    ex = list(dict.fromkeys(ex))
    fig, axs = plt.subplots(1, len(ex), figsize=(4 * len(ex), 4.5), sharey=False)
    for ax, o in zip(np.atleast_1d(axs), ex):
        g = r[r["oferta"] == o]
        x = g["ano"].to_numpy(float)
        lr = stats.linregress(x, g["nota_min"])
        xs = np.array([2018, 2027])
        ax.plot(g["ano"], g["nota_min"], "o", color="#0072B2", label="Observado")
        ax.plot(xs, lr.intercept + lr.slope * xs, "--", color="#444", label="Tendência linear")
        row = tab.loc[o]
        ax.errorbar(2027, row["projeção 2027"], yerr=[[row["projeção 2027"] - row["IP95 inferior"]], [row["IP95 superior"] - row["projeção 2027"]]],
                    fmt="s", color="#D55E00", capsize=4, label="Projeção 2027 (IP 95%)")
        ax.set_title(o, fontsize=9)
        ax.set_xlabel("Ano")
    np.atleast_1d(axs)[0].set_ylabel("Nota de corte AC (pontos)")
    np.atleast_1d(axs)[0].legend(fontsize=7)
    fig.suptitle("Exercício de tendência linear 2018–2026 e projeção para 2027 (não é previsão)")
    return salvar(fig, "17_tendencia_projecao")


def post(res, fig):
    tab, te = res["tab"], res["teste"]
    cob = te["dentro"].mean() * 100
    mae, mae_ing = te["erro"].abs().mean(), te["ingenuo"].abs().mean()
    sig = (tab["p-valor"] < 0.05).sum()
    cols = ["pontos", "inclinação (pts/ano)", "nota 2026", "projeção 2027", "IP95 inferior", "IP95 superior", "largura IP95"]
    escrever_post("17-tendencia-e-projecao-2027", f"""
# Projetar a nota de corte de 2027 com uma reta: um exercício com margem de erro de dezenas de pontos

**Resumo.** Ajustamos uma reta à nota de corte de 2018 a 2026 de {len(tab)} ofertas (ampla concorrência, chamada regular) e projetamos 2027. O intervalo de predição de 95% tem largura mediana de {num(tab['largura IP95'].median())} pontos. Num retroteste (projetar 2026 com dados até 2025), o erro médio da reta foi {num(mae)} pontos, contra {num(mae_ing)} pontos de simplesmente repetir a nota do ano anterior. **Isto é um exercício, não uma previsão confiável.**

## Pergunta

Se a tendência de 2018–2026 continuasse, qual seria a nota de corte de 2027 e quão incerta é essa conta?

## Dados usados

- `data/notas_corte.csv`: chamada regular, cota `AC`, dois campi, **2018 a 2026** (uma edição por ano, chamada 0). 2014–2017 ficam de fora por terem duas edições por ano ou chamada única com outro formato.
- Ofertas com pelo menos {MIN_PONTOS} anos e presentes em 2026 ({len(tab)} ofertas).

## Método

1. **Regressão linear simples** por oferta: `nota = a + b × ano`. `b` é a variação média por ano.
2. **Projeção** para 2027 com **intervalo de predição de 95%**: `ŷ ± t(0,975; n−2) · s · √(1 + 1/n + (2027 − x̄)² / Σ(x − x̄)²)`, em que `s` é o desvio-padrão dos resíduos. Esse intervalo inclui a incerteza da reta e a variação de um ano isolado.
3. **Retroteste:** refazemos a conta sem 2026, projetamos 2026 e comparamos com o valor real. Medimos a % de vezes em que o valor real caiu dentro do intervalo e o erro médio absoluto, contra uma regra ingênua (repetir a nota de 2025).

## Resultados

**Tabela 1 – Retroteste (projeção de 2026 com dados até 2025).**

| Medida | Valor |
|---|---|
| Ofertas testadas | {len(te)} |
| % com valor real dentro do IP 95% | {num(cob)}% |
| Erro médio absoluto da reta | {num(mae)} pontos |
| Erro médio absoluto da regra "repetir 2025" | {num(mae_ing)} pontos |
| Erro médio (real − projetado) | {num(te['erro'].mean())} pontos |

**Tabela 2 – Projeções para 2027: as 10 maiores.**

{md(tab[cols].head(10), index=True, decimais=1)}

**Tabela 3 – Projeções para 2027: as 10 menores.**

{md(tab[cols].tail(10), index=True, decimais=1)}

![Tendência]({fig})

*Figura 1 – Exemplos de ajuste linear e projeção 2027 com intervalo de predição de 95%: a maior projeção, a maior e a menor inclinação e a menor projeção. Fonte: SISU/UFMG; elaboração própria.*

## Interpretação

- Só {sig} das {len(tab)} retas têm inclinação estatisticamente diferente de zero (p < 0,05). Na maioria das ofertas a variação ano a ano é grande perto da tendência.
- No retroteste, o valor real de 2026 ficou dentro do intervalo em {num(cob, 0)}% dos casos. O erro médio (real − projetado) de {num(te['erro'].mean())} pontos mostra que 2026 {'veio acima' if te['erro'].mean() > 0 else 'veio abaixo'} da tendência na maioria das ofertas. Um ano atípico afeta todas as ofertas juntas, e a reta não antecipa isso. Um intervalo que se diz de 95% e acerta {num(cob, 0)}% das vezes está **estreito demais**: a incerteza real é maior que a calculada pelo modelo.
- {'A reta não superou a regra ingênua de repetir o ano anterior.' if mae >= mae_ing else 'A reta foi um pouco melhor que repetir o ano anterior, mas com erro da mesma ordem de grandeza.'} Para um candidato, a faixa do intervalo importa mais que o número central.

## Limitações e ressalvas

- **Não use estes números para decidir inscrição.** A nota de corte de 2027 depende de vagas, número de inscritos, notas do ENEM 2026 e regras do SISU 2027, e nada disso está no modelo.
- {RESSALVA_TEMPO}
- Com 7 a 9 pontos por oferta, a reta é muito sensível a um único ano. O intervalo supõe resíduos independentes e com distribuição normal, o que é só uma aproximação.
- Mudanças de regra no meio da série (cotas em 2024) não são modeladas, embora afetem menos a AC.

## Como reproduzir

```bash
python scripts/17_tendencia_projecao.py
```
""")


def checar(res):
    tab, r = res["tab"], res["r"]
    o = tab.index[0]
    g = r[r["oferta"] == o]
    b = np.polyfit(g["ano"], g["nota_min"], 1)
    assert abs(np.polyval(b, 2027) - tab.loc[o, "projeção 2027"]) < 1e-6
    assert (tab["IP95 inferior"] < tab["projeção 2027"]).all() and (tab["projeção 2027"] < tab["IP95 superior"]).all()


def main():
    res = calcular()
    checar(res)
    post(res, figura(res))


if __name__ == "__main__":
    main()
