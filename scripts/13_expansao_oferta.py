"""13 — Expansão da oferta: cursos, ofertas, campi e linhas por edição."""
import matplotlib.pyplot as plt

from comum import base, escrever_post, md, salvar


def calcular():
    d = base()
    reg = d[d["regular"]]
    tab = reg.groupby("edicao_chave").agg(cursos=("curso_id", "nunique"), ofertas=("oferta", "nunique"),
                                          campi=("campus", "nunique"), cotas=("cota_padrao", "nunique"),
                                          linhas_regular=("nota_min", "size"))
    tab["ofertas_BH"] = reg[reg["campus"] == "Belo Horizonte"].groupby("edicao_chave")["oferta"].nunique()
    tab["ofertas_MOC"] = reg[reg["campus"] == "Montes Claros"].groupby("edicao_chave")["oferta"].nunique()
    tab["linhas_total"] = d.groupby("edicao_chave").size()
    tab["chamadas"] = d.groupby("edicao_chave")["chamada"].nunique()
    # Entradas e saídas de cursos entre edições "cheias" (ignora as segundas edições de 2014/2015, que são parciais).
    eds = [e for e in tab.index if not e.endswith("-2")]
    nomes = reg.drop_duplicates("curso_id").set_index("curso_id")["curso_nome"]
    mods = reg.drop_duplicates("curso_id").set_index("curso_id")["modelo"]
    rot = lambda c: nomes[c] + (" (Lic.)" if mods[c] == "Licenciatura" else "")
    mov = []
    for a, b in zip(eds, eds[1:]):
        ca, cb = set(reg[reg["edicao_chave"] == a]["curso_id"]), set(reg[reg["edicao_chave"] == b]["curso_id"])
        if cb - ca or ca - cb:
            mov.append({"Edição": b, "Entram": "; ".join(sorted(map(rot, cb - ca))) or "—",
                        "Saem": "; ".join(sorted(map(rot, ca - cb))) or "—"})
    return {"d": d, "tab": tab, "mov": mov}


def figura(res):
    t = res["tab"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.5, 5))
    a1.plot(t.index, t["ofertas"], marker="o", label="Ofertas (curso × campus × turno)")
    a1.plot(t.index, t["cursos"], marker="s", label="Cursos (curso_id)")
    a1.plot(t.index, t["ofertas_MOC"], marker="^", label="Ofertas em Montes Claros")
    a1.set_ylim(0, None)
    a1.set_ylabel("Quantidade")
    a1.set_title("Cursos e ofertas por edição (chamada regular)")
    a1.legend(fontsize=8)
    a2.bar(t.index, t["linhas_total"], color="#56B4E9")
    a2.set_ylabel("Linhas na base (todas as chamadas)")
    a2.set_title("Linhas por edição: efeito das listas de espera")
    for a in (a1, a2):
        a.set_xlabel("Edição do SISU")
        a.tick_params(axis="x", rotation=60)
    return salvar(fig, "13_expansao_oferta")


def post(res, fig):
    t = res["tab"]
    escrever_post("13-expansao-da-oferta", f"""
# A oferta no SISU/UFMG passou de {t.loc['2014-1', 'ofertas']} para {t.loc['2026-1', 'ofertas']} ofertas, mas o salto de linhas vem das listas de espera

**Resumo.** O número de cursos na chamada regular foi de {t.loc['2014-1', 'cursos']} (2014-1) para {t.loc['2026-1', 'cursos']} (2026-1), e o de ofertas (curso × campus × turno) de {t.loc['2014-1', 'ofertas']} para {t.loc['2026-1', 'ofertas']}. Os dois campi aparecem em todas as primeiras edições. O número de linhas da base passa de algumas centenas para mais de 10 mil a partir de 2023, efeito da publicação das listas de espera e das novas modalidades de cota, não da criação de cursos.

## Pergunta

Como mudou o tamanho da oferta da UFMG no SISU entre 2014 e 2026?

## Dados usados

- `data/notas_corte.csv`: chamada regular para contar cursos e ofertas; todas as chamadas para contar linhas.
- **Não há dado de vagas** na base. "Oferta" aqui é uma combinação curso × campus × turno que aparece no PDF, não o número de vagas.

## Método

Contagens distintas por edição. Para entradas e saídas de cursos, comparamos cada edição com a anterior, pulando as segundas edições de 2014 e 2015, que oferecem só parte dos cursos.

## Resultados

**Tabela 1 – Tamanho da oferta por edição.**

{md(t.rename_axis('Edição').rename(columns={'cursos': 'Cursos', 'ofertas': 'Ofertas', 'campi': 'Campi', 'cotas': 'Códigos de cota', 'linhas_regular': 'Linhas (regular)', 'ofertas_BH': 'Ofertas BH', 'ofertas_MOC': 'Ofertas MOC', 'linhas_total': 'Linhas (todas)', 'chamadas': 'Chamadas'}), index=True)}

![Expansão]({fig})

*Figura 1 – Esquerda: cursos e ofertas por edição. Direita: total de linhas por edição. Fonte: SISU/UFMG; elaboração própria.*

**Tabela 2 – Cursos que entram e saem (pelo `curso_id`).**

{md(__import__('pandas').DataFrame(res['mov']))}

## Interpretação

- O crescimento de cursos e ofertas é modesto e concentrado em 2016 e em 2024–2026.
- Várias "entradas" e "saídas" são **renomeações**, não cursos novos. Exemplos: Comunicação Social → Jornalismo, Relações Públicas e Publicidade (2016); Antropologia → Antropologia e Arqueologia (2024); Engenharia Metalúrgica → Metalúrgica e de Materiais (2024); Ciência da Computação + Sistemas de Informação → curso combinado (2025). A base mantém `curso_id` separados nesses casos (post 20).
- O número de linhas não mede expansão da universidade. Ele cresce porque a base passa a ter listas de espera (2022+) e mais modalidades de cota (2018+, 2025+).

## Limitações e ressalvas

- Sem dado de vagas, não é possível medir a expansão real de oferta.
- As notas do ENEM e as vagas mudam a cada ano; esta análise só conta o que aparece nos PDFs.

## Como reproduzir

```bash
python scripts/13_expansao_oferta.py
```
""")


def checar(res):
    d, t = res["d"], res["tab"]
    assert t["linhas_total"].sum() == len(d)
    from comum import final
    f = final()
    assert (f.groupby("edicao_chave")["curso_id"].nunique() == t["cursos"]).all()


def main():
    res = calcular()
    checar(res)
    post(res, figura(res))


if __name__ == "__main__":
    main()
