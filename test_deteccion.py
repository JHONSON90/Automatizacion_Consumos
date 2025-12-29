"""
Script de prueba para verificar la detección de nombres de archivo
"""

# Simulación de cómo funciona el watcher
from pathlib import Path

PALABRAS_CLAVE = [
    "consumo de pacientes",     # Con "de" en el medio
    "consumos de pacientes",    # Con "de" en el medio
    "consumo pacientes",        # Sin "de" (más común)
    "consumos pacientes",       # Sin "de" (más común)
]

# Archivos de prueba
archivos_prueba = [
    "CONSUMO PACIENTES.xlsx",
    "CONSUMOS PACIENTES.xlsx",
    "consumo de pacientes.xlsx",
    "Consumo Pacientes Noviembre.xlsx",
    "GASTOS NOVIEMBRE.xlsx",
    "SEGUIMIENTO DE HEMOCOMPONENTES 2025.xls",
]

print("=" * 70)
print("PRUEBA DE DETECCIÓN DE ARCHIVOS")
print("=" * 70)

for archivo in archivos_prueba:
    ruta = Path(archivo)
    nombre = ruta.stem.lower()  # Nombre SIN extensión, en minúsculas
    
    detectado = any(palabra in nombre for palabra in PALABRAS_CLAVE)
    
    estado = "✓ VÁLIDO" if detectado else "✗ IGNORADO"
    print(f"\n{estado:12} | {archivo}")
    print(f"             | Stem: '{nombre}'")
    
    if detectado:
        # Mostrar cuál palabra clave coincidió
        for palabra in PALABRAS_CLAVE:
            if palabra in nombre:
                print(f"             | Coincide con: '{palabra}'")
                break

print("\n" + "=" * 70)
