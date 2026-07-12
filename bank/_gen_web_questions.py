"""Genera preguntas via NotebookLM restringido a una sola fuente web por llamada (citas 1:1 verificables).

Uso: python _gen_web_questions.py <mod_num>

Lee scratchpad/module_sources.json (mapeo modulo -> fuentes con conteo por fuente),
llama 'notebooklm ask -s <id>' de forma serial (nunca en paralelo, la API no lo soporta),
y guarda la respuesta cruda de cada fuente en scratchpad/raw_m{mod}_{n}.json para revision manual posterior.
"""
import json, subprocess, sys, os

SCRATCH = r"C:\Users\Dell\AppData\Local\Temp\claude\C--instrumentacion\506eee72-e097-4170-8e49-bd8547199a8e\scratchpad"

COUNTS = {
    "1": [4, 4, 4],
    "2": [4, 4, 4, 4, 4],
    "3": [3, 3],
    "4": [5, 5, 4],
    "5": [4, 4],
    "6": [4, 3, 3],
    "7": [3, 3],
    "8": [3, 3],
    "9": [2, 2],
    "10": [3, 3, 3, 3],
}

PROMPT_TMPL = """Basandote UNICAMENTE en esta fuente, genera exactamente {n} preguntas de opcion multiple en espanol sobre instrumentacion industrial, nivel tecnico intermedio-avanzado, formato examen de certificacion profesional. Cada pregunta debe tener: q (enunciado), options (4 opciones), correct (indice 0-based de la respuesta correcta), explanation (explicacion tecnica detallada de por que es correcta y por que las otras opciones son incorrectas), difficulty (1, 2 o 3). No inventes datos que no esten en la fuente. Devuelve SOLO un array JSON valido, sin texto adicional antes ni despues, sin backticks de markdown."""

def main(mod):
    with open(os.path.join(SCRATCH, "module_sources.json"), encoding="utf-8") as f:
        mapping = json.load(f)
    sources = mapping[mod]["sources"]
    counts = COUNTS[mod]
    assert len(counts) == len(sources), f"m{mod}: {len(counts)} counts vs {len(sources)} sources"

    for i, (src, n) in enumerate(zip(sources, counts)):
        out_path = os.path.join(SCRATCH, f"raw_m{int(mod):02d}_{i}.json")
        if os.path.exists(out_path):
            print(f"  [ya existe, saltado] {out_path}")
            continue
        prompt = PROMPT_TMPL.format(n=n)
        print(f"Asking source {src['id'][:8]} ({src['title'][:50]}) for {n} questions...")
        p = subprocess.run(
            ["notebooklm", "ask", "-s", src["id"], prompt, "--json"],
            capture_output=True, text=True, timeout=90,
            encoding="utf-8", errors="replace"
        )
        if p.returncode != 0:
            print("ERROR:", p.stderr[:500])
            continue
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(p.stdout)
        print(f"  guardado -> {out_path}")

if __name__ == "__main__":
    main(sys.argv[1])
