"""
Reconstruye MI-500-instrumentacion.html a partir de template.html + bank/*.json.

Uso:
    python build.py

Flujo para anadir/regenerar preguntas:
  1. Edita o anade bank/mXX.json (uno por modulo, mismo formato que los existentes:
     {"id": int, "name": str, "questions": [{"q","options","correct","explanation","difficulty","module"}, ...]})
  2. Corre este script para reconstruir el HTML final.
  3. Abre MI-500-instrumentacion.html para verificar. El progreso guardado en el
     navegador (localStorage, clave mi500_state_v1) se basa en el indice de la
     pregunta dentro de su modulo; anadir preguntas al final de un modulo es seguro,
     pero insertar/borrar preguntas en medio desordena las estadisticas ya guardadas.
"""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
BANK_DIR = os.path.join(ROOT, "bank")
TEMPLATE = os.path.join(ROOT, "template.html")
OUTPUT = os.path.join(ROOT, "MI-500-instrumentacion.html")

def main():
    modules = []
    files = sorted(f for f in os.listdir(BANK_DIR) if f.endswith(".json"))
    for fname in files:
        with open(os.path.join(BANK_DIR, fname), encoding="utf-8") as f:
            modules.append(json.load(f))
    modules.sort(key=lambda m: m["id"])

    total = sum(len(m["questions"]) for m in modules)
    print(f"Modulos: {len(modules)} | Preguntas totales: {total}")

    with open(TEMPLATE, encoding="utf-8") as f:
        template = f.read()

    bank_json = json.dumps(modules, ensure_ascii=False)
    if "__BANK_DATA__" not in template:
        raise SystemExit("template.html no contiene el marcador __BANK_DATA__")
    out = template.replace("__BANK_DATA__", bank_json)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"Generado: {OUTPUT}")

if __name__ == "__main__":
    main()
