"""Anexa un lote de preguntas escritas a mano (JSON array plano) a bank/mXX.json, con validacion y dedup.

Uso: python _append_manual.py <mod_num> <archivo_json_con_array_de_preguntas>

Cada pregunta debe tener: q, options (4), correct (0-3), explanation, source, difficulty (1|2|3).
El campo "module" se asigna automaticamente.
"""
import json, re, sys, os

ROOT = os.path.dirname(os.path.abspath(__file__))
CITE_RE = re.compile(r"\s*\[[0-9,\s\-]+\]")

def clean(s):
    if not isinstance(s, str):
        return s
    return CITE_RE.sub("", s).strip()

def main(mod_num, input_path):
    bank_path = os.path.join(ROOT, f"m{mod_num:02d}.json")
    with open(input_path, encoding="utf-8") as f:
        new_qs = json.load(f)
    if not isinstance(new_qs, list):
        raise SystemExit(f"m{mod_num:02d}: el archivo de entrada no es un array JSON")

    with open(bank_path, encoding="utf-8") as f:
        bank = json.load(f)

    existing_texts = {q["q"].strip().lower() for q in bank["questions"]}
    added = 0
    for q in new_qs:
        for k in ("q", "options", "correct", "explanation", "source", "difficulty"):
            if k not in q:
                raise SystemExit(f"m{mod_num:02d}: falta campo '{k}' en una pregunta: {q}")
        if len(q["options"]) != 4:
            raise SystemExit(f"m{mod_num:02d}: pregunta sin 4 opciones: {q['q']}")
        if not (0 <= q["correct"] <= 3):
            raise SystemExit(f"m{mod_num:02d}: indice 'correct' invalido: {q}")
        if q["difficulty"] not in (1, 2, 3):
            raise SystemExit(f"m{mod_num:02d}: 'difficulty' invalida: {q}")
        q["q"] = clean(q["q"])
        q["explanation"] = clean(q["explanation"])
        q["source"] = clean(q["source"])
        q["options"] = [clean(o) for o in q["options"]]
        q["module"] = mod_num
        if q["q"].strip().lower() in existing_texts:
            print(f"  [saltada, duplicada] {q['q'][:60]}...")
            continue
        bank["questions"].append(q)
        existing_texts.add(q["q"].strip().lower())
        added += 1

    with open(bank_path, "w", encoding="utf-8") as f:
        json.dump(bank, f, ensure_ascii=False, indent=2)

    print(f"m{mod_num:02d}: {added} preguntas nuevas anadidas (total ahora: {len(bank['questions'])})")

if __name__ == "__main__":
    main(int(sys.argv[1]), sys.argv[2])
