"""Aplica un lote de citas de fuente (respuesta de notebooklm ask) a un rango de preguntas de un modulo."""
import json, re, sys, os

ROOT = os.path.dirname(os.path.abspath(__file__))
BAD_ESCAPE_RE = re.compile(r'\\(?!["\\/bfnrtu])')

def fix_invalid_json_escapes(raw):
    return BAD_ESCAPE_RE.sub(r"\\\\", raw)

def clean(s):
    return s.strip().strip('"').strip()

def main(mod_num, start, count):
    resp_path = os.path.join(ROOT, f"_srcresp_m{mod_num:02d}_{start:02d}.json")
    bank_path = os.path.join(ROOT, f"m{mod_num:02d}.json")

    with open(resp_path, encoding="utf-8") as f:
        resp = json.load(f)
    if "answer" not in resp:
        raise SystemExit(f"m{mod_num:02d}[{start}:{start+count}]: respuesta con error: {resp}")

    answer = resp["answer"].strip()
    answer = re.sub(r"^```(json)?", "", answer).strip()
    answer = re.sub(r"```$", "", answer).strip()
    answer = fix_invalid_json_escapes(answer)
    sources = json.loads(answer)

    with open(bank_path, encoding="utf-8") as f:
        bank = json.load(f)

    qs = bank["questions"]
    target = qs[start:start + count]
    if len(sources) != len(target):
        raise SystemExit(f"m{mod_num:02d}[{start}:{start+count}]: {len(sources)} fuentes vs {len(target)} preguntas esperadas — no se aplica")

    for q, src in zip(target, sources):
        q["source"] = clean(src)

    with open(bank_path, "w", encoding="utf-8") as f:
        json.dump(bank, f, ensure_ascii=False, indent=2)

    print(f"m{mod_num:02d}[{start}:{start+count}]: {len(target)} fuentes aplicadas")

if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
