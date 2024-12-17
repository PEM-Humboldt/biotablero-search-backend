import subprocess


def run_aerich_init():
    try:
        subprocess.check_call(
            ["aerich", "init", "-t", "app.utils.config.TORTOISE_ORM"]
        )
        subprocess.check_call(["aerich", "init-db"])
        return "Aerich inicializado y base de datos preparada correctamente."
    except subprocess.CalledProcessError as e:
        return f"Error al inicializar Aerich o preparar la base de datos: {e}"


def run_aerich_migrate():
    result = subprocess.run(
        ["aerich", "migrate"], capture_output=True, text=True
    )
    if result.returncode != 0:
        return f"Error al ejecutar migraciones: {result.stderr}"
    return f"Migraciones ejecutadas correctamente: {result.stderr}"


def run_aerich_upgrade():
    result = subprocess.run(
        ["aerich", "upgrade"], capture_output=True, text=True
    )
    if result.returncode != 0:
        return f"Error al ejecutar upgrade: {result.stderr}"
    return f"Upgrade ejecutado correctamente:{result.stderr}"
