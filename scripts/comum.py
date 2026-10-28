"""Funções compartilhadas pelas 20 análises: caminhos, leitura, filtros e estilo.

Todas as regras de filtro que valem para o projeto inteiro ficam aqui, para que
cada script use exatamente a mesma definição de "chamada regular", "final" etc.
"""
import pathlib
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"
FIG = RAIZ / "figuras"
POSTS = RAIZ / "posts"
SEED = 20260101

FONTE = "Fonte: SISU/UFMG, PDFs oficiais de notas máximas e mínimas 2014–2026; elaboração própria."

# Okabe-Ito: paleta segura para daltonismo.
CORES = ["#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7", "#56B4E9", "#999933", "#000000"]

COTA_DESC = {
    "AC": "Ampla concorrência",
    "LB_PPI": "Escola pública, renda baixa, PPI",
    "LB_EP": "Escola pública, renda baixa",
    "LB_PCD": "Escola pública, renda baixa, PCD",
    "LB_Q": "Escola pública, renda baixa, quilombola",
    "LI_PPI": "Escola pública, PPI (qualquer renda)",
    "LI_EP": "Escola pública (qualquer renda)",
    "LI_PCD": "Escola pública, PCD (qualquer renda)",
    "LI_Q": "Escola pública, quilombola (qualquer renda)",
    "LB_PPI_PCD": "Escola pública, renda baixa, PPI e PCD (2018–2023)",
    "LI_PPI_PCD": "Escola pública, PPI e PCD, qualquer renda (2018–2023)",
}


def ler(nome):
    """Lê um CSV de data/ e falha com mensagem clara se ele não existir."""
    caminho = DATA / nome
    if not caminho.exists():
        raise FileNotFoundError(
            f"Arquivo de entrada não encontrado: {caminho}\n"
            "Os CSVs limpos devem estar em data/ (veja README.md, seção 'Dados')."
        )
    return pd.read_csv(caminho, encoding="utf-8-sig")


def base():
    """Base longa (todas as chamadas) com a coluna `regular`."""
    d = ler("notas_corte.csv")
    # Chamada regular = menor chamada da edição (0; mas 11 em 2016 e 10 em 2017, chamada única).
    d["regular"] = d["chamada"] == d.groupby("edicao_chave")["chamada"].transform("min")
    d["oferta"] = rotulo_oferta(d)
    return d


def final():
    """Uma linha por chave, na maior chamada existente (is_final)."""
    d = ler("notas_corte_final.csv")
    d["oferta"] = rotulo_oferta(d)
    return d


def regular_ac(d=None, campus="Belo Horizonte"):
    """Nota de corte da chamada regular, ampla concorrência (uma linha por oferta × edição)."""
    d = base() if d is None else d
    r = d[d["regular"] & (d["cota_padrao"] == "AC")]
    if campus:
        r = r[r["campus"] == campus]
    return r.copy()


def rotulo_oferta(d):
    """'Curso (Lic.) – Turno' — oferta = curso_id × campus × turno."""
    lic = d["modelo"].eq("Licenciatura").map({True: " (Lic.)", False: ""})
    mc = d["campus"].eq("Montes Claros").map({True: ", MOC", False: ""})
    return d["curso_nome"] + lic + " – " + d["turno"] + mc


def ordem_edicoes(d):
    return sorted(d["edicao_chave"].unique())


def md(df, decimais=2, index=False):
    """Tabela Markdown sem dependências extras."""
    df = df.reset_index() if index else df
    fmt = lambda v: ("–" if v != v else f"{v:.{decimais}f}".replace(".", ",")) if isinstance(v, float) else str(v)
    linhas = ["| " + " | ".join(map(str, df.columns)) + " |", "|" + "---|" * len(df.columns)]
    linhas += ["| " + " | ".join(fmt(v).replace("|", "/") for v in row) + " |" for row in df.itertuples(index=False)]
    return "\n".join(linhas)


def num(v, d=1):
    """Número no formato brasileiro (vírgula decimal)."""
    return f"{v:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def estilo():
    plt.rcParams.update({
        "figure.dpi": 110, "savefig.dpi": 150, "font.size": 10,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.alpha": 0.3, "axes.prop_cycle": plt.cycler(color=CORES),
    })


def salvar(fig, nome, fonte=FONTE):
    """Grava figuras/<nome>.png com a nota de fonte no rodapé."""
    FIG.mkdir(exist_ok=True)
    fig.text(0.01, 0.005, fonte, fontsize=7.5, color="#444", ha="left", va="bottom")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(FIG / f"{nome}.png")
    plt.close(fig)
    return f"../figuras/{nome}.png"


def escrever_post(nome, texto):
    POSTS.mkdir(exist_ok=True)
    (POSTS / f"{nome}.md").write_text(texto.strip() + "\n", encoding="utf-8")
    print(f"post: posts/{nome}.md")


RESSALVA_TEMPO = (
    "As notas do ENEM são padronizadas a cada edição, e o número de vagas, as regras de cota e o "
    "perfil dos candidatos mudam de um ano para outro. Diferenças entre anos mostram o que foi "
    "observado, não uma mudança na \"dificuldade\" do curso."
)

RESSALVA_CORTE = (
    "Nota de corte é a nota do último classificado. Ela depende de quantas pessoas se inscreveram, "
    "de suas notas e do número de vagas; não mede a qualidade do curso. A base não traz o número de "
    "candidatos, então \"mais concorrido\" aqui significa \"maior nota de corte\"."
)

estilo()
