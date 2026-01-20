from invoke import task
from rich.console import Console
from pathlib import Path

console = Console()

@task
def procesar(ctx, archivo, mes, anio):
    console.rule(f"[bold blue]Inicio de Automatización - {mes} {anio}")
    
    # Crear archivo importacion.py dinámicamente
    ruta_importacion = Path("scripst/importacion.py")
    console.log(f"[cyan]Generando módulo de importación...[/]")
    
    codigo_importacion = f'''"""
Módulo generado automáticamente para importar datos del archivo detectado
"""
import pandas as pd

# Cargar el archivo detectado
RUTA_ARCHIVO = r"{archivo}"
data = pd.read_excel(RUTA_ARCHIVO)

print(f"[OK] Archivo cargado: {{RUTA_ARCHIVO}}")
print(f"[OK] Registros encontrados: {{len(data)}}")
'''
    
    ruta_importacion.write_text(codigo_importacion, encoding='utf-8')
    console.log(f"[green]✓ Módulo de importación creado[/]")
    
    try:
        console.log(f"[cyan]Ejecutando script 1: Análisis de hallazgos...[/]")
        ctx.run(f'python scripst/script_1.py "{mes}" "{anio}"')
        console.log(f"[green]✓ Script 1 completado[/]")

        console.log(f"[cyan]Ejecutando script 2: Corrección de datos...[/]")
        ctx.run(f'python scripst/script_2.py "{mes}" "{anio}"')
        console.log(f"[green]✓ Script 2 completado[/]")
        
        # Pausa para autorización del usuario
        console.rule("[bold yellow]⏸ Revisión de Datos")
        console.print("\n[bold cyan]📋 Archivos generados hasta ahora:[/]")
        console.print(f"   • Hallazgos/HALLAZGOS MES DE {mes} DE {anio}.xlsx")
        console.print(f"   • Hallazgos/analisis_cantidades/ANALISIS CANTIDADES MES DE {mes} DE {anio}.xlsx")
        console.print(f"   • Hallazgos/variacion_costo/ANALISIS COSTO UNITARIO {mes} DE {anio}.xlsx")
        console.print(f"   • Arreglados/CONSUMO PACIENTES DEL MES DE {mes} DE {anio}.xlsx")
        console.print("\n[bold yellow]⚠ Por favor, revise los archivos generados antes de continuar.[/]")
        console.print("[dim]El siguiente paso generará el informe final cruzando datos con ENTRADAS.[/]\n")
        
        respuesta = input("¿Desea continuar con el script 3 (Informe Final)? [S/n]: ").strip().lower()
        
        if respuesta in ['n', 'no']:
            console.print("\n[bold yellow]⊘ Proceso cancelado por el usuario.[/]")
            console.print("[dim]Los archivos generados se mantienen en sus carpetas.[/]")
            return
        
        console.rule("[bold blue]Continuando con Informe Final")
        console.log(f"[cyan]Generando informe final...[/]")
        ctx.run(f'python scripst/script_3.py "{mes}" "{anio}"')
        console.log(f"[green]✓ Informe generado[/]")
        
        console.rule("[bold green]✓ Proceso Finalizado Correctamente")
        
    except Exception as e:
        console.log(f"[bold red]✗ Error en el procesamiento:[/] {e}")
        raise
    finally:
        # Limpiar el archivo temporal
        if ruta_importacion.exists():
            ruta_importacion.unlink()
            console.log(f"[dim]Módulo de importación eliminado[/]")