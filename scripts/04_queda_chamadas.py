"""04 — Quanto a nota de corte cai entre a chamada regular e a última chamada (2022–2026)?"""
import matplotlib.pyplot as plt
import pandas as pd

from comum import base, escrever_post, final, md, num, salvar

EDICOES = ["2022-1", "2023-1", "2024-1", "2025-1", "2026-1"]
CHAVE = ["edicao_chave", "curso_id", "campus", "turno", "cota_padrao"]


def calcular():
    d, f = base(), final()
    reg = d[d["regular"] & d["edicao_chave"].isin(EDICOES)]
    m = reg.merge(f, on=CHAVE, suffixes=("_reg", "_fin"))
    m["queda"] = m["nota_min_reg"] - m["nota_min_fin"]
    m["grupo"] = m["cota_padrao"].eq("AC").map({True: "Ampla concorrência", False: "Cotas"})
    tab = m.groupby("edicao_chave").agg(
        chaves=("queda", "size"),
        ultima_chamada=("chamada_fin", "max"),
        mediana_AC=("queda", lambda q: q[m.loc[q.index, "grupo"] == "Ampla concorrência"].median()),
        mediana_cotas=("queda", lambda q: q[m.loc[q.index, "grupo"] == "Cotas"].median()),
        media_geral=("queda", "mean"),
        pct_sem_queda=("queda", lambda q: (q == 0).mean() * 100),
    ).reset_index()
    # Curva: queda acumulada mediana (AC) em cada chamada presente.
    ac = d[d["edicao_chave"].isin(EDICOES) & (d["cota_padrao"] == "AC")]
    r0 = ac[ac["regular"]][CHAVE + ["nota_min"]].rename(columns={"nota_min": "n0"})
    ac = ac.merge(r0, on=CHAVE)
    ac["queda"] = ac["n0"] - ac["nota_min"]
    curva = ac.groupby(["edicao_chave", "chamada"])["queda"].median().reset_index()
    por_cota = m[m["edicao_chave"].isin(["2024-1", "2025-1", "2026-1"])].groupby("cota_padrao")["queda"].agg(
        ["size", "median", "mean"]).sort_values("median", ascending=False).reset_index()
    return {"m": m, "tab": tab, "curva": curva, "por_cota": por_cota}


def figura(res):
    m, curva = res["m"], res["curva"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 5))
    for i, ed in enumerate(EDICOES):
        c = curva[curva["edicao_chave"] == ed]
        a1.plot(c["chamada"], c["queda"], marker="o", ms=3.5, label=ed + (" (lacunas)" if ed in ("2022-1", "2023-1") else ""))
    a1.set_xlabel("Chamada (0 = regular)")
    a1.set_ylabel("Queda mediana acumulada da nota de corte (pontos)")
    a1.set_title("Ampla concorrência: queda acumulada por chamada")
    a1.legend(title="Edição")
    dados = [m[(m["edicao_chave"] == e) & (m["grupo"] == g)]["queda"] for e in EDICOES for g in ("Ampla concorrência", "Cotas")]
    pos = [i * 3 + j for i in range(len(EDICOES)) for j in (0, 1)]
    bp = a2.boxplot(dados, positions=pos, widths=0.8, patch_artist=True, showfliers=False)
    for k, box in enumerate(bp["boxes"]):
        box.set_facecolor(["#0072B2", "#E69F00"][k % 2])
    a2.set_xticks([i * 3 + 0.5 for i in range(len(EDICOES))], EDICOES)
    a2.set_xlabel("Edição")
    a2.set_ylabel("Queda: regular − última chamada (pontos)")
    a2.set_title("Distribuição da queda total (sem valores extremos)")
    a2.legend([bp["boxes"][0], bp["boxes"][1]], ["Ampla concorrência", "Cotas"])
    return salvar(fig, "04_queda_chamadas")


def post(res, fig):
    t, pc = res["tab"], res["por_cota"]
    t2 = t.rename(columns={"edicao_chave": "Edição", "chaves": "Chaves", "ultima_chamada": "Última chamada na base",
                           "mediana_AC": "Queda mediana AC", "mediana_cotas": "Queda mediana cotas",
                           "media_geral": "Queda média (todas)", "pct_sem_queda": "% sem queda"})
    g = t.set_index("edicao_chave")
    escrever_post("04-queda-entre-chamadas", f"""
# A lista de espera derruba a nota de corte, sobretudo nas cotas para pessoas pretas, pardas e indígenas

**Resumo.** Entre a chamada regular e a última chamada presente na base, a nota de corte mediana da ampla concorrência caiu de {num(t['mediana_AC'].min())} a {num(t['mediana_AC'].max())} pontos, dependendo da edição (2022–2026). Em 2024–2026, as cotas PPI de renda baixa (LB_PPI) tiveram a maior queda mediana ({num(pc.set_index('cota_padrao').loc['LB_PPI', 'median'])} pontos). Já as cotas PCD e quilombola quase não se mexem na mediana.

## Pergunta

Quanto a nota de corte cai entre a chamada regular (chamada 0) e a última chamada da lista de espera? Isso mudou entre 2022 e 2026?

## Dados usados

- `data/notas_corte.csv`, chamada regular de 2022-1 a 2026-1.
- `data/notas_corte_final.csv` (`is_final == True`): a última chamada **presente na base** para cada chave.
- Chave = edição × curso × campus × turno × cota. As duas tabelas casam 1 para 1 (nenhuma chave perdida).
- Antes de 2022 a base só tem a chamada regular, por isso o período começa em 2022.

## Método

Para cada chave, `queda = nota_min(chamada regular) − nota_min(última chamada)`. Como `nota_min` é acumulada, a queda nunca é negativa (validado no post 20). Resumimos pela mediana, que é menos sensível a grupos com uma só vaga do que a média. O painel da esquerda da figura mostra a queda mediana acumulada da AC em cada chamada intermediária.

## Resultados

**Tabela 1 – Queda da nota de corte por edição.**

{md(t2, decimais=1)}

![Queda entre chamadas]({fig})

*Figura 1 – Esquerda: queda mediana acumulada (AC) a cada chamada; em 2022 e 2023 faltam chamadas na base, então as linhas ligam só as chamadas existentes. Direita: distribuição da queda total por edição, AC × cotas. Fonte: SISU/UFMG; elaboração própria.*

**Tabela 2 – Queda por modalidade de cota, 2024–2026 (mesmo sistema de códigos).**

{md(pc.rename(columns={'cota_padrao': 'Cota', 'size': 'Chaves', 'median': 'Mediana', 'mean': 'Média'}), decimais=1)}

## Interpretação

- A maior parte da queda acontece nas primeiras chamadas da lista de espera. Depois a curva achata.
- Agregando todas as cotas, a queda mediana fica perto da AC (Tabela 1). Separando por modalidade (Tabela 2), aparecem dois padrões: as cotas PPI e LB_EP caem **mais** que a AC, e as cotas PCD e quilombola têm mediana zero. Nestas há poucas vagas e muitas vezes nenhuma troca do último classificado ao longo das chamadas.
- Em {num(t['pct_sem_queda'].min())}% a {num(t['pct_sem_queda'].max())}% das chaves a nota não caiu nada entre a regular e a última chamada.
- Para quem consulta a nota de corte: a nota da chamada regular é bem mais alta que a nota com que a última pessoa entrou. Comparar a sua nota só com a chamada regular superestima a nota necessária.

## Limitações e ressalvas

- **2022 e 2023 têm lacunas de chamada** (2022 só tem as chamadas 0, 4, 5, 10 e 12; 2023 não tem as chamadas 2, 4 e 6). A "última chamada" é a última presente nos dados, não necessariamente a última que existiu.
- O número de chamadas difere entre edições (última chamada: {', '.join(f"{e}: {c}" for e, c in zip(t['edicao_chave'], t['ultima_chamada']))}). Mais chamadas tendem a produzir quedas maiores, então as edições não são comparáveis em pé de igualdade.
- Até 2023 os códigos de cota eram outros (era E2). A Tabela 2 usa só 2024–2026 para não misturar eras.
- As notas do ENEM e as vagas mudam a cada ano.

## Como reproduzir

```bash
python scripts/04_queda_chamadas.py
```
""")


def checar(res):
    m = res["m"]
    f = final()
    assert len(m) == len(f[f["edicao_chave"].isin(EDICOES)]), "chaves regular × final não casam 1:1"
    assert (m["queda"] >= 0).all()
    x = m[(m["edicao_chave"] == "2026-1") & (m["curso_id"] == "medicina-bach") & (m["cota_padrao"] == "AC")]
    y = f[(f["edicao_chave"] == "2026-1") & (f["curso_id"] == "medicina-bach") & (f["cota_padrao"] == "AC")]
    assert abs(x["nota_min_fin"].iat[0] - y["nota_min"].iat[0]) < 1e-9


def main():
    res = calcular()
    checar(res)
    post(res, figura(res))


if __name__ == "__main__":
    main()
