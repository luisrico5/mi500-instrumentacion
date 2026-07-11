"""Aplica un lote de explicaciones detalladas (respuesta de notebooklm ask) a un rango de preguntas de un modulo."""
import json, re, sys, os

ROOT = os.path.dirname(os.path.abspath(__file__))
CITE_RE = re.compile(r"\s*\[[0-9,\s\-]+\]")
BAD_ESCAPE_RE = re.compile(r'\\(?!["\\/bfnrtu])')

LATEX_REPLACEMENTS = [
    (re.compile(r"\\sqrt\{([^}]*)\}"), r"√(\1)"),
    (re.compile(r"\\frac\{([^}]*)\}\{([^}]*)\}"), r"(\1/\2)"),
    (re.compile(r"\\times"), "×"),
    (re.compile(r"\\cdot"), "·"),
    (re.compile(r"\\Delta"), "Δ"),
    (re.compile(r"\\pm"), "±"),
    (re.compile(r"\\approx"), "≈"),
    (re.compile(r"\\text\{([^}]*)\}"), r"\1"),
    (re.compile(r"[{}$]"), ""),
]

def fix_invalid_json_escapes(raw):
    return BAD_ESCAPE_RE.sub(r"\\\\", raw)

def clean(s):
    s = CITE_RE.sub("", s).strip()
    for pattern, repl in LATEX_REPLACEMENTS:
        s = pattern.sub(repl, s)
    return s.strip()

def main(mod_num, start, count):
    resp_path = os.path.join(ROOT, f"_bxresp_m{mod_num:02d}_{start:02d}.json")
    bank_path = os.path.join(ROOT, f"m{mod_num:02d}.json")

    with open(resp_path, encoding="utf-8") as f:
        resp = json.load(f)
    if "answer" not in resp:
        raise SystemExit(f"m{mod_num:02d}[{start}:{start+count}]: respuesta con error: {resp}")

    answer = resp["answer"].strip()
    answer = re.sub(r"^```(json)?", "", answer).strip()
    answer = re.sub(r"```$", "", answer).strip()
    answer = fix_invalid_json_escapes(answer)
    explanations = json.loads(answer)

    with open(bank_path, encoding="utf-8") as f:
        bank = json.load(f)

    qs = bank["questions"]
    target = qs[start:start + count]
    if len(explanations) != len(target):
        raise SystemExit(f"m{mod_num:02d}[{start}:{start+count}]: {len(explanations)} explicaciones vs {len(target)} preguntas esperadas — no se aplica")

    for q, exp in zip(target, explanations):
        q["explanation"] = clean(exp)

    with open(bank_path, "w", encoding="utf-8") as f:
        json.dump(bank, f, ensure_ascii=False, indent=2)

    print(f"m{mod_num:02d}[{start}:{start+count}]: {len(target)} explicaciones actualizadas")

if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
