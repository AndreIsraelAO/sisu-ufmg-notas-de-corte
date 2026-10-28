"""02 — Ranking por edição: quais ofertas ficam no topo de forma estável?"""
import matplotlib.pyplot as plt

from comum import RESSALVA_CORTE, RESSALVA_TEMPO, escrever_post, md, regular_ac, salvar

TOP = 10


def calcular():
    r = regular_ac()
    r["posicao"] = r.groupby("edicao_chave")["nota_min"].rank(ascending=False, method="min").astype(int)
    n_ed = r["edicao_chave"].nunique()
    no_top = r[r["posicao"] <= TOP]
    cont = no_top.groupby("oferta").agg(vezes_no_top10=("posicao", "size"), melhor=("posicao", "min"),
                                        mediana=("posicao", "median"))
    cont["edições_existentes"] = r.groupby("oferta")["edicao_chave"].nunique().reindex(cont.index)
    cont = cont.sort_values(["vezes_no_top10", "mediana"], ascending=[False, True])
    lideres = r[r["posicao"] == 1][["edicao_chave", "oferta", "nota_min"]].sort_values("edicao_chave")
    posicoes = r[r["oferta"].isin(cont.index[:12])].pivot_table(index="oferta", columns="edicao_chave", values="posicao")
    return {"r": r, "cont": cont, "lideres": lideres, "posicoes": posicoes.loc[cont.index[:12]], "n_ed": n_ed}


def figura(res):
    c = res["cont"].iloc[::-1]
    fig, ax = plt.subplots(figsize=(9, 7))
    cores = ["#0072B2" if v == res["n_ed"] else "#56B4E9" for v in c["vezes_no_top10"]]
    ax.barh(c.index, c["vezes_no_top10"], color=cores)
    ax.axvline(res["n_ed"], color="#444", ls=":", lw=1)
    ax.set_xlabel(f"Número de edições no top {TOP} (de {res['n_ed']})")
    ax.set_ylabel("Oferta (curso – turno)")
    ax.set_title(f"Quantas vezes cada oferta ficou entre as {TOP} maiores\nnotas de corte (AC, chamada regular, BH)\nazul escuro = no top {TOP} em todas as edições", fontsize=10)
    ax.tick_params(axis="y", labelsize=8)
    return salvar(fig, "02_ranking_top10")


def post(res, fig):
    c, n = res["cont"], res["n_ed"]
    sempre = c[c["vezes_no_top10"] == n].index.tolist()
    med1 = res["lideres"]["oferta"].value_counts()
    escrever_post("02-ranking-topo", f"""
# Medicina liderou todas as edições; só {len(sempre)} ofertas ficaram sempre no top 10

**Resumo.** Em {n} edições do SISU/UFMG (2014–2026), {len(c)} ofertas diferentes entraram ao menos uma vez no top {TOP} de nota de corte (ampla concorrência, chamada regular, BH). Só {len(sempre)} estiveram lá em todas: {', '.join(sempre)}. **{med1.index[0]}** teve a maior nota em {med1.iat[0]} das {n} edições.

## Pergunta

Quais ofertas aparecem no topo do ranking de nota de corte de forma estável, e quais entram e saem?

## Dados usados

- `data/notas_corte.csv`: chamada regular, cota `AC`, campus Belo Horizonte.
- Unidade: oferta = curso × turno, em cada uma das 15 edições (`edicao_chave`).

## Método

Em cada edição, as ofertas são ordenadas pela nota de corte, da maior para a menor (posição 1 = maior nota; empates recebem a mesma posição). Para cada oferta, contamos quantas vezes ela ficou entre as {TOP} primeiras e anotamos a melhor posição e a mediana das posições nessas vezes. A coluna "edições existentes" mostra em quantas edições a oferta existia, porque um curso novo não pode ter aparecido antes de existir.

## Resultados

**Tabela 1 – Ofertas que entraram no top {TOP} ao menos uma vez.**

{md(c.reset_index().rename(columns={'oferta': 'Oferta', 'vezes_no_top10': 'Vezes no top 10', 'melhor': 'Melhor posição', 'mediana': 'Mediana da posição (no top 10)', 'edições_existentes': 'Edições existentes'}), decimais=1)}

![Vezes no top 10]({fig})

*Figura 1 – Número de edições em que cada oferta ficou entre as 10 maiores notas de corte. Fonte: SISU/UFMG; elaboração própria.*

**Tabela 2 – Maior nota de corte de cada edição.**

{md(res['lideres'].rename(columns={'edicao_chave': 'Edição', 'oferta': 'Oferta', 'nota_min': 'Nota de corte'}))}

**Tabela 3 – Posição no ranking das 12 ofertas mais frequentes, por edição** (vazio = oferta não existia na edição).

{md(res['posicoes'].astype('Int64').astype(str).replace('<NA>', '').reset_index().rename(columns={'oferta': 'Oferta'}))}

## Interpretação

- O topo é dominado por um mesmo grupo de cursos. A rotatividade acontece sobretudo nas últimas posições do top 10, onde as diferenças de nota são de poucos pontos.
- Cursos criados recentemente (Ciência de Dados em 2024; Engenharia de Computação e o curso combinado de Ciência da Computação e Sistemas de Informação em 2025) entram direto no topo. Eles aparecem poucas vezes na tabela só porque existem há pouco tempo.
- Estar no top 10 está associado a cursos de alta procura, mas a posição também depende do número de vagas da oferta.

## Limitações e ressalvas

- {RESSALVA_CORTE}
- {RESSALVA_TEMPO}
- O número de ofertas por edição varia (77 em 2014-1, 56 em 2014-2, 94 em 2026-1). A posição 10 numa edição pequena não equivale exatamente à posição 10 numa edição grande.

## Como reproduzir

```bash
python scripts/02_ranking_topo.py
```
""")


def checar(res):
    r = res["r"]
    for ed, g in r.groupby("edicao_chave"):
        lider = res["lideres"].set_index("edicao_chave").loc[ed, "nota_min"]
        assert lider == g["nota_min"].max(), ed
    assert res["cont"]["vezes_no_top10"].sum() == (r["posicao"] <= TOP).sum()


def main():
    res = calcular()
    checar(res)
    post(res, figura(res))


if __name__ == "__main__":
    main()
