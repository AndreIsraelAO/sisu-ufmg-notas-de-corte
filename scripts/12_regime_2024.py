"""12 — A mudança de códigos de cota em 2024: o que muda, o que é comparável e o que não é."""
import matplotlib.pyplot as plt

from comum import base, escrever_post, ler, md, num, salvar

CHAVE = ["edicao_chave", "curso_id", "campus", "turno"]
COMPARAVEIS = ["LI_EP", "LB_EP", "LI_PPI", "LB_PPI"]


def calcular():
    d = base()
    depara = ler("de_para_cotas.csv")[["era", "cota_raw", "cota_padrao", "confianca"]]
    reg = d[d["regular"]]
    presenca = reg.pivot_table(index="cota_padrao", columns="era_cota", values="oferta", aggfunc="nunique").fillna(0).astype(int)
    ac = reg[reg["cota_padrao"] == "AC"][CHAVE + ["nota_min"]].rename(columns={"nota_min": "nota_ac"})
    m = reg[reg["cota_padrao"].isin(COMPARAVEIS) & (reg["ano"] >= 2018)].merge(ac, on=CHAVE)
    m["gap"] = m["nota_ac"] - m["nota_min"]
    serie = m.groupby(["ano", "cota_padrao"])["gap"].median().unstack()
    # Salto 2023 → 2024 na distância mediana, comparado com a variação média anual típica de 2018–2023.
    salto = (serie.loc[2024] - serie.loc[2023]).rename("salto 2023→2024")
    tipico = serie.loc[2018:2023].diff().abs().mean().rename("variação anual típica 2018–2023")
    comp = salto.to_frame().join(tipico)
    comp["renda"] = ["baixa (limite mudou)" if c.startswith("LB") else "qualquer (sem mudança)" for c in comp.index]
    return {"d": d, "depara": depara, "presenca": presenca, "serie": serie, "comp": comp}


def figura(res):
    s = res["serie"]
    fig, ax = plt.subplots(figsize=(10, 5.5))
    for i, c in enumerate(COMPARAVEIS):
        ax.plot(s.index, s[c], marker="o", ls="-" if c.startswith("LI") else "--",
                color=["#0072B2", "#E69F00", "#009E73", "#D55E00"][i], label=c)
    ax.axvspan(2023.5, 2026.5, color="#999", alpha=0.12, label="era E3 (códigos LB/LI)")
    ax.set_xlabel("Ano (edição única)")
    ax.set_ylabel("Mediana de AC − cota (pontos)")
    ax.set_title("Distância mediana entre ampla concorrência e cotas, 2018–2026\n(linha contínua = qualquer renda; tracejada = renda baixa)")
    ax.legend()
    return salvar(fig, "12_regime_2024")


def post(res, fig):
    c = res["comp"]
    acima = [k for k, v in c.iterrows() if v["salto 2023→2024"] > v["variação anual típica 2018–2023"]]
    abaixo = [k for k in c.index if k not in acima]
    escrever_post("12-mudanca-de-regime-2024", f"""
# 2024 trocou os códigos de cota: algumas séries continuam, outras quebram

**Resumo.** Em 2024 a UFMG passou a usar os códigos LB/LI, que substituíram 1.1–4.2 (2018–2023) e 1–4 (2014–2017). Quatro cotas têm equivalência direta e podem ser seguidas no tempo: LB_PPI, LB_EP, LI_PPI e LI_EP. As cotas PCD perderam o recorte PPI, e as quilombolas só entram na base em 2025. Na passagem 2023→2024, a distância para a AC variou {num(c.loc['LB_PPI', 'salto 2023→2024'])} pontos na LB_PPI e {num(c.loc['LI_EP', 'salto 2023→2024'])} na LI_EP. As cotas de renda baixa saltaram acima do normal; as de qualquer renda, não.

## Pergunta

O que muda com os códigos de cota de 2024, o que continua comparável com os anos anteriores e o que não continua?

## Dados usados

- `data/de_para_cotas.csv`: tabela de equivalência com a confiança de cada correspondência.
- `data/notas_corte.csv`: chamada regular, 2018–2026, cotas comparáveis (`LB_PPI`, `LB_EP`, `LI_PPI`, `LI_EP`) contra a AC da mesma oferta.

## Método

1. Tabela de equivalência e presença de cada código por era.
2. Para as quatro cotas comparáveis, a distância mediana `AC − cota` por ano. O "salto" 2023→2024 é comparado com a variação anual típica de 2018–2023 (média do valor absoluto das variações ano a ano). Um salto bem maior que o típico sugere efeito da troca de regra. Isso é uma comparação descritiva, não um teste causal.

## Resultados

**Tabela 1 – Equivalência de códigos (de `de_para_cotas.csv`).**

{md(res['depara'].rename(columns={'era': 'Era', 'cota_raw': 'Código original', 'cota_padrao': 'Código padronizado', 'confianca': 'Confiança'}))}

**Tabela 2 – Ofertas com cada código (chamada regular, soma das edições da era).**

{md(res['presenca'].rename_axis('Código'), index=True)}

**Tabela 3 – Salto da distância mediana AC − cota entre 2023 e 2024.**

{md(c.reset_index().rename(columns={'cota_padrao': 'Cota', 'renda': 'Renda'}), decimais=1)}

![Regime 2024]({fig})

*Figura 1 – Distância mediana entre AC e as quatro cotas comparáveis, 2018–2026. Fonte: SISU/UFMG; elaboração própria.*

## Interpretação: o que é comparável

| Item | Comparável entre eras? | Por quê |
|---|---|---|
| AC | Sim | Mesmo código e conceito |
| LI_EP, LI_PPI | Sim (confiança média) | Mesmo recorte; não depende de renda |
| LB_EP, LB_PPI | Com ressalva (média) | Limite de renda caiu de 1,5 para 1 salário mínimo per capita em 2024 |
| LB_PCD, LI_PCD | Com ressalva (média), só desde 2018 | Em 2018–2023 havia versões PCD com e sem PPI |
| LB_PPI_PCD, LI_PPI_PCD | **Não** (baixa) | Deixam de existir em 2024; não há código equivalente |
| LB_Q, LI_Q | **Não** antes de 2025 | Em 2024 a lista quilombola está só no PDF; LI_Q tem 2 linhas |

- Se a troca de regra tivesse efeito, a expectativa seria um salto maior nas cotas "LB", cujo limite de renda mudou, do que nas "LI". É o que se observa: {', '.join(acima) if acima else 'nenhuma cota'} {'saltaram' if len(acima) > 1 else 'saltou'} mais que a variação típica de 2018–2023, e {', '.join(abaixo)} não. O padrão é **compatível** com a redução do limite de renda (de 1,5 para 1 salário mínimo), que deixa o grupo LB mais restrito. Mas é um único ano, sem controle para outras mudanças.
- Além do código, 2024 coincide com a mudança nas regras de concorrência: desde 2024 nenhuma cota teve nota acima da AC (post 10).

## Limitações e ressalvas

- A equivalência entre eras foi **inferida das legendas dos PDFs**. Os editais não foram lidos (veja `docs/relatorio_qualidade_base.md`).
- Um ano só (2024) de comparação imediata. Variações de ENEM e vagas no mesmo ano se confundem com a mudança de regra.
- Quilombolas de 2024 não estão na base.

## Como reproduzir

```bash
python scripts/12_regime_2024.py
```
""")


def checar(res):
    d = res["d"]
    assert set(d[d["ano"] >= 2024]["era_cota"]) == {"E3_2024+"}
    assert d[(d["ano"] >= 2024) & d["cota_padrao"].isin(["LB_PPI_PCD", "LI_PPI_PCD"])].empty
    assert len(res["depara"]) == 23
    # O resumo do post afirma: cotas LB saltaram acima do típico em 2024, cotas LI não.
    c = res["comp"]
    acima = set(c.index[c["salto 2023→2024"] > c["variação anual típica 2018–2023"]])
    assert acima == {"LB_EP", "LB_PPI"}, acima


def main():
    res = calcular()
    checar(res)
    post(res, figura(res))


if __name__ == "__main__":
    main()
