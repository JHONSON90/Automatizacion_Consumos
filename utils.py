"""
Utilidades para el sistema de monitoreo de consumos de pacientes
"""
import re
from pathlib import Path
from datetime import datetime
import os

# Mapeo de nombres de meses a números
MESES = {
    'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
    'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
    'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
}

# Mapeo de meses a abreviaturas de 3 letras
MESES_ABREV = {
    'ENERO': 'ENE', 'FEBRERO': 'FEB', 'MARZO': 'MAR', 'ABRIL': 'ABR',
    'MAYO': 'MAY', 'JUNIO': 'JUN', 'JULIO': 'JUL', 'AGOSTO': 'AGO',
    'SEPTIEMBRE': 'SEP', 'OCTUBRE': 'OCT', 'NOVIEMBRE': 'NOV', 'DICIEMBRE': 'DIC'
}


def mes_a_abreviatura(mes_completo: str) -> str:
    """
    Convierte el nombre completo del mes a su abreviatura de 3 letras.
    
    Args:
        mes_completo: Nombre del mes (ej: "NOVIEMBRE", "noviembre")
        
    Returns:
        Abreviatura del mes (ej: "NOV")
    """
    mes_upper = mes_completo.upper()
    return MESES_ABREV.get(mes_upper, mes_upper[:3])


def buscar_archivo_informe_consumos(mes: str, anio: str) -> Path:
    """
    Busca el archivo de ENTRADAS (InformeConsumos) correspondiente al mes en Descargas.
    
    IMPORTANTE: Este NO es el archivo de "consumos de pacientes" que detecta el watchdog.
    Este es el archivo de ENTRADAS que necesita el script_3 para cruzar datos.
    
    Patrón del archivo: XXXXXXX-InformeConsumos-MMMYYYY.xlsx
    Ejemplo: 901S055-InformeConsumos-NOV2025.xlsx
    
    Args:
        mes: Nombre del mes completo (ej: "NOVIEMBRE")
        anio: Año del informe (ej: "2025", "2026")
        
    Returns:
        Path al archivo de ENTRADAS encontrado
        
    Raises:
        FileNotFoundError: Si no se encuentra el archivo
    """
    # Convertir mes a abreviatura
    mes_abrev = mes_a_abreviatura(mes)
    
    # Rutas donde buscar (en orden de prioridad)
    rutas_busqueda = [
        Path.home() / "Downloads",  # C:\Users\COSTOS\Downloads
        Path.home() / "Descargas",  # Por si está en español
        Path("."),  # Carpeta actual del proyecto
    ]
    
    # Patrón del archivo: cualquier cosa-InformeConsumos-MMMYYYY.xlsx
    patron = f"*-InformeConsumos{mes_abrev}{anio}.xlsx"
    
    for ruta in rutas_busqueda:
        if not ruta.exists():
            continue
            
        # Buscar archivos que coincidan con el patrón
        archivos = list(ruta.glob(patron))
        
        if archivos:
            # Retornar el primer archivo encontrado
            archivo = archivos[0]
            print(f"[OK] Archivo ENTRADAS (InformeConsumos) encontrado: {archivo.name}")
            return archivo
    
    # Si no se encuentra, mostrar mensaje de error claro
    raise FileNotFoundError(
        f"No se encontró el archivo de ENTRADAS (InformeConsumos) para {mes} {anio}.\n"
        f"Patrón buscado: {patron}\n"
        f"Rutas revisadas: {', '.join(str(r) for r in rutas_busqueda if r.exists())}\n"
        f"Este archivo debe estar en Descargas antes de procesar."
    )


def extraer_mes_de_ruta(ruta_archivo: str) -> str:
    """
    Extrae el mes de la ruta del archivo analizando la estructura de carpetas.
    
    Busca patrones como:
    - "11-NOVIEMBRE"
    - "12-DICIEMBRE"
    
    Args:
        ruta_archivo: Ruta completa del archivo
        
    Returns:
        Nombre del mes en español (ej: "NOVIEMBRE")
    """
    ruta = Path(ruta_archivo)
    
    # Buscar en las partes de la ruta
    for parte in ruta.parts:
        # Patrón: XX-NOMBRE_MES
        match = re.match(r'(\d{1,2})-([A-Z]+)', parte.upper())
        if match:
            numero_mes, nombre_mes = match.groups()
            return nombre_mes
    
    # Si no se encuentra, intentar con la fecha de modificación
    fecha_mod = datetime.fromtimestamp(ruta.stat().st_mtime)
    meses_lista = list(MESES.keys())
    return meses_lista[fecha_mod.month - 1].upper()


def extraer_anio_de_ruta(ruta_archivo: str) -> str:
    """
    Extrae el año de la ruta del archivo analizando la estructura de carpetas.
    
    Busca patrones como:
    - "COSTOS 2025"
    - "COSTOS 2026"
    
    Args:
        ruta_archivo: Ruta completa del archivo
        
    Returns:
        Año como string (ej: "2025")
    """
    ruta = Path(ruta_archivo)
    
    # Buscar en las partes de la ruta
    for parte in ruta.parts:
        # Patrón: COSTOS XXXX
        match = re.search(r'COSTOS\s+(\d{4})', parte.upper())
        if match:
            return match.group(1)
            
    # Si no se encuentra, intentar con la fecha de modificación o año actual
    try:
        return str(datetime.fromtimestamp(ruta.stat().st_mtime).year)
    except:
        return str(datetime.now().year)


def extraer_mes_de_nombre_archivo(nombre_archivo: str) -> str:
    """
    Intenta extraer el mes del nombre del archivo.
    
    Args:
        nombre_archivo: Nombre del archivo
        
    Returns:
        Nombre del mes si se encuentra, None en caso contrario
    """
    nombre_archivo = nombre_archivo.lower()
    
    for mes in MESES.keys():
        if mes in nombre_archivo:
            return mes.upper()
    
    return None


def crear_carpetas_salida():
    """
    Crea las carpetas de salida necesarias si no existen
    """
    carpetas = [
        "Hallazgos",
        "Hallazgos/analisis_cantidades",
        "Hallazgos/variacion_costo",
        "Arreglados",
        "informes de consumo"
    ]
    
    for carpeta in carpetas:
        Path(carpeta).mkdir(parents=True, exist_ok=True)
