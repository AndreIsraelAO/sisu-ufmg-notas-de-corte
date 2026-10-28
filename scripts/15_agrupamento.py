"""15 — Agrupamento (k-means) das ofertas por perfil de nota, 2024–2026."""
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

from comum import CORES, SEED, base, escrever_post, final, md, num, salvar

ANOS = [2024, 2025, 2026]
CHAVE = ["edicao_chave", "curso_id", "campus", "turno"]
VARS = {"nota_ac": "Nota de corte AC", "amplitude": "Amplitude AC (máx − mín)",
        "gap_lb_ppi": "Distância AC − LB_PPI", "queda": "Queda AC na lista de espera"}
KS = range(2, 9)


def calcular():
    d, f = base(), final()
    reg = d[d["regular"] & d["ano"].isin(ANOS)]
    ac = reg[reg["cota_padrao"] == "AC"].copy()
    ac["amplitude"] = ac["nota_max"] - ac["nota_min"]
    lb = reg[reg["cota_padrao"] == "LB_PPI"][CHAVE + ["nota_min"]].rename(columns={"nota_min": "nota_lb"})
    fa = f[(f["cota_padrao"] == "AC") & f["ano"].isin(ANOS)][CHAVE + ["nota_min"]].rename(columns={"nota_min": "nota_fin"})
    x = ac.merge(lb, on=CHAVE).merge(fa, on=CHAVE)
    x["gap_lb_ppi"] = x["nota_min"] - x["nota_lb"]
    x["queda"] = x["nota_min"] - x["nota_fin"]
    x["nota_ac"] = x["nota_min"]
    feat = x.groupby("oferta").agg(edicoes=("ano", "nunique"), **{v: (v, "mean") for v in VARS})
    feat = feat[feat["edicoes"] == len(ANOS)].drop(columns="edicoes")
    z = StandardScaler().fit_transform(feat)
    aval = []
    for k in KS:
        km = KMeans(n_clusters=k, n_init=50, random_state=SEED).fit(z)
        aval.append({"k": k, "silhueta": silhouette_score(z, km.labels_), "inércia": km.inertia_})
    aval = pd.DataFrame(aval)
    k = int(aval.loc[aval["silhueta"].idxmax(), "k"])
    km = KMeans(n_clusters=k, n_init=50, random_state=SEED).fit(z)
    feat["grupo"] = km.labels_
    # Renumera os grupos pela nota de corte média (Grupo 1 = maior nota), para a saída não depender da ordem do k-means.
    ordem = feat.groupby("grupo")["nota_ac"].mean().sort_values(ascending=False).index
    feat["grupo"] = feat["grupo"].map({g: i + 1 for i, g in enumerate(ordem)})
    perfil = feat.groupby("grupo").agg(ofertas=("nota_ac", "size"), **{v: (v, "mean") for v in VARS})
    return {"feat": feat, "aval": aval, "k": k, "perfil": perfil}


def figura(res):
    a, feat = res["aval"], res["feat"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.5, 5.2))
    a1.plot(a["k"], a["silhueta"], marker="o", color="#0072B2", label="Silhueta (maior = melhor)")
    a1.set_xlabel("Número de grupos (k)")
    a1.set_ylabel("Coeficiente de silhueta", color="#0072B2")
    a1b = a1.twinx()
    a1b.plot(a["k"], a["inércia"], marker="s", ls="--", color="#D55E00", label="Inércia")
    a1b.set_ylabel("Inércia (soma das distâncias² ao centro)", color="#D55E00")
    a1b.grid(False)
    a1.axvline(res["k"], color="#444", ls=":")
    a1.set_title(f"Escolha de k: silhueta máxima em k = {res['k']}")
    for g, sub in feat.groupby("grupo"):
        a2.scatter(sub["nota_ac"], sub["gap_lb_ppi"], s=22, color=CORES[g - 1], label=f"Grupo {g}")
    a2.set_xlabel("Nota de corte AC, média 2024–2026 (pontos)")
    a2.set_ylabel("Distância AC − LB_PPI (pontos)")
    a2.set_title("Ofertas por grupo (2 das 4 variáveis)")
    a2.legend()
    return salvar(fig, "15_agrupamento")


def post(res, fig):
    feat, perfil, a, k = res["feat"], res["perfil"], res["aval"], res["k"]
    membros = "\n".join(f"- **Grupo {g}** ({len(s)}): {', '.join(sorted(s.index))}" for g, s in feat.groupby("grupo"))
    escrever_post("15-agrupamento-de-cursos", f"""
# Agrupando as ofertas pelo perfil de nota: {k} grupos

**Resumo.** Usando quatro medidas de 2024–2026 (nota de corte da AC, amplitude, distância para a cota LB_PPI e queda na lista de espera), o k-means separou {len(feat)} ofertas em {k} grupos. O número de grupos foi escolhido pelo maior coeficiente de silhueta ({num(a['silhueta'].max(), 3)}). O grupo 1 reúne as {perfil.loc[1, 'ofertas']} ofertas com nota de corte média de {num(perfil.loc[1, 'nota_ac'])} pontos.

## Pergunta

As ofertas da UFMG formam grupos com perfis de nota parecidos?

## Dados usados

- `data/notas_corte.csv` (chamada regular) e `data/notas_corte_final.csv` (última chamada), edições 2024-1 a 2026-1 (era de cotas E3, confiança alta), dois campi.
- Só ofertas com as quatro medidas nas três edições ({len(feat)} ofertas).

## Método

1. Para cada oferta, média de 2024–2026 de: {'; '.join(VARS.values())}.
2. **Padronização** (z-score: subtrai a média e divide pelo desvio-padrão), para que nenhuma variável domine por ter escala maior.
3. **k-means** com k de 2 a 8 (`random_state={SEED}`, 50 inicializações). O k-means junta ofertas cujas medidas estão próximas umas das outras.
4. **Escolha de k pela silhueta.** Para cada oferta, a silhueta compara a distância média ao próprio grupo (a) com a distância média ao grupo vizinho mais próximo (b): `s = (b − a) / max(a, b)`. Vai de −1 a 1; quanto maior a média, mais bem separados os grupos. A inércia ("cotovelo") aparece como apoio.

## Resultados

**Tabela 1 – Avaliação de k.**

{md(a, decimais=3)}

**Tabela 2 – Perfil médio de cada grupo (pontos).**

{md(perfil.rename(columns={'ofertas': 'Ofertas', **VARS}).rename_axis('Grupo'), index=True, decimais=1)}

![Agrupamento]({fig})

*Figura 1 – Esquerda: silhueta e inércia para cada k. Direita: ofertas coloridas por grupo, em duas das quatro variáveis. Fonte: SISU/UFMG; elaboração própria.*

**Membros de cada grupo:**

{membros}

## Interpretação

- **Grupo 1:** nota de corte alta, amplitude estreita e distância moderada para a LB_PPI ({num(perfil.loc[1, 'gap_lb_ppi'])} pontos). Reúne Medicina, Direito, cursos de saúde, comunicação e algumas engenharias noturnas.
- **Grupo 2:** nota um pouco menor que o grupo 1, mas com a **maior distância para a LB_PPI** ({num(perfil.loc[2, 'gap_lb_ppi'])} pontos). É formado quase só por engenharias diurnas e cursos de exatas (Estatística, Matemática, Física, Química, Economia). Ou seja, o agrupamento não é só uma ordenação por nota: a distância AC − cota separa exatas de saúde e humanas com nota parecida.
- **Grupo 3:** notas de corte menores, com cursos de humanidades, licenciaturas e cursos de nicho de BH.
- **Grupo 4:** as {perfil.loc[4, 'ofertas']} ofertas de **Montes Claros**, marcadas sobretudo pela queda muito grande na lista de espera ({num(perfil.loc[4, 'queda'])} pontos em média, contra {num(perfil.loc[1:3, 'queda'].min())}–{num(perfil.loc[1:3, 'queda'].max())} nos outros grupos).
- Uma silhueta média de {num(a['silhueta'].max(), 2)} indica uma estrutura de grupos {'razoável' if a['silhueta'].max() >= 0.35 else 'fraca'}. As fronteiras são graduais, não há "tipos" de curso bem separados.
- Os grupos descrevem perfis de nota. Não dizem nada sobre qualidade ou área do curso (post 18).

## Limitações e ressalvas

- O resultado depende das variáveis escolhidas e da padronização. Outras medidas dariam outros grupos.
- Só três edições, com ENEM e vagas diferentes em cada uma.
- O k-means supõe grupos aproximadamente "redondos" e de tamanho parecido.

## Como reproduzir

```bash
python scripts/15_agrupamento.py
```
""")


def checar(res):
    feat = res["feat"]
    assert feat["grupo"].nunique() == res["k"]
    assert res["perfil"]["ofertas"].sum() == len(feat)
    assert res["perfil"]["nota_ac"].is_monotonic_decreasing
    # O texto do post descreve estes padrões; se mudarem, o texto precisa ser revisto.
    assert res["k"] == 4
    assert all(", MOC" in o for o in feat[feat["grupo"] == 4].index)
    assert res["perfil"]["gap_lb_ppi"].idxmax() == 2 and res["perfil"]["queda"].idxmax() == 4


def main():
    res = calcular()
    checar(res)
    post(res, figura(res))


if __name__ == "__main__":
    main()
