"""18 — Áreas do conhecimento: notas de corte médias por área."""
import matplotlib.pyplot as plt

from comum import CORES, RESSALVA_CORTE, RESSALVA_TEMPO, escrever_post, ler, md, num, regular_ac, salvar

ANOS = [2024, 2025, 2026]


def calcular():
    areas = ler("areas_conhecimento.csv")
    r = regular_ac(campus=None).merge(areas[["curso_id", "area"]], on="curso_id", how="left")
    assert r["area"].notna().all(), "curso sem área em data/areas_conhecimento.csv"
    rec = r[r["ano"].isin(ANOS)]
    por_oferta = rec.groupby(["area", "oferta"])["nota_min"].mean().reset_index()
    resumo = por_oferta.groupby("area")["nota_min"].agg(ofertas="size", media="mean", mediana="median",
                                                        minimo="min", maximo="max").sort_values("mediana", ascending=False)
    serie = r.groupby(["edicao_chave", "area"])["nota_min"].median().unstack()[resumo.index]
    mapa = areas.groupby("area")["curso_id"].size().rename("cursos no mapeamento")
    return {"r": r, "areas": areas, "por_oferta": por_oferta, "resumo": resumo.join(mapa), "serie": serie}


def figura(res):
    po, ordem, s = res["por_oferta"], res["resumo"].index.tolist(), res["serie"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13.5, 5.5))
    a1.boxplot([po[po["area"] == a]["nota_min"] for a in ordem], tick_labels=[a.replace(" e ", "\ne ").replace(", ", ",\n") for a in ordem],
               patch_artist=True, boxprops={"facecolor": "#56B4E9"}, medianprops={"color": "#000"})
    a1.set_ylabel("Nota de corte média 2024–2026 por oferta (pontos)")
    a1.set_title("Distribuição por área, 2024–2026")
    a1.tick_params(axis="x", labelsize=7.5, rotation=35)
    for i, a in enumerate(ordem):
        a2.plot(s.index, s[a], marker="o", ms=3, color=CORES[i], label=a)
    a2.set_xlabel("Edição do SISU")
    a2.set_ylabel("Mediana da nota de corte (pontos)")
    a2.set_title("Mediana por área e edição")
    a2.tick_params(axis="x", rotation=60)
    a2.legend(fontsize=7.5)
    fig.suptitle("Notas de corte por área do conhecimento (ampla concorrência, chamada regular, dois campi)")
    return salvar(fig, "18_areas_conhecimento")


def post(res, fig):
    rs = res["resumo"]
    escrever_post("18-areas-do-conhecimento", f"""
# {rs.index[0]} e {rs.index[1]} no topo, {rs.index[-1]} embaixo, mas as áreas se sobrepõem muito

**Resumo.** Em 2024–2026, a área com maior nota de corte mediana (ampla concorrência, chamada regular) foi **{rs.index[0]}** ({num(rs['mediana'].iat[0])} pontos) e a menor foi **{rs.index[-1]}** ({num(rs['mediana'].iat[-1])}). A diferença entre as medianas extremas é de {num(rs['mediana'].iat[0] - rs['mediana'].iat[-1])} pontos, menor que a variação dentro de várias áreas.

## Pergunta

Há diferença de nota de corte entre as áreas do conhecimento?

## Dados usados

- `data/notas_corte.csv`: chamada regular, cota `AC`, dois campi.
- `data/areas_conhecimento.csv`: **tabela de mapeamento criada para este projeto**, que liga cada um dos 88 `curso_id` a uma de seis áreas, com uma coluna de observação para os casos discutíveis.

### Como as áreas foram definidas

O mapeamento parte das grandes áreas do CNPq, com duas simplificações: Exatas e da Terra junto com Engenharias, e Biológicas junto com Agrárias. Os casos de fronteira estão documentados no CSV (coluna `observacao`). Exemplos: Biomedicina foi para Saúde (no CNPq fica em Biológicas); Ciências Atuariais foi para Sociais Aplicadas; Engenharias Florestal, Agrícola e de Alimentos foram para Agrárias, como no CNPq. Quem discordar pode editar o CSV e rodar o script de novo.

**Tabela 1 – Cursos por área no mapeamento.**

{md(res['areas'].groupby('area')['curso_id'].apply(lambda c: ', '.join(c)).reset_index().rename(columns={'area': 'Área', 'curso_id': 'curso_id'}))}

## Método

1. Média da nota de corte de 2024–2026 por oferta (curso × campus × turno).
2. Resumo por área: número de ofertas, média, mediana, mínimo e máximo.
3. Série histórica: mediana das ofertas da área em cada edição.

## Resultados

**Tabela 2 – Nota de corte por área, 2024–2026 (média por oferta).**

{md(rs.rename_axis('Área').rename(columns={'ofertas': 'Ofertas', 'media': 'Média', 'mediana': 'Mediana', 'minimo': 'Mínimo', 'maximo': 'Máximo', 'cursos no mapeamento': 'Cursos no mapeamento (todas as edições)'}), index=True, decimais=1)}

![Áreas]({fig})

*Figura 1 – Esquerda: distribuição das notas de corte por área (2024–2026). Direita: mediana por área ao longo das edições. Fonte: SISU/UFMG; elaboração própria.*

## Interpretação

- As caixas se sobrepõem bastante. Saber a área de um curso diz pouco sobre a nota de corte: há cursos de exatas com nota baixa e cursos de humanas com nota alta.
- Ciências Biológicas e Agrárias aparece embaixo em parte porque inclui os cursos de Montes Claros, que têm notas de corte menores (post 06).
- A ordem das áreas é parecida ao longo das edições (painel direito), o que combina com a estabilidade do ranking (post 16).

## Limitações e ressalvas

- O mapeamento de áreas é uma **decisão do autor**, não uma classificação oficial da UFMG.
- Áreas com poucas ofertas (Letras e Artes) têm resumos instáveis.
- {RESSALVA_CORTE}
- {RESSALVA_TEMPO}

## Como reproduzir

```bash
python scripts/18_areas_conhecimento.py
```
""")


def checar(res):
    areas = ler("areas_conhecimento.csv")
    cursos = ler("de_para_cursos.csv")
    assert set(areas["curso_id"]) == set(cursos["curso_id"]) and areas["curso_id"].is_unique
    assert res["resumo"]["ofertas"].sum() == res["por_oferta"]["oferta"].nunique()


def main():
    res = calcular()
    checar(res)
    post(res, figura(res))


if __name__ == "__main__":
    main()
