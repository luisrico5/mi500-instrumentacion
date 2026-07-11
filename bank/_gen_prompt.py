"""Genera el prompt para pedir preguntas nuevas de un modulo via notebooklm ask."""
import json, sys, os

ROOT = os.path.dirname(os.path.abspath(__file__))

def main(mod_num, n_new=5):
    fname = os.path.join(ROOT, f"m{mod_num:02d}.json")
    with open(fname, encoding="utf-8") as f:
        data = json.load(f)
    existing = [q["q"] for q in data["questions"]]
    dedup = "\n".join(f"- {q}" for q in existing)
    prompt = f"""Eres un generador de banco de preguntas para un examen de posgrado en instrumentacion industrial (Maestria en Instrumentacion). Trabaja SOLO con el contenido de las fuentes de este cuaderno (Creus 8a ed., PDF de ajuste y calibracion, instrumentacionycontrol.net, instrumentationtools.com).

Modulo: "{data['name']}" (modulo numero {mod_num} de 10).

Genera EXACTAMENTE {n_new} preguntas de opcion multiple NUEVAS y distintas (no repitas, no parafrasees) de las que ya existen en este modulo, listadas abajo. Deben cubrir subtemas o angulos que las preguntas existentes no cubren.

Preguntas ya existentes en este modulo (NO las repitas ni las parafrasees):
{dedup}

Distribucion de dificultad exacta para las {n_new} preguntas nuevas: 2 de dificultad 1 (conceptos basicos/definiciones), 2 de dificultad 2 (aplicacion o comparacion tecnica), 1 de dificultad 3 (calculo numerico o caso practico avanzado, con datos concretos y una unica respuesta numerica correcta calculable).

Cada pregunta debe tener 4 opciones de respuesta, una sola correcta, y una explicacion breve (1-2 frases) que justifique la respuesta correcta citando el criterio tecnico de la fuente.

Responde UNICAMENTE con un array JSON valido, sin texto adicional, sin markdown, sin bloques de codigo, con este formato exacto por pregunta:
{{"q": "texto de la pregunta", "options": ["opcion A", "opcion B", "opcion C", "opcion D"], "correct": <indice 0-3 de la opcion correcta>, "explanation": "explicacion breve", "difficulty": <1|2|3>, "module": {mod_num}}}

El array debe tener exactamente {n_new} elementos, en el orden de dificultad indicado (1,1,2,2,3)."""
    out = os.path.join(ROOT, f"_prompt_m{mod_num:02d}.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write(prompt)
    print(out)

if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 5)
