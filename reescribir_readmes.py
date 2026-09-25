"""Genera los README profesionales de los repositorios del portafolio.

Cada README se construye a partir del contenido definido en
``contenido_readmes`` y se compone de:

- Titulo con el nombre del repositorio (``# nombre``).
- Introduccion y secciones (Caracteristicas, Tecnologias, Uso o
  Instalacion y uso, Estructura del proyecto, etc.).
- La seccion final de licencia (fija).

Reglas aplicadas por el generador:
- No se usan emojis en ningun caso (se valida al generar).
- No se incluye la antigua plantilla ("## Descripcion" del portafolio).
- El README termina siempre con la seccion de licencia indicada.

Uso:
    python reescribir_readmes.py [--raiz RUTA]

Por defecto trabaja sobre las copias locales en
~/Repositorios-copy (subcarpetas publico/ y privado/).
"""
import argparse
from pathlib import Path

from contenido_readmes import CONTENIDO

# Raiz con las copias locales de los repositorios (publico/ y privado/)
RAIZ_DEFECTO = Path.home() / "Repositorios-copy"

# Seccion de licencia fija que cierra todos los README. Los dos espacios tras
# "MIT." son el salto de linea Markdown y deben conservarse.
TEXTO_LICENCIA = (
    "## Licencia\n"
    "Este proyecto está bajo la licencia **MIT**.  \n"
    "Consulta el archivo [LICENSE](LICENSE) para más detalles."
)

# Rangos Unicode que cubren practicamente todos los emojis
_RANGOS_EMOJIS = [
    (0x1F000, 0x1FAFF),
    (0x2600, 0x27BF),
    (0x2B00, 0x2BFF),
    (0xFE00, 0xFE0F),
    (0x2190, 0x21FF),
]


def contiene_emojis(texto):
    """Devuelve True si el texto contiene caracteres del rango Unicode de emojis."""
    return any(
        inicio <= ord(punto) <= fin
        for punto in texto
        for inicio, fin in _RANGOS_EMOJIS
    )


def _bloques_de_entrada(nombre, entrada):
    """Convierte la entrada de CONTENIDO en una lista de bloques (encabezado, cuerpo)."""
    bloques = [(None, entrada[0])]
    bloques.extend(entrada[1:])
    return bloques


def generar_readme(nombre, entrada):
    """Genera el contenido del nuevo README a partir de su contenido estructurado."""
    partes = [f"# {nombre}", ""]

    for encabezado, cuerpo in _bloques_de_entrada(nombre, entrada):
        if contiene_emojis(cuerpo):
            raise ValueError(f"La entrada de '{nombre}' contiene emojis.")
        if encabezado:
            partes.append(f"## {encabezado}")
            partes.append("")
        partes.append(cuerpo.strip())
        partes.append("")

    partes.append(TEXTO_LICENCIA)
    partes.append("")
    return "\n".join(partes)


def reescribir_readme(ruta_readme, nombre, entrada):
    """Escribe el nuevo README en ruta_readme. Devuelve el contenido escrito."""
    contenido = generar_readme(nombre, entrada)
    ruta_readme.write_text(contenido, encoding="utf-8")
    return contenido


def main():
    analizador = argparse.ArgumentParser(
        description="Genera README profesionales (sin emojis, con secciones y licencia final)."
    )
    analizador.add_argument(
        "--raiz",
        default=str(RAIZ_DEFECTO),
        help=f"Raiz con las copias locales de los repositorios (por defecto '{RAIZ_DEFECTO}').",
    )
    argumentos = analizador.parse_args()

    raiz = Path(argumentos.raiz)
    if not raiz.is_dir():
        print(f"Error: no existe el directorio '{raiz}'.")
        return

    generados = 0
    for ruta_relativa, entrada in CONTENIDO.items():
        ruta_readme = raiz / ruta_relativa / "README.md"
        if not ruta_readme.is_file():
            print(f"AVISO: no se encontro README.md en '{ruta_relativa}'. Se omite.")
            continue

        nombre = Path(ruta_relativa).name
        try:
            reescribir_readme(ruta_readme, nombre, entrada)
        except ValueError as error:
            print(f"ERROR: {error}. Se omite '{ruta_relativa}'.")
            continue

        generados += 1
        print(f"- {ruta_relativa}")

    print(f"\nSe generaron {generados} README(s).")


if __name__ == "__main__":
    main()
