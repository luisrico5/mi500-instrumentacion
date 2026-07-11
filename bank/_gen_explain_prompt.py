"""Genera el prompt para pedir explicaciones de estudio mas detalladas de un modulo."""
import json, sys, os

ROOT = os.path.dirname(os.path.abspath(__file__))
LETTERS = "ABCD"

def main(mod_num):
    fname = os.path.join(ROOT, f"m{mod_num:02d}.json")
    with open(fname, encoding="utf-8") as f:
        data = json.load(f)
    qs = data["questions"]
    n = len(qs)

    lines = []
    for i, q in enumerate(qs, 1):
        opts = "; ".join(f"{LETTERS[j]}) {o}" for j, o in enumerate(q["options"]))
        correct_letter = LETTERS[q["correct"]]
        lines.append(f"{i}. {q['q']} Opciones: {opts}. Respuesta correcta: {correct_letter}) {q['options'][q['correct']]}.")
    listado = "\n".join(lines)

    prompt = f"""Eres un tutor experto en instrumentacion industrial preparando material de estudio para un examen de maestria. Trabaja SOLO con el contenido de las fuentes de este cuaderno (Creus 8a ed., PDF de ajuste y calibracion, instrumentacionycontrol.net, instrumentationtools.com).

Modulo: "{data['name']}" (modulo {mod_num} de 10). Abajo hay {n} preguntas de opcion multiple ya resueltas (con su respuesta correcta marcada).

Para CADA una de las {n} preguntas, en el MISMO ORDEN, sin omitir ninguna, escribe una explicacion de estudio (modo repaso) MAS DETALLADA que la de un examen normal. Debe incluir:
- Por que la opcion correcta es correcta, citando la definicion, formula o criterio tecnico exacto de la fuente.
- Por que al menos una de las opciones incorrectas es una confusion tipica (que error conceptual representa).
- Si la pregunta implica un calculo, el desarrollo numerico paso a paso.
Extension: 3 a 5 frases por pregunta, en espanol tecnico claro, como si fuera una nota de estudio para repasar el tema, no solo para justificar la respuesta de un examen.

Preguntas:
{listado}

Responde UNICAMENTE con un array JSON de exactamente {n} strings (una explicacion por pregunta, en el mismo orden), sin objetos, sin markdown, sin numeracion, sin texto adicional antes o despues del array."""
    out = os.path.join(ROOT, f"_xprompt_m{mod_num:02d}.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write(prompt)
    print(out, f"({n} preguntas)")

if __name__ == "__main__":
    main(int(sys.argv[1]))
