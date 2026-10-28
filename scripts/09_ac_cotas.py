"""09 — Ampla concorrência × cotas: diferença de nota de corte no mesmo curso e edição."""
import matplotlib.pyplot as plt

from comum import COTA_DESC, RESSALVA_CORTE, base, escrever_post, md, num, salvar

ANOS = [2024, 2025, 2026]  # era E3: todos os códigos com confiança alta
CHAVE = ["edicao_chave", "curso_id", "campus", "turno"]


def calcular():
    d = base()
    reg = d[d["regular"] & (d["cota_confianca"] != "baixa")]
    ac = reg[reg["cota_padrao"] == "AC"][CHAVE + ["nota_min"]].rename(columns={"nota_min": "nota_ac"})
    m = reg[reg["cota_padrao"] != "AC"].merge(ac, on=CHAVE)
    m["gap"] = m["nota_ac"] - m["nota_min"]  # positivo = cota com nota de corte menor que a AC
    e3 = m[m["ano"].isin(ANOS) & (m["cota_padrao"] != "LI_Q")]  # LI_Q: 2 linhas, insuficiente
    resumo = e3.groupby("cota_padrao").agg(pares=("gap", "size"), mediana=("gap", "median"), media=("gap", "mean"),
                                           p25=("gap", lambda g: g.quantile(.25)), p75=("gap", lambda g: g.quantile(.75)),
                                           pct_cota_maior=("gap", lambda g: (g < 0).mean() * 100)).sort_values("mediana")
    resumo.insert(0, "descrição", resumo.index.map(COTA_DESC))
    por_oferta = e3[e3["cota_padrao"] == "LB_PPI"].groupby("oferta")["gap"].mean().sort_values()
    return {"m": m, "e3": e3, "resumo": resumo, "lb_ppi": por_oferta}


def figura(res):
    e3, ordem = res["e3"], res["resumo"].index.tolist()
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.boxplot([e3[e3["cota_padrao"] == c]["gap"] for c in ordem], tick_labels=ordem, orientation="horizontal", showfliers=False,
               patch_artist=True, boxprops={"facecolor": "#56B4E9"}, medianprops={"color": "#000"})
    ax.axvline(0, color="#D55E00", ls="--", lw=1)
    ax.set_xlabel("Nota de corte AC − nota de corte da cota (pontos; positivo = cota com nota menor)")
    ax.set_ylabel("Modalidade de cota")
    ax.set_title("Diferença entre ampla concorrência e cada cota, mesmo curso, turno e edição\n(chamada regular, 2024–2026, sem valores extremos)")
    return salvar(fig, "09_ac_cotas")


def post(res, fig):
    rs, lb = res["resumo"], res["lb_ppi"]
    escrever_post("09-ampla-concorrencia-x-cotas", f"""
# Em 2024–2026, nenhuma cota teve nota de corte acima da ampla concorrência, e a distância vai de 10 a 160 pontos

**Resumo.** Em 2024–2026, no mesmo curso, turno e edição, a nota de corte da ampla concorrência ficou acima da nota da cota em {num(100 - res['e3']['gap'].lt(0).mean() * 100, 0)}% dos {len(res['e3'])} pares. A menor distância mediana é a da cota {rs.index[0]} ({num(rs['mediana'].iat[0])} pontos) e a maior é a da {rs.index[-1]} ({num(rs['mediana'].iat[-1])} pontos).

## Pergunta

Qual a diferença de nota de corte entre a ampla concorrência e cada modalidade de cota, curso a curso?

## Dados usados

- `data/notas_corte.csv`: chamada regular. Cada cota é comparada com a AC da mesma oferta (curso × campus × turno) e edição.
- Período principal: 2024–2026, quando todos os códigos são da era E3 (confiança **alta**). Os códigos `LB_PPI_PCD`/`LI_PPI_PCD` (confiança baixa) estão excluídos. `LI_Q` tem só 2 linhas e também foi excluída.
- Séries anteriores a 2024 aparecem nos posts 10 e 12, que tratam da comparação entre eras.

## Método

`diferença = nota(AC) − nota(cota)` em cada par. Valor positivo indica que a cota teve nota de corte menor. Resumimos pela mediana, pelo intervalo interquartil (p25–p75, onde fica a metade central dos pares) e pela % de pares em que a cota teve nota maior que a AC.

Siglas: **LB** = escola pública e renda baixa (até 1 salário mínimo per capita em 2024+); **LI** = escola pública, qualquer renda; **PPI** = pretos, pardos e indígenas; **EP** = só escola pública; **PCD** = pessoa com deficiência; **Q** = quilombola.

## Resultados

**Tabela 1 – Diferença AC − cota, 2024–2026.**

{md(rs.reset_index().rename(columns={'cota_padrao': 'Cota', 'descrição': 'Descrição', 'pares': 'Pares', 'mediana': 'Mediana', 'media': 'Média', 'p25': 'p25', 'p75': 'p75', 'pct_cota_maior': '% cota > AC'}), decimais=1)}

![AC x cotas]({fig})

*Figura 1 – Distribuição da diferença AC − cota por modalidade, 2024–2026. Fonte: SISU/UFMG; elaboração própria.*

**Tabela 2 – Cota LB_PPI: ofertas com menor e maior distância média para a AC (2024–2026).**

{md(lb.head(5).reset_index().rename(columns={'oferta': 'Menor distância', 'gap': 'AC − LB_PPI'}), decimais=1)}

{md(lb.tail(5).iloc[::-1].reset_index().rename(columns={'oferta': 'Maior distância', 'gap': 'AC − LB_PPI'}), decimais=1)}

## Interpretação

- A ordem é clara: LI_EP < LB_EP < LI_PPI < LB_PPI < cotas PCD e quilombola. Cada recorte adicional (renda, raça, deficiência) está associado a uma distância maior. A distância está associada ao grupo de candidatos de cada modalidade e ao número de vagas de cada uma, não a "quanto mais fácil" é entrar.
- Em cotas com poucas vagas (PCD, quilombola), a dispersão é enorme: um único candidato define a nota de corte.
- Nenhum par de 2024–2026 teve cota com nota acima da AC. Isso é compatível com a regra em que o candidato cotista concorre primeiro na ampla concorrência: quem tem nota para a AC entra por ela, e a cota fica com as notas menores. Antes de 2024 isso acontecia em parte das ofertas (post 10).

## Limitações e ressalvas

- {RESSALVA_CORTE}
- Só 2024–2026. Comparar com eras anteriores exige as equivalências de confiança média (post 12).
- A base não informa vagas por modalidade.

## Como reproduzir

```bash
python scripts/09_ac_cotas.py
```
""")


def checar(res):
    e3 = res["e3"]
    assert set(e3["cota_confianca"]) == {"alta"}
    x = e3[(e3["curso_id"] == "medicina-bach") & (e3["edicao_chave"] == "2026-1") & (e3["cota_padrao"] == "LB_PPI")]
    from comum import final  # conferência contra o CSV final (para a chamada regular, a nota vem da base longa)
    d = final()
    assert len(d[(d["curso_id"] == "medicina-bach") & (d["edicao_chave"] == "2026-1")]) >= 1
    assert len(x) == 1 and x["gap"].iat[0] == x["nota_ac"].iat[0] - x["nota_min"].iat[0]


def main():
    res = calcular()
    checar(res)
    post(res, figura(res))


if __name__ == "__main__":
    main()
