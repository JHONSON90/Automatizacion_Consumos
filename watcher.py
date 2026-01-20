import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rich.console import Console
from pathlib import Path
from utils import extraer_mes_de_ruta, extraer_mes_de_nombre_archivo, extraer_anio_de_ruta

console = Console()

PALABRAS_CLAVE = [
    "consumo de pacientes",     # Con "de" en el medio
    "consumos de pacientes",    # Con "de" en el medio
    "consumo pacientes",        # Sin "de" (más común)
    "consumos pacientes",       # Sin "de" (más común)
]

class ExcelHandler(FileSystemEventHandler):

    def on_created(self, event):
        if event.is_directory:
            return

        ruta = Path(event.src_path)

        if ruta.suffix.lower() not in [".xlsx", ".xls"]:
            return

        nombre = ruta.stem.lower()  # Nombre SIN extensión, en minúsculas
        
        console.log(f"[dim]Detectado archivo: {ruta.name} | Buscando en: '{nombre}'[/]")

        if any(palabra in nombre for palabra in PALABRAS_CLAVE):
            console.log(f"[bold green]✓ Archivo válido detectado:[/] {ruta.name}")
            
            # Intentar extraer el mes del nombre del archivo primero
            mes = extraer_mes_de_nombre_archivo(ruta.stem)
            
            # Si no se encuentra, extraer de la ruta
            if not mes:
                mes = extraer_mes_de_ruta(str(ruta))
            
            # Extraer año de la ruta
            anio = extraer_anio_de_ruta(str(ruta))
            
            console.log(f"[cyan]📅 Mes detectado:[/] {mes}")
            console.log(f"[cyan]📅 Año detectado:[/] {anio}")
            console.log(f"[cyan]📂 Ruta:[/] {ruta}")
            
            # Ejecutar el procesamiento con archivo, mes y año
            subprocess.run(
                ["invoke", "procesar", "--archivo", str(ruta), "--mes", mes, "--anio", anio],
                shell=True
            )

        else:
            console.log(f"[yellow]⊘ Archivo ignorado:[/] {ruta.name}")


def iniciar_monitoreo(rutas):
    observer = Observer()
    handler = ExcelHandler()

    for ruta in rutas:
        observer.schedule(handler, ruta, recursive=True)
        console.log(f"Monitoreando: {ruta}")

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()