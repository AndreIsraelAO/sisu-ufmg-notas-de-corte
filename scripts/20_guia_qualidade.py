"""20 — Guia de uso e qualidade dos dados (rodar antes das outras análises)."""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from comum import base, escrever_post, final, ler, md, num, salvar

CHAVE = ["ano", "edicao_chave", "curso_id", "campus", "turno", "cota_padrao"]


def calcular():
    d, f = base(), final()
    cursos = ler("de_para_cursos.csv")
    checks = []

    def check(nome, ok, detalhe):
        checks.append({"Validação": nome, "Resultado": "PASSOU" if ok else "FALHOU", "Detalhe": detalhe})

    check("Linhas da base longa", len(d) == 52144, f"{len(d)} (esperado 52.144)")
    check("Linhas da base final", len(f) == 8405, f"{len(f)} (esperado 8.405)")
    dup = d.duplicated(CHAVE + ["chamada"]).sum()
    check("Chave única (edição × curso × campus × turno × chamada × cota)", dup == 0, f"{dup} duplicatas")
    check("Final = uma linha por chave sem chamada", f.duplicated(CHAVE).sum() == 0 and len(f) == d.groupby(CHAVE).ngroups,
          f"{d.groupby(CHAVE).ngroups} chaves")
    maxch = d.groupby(CHAVE)["chamada"].transform("max")
    check("is_final marca a maior chamada da chave", (d["is_final"] == (d["chamada"] == maxch)).all(), "comparado linha a linha")
    m = d[d["is_final"]].merge(f, on=CHAVE + ["chamada"], suffixes=("", "_f"))
    check("notas_corte_final.csv = linhas is_final da base longa",
          len(m) == len(f) and np.allclose(m["nota_min"], m["nota_min_f"]), f"{len(m)} linhas casadas")
    check("nota_min ≤ nota_max", (d["nota_min"] <= d["nota_max"]).all(), f"{(d['nota_min'] > d['nota_max']).sum()} violações")
    check("0 < nota ≤ 1000", d[["nota_min", "nota_max"]].gt(0).all().all() and d[["nota_min", "nota_max"]].le(1000).all().all(),
          f"mín {d['nota_min'].min()}, máx {d['nota_max'].max()}")
    s = d.sort_values(CHAVE + ["chamada"])
    sobe = (s.groupby(CHAVE)["nota_min"].diff() > 0).sum()
    check("nota_min nunca sobe entre chamadas", sobe == 0, f"{sobe} subidas")
    varmax = (s.groupby(CHAVE)["nota_max"].nunique() > 1).sum()
    check("nota_max constante entre chamadas", varmax == 0, f"{varmax} chaves com nota_max variável")
    nreg = d[d["regular"]].groupby("edicao_chave")["chamada"].nunique()
    check("Uma chamada regular por edição", (nreg == 1).all(), "0 em todas, exceto 11 (2016) e 10 (2017)")
    sem = set(d["curso_id"]) - set(cursos["curso_id"])
    check("Todo curso_id está em de_para_cursos.csv", not sem, f"{len(sem)} sem mapeamento")
    baixa = sorted(d.loc[d["cota_confianca"] == "baixa", "cota_padrao"].unique())
    check("Confiança baixa só nos códigos legados PPI+PCD", baixa == ["LB_PPI_PCD", "LI_PPI_PCD"], ", ".join(baixa))
    q24 = d[(d["ano"] == 2024) & d["cota_padrao"].isin(["LB_Q", "LI_Q"])]
    check("2024 sem cota quilombola na base (só no PDF)", q24.empty, f"{len(q24)} linhas")
    ac = d[d["cota_padrao"] == "AC"]
    check("Toda oferta da chamada regular tem linha AC",
          d[d["regular"]].groupby(["edicao_chave", "curso_id", "campus", "turno"]).ngroups
          == ac[ac["regular"]].groupby(["edicao_chave", "curso_id", "campus", "turno"]).ngroups, "ofertas comparadas")
    checks = pd.DataFrame(checks)

    por_ed = d.groupby("edicao_chave").agg(
        linhas=("nota_min", "size"),
        linhas_regular=("regular", "sum"),
        chamadas=("chamada", lambda c: ", ".join(map(str, sorted(c.unique())))),
        ofertas=("oferta", "nunique"),
        cursos=("curso_id", "nunique"),
        cotas=("cota_padrao", "nunique"),
    ).reset_index()
    por_ed["linhas_final"] = f.groupby("edicao_chave").size().values
    era = d.groupby(["era_cota", "cota_confianca"])["cota_padrao"].agg(lambda c: ", ".join(sorted(c.unique()))).reset_index()
    return {"checks": checks, "por_ed": por_ed, "era": era, "d": d}


def figura(res):
    p = res["por_ed"]
    d = res["d"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.8))
    x = np.arange(len(p))
    a1.bar(x, p["linhas_regular"], label="Chamada regular")
    a1.bar(x, p["linhas"] - p["linhas_regular"], bottom=p["linhas_regular"], label="Listas de espera")
    a1.set_xticks(x, p["edicao_chave"], rotation=60)
    a1.set_ylabel("Linhas na base (curso × turno × cota × chamada)")
    a1.set_xlabel("Edição do SISU")
    a1.set_title("Linhas por edição: o salto de 2022–2023 vem das listas de espera")
    a1.legend()
    ch = d[["edicao_chave", "chamada"]].drop_duplicates()
    ch["x"] = ch["edicao_chave"].map({e: i for i, e in enumerate(p["edicao_chave"])})
    a2.scatter(ch["x"], ch["chamada"], s=28, color="#0072B2")
    a2.set_xticks(x, p["edicao_chave"], rotation=60)
    a2.set_ylabel("Número da chamada (0 = regular)")
    a2.set_xlabel("Edição do SISU")
    a2.set_title("Chamadas presentes: lacunas em 2022 e 2023")
    return salvar(fig, "20_linhas_e_chamadas")


def post(res, fig):
    c, p, era = res["checks"], res["por_ed"], res["era"]
    n_ok = (c["Resultado"] == "PASSOU").sum()
    escrever_post("20-guia-uso-e-qualidade", f"""
# Antes de tudo: como esta base funciona e onde ela engana

**Resumo.** A base tem {num(len(res['d']), 0)} linhas e 15 edições do SISU/UFMG (2014–2026). Todas as {n_ok} de {len(c)} validações automáticas passaram. Os maiores riscos não são erros nos números, e sim armadilhas de uso: 2014 e 2015 têm duas edições, a nota de corte cai a cada chamada da lista de espera e os códigos de cota mudaram duas vezes.

## Pergunta

Os dados são confiáveis e quais regras evitam conclusões erradas nas outras 19 análises?

## Dados usados

- `data/notas_corte.csv`: base longa, uma linha por edição × curso × campus × turno × chamada × cota.
- `data/notas_corte_final.csv`: só a maior chamada de cada chave (`is_final == True`).
- `data/de_para_cursos.csv` e `data/de_para_cotas.csv`: tabelas de equivalência.
- Nenhum filtro: este post olha a base inteira.

## Método

O script `scripts/20_guia_qualidade.py` refaz, a partir dos CSVs prontos, as checagens que importam para as análises. Exemplos: a chave é única, `nota_min ≤ nota_max`, a nota mínima nunca sobe de uma chamada para a seguinte e `notas_corte_final.csv` é igual às linhas `is_final` da base longa. Se alguma falhar, o script para com erro. A conferência contra os PDFs oficiais foi feita na construção da base e está em [`docs/relatorio_qualidade_base.md`](../docs/relatorio_qualidade_base.md).

## Resultados

**Tabela 1 – Validações automáticas.**

{md(c)}

**Tabela 2 – Cobertura por edição.** "Ofertas" = combinações curso × campus × turno.

{md(p[['edicao_chave', 'linhas', 'linhas_regular', 'linhas_final', 'ofertas', 'cursos', 'cotas', 'chamadas']].set_axis(
        ['Edição', 'Linhas', 'Linhas (regular)', 'Linhas (final)', 'Ofertas', 'Cursos', 'Cotas', 'Chamadas presentes'], axis=1))}

![Linhas e chamadas por edição]({fig})

*Figura 1 – À esquerda, linhas por edição, separando chamada regular e listas de espera. À direita, quais chamadas existem em cada edição. Fonte: SISU/UFMG; elaboração própria.*

**Tabela 3 – Eras de cota e confiança da equivalência.**

{md(era.rename(columns={'era_cota': 'Era', 'cota_confianca': 'Confiança', 'cota_padrao': 'Códigos padronizados'}))}

## Interpretação: as regras usadas em todo o projeto

1. **Edição, não ano.** 2014 e 2015 tiveram duas edições (`2014-1`, `2014-2`...). A segunda edição oferece menos cursos ({p.loc[p.edicao_chave == '2014-2', 'ofertas'].iat[0]} ofertas em 2014-2 contra {p.loc[p.edicao_chave == '2014-1', 'ofertas'].iat[0]} em 2014-1). Todas as análises agrupam por `edicao_chave`.
2. **Chamada regular para séries longas.** De 2014 a 2021 só existe a chamada regular. A partir de 2022 aparecem as listas de espera, e a nota mínima cai a cada chamada. Misturar as duas coisas criaria uma "queda" artificial. Por isso as séries 2014–2026 usam a **chamada regular**, definida como a menor chamada da edição: 0 em quase todas, mas **11 em 2016 e 10 em 2017**, que tiveram um único PDF de chamada regular.
3. **Nota "final"** (`is_final`) só é usada quando a pergunta envolve a lista de espera (posts 04 e 15). Ela é a maior chamada *presente nos dados*: **2022 só tem as chamadas {p.loc[p.edicao_chave == '2022-1', 'chamadas'].iat[0]}** e 2023 não tem as chamadas 2, 4 e 6.
4. **Cotas entre eras.** E1 (2014–2017) usava códigos 1–4, E2 (2018–2023) usava 1.1–4.2 e E3 (2024+) usa LB/LI. Comparações entre eras usam só equivalências de confiança alta ou média. Os códigos `LB_PPI_PCD` e `LI_PPI_PCD` (confiança baixa) nunca são comparados com outras eras. O limite de renda das cotas "LB" passou de 1,5 para 1 salário mínimo em 2024. As cotas "LI" (independentes de renda) não sofrem essa mudança e são as preferidas para séries longas.
5. **Quilombolas.** Em 2024 a lista de quilombolas existe só no PDF e não está na base. LB_Q e LI_Q aparecem a partir de 2025.
6. **Cursos renomeados.** O `curso_id` é estável, mas a base **não** uniu renomeações prováveis, como Antropologia → Antropologia e Arqueologia (2024) e Engenharia Metalúrgica → Metalúrgica e de Materiais (2024). Também não uniu Ciência da Computação e Sistemas de Informação → curso combinado (2025). Este projeto mantém essa decisão: cada nome é tratado como curso próprio.
7. **Turno 2014.** Os PDFs de 2014 dizem "Diurno" e "Tarde". A base converte para Matutino e Vespertino com base na correspondência com 2015 (`turno_ajustado`).

## Limitações e ressalvas

- A conferência contra os PDFs foi amostral (5 linhas por ano) mais uma reconciliação de valores para 2015+. Não houve releitura célula a célula.
- A base não tem número de vagas nem de candidatos. "Concorrência" é sempre inferida pela nota de corte.
- Grupos de cota com uma ou duas vagas (sobretudo PCD) podem ter notas de corte muito baixas ou muito altas por causa de um único candidato.
- As notas do ENEM e as vagas mudam a cada ano. Comparações no tempo descrevem o que foi observado, sem explicar a causa.
- A base é agregada por curso, campus, turno e cota e não contém dados pessoais.

## Como reproduzir

```bash
python scripts/20_guia_qualidade.py
```

Para rodar tudo: `python scripts/run_all.py`.
""")


def checar(res):
    c = res["checks"]
    falhas = c[c["Resultado"] != "PASSOU"]
    assert falhas.empty, f"Validações falharam:\n{falhas}"


def main():
    res = calcular()
    checar(res)
    post(res, figura(res))


if __name__ == "__main__":
    main()
