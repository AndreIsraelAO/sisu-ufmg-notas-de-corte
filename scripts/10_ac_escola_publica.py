"""10 — Ampla concorrência × escola pública ao longo do tempo: a distância diminui?"""
import matplotlib.pyplot as plt
from scipy.stats import linregress

from comum import RESSALVA_TEMPO, base, escrever_post, md, num, salvar

CHAVE = ["edicao_chave", "curso_id", "campus", "turno"]
COTAS = {"LI_EP": "Escola pública, qualquer renda (LI_EP)", "LB_EP": "Escola pública, renda baixa (LB_EP)"}


def calcular():
    d = base()
    reg = d[d["regular"]]
    ac = reg[reg["cota_padrao"] == "AC"][CHAVE + ["nota_min"]].rename(columns={"nota_min": "nota_ac"})
    m = reg[reg["cota_padrao"].isin(COTAS)].merge(ac, on=CHAVE)
    assert set(m["cota_confianca"]) <= {"alta", "media"}
    m["gap"] = m["nota_ac"] - m["nota_min"]
    serie = m.groupby(["cota_padrao", "edicao_chave", "ano"])["gap"].agg(
        pares="size", mediana="median", p25=lambda g: g.quantile(.25), p75=lambda g: g.quantile(.75)).reset_index()
    tend = {}
    for c in COTAS:
        s = serie[serie["cota_padrao"] == c]
        lr = linregress(s["ano"] + (s["edicao_chave"].str[-1].astype(int) - 1) * 0.5, s["mediana"])
        tend[c] = lr
        s18 = s[s["ano"] >= 2018]
        tend[c + "_2018"] = linregress(s18["ano"], s18["mediana"])
    tab = serie.pivot_table(index="edicao_chave", columns="cota_padrao", values="mediana")
    neg = m.assign(neg=m["gap"] < 0).groupby(["edicao_chave", "cota_padrao"])["neg"].mean().unstack() * 100
    tab = tab.join(neg.add_prefix("% cota > AC – "))
    return {"m": m, "serie": serie, "tend": tend, "tab": tab}


def figura(res):
    s = res["serie"]
    fig, ax = plt.subplots(figsize=(11, 5.5))
    for i, (c, rot) in enumerate(COTAS.items()):
        g = s[s["cota_padrao"] == c]
        cor = ["#0072B2", "#E69F00"][i]
        ax.plot(g["edicao_chave"], g["mediana"], marker="o", color=cor, label=rot + " – mediana")
        ax.fill_between(g["edicao_chave"], g["p25"], g["p75"], color=cor, alpha=0.15, label=rot + " – p25 a p75")
    for x, t in (("2018-1", "era E2"), ("2024-1", "era E3")):
        ax.axvline(x, color="#666", ls=":", lw=1)
        ax.text(x, ax.get_ylim()[1], " " + t, va="top", fontsize=8, color="#444")
    ax.axhline(0, color="#333", lw=0.8)
    ax.set_xlabel("Edição do SISU")
    ax.set_ylabel("Nota de corte AC − nota da cota (pontos)")
    ax.set_title("Distância entre ampla concorrência e cotas de escola pública\n(mesmo curso, turno e edição; chamada regular)")
    ax.tick_params(axis="x", rotation=60)
    ax.legend(fontsize=8)
    return salvar(fig, "10_ac_escola_publica")


def post(res, fig):
    t, tend = res["tab"], res["tend"]
    li, lb = tend["LI_EP"], tend["LB_EP"]
    pico = t["LI_EP"].idxmax()
    li18, lb18 = tend["LI_EP_2018"], tend["LB_EP_2018"]
    ini = t.loc[["2014-1", "2014-2", "2015-1", "2015-2", "2016-1", "2017-1"]].mean()
    fim = t.loc[["2024-1", "2025-1", "2026-1"]].mean()
    escrever_post("10-ampla-concorrencia-x-escola-publica", f"""
# A distância entre ampla concorrência e escola pública subiu até {pico}, caiu até 2020 e está estável desde então

**Resumo.** Na cota de escola pública independente de renda (LI_EP), a distância mediana para a ampla concorrência foi de {num(ini['LI_EP'])} pontos em média em 2014–2017 e de {num(fim['LI_EP'])} pontos em 2024–2026. Na cota de escola pública com renda baixa (LB_EP), os valores foram {num(ini['LB_EP'])} e {num(fim['LB_EP'])} pontos. A série não é uma linha reta: na LI_EP a distância saiu de valores negativos em 2014, chegou a {num(t.loc[pico, 'LI_EP'])} pontos em {pico} e voltou para cerca de 10 pontos a partir de 2020. Por isso a tendência linear do período todo é quase nula ({num(li.slope, 2)} ponto/ano).

## Pergunta

A diferença de nota de corte entre a ampla concorrência e as cotas de escola pública diminuiu ao longo do tempo?

## Dados usados

- `data/notas_corte.csv`: chamada regular, 15 edições, dois campi.
- Cotas: `LI_EP` (escola pública, qualquer renda) e `LB_EP` (escola pública, renda baixa). Nas três eras de códigos, as duas têm equivalência de confiança **média** (2014–2023) ou **alta** (2024+). Os códigos originais eram 4 / 4.2 / LI_EP e 2 / 2.2 / LB_EP.
- Cada cota é comparada com a AC da mesma oferta e edição.

## Método

1. `diferença = nota(AC) − nota(cota)` por oferta e edição. Resumo por edição: mediana e faixa p25–p75.
2. Tendência: regressão linear simples da mediana contra o tempo (`mediana = a + b × ano`, com as segundas edições em ano + 0,5). `b` é a variação média por ano. O intervalo de confiança aproximado é `b ± 1,96 × erro padrão`. Como a série claramente não é linear, também ajustamos a reta só para 2018–2026 (mesma era de códigos até 2023 e mesmo desenho de cotas). Com tão poucos pontos e mudanças de regra no meio da série, isso é uma descrição, não um teste forte.

## Resultados

**Tabela 1 – Diferença mediana AC − cota, por edição.**

{md(t.rename(columns=COTAS).rename_axis('Edição'), index=True, decimais=1)}

**Tabela 2 – Tendência linear da mediana.**

| Cota | Inclinação (pontos/ano) | IC 95% aproximado | R² | p-valor |
|---|---|---|---|---|
| LI_EP | {num(li.slope, 2)} | {num(li.slope - 1.96 * li.stderr, 2)} a {num(li.slope + 1.96 * li.stderr, 2)} | {num(li.rvalue ** 2, 2)} | {num(li.pvalue, 3)} |
| LB_EP | {num(lb.slope, 2)} | {num(lb.slope - 1.96 * lb.stderr, 2)} a {num(lb.slope + 1.96 * lb.stderr, 2)} | {num(lb.rvalue ** 2, 2)} | {num(lb.pvalue, 3)} |
| LI_EP, só 2018–2026 | {num(li18.slope, 2)} | {num(li18.slope - 1.96 * li18.stderr, 2)} a {num(li18.slope + 1.96 * li18.stderr, 2)} | {num(li18.rvalue ** 2, 2)} | {num(li18.pvalue, 3)} |
| LB_EP, só 2018–2026 | {num(lb18.slope, 2)} | {num(lb18.slope - 1.96 * lb18.stderr, 2)} a {num(lb18.slope + 1.96 * lb18.stderr, 2)} | {num(lb18.rvalue ** 2, 2)} | {num(lb18.pvalue, 3)} |

![AC x escola pública]({fig})

*Figura 1 – Diferença mediana (linha) e faixa interquartil (sombra) entre AC e cotas de escola pública. Linhas pontilhadas marcam as mudanças de código de cota. Fonte: SISU/UFMG; elaboração própria.*

## Interpretação

- **Cota acima da AC.** Em {num(t.loc['2014-1', '% cota > AC – LI_EP'], 0)}% das ofertas de 2014-1, a nota de corte da LI_EP foi **maior** que a da AC. Essa fração caiu ao longo do tempo e é **zero de 2024 em diante**, nas duas cotas. Isso é compatível com regras de seleção em que quem tem nota para a AC entra por ela, deixando a cota para as notas menores. A base não contém as regras, então isso é uma hipótese.
- A subida até 2016 coincide com a implantação gradual da Lei de Cotas (Lei 12.711/2012), que dava às universidades até 2016 para reservar 50% das vagas. A base não tem o número de vagas por cota, então essa associação não pode ser testada aqui.
- O padrão observado também deve ser lido junto com as mudanças de regra posteriores: em 2018 entrou o recorte PCD separado e em 2024 o limite de renda da LB caiu de 1,5 para 1 salário mínimo. A série LI_EP é a mais limpa, porque não depende de renda.
- Uma distância menor indica que o último aprovado na cota ficou mais próximo do último aprovado na AC. Isso pode estar associado a mudanças no perfil dos candidatos, nas vagas ou nas regras de migração entre listas. A base não permite separar esses fatores.

## Limitações e ressalvas

- {RESSALVA_TEMPO}
- A equivalência de códigos entre eras é de confiança **média**, inferida das legendas dos PDFs, sem confirmação no edital.
- O limite de renda da LB_EP mudou em 2024. A comparação da LB_EP antes e depois de 2024 não é exatamente do mesmo grupo.
- A regressão linear ignora a dependência entre anos e as mudanças de regra. O intervalo de confiança é só indicativo.

## Como reproduzir

```bash
python scripts/10_ac_escola_publica.py
```
""")


def checar(res):
    m = res["m"]
    x = m[(m["edicao_chave"] == "2026-1") & (m["cota_padrao"] == "LI_EP")]["gap"].median()
    assert abs(x - res["tab"].loc["2026-1", "LI_EP"]) < 1e-9
    assert res["serie"]["pares"].min() > 40


def main():
    res = calcular()
    checar(res)
    post(res, figura(res))


if __name__ == "__main__":
    main()
