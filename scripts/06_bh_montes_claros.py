"""06 — Belo Horizonte × Montes Claros: o mesmo curso nos dois campi."""
import matplotlib.pyplot as plt

from comum import RESSALVA_CORTE, RESSALVA_TEMPO, escrever_post, md, num, regular_ac, salvar


def calcular():
    r = regular_ac(campus=None)
    # Cursos (curso_id) oferecidos nos dois campi na mesma edição.
    dois = r.groupby(["edicao_chave", "curso_id"])["campus"].nunique()
    comuns = sorted(dois[dois == 2].reset_index()["curso_id"].unique())
    par = r[r["curso_id"].isin(comuns) & (r["turno"] == "Noturno")]
    par = par.pivot_table(index="edicao_chave", columns="campus", values="nota_min").dropna()
    par["diferença (BH − MOC)"] = par["Belo Horizonte"] - par["Montes Claros"]
    geral = r.groupby(["edicao_chave", "campus"])["nota_min"].median().unstack()
    n_of = r.groupby(["edicao_chave", "campus"])["oferta"].nunique().unstack()
    geral["diferença das medianas"] = geral["Belo Horizonte"] - geral["Montes Claros"]
    geral["ofertas BH"], geral["ofertas MOC"] = n_of["Belo Horizonte"], n_of["Montes Claros"]
    return {"r": r, "comuns": comuns, "par": par, "geral": geral}


def figura(res):
    par, geral = res["par"], res["geral"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    for i, c in enumerate(["Belo Horizonte", "Montes Claros"]):
        a1.plot(par.index, par[c], marker="o", label=c, color=["#0072B2", "#D55E00"][i])
        a2.plot(geral.index, geral[c], marker="o", label=c, color=["#0072B2", "#D55E00"][i])
    a1.set_title("Administração – Noturno (único curso nos dois campi)")
    a2.set_title("Mediana de todas as ofertas do campus")
    for a in (a1, a2):
        a.set_xlabel("Edição do SISU")
        a.tick_params(axis="x", rotation=60)
        a.legend(title="Campus")
    a1.set_ylabel("Nota de corte (AC, chamada regular)")
    return salvar(fig, "06_bh_montes_claros")


def post(res, fig):
    par, geral = res["par"], res["geral"]
    antes = par.loc[par.index < "2018-1", "diferença (BH − MOC)"].mean()
    depois = par.loc[par.index >= "2018-1", "diferença (BH − MOC)"].mean()
    escrever_post("06-bh-x-montes-claros", f"""
# Belo Horizonte × Montes Claros: a diferença caiu muito a partir de 2018

**Resumo.** Só um curso é oferecido nos dois campi: **Administração (Noturno)**. Nele, a nota de corte de BH superou a de Montes Claros em média {num(antes)} pontos de 2014 a 2017 e {num(depois)} pontos de 2018 a 2026. A mesma redução aparece na mediana geral dos campi, mas lá os cursos são diferentes.

## Pergunta

Para os cursos oferecidos nos dois campi, qual a diferença de nota de corte entre Belo Horizonte e Montes Claros?

## Dados usados

- `data/notas_corte.csv`: chamada regular, cota `AC`, dois campi.
- Cursos presentes nos dois campi na mesma edição, pelo `curso_id`: **{', '.join(res['comuns'])}**. Os dois são do turno Noturno.
- Edições em que os dois campi aparecem: {len(par)} (Montes Claros não aparece nas segundas edições de 2014 e 2015).

## Método

- **Comparação pareada:** `diferença = nota(BH) − nota(MOC)` para o mesmo curso, turno, cota e edição.
- **Complemento:** mediana da nota de corte de todas as ofertas de cada campus. Essa comparação mistura cursos diferentes (Montes Claros tem Agronomia, Zootecnia e engenharias agrárias; BH tem quase todo o resto) e serve só de contexto.

## Resultados

**Tabela 1 – Administração – Noturno, nota de corte AC.**

{md(par, index=True)}

**Tabela 2 – Mediana das notas de corte por campus (cursos diferentes).**

{md(geral, index=True, decimais=1)}

![BH x Montes Claros]({fig})

*Figura 1 – Esquerda: Administração – Noturno nos dois campi. Direita: mediana das notas de corte de cada campus. Fonte: SISU/UFMG; elaboração própria.*

## Interpretação

- Com um único curso em comum, a comparação "mesmo curso, outro campus" é um estudo de caso, não uma regra geral.
- A diferença de Administração diminuiu de forma brusca entre 2017-1 e 2018-1 ({num(par.loc['2017-1', 'diferença (BH − MOC)'])} → {num(par.loc['2018-1', 'diferença (BH − MOC)'])} pontos). Isso coincide com a mudança do sistema de cotas (era E2) e com outras mudanças no SISU, mas a base não permite atribuir uma causa.
- Mesmo depois de 2018, BH segue com nota de corte maior em todas as edições.

## Limitações e ressalvas

- **Esta análise foi ajustada:** a pergunta original pedia "os cursos oferecidos nos dois campi", mas a base só tem um. O complemento por campus inteiro não compara cursos iguais.
- {RESSALVA_CORTE}
- {RESSALVA_TEMPO}
- O número de vagas de cada campus não está na base.

## Como reproduzir

```bash
python scripts/06_bh_montes_claros.py
```
""")


def checar(res):
    r = res["r"]
    x = r[(r["curso_id"] == "administracao-bach") & (r["edicao_chave"] == "2026-1") & (r["turno"] == "Noturno")]
    bh = x[x["campus"] == "Belo Horizonte"]["nota_min"].iat[0]
    moc = x[x["campus"] == "Montes Claros"]["nota_min"].iat[0]
    assert abs(res["par"].loc["2026-1", "diferença (BH − MOC)"] - (bh - moc)) < 1e-9
    assert res["comuns"] == ["administracao-bach"], "mudou o conjunto de cursos nos dois campi; revise o texto"


def main():
    res = calcular()
    checar(res)
    post(res, figura(res))


if __name__ == "__main__":
    main()
