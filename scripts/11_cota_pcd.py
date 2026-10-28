"""11 — Cota PCD: onde aparece, em quais cursos e com que nota de corte."""
import matplotlib.pyplot as plt

from comum import base, escrever_post, md, num, salvar

PCD = ["LB_PCD", "LI_PCD", "LB_PPI_PCD", "LI_PPI_PCD"]
CHAVE = ["edicao_chave", "curso_id", "campus", "turno"]


def calcular():
    d = base()
    reg = d[d["regular"]]
    ofertas = reg.groupby("edicao_chave")["oferta"].nunique()
    pcd = reg[reg["cota_padrao"].isin(PCD)]
    cob = pcd.groupby(["edicao_chave", "cota_padrao"])["oferta"].nunique().unstack()
    cob = (cob.div(ofertas, axis=0) * 100).reindex(ofertas.index)
    ac = reg[reg["cota_padrao"] == "AC"][CHAVE + ["nota_min"]].rename(columns={"nota_min": "nota_ac"})
    m = pcd.merge(ac, on=CHAVE)
    m["gap"] = m["nota_ac"] - m["nota_min"]
    m["vaga_unica"] = m["nota_min"] == m["nota_max"]  # um só classificado (ou empate): mín = máx
    e3 = m[m["ano"] >= 2024]
    resumo = e3.groupby("cota_padrao").agg(linhas=("gap", "size"), ofertas=("oferta", "nunique"),
                                           nota_mediana=("nota_min", "median"), nota_min=("nota_min", "min"),
                                           nota_max=("nota_min", "max"), gap_mediano=("gap", "median"),
                                           pct_min_igual_max=("vaga_unica", lambda v: v.mean() * 100)).reset_index()
    # Ofertas sem nenhuma linha PCD em 2026 (regular).
    of26 = set(reg[reg["edicao_chave"] == "2026-1"]["oferta"])
    com26 = set(pcd[pcd["edicao_chave"] == "2026-1"]["oferta"])
    extremos = m.nsmallest(5, "nota_min")[["edicao_chave", "oferta", "cota_padrao", "nota_min", "nota_max", "nota_ac"]]
    return {"d": d, "m": m, "cob": cob, "resumo": resumo, "sem26": sorted(of26 - com26), "extremos": extremos, "e3": e3}


def figura(res):
    cob, e3 = res["cob"], res["e3"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.5, 5))
    for i, c in enumerate(PCD):
        a1.plot(cob.index, cob[c], marker="o", label=c, color=["#0072B2", "#E69F00", "#009E73", "#CC79A7"][i])
    a1.set_ylim(0, 105)
    a1.set_ylabel("% das ofertas com linha da cota (chamada regular)")
    a1.set_xlabel("Edição do SISU")
    a1.set_title("Presença das cotas PCD por edição")
    a1.tick_params(axis="x", rotation=60)
    a1.legend(title="Cota")
    grupos = ["LB_PCD", "LI_PCD"]
    a2.boxplot([e3["nota_ac"].drop_duplicates()] + [e3[e3["cota_padrao"] == c]["nota_min"] for c in grupos],
               tick_labels=["AC (mesmas ofertas)"] + grupos, patch_artist=True, boxprops={"facecolor": "#56B4E9"},
               medianprops={"color": "#000"})
    a2.set_ylabel("Nota de corte (pontos)")
    a2.set_title("Notas de corte 2024–2026, chamada regular")
    return salvar(fig, "11_cota_pcd")


def post(res, fig):
    rs, cob = res["resumo"].set_index("cota_padrao"), res["cob"]
    escrever_post("11-cota-pcd", f"""
# A cota PCD existe desde 2018 e tem as notas de corte mais dispersas da base

**Resumo.** As cotas para pessoas com deficiência (PCD) aparecem a partir de 2018. Em 2026-1 havia linha de LB_PCD em {num(cob.loc['2026-1', 'LB_PCD'], 0)}% e de LI_PCD em {num(cob.loc['2026-1', 'LI_PCD'], 0)}% das ofertas. Em 2024–2026, a nota de corte mediana da LI_PCD ficou {num(rs.loc['LI_PCD', 'gap_mediano'])} pontos abaixo da ampla concorrência do mesmo curso. Em {num(rs.loc['LB_PCD', 'pct_min_igual_max'], 0)}% das linhas LB_PCD a nota mínima é igual à máxima, sinal de um único aprovado no grupo.

## Pergunta

Onde aparece a cota PCD, em quais cursos e com que nota de corte?

## Dados usados

- `data/notas_corte.csv`: chamada regular, dois campi.
- Cotas PCD: `LB_PCD` e `LI_PCD` (2018–2023 com confiança média; 2024+ alta) e os códigos legados `LB_PPI_PCD` e `LI_PPI_PCD` (2018–2023, PPI + PCD, confiança **baixa**). Os legados aparecem só na contagem de presença e **não** são comparados com 2024+.
- Comparação de notas restrita a 2024–2026 (era E3).

## Método

- **Presença:** % das ofertas (curso × campus × turno) da edição que têm uma linha da cota na chamada regular. Ausência de linha significa que o PDF não listou classificado naquela cota. Pode ser vaga não ofertada ou sem candidato aprovado; a base não diferencia.
- **Nota:** mediana, mínimo e máximo da nota de corte e a diferença para a AC da mesma oferta (`AC − PCD`).
- **Indício de vaga única:** `nota_min == nota_max`, ou seja, um só aprovado (ou empate).

## Resultados

**Tabela 1 – Presença das cotas PCD (% das ofertas da edição).**

{md(cob.rename_axis('Edição'), index=True, decimais=1)}

**Tabela 2 – Notas de corte das cotas PCD, 2024–2026.**

{md(res['resumo'].rename(columns={'cota_padrao': 'Cota', 'linhas': 'Linhas', 'ofertas': 'Ofertas', 'nota_mediana': 'Nota mediana', 'nota_min': 'Menor nota', 'nota_max': 'Maior nota', 'gap_mediano': 'AC − PCD (mediana)', 'pct_min_igual_max': '% mín = máx'}), decimais=1)}

![Cota PCD]({fig})

*Figura 1 – Esquerda: presença das cotas PCD por edição. Direita: distribuição das notas de corte PCD e da AC nas mesmas ofertas, 2024–2026. Fonte: SISU/UFMG; elaboração própria.*

**Tabela 3 – As 5 menores notas de corte PCD da série (2018–2026).**

{md(res['extremos'].rename(columns={'edicao_chave': 'Edição', 'oferta': 'Oferta', 'cota_padrao': 'Cota', 'nota_min': 'Nota de corte', 'nota_max': 'Nota máxima', 'nota_ac': 'Nota AC'}))}

Ofertas da chamada regular de 2026-1 **sem** nenhuma linha PCD: {', '.join(res['sem26']) if res['sem26'] else 'nenhuma'}.

## Interpretação

- A presença da cota PCD caiu entre 2018 e 2023 e voltou a subir a partir de 2024, quando o sistema de códigos mudou. A base não permite dizer se isso reflete mais vagas ofertadas ou mais aprovados.
- As notas PCD são muito dispersas. Com uma ou duas vagas por grupo, um único candidato define a nota de corte, o que gera valores extremos (Tabela 3). A média da cota PCD de um curso não deve ser usada como referência de "nota necessária".

## Limitações e ressalvas

- A equivalência 2018–2023 → 2024+ é de confiança média (`LB_PCD`, `LI_PCD`) ou baixa (códigos PPI+PCD). Em 2018–2023 havia duas cotas PCD por faixa de renda (com e sem PPI), e em 2024+ só uma.
- Em 2024 a LB_PCD e a LI_PCD aparecem só em parte dos cursos (veja o relatório da base).
- As notas do ENEM e as vagas mudam a cada ano.

## Como reproduzir

```bash
python scripts/11_cota_pcd.py
```
""")


def checar(res):
    d = res["d"]
    x = d[d["regular"] & (d["edicao_chave"] == "2026-1") & (d["cota_padrao"] == "LI_PCD")]["oferta"].nunique()
    tot = d[d["regular"] & (d["edicao_chave"] == "2026-1")]["oferta"].nunique()
    assert abs(res["cob"].loc["2026-1", "LI_PCD"] - x / tot * 100) < 1e-9
    assert res["cob"].loc[["2014-1", "2017-1"]].isna().all().all(), "PCD não deveria existir antes de 2018"


def main():
    res = calcular()
    checar(res)
    post(res, figura(res))


if __name__ == "__main__":
    main()
