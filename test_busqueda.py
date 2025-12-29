"""
Script de prueba para verificar la búsqueda de archivos InformeConsumos
"""
from utils import buscar_archivo_informe_consumos, mes_a_abreviatura

print("=" * 60)
print("PRUEBA DE BÚSQUEDA DE ARCHIVOS INFORMECONSUMOS")
print("=" * 60)

# Probar conversión de meses a abreviaturas
print("\n1. Prueba de conversión de meses a abreviaturas:")
print("-" * 60)
meses_prueba = ["NOVIEMBRE", "SEPTIEMBRE", "ENERO", "DICIEMBRE"]
for mes in meses_prueba:
    abrev = mes_a_abreviatura(mes)
    print(f"   {mes:12} → {abrev}")

# Probar búsqueda de archivos
print("\n2. Prueba de búsqueda de archivos:")
print("-" * 60)
mes_test = "SEPTIEMBRE"
print(f"   Buscando archivo para: {mes_test}")
print(f"   Patrón esperado: *-InformeConsumos-SEP2025.xlsx")

try:
    archivo = buscar_archivo_informe_consumos(mes_test)
    print(f"   ✓ ÉXITO: {archivo}")
except FileNotFoundError as e:
    print(f"   ✗ No encontrado (esto es normal si no tienes el archivo)")
    print(f"   {e}")

print("\n" + "=" * 60)
