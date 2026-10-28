"""Testes: cada análise roda `calcular()` + `checar()`, e alguns números são recalculados direto dos CSVs,
sem passar por scripts/comum.py, para pegar erros nas regras de filtro compartilhadas."""
import importlib
import pathlib
import sys

import pandas as pd
import pytest
from scipy.stats import spearmanr

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
MODULOS = sorted(p.stem for p in (RAIZ / "scripts").glob("[0-9][0-9]_*.py"))


@pytest.fixture(scope="module")
def longa():
    return pd.read_csv(RAIZ / "data" / "notas_corte.csv", encoding="utf-8-sig")


@pytest.fixture(scope="module")
def fin():
    return pd.read_csv(RAIZ / "data" / "notas_corte_final.csv", encoding="utf-8-sig")


def carregar(nome):
    return importlib.import_module(nome)


def test_vinte_scripts():
    assert len(MODULOS) == 20


@pytest.mark.parametrize("nome", MODULOS)
def test_calcula_e_checa(nome):
    m = carregar(nome)
    m.checar(m.calcular())


def test_arquivo_ausente_da_erro_claro(monkeypatch, tmp_path):
    import comum
    monkeypatch.setattr(comum, "DATA", tmp_path)
    with pytest.raises(FileNotFoundError, match="não encontrado"):
        comum.base()


def test_contagens_finais(longa, fin):
    assert len(longa) == 52144 and len(fin) == 8405
    # 2014–2021 só têm a chamada regular: final == regular.
    antes = longa[longa["ano"] <= 2021]
    assert antes.groupby("edicao_chave").size().equals(fin[fin["ano"] <= 2021].groupby("edicao_chave").size())


def test_01_valor_medicina(longa):
    x = longa[(longa["curso_id"] == "medicina-bach") & (longa["edicao_chave"] == "2026-1")
              & (longa["chamada"] == 0) & (longa["cota_padrao"] == "AC")]["nota_min"].iat[0]
    serie = carregar("01_evolucao_top10").calcular()["serie"]
    assert serie.loc["Medicina – Integral", "2026-1"] == x


def test_04_queda_soma(longa, fin):
    res = carregar("04_queda_chamadas").calcular()
    m = res["m"]
    ed = fin[fin["edicao_chave"].isin(["2022-1", "2023-1", "2024-1", "2025-1", "2026-1"])]
    assert len(m) == len(ed)
    reg = longa[(longa["chamada"] == 0) & (longa["ano"] >= 2022)]
    esperado = reg["nota_min"].sum() - ed["nota_min"].sum()
    assert abs(m["queda"].sum() - esperado) < 1e-6


def test_13_cursos_por_edicao(fin):
    t = carregar("13_expansao_oferta").calcular()["tab"]
    assert (fin.groupby("edicao_chave")["curso_id"].nunique() == t["cursos"]).all()
    assert t.loc["2026-1", "cursos"] == 74


def test_16_spearman(longa):
    ac = longa[(longa["cota_padrao"] == "AC") & (longa["campus"] == "Belo Horizonte") & (longa["chamada"] == 0)]
    a = ac[ac["edicao_chave"] == "2025-1"].set_index(["curso_id", "turno"])["nota_min"]
    b = ac[ac["edicao_chave"] == "2026-1"].set_index(["curso_id", "turno"])["nota_min"]
    par = pd.concat([a, b], axis=1, join="inner")
    rho = spearmanr(par.iloc[:, 0], par.iloc[:, 1])[0]
    t = carregar("16_estabilidade_ranking").calcular()["tab"]
    assert abs(t[(t["de"] == "2025-1") & (t["para"] == "2026-1")]["rho"].iat[0] - rho) < 1e-12


def test_15_reprodutivel():
    m = carregar("15_agrupamento")
    a, b = m.calcular()["feat"]["grupo"], m.calcular()["feat"]["grupo"]
    assert a.equals(b)


def test_18_mapeamento_completo():
    areas = pd.read_csv(RAIZ / "data" / "areas_conhecimento.csv")
    cursos = pd.read_csv(RAIZ / "data" / "de_para_cursos.csv", encoding="utf-8-sig")
    assert set(areas["curso_id"]) == set(cursos["curso_id"])
    assert areas["area"].nunique() == 6


def test_19_so_ampla_concorrencia():
    r = carregar("19_altas_quedas").calcular()["r"]
    assert set(r["cota_padrao"]) == {"AC"}
