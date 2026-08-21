import subprocess

from config import GITHUB_USER, GITHUB_EMAIL, CARPETA_REPOS, YEAR, README_TEMPLATE, LICENSE_TEMPLATE
from github_api import descargar_template, crear_repo_remoto, obtener_repos


def _git(carpeta, *argumentos, check=True):
    return subprocess.run(["git", "-C", str(carpeta), *argumentos], check=check)


def _git_con_usuario(carpeta, *argumentos):
    return _git(
        carpeta,
        "-c", f"user.name={GITHUB_USER}",
        "-c", f"user.email={GITHUB_EMAIL}",
        *argumentos,
        check=False,
    )


def crear_repo(nombre, visibilidad, gitignore):
    carpeta_repo = CARPETA_REPOS / ("privado" if visibilidad else "publico") / nombre

    if carpeta_repo.exists():
        return f"Error: La carpeta '{carpeta_repo}' ya existe localmente."

    carpeta_repo.mkdir(parents=True)

    (carpeta_repo / "README.md").write_text(
        README_TEMPLATE.format(project_name=nombre), encoding="utf-8"
    )
    (carpeta_repo / "LICENSE").write_text(
        LICENSE_TEMPLATE.format(year=YEAR, user=GITHUB_USER), encoding="utf-8"
    )

    if gitignore:
        contenido_gitignore = descargar_template(f"{gitignore}.gitignore")

        if contenido_gitignore:
            (carpeta_repo / ".gitignore").write_text(contenido_gitignore, encoding="utf-8")
        else:
            print(f"Aviso: No se pudo descargar el template '{gitignore}'. Se omitirá el .gitignore.")

    _git(carpeta_repo, "init")
    _git(carpeta_repo, "branch", "-M", "main")

    archivos = ["LICENSE", "README.md"]
    if gitignore and (carpeta_repo / ".gitignore").exists():
        archivos.append(".gitignore")

    _git(carpeta_repo, "add", *archivos)

    commit = _git_con_usuario(carpeta_repo, "commit", "-m", "Creando estructura inicial")
    if commit.returncode != 0:
        return f"Error: No se pudo crear el commit inicial en '{carpeta_repo}'."

    respuesta = crear_repo_remoto(nombre, visibilidad)

    if respuesta.status_code in [201, 422]:
        _git(carpeta_repo, "remote", "remove", "origin", check=False)
        _git(carpeta_repo, "remote", "add", "origin", f"git@github.com:{GITHUB_USER}/{nombre}.git")
        _git(carpeta_repo, "push", "-u", "origin", "main")
        return f"Repositorio '{nombre}' creado y subido correctamente."

    return f"Error creando repo en GitHub: {respuesta.status_code} {respuesta.text}"


def clonar_repo(nombre, visibilidad):
    carpeta_repo = CARPETA_REPOS / visibilidad / nombre
    url_clona = f"git@github.com:{GITHUB_USER}/{nombre}.git"

    try:
        subprocess.run(["git", "clone", url_clona, str(carpeta_repo)], check=True)
        return f"Repositorio '{nombre}' clonado en {carpeta_repo} correctamente."
    except subprocess.CalledProcessError:
        return f"Error al clonar '{nombre}'"


def clonar_todos():
    try:
        repos = obtener_repos()
    except RuntimeError as error:
        return str(error), "error"

    for repo in repos:
        nombre = repo["name"]
        carpeta_repo = CARPETA_REPOS / ("privado" if repo["private"] else "publico") / nombre

        if not carpeta_repo.exists():
            subprocess.run(["git", "clone", repo["ssh_url"], str(carpeta_repo)], check=True)

    return f"Todos los repositorios han sido clonados en {CARPETA_REPOS} correctamente", "success"


def estado_archivos(carpeta_repo):
    """Devuelve la lista de archivos con cambios pendientes según git status."""
    resultado = subprocess.run(
        ["git", "-C", str(carpeta_repo), "status", "--porcelain"],
        capture_output=True, text=True
    )

    archivos = []
    for linea in resultado.stdout.strip().split("\n"):
        if linea:
            estado = linea[:2].strip()
            archivo = linea[2:].strip()
            archivos.append({"estado": estado, "archivo": archivo})

    return archivos


def hacer_commit(carpeta_repo, archivos, mensaje):
    add = _git(carpeta_repo, "add", *archivos, check=False)
    if add.returncode != 0:
        return False

    commit = _git_con_usuario(carpeta_repo, "commit", "-m", mensaje)
    return commit.returncode == 0


def hacer_push(carpeta_repo):
    push = _git(carpeta_repo, "push", "origin", "main", check=False)
    return push.returncode == 0


def crear_tag(carpeta_repo, version, mensaje):
    tag = _git_con_usuario(carpeta_repo, "tag", "-a", version, "-m", mensaje)
    if tag.returncode != 0:
        return False

    push_tag = _git(carpeta_repo, "push", "origin", version, check=False)
    return push_tag.returncode == 0
