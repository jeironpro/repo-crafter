# repo-crafter

## Descripción
Este proyecto forma parte de mi portafolio personal.  
El objetivo es demostrar buenas prácticas de programación, organización y documentación en GitHub.  
El proyecto se mejoró visualmente usando el modelo de OpenCode.

## Características
- **Gestión de repositorios**: crear, clonar todos, renombrar y eliminar repos directamente desde la interfaz.
- **Visibilidad y despliegue**: alterna público/privado y activa/desactiva GitHub Pages por repo.
- **Topics**: añade y quita topics de cada repo con validación.
- **Explorador de archivos**: navega carpetas y archivos de cada repo (vía API de GitHub) y visualiza archivos de texto plano en un visor integrado.
- **Resumen descargable**: genera un resumen clasificado (desplegados / públicos / privados) en **PDF** o **DOCX editable**.
- **Búsqueda y paginación**: filtro instantáneo por nombre, visibilidad, página y topic; paginación client-side. El estado (filtros, página, explorador) se mantiene en la URL.

## Uso
Para utilizar esta aplicación, sigue estos pasos:

### 1. Crea y configura un entorno virtual python:
    1. Crea el entorno:
        - python -m venv .venv

    2. Activa el entorno:
        - source .venv/bin/activate

    3. Instala las dependencias:
        - pip install -r requirements.txt

> **Nota:** la generación del PDF usa WeasyPrint, que requiere librerías del sistema.
> En Debian/Ubuntu: `sudo apt install libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf-2.0-0`

### 2. Crea un token clásico en GitHub:
    1. Accede a tu cuenta de GitHub y ve a
    **Settings → Developer settings → Personal access tokens → Tokens (classic)**

    2. Haz clic en **“Generate new token (classic)”**.

    3. Selecciona los permisos necesarios:
        - `repo`  
        - `delete_repo`

    4. Copia el token generado y guárdalo en un lugar seguro.

### 3. Crea un archivo .env 
    1. En la raíz del proyecto, crea un archivo llamado `.env` y añade las siguientes variables de entorno:
        - GITHUB_TOKEN=tu_token_aqui
        - GITHUB_USER=tu_usuario_de_github
        - GITHUB_EMAIL=tu_email_de_github

### 4. Ejecuta la aplicación:
    1. Desde la raíz del proyecto:
        - python app.py

    2. Para modo debug:
        - FLASK_DEBUG=1 python app.py

## Tests
    - python -m pytest tests -q

## Licencia
Este proyecto está bajo la licencia **MIT**.  
Consulta el archivo [LICENSE](LICENSE) para más detalles.
