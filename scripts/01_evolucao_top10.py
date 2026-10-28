"""01 — Evolução da nota de corte das 10 ofertas com maior nota (chamada regular, AC, BH)."""
import matplotlib.pyplot as plt

from comum import RESSALVA_CORTE, RESSALVA_TEMPO, escrever_post, md, num, regular_ac, salvar

RECENTES = ["2024-1", "2025-1", "2026-1"]
MIN_EDICOES = 13  # de 15: exige série longa para que "evolução" faça sentido


def calcular():
    r = regular_ac()
    p = r.pivot_table(index="oferta", columns="edicao_chave", values="nota_min")
    elegiveis = p[p[RECENTES].notna().all(axis=1) & (p.notna().sum(axis=1) >= MIN_EDICOES)]
    top = elegiveis[RECENTES].mean(axis=1).sort_values(ascending=False).head(10).index
    serie = p.loc[top]
    tab = serie[["2014-1", "2018-1", "2022-1", "2026-1"]].copy()
    tab["média 2024–26"] = serie[RECENTES].mean(axis=1)
    tab["variação 2014-1→2026-1"] = serie["2026-1"] - serie["2014-1"]
    return {"r": r, "serie": serie, "tab": tab.round(2), "n_eleg": len(elegiveis), "n_total": len(p)}


def figura(res):
    s = res["serie"]
    fig, ax = plt.subplots(figsize=(11, 6))
    estilos = ["-", "--"]
    for i, (nome, linha) in enumerate(s.iterrows()):
        ax.plot(s.columns, linha.values, marker="o", ms=3.5, ls=estilos[i // 8], label=nome)
    ax.set_title("Nota de corte das 10 ofertas com maior nota em 2024–2026\n(chamada regular, ampla concorrência, Belo Horizonte)")
    ax.set_xlabel("Edição do SISU")
    ax.set_ylabel("Nota de corte (nota do último classificado)")
    ax.tick_params(axis="x", rotation=60)
    ax.legend(fontsize=8, loc="center left", bbox_to_anchor=(1, 0.5), title="Curso – turno")
    return salvar(fig, "01_evolucao_top10")


def post(res, fig):
    t = res["tab"]
    sobe = (t["variação 2014-1→2026-1"] > 0).sum()
    lider = t.index[0]
    med_var = t["variação 2014-1→2026-1"].median()
    escrever_post("01-evolucao-maiores-notas", f"""
# As maiores notas de corte da UFMG subiram, e Medicina segue isolada no topo

**Resumo.** Entre as ofertas de Belo Horizonte com série longa, as 10 com maior nota de corte em 2024–2026 são, em geral, as mesmas engenharias e cursos de prestígio. {sobe} das 10 tiveram em 2026 nota maior que em 2014 (mediana de {num(med_var)} pontos). **{lider}** lidera com média de {num(t.iloc[0]['média 2024–26'])} pontos em 2024–2026.

## Pergunta

Como evoluiu, de 2014 a 2026, a nota de corte das ofertas com as maiores notas da UFMG em Belo Horizonte?

## Dados usados

- `data/notas_corte.csv`, filtrado em: chamada regular (menor chamada da edição), cota `AC` (ampla concorrência), campus Belo Horizonte.
- Unidade: **oferta** = curso (`curso_id`) × turno. Cada turno tem nota de corte própria.
- Ofertas elegíveis: presentes em 2024, 2025 e 2026 **e** em pelo menos {MIN_EDICOES} das 15 edições ({res['n_eleg']} de {res['n_total']} ofertas). Isso deixa de fora cursos novos, como Ciência de Dados e Engenharia de Computação, que aparecem no post 02.

## Método

1. Para cada oferta, calculamos a média da nota de corte em 2024-1, 2025-1 e 2026-1.
2. As 10 maiores médias formam o grupo analisado.
3. Mostramos a série completa por edição (2014 e 2015 têm duas edições cada) e a variação simples `nota(2026-1) − nota(2014-1)`.

## Resultados

**Tabela 1 – Nota de corte (AC, chamada regular) em edições selecionadas.**

{md(t, index=True)}

![Evolução das maiores notas]({fig})

*Figura 1 – Nota de corte por edição das 10 ofertas com maior média em 2024–2026. Linhas tracejadas apenas distinguem as últimas séries. Fonte: SISU/UFMG; elaboração própria.*

## Interpretação

- As 10 ofertas ficaram mais próximas entre si: a distância entre a maior e a menor nota do grupo era de {num(res['serie']['2014-1'].max() - res['serie']['2014-1'].min())} pontos em 2014-1 e de {num(res['serie']['2026-1'].max() - res['serie']['2026-1'].min())} pontos em 2026-1.
- O grupo do topo é estável: Medicina, engenharias tradicionais (Aeroespacial, Química, Mecânica), Direito e Economia estão perto do teto ao longo de toda a série.
- A segunda edição de 2014 e de 2015 (`2014-2`, `2015-2`) costuma ter notas menores que a primeira. Isso é associado à edição, não a uma queda do curso. Por isso as edições nunca são juntadas por ano.
- A alta observada em 2026 em várias ofertas é uma **diferença observada**. Não dá para dizer, só com esta base, se ela vem de mais candidatos, de menos vagas ou de mudança na escala do ENEM.

## Limitações e ressalvas

- {RESSALVA_CORTE}
- {RESSALVA_TEMPO}
- Ciência da Computação (Matutino) deixa de existir em 2025 com esse nome. O curso combinado "Ciência da Computação e Sistemas de Informação" é tratado como outro curso (veja o post 20).
- 2016 e 2017 usam a chamada 11 e 10, que é a chamada regular única dessas edições.

## Como reproduzir

```bash
python scripts/01_evolucao_top10.py
```
""")


def checar(res):
    r = res["r"]
    v = r[(r["oferta"] == "Medicina – Integral") & (r["edicao_chave"] == "2026-1")]["nota_min"]
    assert len(v) == 1 and abs(v.iat[0] - res["serie"].loc["Medicina – Integral", "2026-1"]) < 1e-9
    assert len(res["serie"]) == 10


def main():
    res = calcular()
    checar(res)
    post(res, figura(res))


if __name__ == "__main__":
    main()
