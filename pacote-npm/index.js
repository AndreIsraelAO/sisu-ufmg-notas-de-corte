const path = require("path");
const fs = require("fs");

// Caminho de um CSV do dataset (ex.: "notas_corte.csv").
exports.caminho = (nome = "notas_corte_final.csv") => {
  const p = path.join(__dirname, "data", nome);
  if (!fs.existsSync(p)) throw new Error(`${nome} não existe em ${path.join(__dirname, "data")}`);
  return p;
};
