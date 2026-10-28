"""07 — Turnos: diferença de nota entre o noturno e o turno diurno do mesmo curso na mesma edição."""
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from comum import RESSALVA_CORTE, RESSALVA_TEMPO, escrever_post, md, num, regular_ac, salvar


def nome(d):
    return d["curso_nome"] + d["modelo"].eq("Licenciatura").map({True: " (Lic.)", False: ""})


def calcular():
    r = regular_ac(campus=None)
    r["curso"] = nome(r)
    chave = ["edicao_chave", "curso_id", "campus"]
    # Só existem pares noturno × diurno: Matutino, Vespertino e Integral nunca coexistem no mesmo curso e edição.
    multi = r[r["turno"] != "Noturno"].groupby(chave)["turno"].nunique()
    assert (multi <= 1).all(), "há dois turnos diurnos no mesmo curso/edição; revise o método"
    diurno = r[r["turno"] != "Noturno"][chave + ["turno", "nota_min"]].rename(columns={"turno": "diurno", "nota_min": "nota_dia"})
    m = r[r["turno"] == "Noturno"].merge(diurno, on=chave)
    m["dif"] = m["nota_min"] - m["nota_dia"]  # Noturno − diurno
    resumo = m.groupby("diurno").agg(pares=("dif", "size"), cursos=("curso_id", "nunique"), mediana=("dif", "median"),
                                     media=("dif", "mean"), pct_menor=("dif", lambda x: (x < 0).mean() * 100)).reset_index()
    tot = {"diurno": "Todos", "pares": len(m), "cursos": m["curso_id"].nunique(), "mediana": m["dif"].median(),
           "media": m["dif"].mean(), "pct_menor": (m["dif"] < 0).mean() * 100}
    resumo.loc[len(resumo)] = tot
    por_curso = m.groupby("curso").agg(edicoes=("dif", "size"), dif_media=("dif", "mean"), min=("dif", "min"),
                                       max=("dif", "max"), pct_menor=("dif", lambda x: (x < 0).mean() * 100))
    # Cursos cujo turno diurno mudou de nome em 2025.
    t24 = r[(r["edicao_chave"] == "2024-1") & (r["turno"] != "Noturno")].set_index(["curso_id", "campus"])["turno"]
    t25 = r[(r["edicao_chave"] == "2025-1") & (r["turno"] != "Noturno")].set_index(["curso_id", "campus"])["turno"]
    mud = t24.to_frame("2024-1").join(t25.rename("2025-1"), how="inner")
    mud = mud[mud["2024-1"] != mud["2025-1"]].reset_index()
    mud["curso"] = mud["curso_id"].map(r.drop_duplicates("curso_id").set_index("curso_id")["curso_nome"])
    return {"r": r, "m": m, "resumo": resumo, "por_curso": por_curso.sort_values("dif_media"), "mud": mud}


def figura(res):
    pc = res["por_curso"].iloc[::-1]
    fig, ax = plt.subplots(figsize=(10, 7))
    cor = ["#0072B2" if v < 0 else "#D55E00" for v in pc["dif_media"]]
    ax.barh(pc.index, pc["dif_media"], color=cor)
    ax.axvline(0, color="#333", lw=1)
    ax.set_xlabel("Diferença média: nota de corte do Noturno − nota do turno diurno (pontos)")
    ax.set_ylabel("Curso")
    ax.set_title("Noturno × turno diurno do mesmo curso e edição\n(AC, chamada regular, 2014–2026)")
    ax.tick_params(axis="y", labelsize=8)
    ax.legend(handles=[Patch(color="#0072B2", label="Noturno com nota menor"), Patch(color="#D55E00", label="Noturno com nota maior")])
    return salvar(fig, "07_turnos")


def post(res, fig):
    s = res["resumo"].set_index("diurno")
    pc, mud = res["por_curso"], res["mud"]
    noite_maior = pc[pc["dif_media"] > 0].index.tolist()
    escrever_post("07-turnos", f"""
# O noturno tem nota de corte menor que o turno diurno em {num(s.loc['Todos', 'pct_menor'], 0)}% das comparações

**Resumo.** Comparando o mesmo curso, edição e campus (ampla concorrência, chamada regular), o Noturno teve nota de corte menor que o turno diurno em {num(s.loc['Todos', 'pct_menor'], 0)}% dos {s.loc['Todos', 'pares']} pares, com diferença mediana de {num(s.loc['Todos', 'mediana'])} pontos. As maiores diferenças estão em {", ".join(pc.index[:4])}. {"Só em " + " e ".join(noite_maior) + " o noturno teve, em média, nota um pouco maior." if noite_maior else ""}

## Pergunta

Nos cursos com mais de um turno, existe diferença de nota de corte entre Matutino, Vespertino, Noturno e Integral?

## Dados usados

- `data/notas_corte.csv`: chamada regular, cota `AC`, dois campi, 15 edições.
- Cursos que, na **mesma edição e campus**, têm o turno Noturno e um turno diurno.

**Achado de dados que mudou a análise:** Matutino, Vespertino e Integral **nunca coexistem** no mesmo curso e edição (o script verifica isso). A única comparação possível é **Noturno × turno diurno**. Além disso, em 2025 o turno diurno de {len(mud)} cursos mudou de nome:

{md(mud[['curso', 'campus', '2024-1', '2025-1']].rename(columns={'curso': 'Curso', 'campus': 'Campus', '2024-1': 'Turno em 2024-1', '2025-1': 'Turno em 2025-1'}))}

Essas mudanças podem refletir reorganização de horários, e não um curso novo. Uma comparação "Integral × Matutino" do mesmo curso seria, na prática, uma comparação 2024 × 2025.

## Método

Para cada curso, campus e edição: `diferença = nota(Noturno) − nota(turno diurno)`. Resumimos pela mediana, pela média e pela % de pares em que o noturno teve nota menor.

## Resultados

**Tabela 1 – Resumo por turno diurno de referência.**

{md(res['resumo'].rename(columns={'diurno': 'Turno diurno', 'pares': 'Pares (curso × edição)', 'cursos': 'Cursos', 'mediana': 'Diferença mediana', 'media': 'Diferença média', 'pct_menor': '% com Noturno menor'}), decimais=1)}

**Tabela 2 – Diferença por curso (Noturno − diurno).**

{md(pc.rename(columns={'edicoes': 'Edições', 'dif_media': 'Diferença média', 'min': 'Mínima', 'max': 'Máxima', 'pct_menor': '% com Noturno menor'}), index=True, decimais=1)}

![Turnos]({fig})

*Figura 1 – Diferença média entre a nota de corte do Noturno e a do turno diurno, por curso. Fonte: SISU/UFMG; elaboração própria.*

## Interpretação

- O padrão dominante é o noturno com nota de corte menor. Nos quatro cursos com maior diferença ela fica entre {num(-pc['dif_media'].iloc[3])} e {num(-pc['dif_media'].iloc[0])} pontos em média.
- Em cursos como Direito, Farmácia e Biblioteconomia a diferença média é pequena e muda de sinal entre edições.
- A diferença observada é compatível com menor procura pelo noturno entre candidatos de nota alta. A base não tem dados de procura nem de vagas para confirmar.

## Limitações e ressalvas

- {RESSALVA_CORTE}
- {RESSALVA_TEMPO}
- Turnos do mesmo curso podem ter número de vagas e currículo diferentes. A diferença não é só efeito do horário.
- Em 2014 os rótulos "Diurno" e "Tarde" foram convertidos para Matutino e Vespertino na construção da base (post 20).

## Como reproduzir

```bash
python scripts/07_turnos.py
```
""")


def checar(res):
    r, m = res["r"], res["m"]
    x = r[(r["curso_id"] == "direito-bach") & (r["edicao_chave"] == "2026-1")].set_index("turno")["nota_min"]
    y = m[(m["curso_id"] == "direito-bach") & (m["edicao_chave"] == "2026-1")]["dif"].iat[0]
    assert abs(y - (x["Noturno"] - x["Matutino"])) < 1e-9
    assert res["resumo"].set_index("diurno").loc["Todos", "pares"] == res["por_curso"]["edicoes"].sum()


def main():
    res = calcular()
    checar(res)
    post(res, figura(res))


if __name__ == "__main__":
    main()
