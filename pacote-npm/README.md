# @andreisraelao/sisu-ufmg-notas-de-corte-dados

Dataset completo das notas de corte do SISU/UFMG, 2014–2026. **Só os dados**: sem scripts, gráficos ou posts. Código e análises: https://github.com/AndreIsraelAO/sisu-ufmg-notas-de-corte

```
echo "@andreisraelao:registry=https://npm.pkg.github.com" >> .npmrc
npm install @andreisraelao/sisu-ufmg-notas-de-corte-dados
```

(O GitHub Packages exige login com um token `read:packages`: `npm login --registry=https://npm.pkg.github.com`.)

```js
const { caminho } = require("@andreisraelao/sisu-ufmg-notas-de-corte-dados");
caminho("notas_corte.csv"); // caminho do CSV (52.144 linhas)
```

Arquivos: `notas_corte.csv`, `notas_corte_final.csv`, `de_para_cursos.csv`, `de_para_cotas.csv`, `areas_conhecimento.csv`, `excecoes_monotonia.csv`. Validações em `qualidade_dados.md`. Licença MIT.
