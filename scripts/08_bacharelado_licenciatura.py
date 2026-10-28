"""08 — Bacharelado × Licenciatura nos cursos que têm as duas modalidades."""
import matplotlib.pyplot as plt

from comum import RESSALVA_CORTE, RESSALVA_TEMPO, escrever_post, md, num, regular_ac, salvar


def calcular():
    r = regular_ac(campus=None)
    r["base"] = r["curso_id"].str.replace(r"-(bach|lic)$", "", regex=True)
    p = r.pivot_table(index=["base", "curso_nome", "campus", "turno", "edicao_chave"], columns="modelo", values="nota_min")
    p = p.dropna().reset_index()  # mesmo curso, campus, turno e edição nas duas modalidades
    p["dif"] = p["Bacharelado"] - p["Licenciatura"]
    p["par"] = p["curso_nome"] + " – " + p["turno"]
    resumo = p.groupby("par").agg(edicoes=("dif", "size"), bach=("Bacharelado", "mean"), lic=("Licenciatura", "mean"),
                                  dif_media=("dif", "mean"), bach_maior=("dif", lambda d: int((d > 0).sum()))).reset_index()
    return {"r": r, "p": p, "resumo": resumo}


def figura(res):
    p = res["p"]
    pares = [x for x in res["resumo"].sort_values("edicoes", ascending=False)["par"] if (p["par"] == x).sum() > 1]
    fig, axs = plt.subplots(1, len(pares), figsize=(5 * len(pares), 4.8), sharey=True)
    for ax, par in zip(axs, pares):
        g = p[p["par"] == par]
        ax.plot(g["edicao_chave"], g["Bacharelado"], marker="o", label="Bacharelado", color="#0072B2")
        ax.plot(g["edicao_chave"], g["Licenciatura"], marker="s", ls="--", label="Licenciatura", color="#D55E00")
        ax.set_title(par, fontsize=10)
        ax.set_xlabel("Edição do SISU")
        ax.tick_params(axis="x", rotation=60)
    axs[0].set_ylabel("Nota de corte (AC, chamada regular)")
    axs[0].legend()
    fig.suptitle("Bacharelado × Licenciatura no mesmo curso, turno e edição")
    return salvar(fig, "08_bacharelado_licenciatura")


def post(res, fig):
    s, p = res["resumo"], res["p"]
    escrever_post("08-bacharelado-x-licenciatura", f"""
# Onde dá para comparar, o bacharelado teve nota de corte maior que a licenciatura

**Resumo.** Só há {len(s)} pares bacharelado/licenciatura no mesmo curso, turno e edição: {', '.join(s['par'])}. O bacharelado teve nota de corte maior em {int(s['bach_maior'].sum())} das {len(p)} comparações, com diferença média por par entre {num(s['dif_media'].min())} e {num(s['dif_media'].max())} pontos.

## Pergunta

Nos cursos que oferecem as duas modalidades, o bacharelado e a licenciatura têm notas de corte diferentes?

## Dados usados

- `data/notas_corte.csv`: chamada regular, cota `AC`, dois campi.
- Pares formados pelo nome do curso sem o sufixo de modalidade (`curso_id` sem `-bach`/`-lic`), no **mesmo turno e edição**.
- Ficam de fora: "Letras (sem modalidade, pré-2018)", que não tem par; e licenciaturas que existiram só em 2014 (Física, Geografia, História, Matemática, Química, Ciências Biológicas), porque nessas edições o bacharelado do mesmo turno não aparece.
- **Atenção:** na base, Pedagogia está marcada como Bacharelado e não tem licenciatura correspondente, então não entra.

## Método

`diferença = nota(Bacharelado) − nota(Licenciatura)` por par e edição. Mostramos a média por par e quantas vezes o bacharelado teve a nota maior.

## Resultados

**Tabela 1 – Resumo por par.**

{md(s.rename(columns={'par': 'Curso – turno', 'edicoes': 'Edições', 'bach': 'Bacharelado (média)', 'lic': 'Licenciatura (média)', 'dif_media': 'Diferença média (B − L)', 'bach_maior': 'Edições com B > L'}), decimais=1)}

**Tabela 2 – Todas as comparações.**

{md(p[['par', 'edicao_chave', 'Bacharelado', 'Licenciatura', 'dif']].rename(columns={'par': 'Curso – turno', 'edicao_chave': 'Edição', 'dif': 'Diferença'}))}

![Bacharelado x Licenciatura]({fig})

*Figura 1 – Nota de corte do bacharelado e da licenciatura nos pares com mais de uma edição. Fonte: SISU/UFMG; elaboração própria.*

## Interpretação

- Nos pares disponíveis o padrão é consistente: bacharelado acima. Mas são só três cursos, todos de Belo Horizonte, e não dá para generalizar para a universidade.
- Em Educação Física a série é longa (15 edições) e a diferença aparece em todas, com média de {num(s.set_index('par').loc['Educação Física – Matutino', 'dif_media'])} pontos. Em Letras, as modalidades só aparecem separadas a partir de 2018.
- Diferenças de nota entre modalidades estão associadas a diferenças de procura e de vagas, que a base não informa.

## Limitações e ressalvas

- Poucos pares; a comparação é descritiva.
- {RESSALVA_CORTE}
- {RESSALVA_TEMPO}

## Como reproduzir

```bash
python scripts/08_bacharelado_licenciatura.py
```
""")


def checar(res):
    r, p = res["r"], res["p"]
    x = r[(r["curso_id"].str.startswith("educacao-fisica")) & (r["edicao_chave"] == "2026-1") & (r["turno"] == "Matutino")]
    d = x[x["modelo"] == "Bacharelado"]["nota_min"].iat[0] - x[x["modelo"] == "Licenciatura"]["nota_min"].iat[0]
    y = p[(p["base"] == "educacao-fisica") & (p["edicao_chave"] == "2026-1")]["dif"].iat[0]
    assert abs(d - y) < 1e-9


def main():
    res = calcular()
    checar(res)
    post(res, figura(res))


if __name__ == "__main__":
    main()
