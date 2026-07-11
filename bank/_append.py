"""Parsea la respuesta de notebooklm ask y anexa las preguntas nuevas al bank/mXX.json correspondiente."""
import json, re, sys, os

ROOT = os.path.dirname(os.path.abspath(__file__))

CITE_RE = re.compile(r"\s*\[\d+\](,\s*\[\d+\])*")

def clean(s):
    if isinstance(s, str):
        return CITE_RE.sub("", s).strip()
    return s

def main(mod_num):
    resp_path = os.path.join(ROOT, f"_resp_m{mod_num:02d}.json")
    bank_path = os.path.join(ROOT, f"m{mod_num:02d}.json")

    with open(resp_path, encoding="utf-8") as f:
        resp = json.load(f)
    answer = resp["answer"].strip()
    # quita posibles fences de markdown
    answer = re.sub(r"^```(json)?", "", answer.strip()).strip()
    answer = re.sub(r"```$", "", answer.strip()).strip()

    new_qs = json.loads(answer)
    if not isinstance(new_qs, list):
        raise SystemExit(f"m{mod_num:02d}: la respuesta no es un array JSON")

    with open(bank_path, encoding="utf-8") as f:
        bank = json.load(f)

    existing_texts = {q["q"].strip().lower() for q in bank["questions"]}
    added = 0
    for q in new_qs:
        for k in ("q", "options", "correct", "explanation", "difficulty"):
            if k not in q:
                raise SystemExit(f"m{mod_num:02d}: falta campo '{k}' en una pregunta nueva: {q}")
        if len(q["options"]) != 4:
            raise SystemExit(f"m{mod_num:02d}: pregunta sin 4 opciones: {q['q']}")
        if not (0 <= q["correct"] <= 3):
            raise SystemExit(f"m{mod_num:02d}: indice 'correct' invalido: {q}")
        if q["difficulty"] not in (1, 2, 3):
            raise SystemExit(f"m{mod_num:02d}: 'difficulty' invalida: {q}")
        q["q"] = clean(q["q"])
        q["explanation"] = clean(q["explanation"])
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
    main(int(sys.argv[1]))
