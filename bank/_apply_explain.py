"""Parsea la respuesta de notebooklm ask (array de explicaciones) y sobrescribe explanation en bank/mXX.json."""
import json, re, sys, os

ROOT = os.path.dirname(os.path.abspath(__file__))
CITE_RE = re.compile(r"\s*\[[0-9,\s\-]+\]")

def clean(s):
    return CITE_RE.sub("", s).strip()

def main(mod_num):
    resp_path = os.path.join(ROOT, f"_xresp_m{mod_num:02d}.json")
    bank_path = os.path.join(ROOT, f"m{mod_num:02d}.json")

    with open(resp_path, encoding="utf-8") as f:
        resp = json.load(f)
    if "answer" not in resp:
        raise SystemExit(f"m{mod_num:02d}: respuesta con error: {resp}")

    answer = resp["answer"].strip()
    answer = re.sub(r"^```(json)?", "", answer).strip()
    answer = re.sub(r"```$", "", answer).strip()
    explanations = json.loads(answer)

    with open(bank_path, encoding="utf-8") as f:
        bank = json.load(f)

    qs = bank["questions"]
    if len(explanations) != len(qs):
        raise SystemExit(f"m{mod_num:02d}: {len(explanations)} explicaciones recibidas vs {len(qs)} preguntas — no se aplica, revisar manualmente")

    for q, exp in zip(qs, explanations):
        q["explanation"] = clean(exp)

    with open(bank_path, "w", encoding="utf-8") as f:
        json.dump(bank, f, ensure_ascii=False, indent=2)

    print(f"m{mod_num:02d}: {len(qs)} explicaciones actualizadas")

if __name__ == "__main__":
    main(int(sys.argv[1]))
