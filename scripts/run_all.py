"""Executa as 20 análises: primeiro a 20 (validações da base), depois 01 a 19. Para no primeiro erro."""
import pathlib
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")

PASTA = pathlib.Path(__file__).resolve().parent
scripts = sorted(PASTA.glob("[0-9][0-9]_*.py"))
scripts = [s for s in scripts if s.name.startswith("20_")] + [s for s in scripts if not s.name.startswith("20_")]
assert len(scripts) == 20, f"esperados 20 scripts, encontrados {len(scripts)}"

for s in scripts:
    print(f"==> {s.name}", flush=True)
    r = subprocess.run([sys.executable, str(s)], cwd=PASTA.parent)
    if r.returncode != 0:
        sys.exit(f"Falhou: {s.name} (código {r.returncode})")
print("OK: 20 análises executadas.")
