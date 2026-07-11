"""Genera el prompt para pedir SOLO la cita de fuente (source) de un rango de preguntas ya existentes."""
import json, sys, os

ROOT = os.path.dirname(os.path.abspath(__file__))
LETTERS = "ABCD"

def main(mod_num, start, count):
    fname = os.path.join(ROOT, f"m{mod_num:02d}.json")
    with open(fname, encoding="utf-8") as f:
        data = json.load(f)
    qs = data["questions"][start:start + count]
    n = len(qs)
    if n == 0:
        raise SystemExit("rango vacio")

    lines = []
    for i, q in enumerate(qs, 1):
        correct_letter = LETTERS[q["correct"]]
        lines.append(f"{i}. {q['q']} Respuesta correcta: {correct_letter}) {q['options'][q['correct']]}. Explicacion: {q['explanation']}")
    listado = "\n".join(lines)

    prompt = f"""Trabaja SOLO con el contenido de las fuentes de este cuaderno: Creus, Instrumentacion Industrial 8a ed. (PDF), Instrumentos industriales: su ajuste y calibracion (PDF), instrumentacionycontrol.net (web), instrumentationtools.com (web).

Modulo: "{data['name']}" (modulo {mod_num} de 10). Abajo hay {n} preguntas ya resueltas con su explicacion.

Para CADA una de las {n} preguntas, en el MISMO ORDEN, indica de que fuente exacta proviene el contenido de la respuesta:
- Si es del libro Creus: escribe "Creus, Instrumentacion Industrial, 8a ed., cap. X" (identifica el numero de capitulo real segun el contenido; si puedes identificar tambien el apartado o pagina aproximada, agregalo).
- Si es del PDF de ajuste y calibracion: escribe "Instrumentos industriales: su ajuste y calibracion, cap. X" (mismo criterio de capitulo/apartado).
- Si es de una pagina web: escribe exactamente el nombre del sitio, "instrumentacionycontrol.net" o "instrumentationtools.com".
Si el contenido combina mas de una fuente, elige la mas relevante para el nucleo de la respuesta.

Preguntas:
{listado}

Responde UNICAMENTE con un array JSON de exactamente {n} strings (una cita de fuente por pregunta, en el mismo orden), sin markdown, sin numeracion, sin texto adicional antes o despues del array."""
    out = os.path.join(ROOT, f"_srcprompt_m{mod_num:02d}_{start:02d}.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write(prompt)
    print(out, f"({n} preguntas, indices {start}-{start+n-1})")

if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
