"""Extrae texto crudo de un rango de paginas de uno de los dos PDF fuente (indices 0-based, como los reporta el outline/bookmarks del PDF).

Uso: python _extract_pdf_text.py <creus|ajuste> <pagina_inicio> <pagina_fin_inclusive>

Nota: el texto extraido tiene corrupcion sistematica de codificacion en este PDF concreto:
las vocales acentuadas y la enye salen como el caracter de reemplazo, y silabas como "ti"
a veces desaparecen de ligaduras (ej. "instrumentacion" puede salir como "instrumentaci?n",
"continuidad" como "conduc vidad"). Hay que reconstruir la palabra correcta por contexto,
nunca copiar el texto crudo tal cual a una pregunta o explicacion.
"""
import sys, os

ROOT = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(ROOT)
FILES = {
    "creus": os.path.join(PARENT, "Instrumentacion_industrial_Creus_8th.pdf"),
    "ajuste": os.path.join(PARENT, "Instrumentos_industriales_su_ajuste_y_ca.pdf"),
}

def main(which, start, end):
    import fitz
    doc = fitz.open(FILES[which])
    for i in range(start, end + 1):
        if i < 0 or i >= len(doc):
            continue
        print(f"\n--- pagina {i} ---\n")
        print(doc[i].get_text())

if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
