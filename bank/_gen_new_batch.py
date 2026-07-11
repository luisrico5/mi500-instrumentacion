"""Genera el prompt para pedir preguntas NUEVAS completas (con explicacion detallada y fuente) en un solo lote."""
import json, sys, os

ROOT = os.path.dirname(os.path.abspath(__file__))
DIFF_CYCLE = [1, 1, 2, 2, 3]

def main(mod_num, n_new):
    fname = os.path.join(ROOT, f"m{mod_num:02d}.json")
    with open(fname, encoding="utf-8") as f:
        data = json.load(f)
    existing = [q["q"] for q in data["questions"]]
    dedup = "\n".join(f"- {q}" for q in existing)
    diffs = [DIFF_CYCLE[i % len(DIFF_CYCLE)] for i in range(n_new)]
    diffs_txt = ", ".join(str(d) for d in diffs)

    prompt = f"""Eres un generador de banco de preguntas para un examen de posgrado en instrumentacion industrial (Maestria en Instrumentacion). Trabaja SOLO con el contenido de las fuentes de este cuaderno: Creus, Instrumentacion Industrial 8a ed. (PDF), Instrumentos industriales: su ajuste y calibracion (PDF), instrumentacionycontrol.net (web), instrumentationtools.com (web).

Modulo: "{data['name']}" (modulo numero {mod_num} de 10).

Genera EXACTAMENTE {n_new} preguntas de opcion multiple NUEVAS y distintas (no repitas, no parafrasees) de las que ya existen en este modulo, listadas abajo. Deben cubrir subtemas o angulos que las preguntas existentes no cubren.

Preguntas ya existentes en este modulo (NO las repitas ni las parafrasees):
{dedup}

Dificultad exacta para las {n_new} preguntas nuevas en este orden: {diffs_txt} (1=basica/definicion, 2=aplicacion o comparacion tecnica, 3=calculo numerico o caso practico avanzado con datos concretos y una unica respuesta numerica calculable).

Cada pregunta debe tener 4 opciones de respuesta (una sola correcta) y DOS campos de texto:
- "explanation": nota de estudio detallada (3 a 5 frases) explicando por que la opcion correcta es correcta citando el criterio tecnico exacto, por que al menos una opcion incorrecta es una confusion tipica, y si hay calculo el desarrollo numerico paso a paso.
- "source": la referencia exacta de donde proviene la respuesta. Si es del libro Creus, escribe "Creus, Instrumentacion Industrial, 8a ed., cap. X" (numero de capitulo real). Si es del PDF de ajuste y calibracion, escribe "Instrumentos industriales: su ajuste y calibracion, cap. X". Si es de una pagina web, escribe exactamente "instrumentacionycontrol.net" o "instrumentationtools.com".

Responde UNICAMENTE con un array JSON valido, sin texto adicional, sin markdown, sin bloques de codigo, con este formato exacto por pregunta:
{{"q": "texto de la pregunta", "options": ["opcion A", "opcion B", "opcion C", "opcion D"], "correct": <indice 0-3 de la opcion correcta>, "explanation": "nota de estudio detallada", "source": "referencia de la fuente", "difficulty": <1|2|3>, "module": {mod_num}}}

El array debe tener exactamente {n_new} elementos, en el orden de dificultad indicado."""
    out = os.path.join(ROOT, f"_newprompt_m{mod_num:02d}.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write(prompt)
    print(out)

if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]))
