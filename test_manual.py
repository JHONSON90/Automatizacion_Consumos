"""
Test manual para verificar la detección
"""
from pathlib import Path

PALABRAS_CLAVE = [
    "consumo de pacientes",     # Con "de" en el medio
    "consumos de pacientes",    # Con "de" en el medio
    "consumo pacientes",        # Sin "de" (más común)
    "consumos pacientes",       # Sin "de" (más común)
]

# Simular el archivo que estás pegando
archivo_test = "CONSUMO PACIENTES.xlsx"
ruta = Path(archivo_test)
nombre = ruta.stem.lower()

print("=" * 60)
print("TEST MANUAL DE DETECCIÓN")
print("=" * 60)
print(f"\nArchivo: {archivo_test}")
print(f"ruta.name: {ruta.name}")
print(f"ruta.stem: {ruta.stem}")
print(f"nombre (stem.lower()): '{nombre}'")
print("\nPalabras clave disponibles:")
for i, palabra in enumerate(PALABRAS_CLAVE, 1):
    print(f"  {i}. '{palabra}'")

print("\nComparaciones:")
for palabra in PALABRAS_CLAVE:
    coincide = palabra in nombre
    print(f"  '{palabra}' in '{nombre}' = {coincide}")
    
detectado = any(palabra in nombre for palabra in PALABRAS_CLAVE)

print("\n" + "=" * 60)
if detectado:
    print("RESULTADO: ✅ ARCHIVO VÁLIDO")
else:
    print("RESULTADO: ❌ ARCHIVO IGNORADO")
print("=" * 60)
