# repo-crafter

## 📌 Descripción
Este proyecto forma parte de mi portafolio personal.  
El objetivo es demostrar buenas prácticas de programación, organización y documentación en GitHub.

## 🧰 Uso
Para utilizar esta aplicación, sigue estos pasos:

### 1. Crea y configura un entorno virtual python:
    1. Crea el entorno:
        - python -m venv .venv

    2. Activa el entorno:
        - source .venv/bin/activate

    3. Instala las dependencias:
        - pip install -r requirements.txt

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

## 📜 Licencia
Este proyecto está bajo la licencia **MIT**.  
Consulta el archivo [LICENSE](LICENSE) para más detalles.