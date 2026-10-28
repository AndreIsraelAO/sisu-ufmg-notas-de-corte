# sisu-ufmg-notas-de-corte-dados

Dataset completo das notas de corte do SISU/UFMG, 2014–2026. **Só os dados**: sem scripts, gráficos ou posts.

Para as 20 análises, o código e os textos, use o repositório: https://github.com/AndreIsraelAO/sisu-ufmg-notas-de-corte

```
pip install sisu-ufmg-notas-de-corte-dados
```

```python
import pandas as pd
from sisu_ufmg_dados import caminho

df = pd.read_csv(caminho("notas_corte.csv"))   # base longa, todas as chamadas
```

| Arquivo | Conteúdo |
|---|---|
| `notas_corte.csv` | base longa (52.144 linhas) |
| `notas_corte_final.csv` | última chamada de cada chave (8.405 linhas) |
| `de_para_cursos.csv` | nome bruto → `curso_id` |
| `de_para_cotas.csv` | código de cota por era → código padronizado + confiança |
| `areas_conhecimento.csv` | `curso_id` → área |
| `excecoes_monotonia.csv` | exceções à queda da nota mínima entre chamadas (vazio) |

`qualidade_dados.md` (dentro do pacote) descreve as validações. A base é agregada por curso, campus, turno, chamada e cota; não há dados pessoais. Fonte: PDFs públicos do SISU/UFMG. Licença MIT.

## Build (mantenedor)

Sdist e wheel são construídos separadamente, porque os CSVs vêm de `../data`:

```
python -m build --sdist && python -m build --wheel && twine upload dist/*
```
