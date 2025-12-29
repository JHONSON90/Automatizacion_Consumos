from watcher import iniciar_monitoreo
from pathlib import Path
from datetime import datetime

def obtener_nombre_mes(n):
    meses = [
        "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
        "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"
    ]
    return meses[n-1]

def main():
    """Iniciar monitoreo de consumos de pacientes con rutas dinámicas"""
    ahora = datetime.now()
    anio = ahora.year
    mes_actual_num = ahora.month
    
    # Lista de meses a monitorear (actual y siguiente para prevenir traslapes)
    meses_info = []
    
    # Mes actual
    meses_info.append((anio, mes_actual_num))
    
    # Mes siguiente
    if mes_actual_num == 12:
        meses_info.append((anio + 1, 1))
    else:
        meses_info.append((anio, mes_actual_num + 1))

    rutas = []
    base_ruta = Path(r"\\192.168.3.70\Costos")
    
    for a, m in meses_info:
        nombre_mes = obtener_nombre_mes(m)
        ruta_mes = base_ruta / f"COSTOS {a}" / f"{m:02d}-{nombre_mes}"
        rutas.append(ruta_mes)

    print("="*60)
    print("🚀 SISTEMA DE MONITOREO AUTOMATIZADO")
    print(f"Fecha sistema: {ahora.strftime('%d/%m/%Y %H:%M')}")
    print("="*60)
    
    rutas_validas = []
    for r in rutas:
        if r.exists():
            rutas_validas.append(str(r))
            print(f"✅ Monitoreando: {r}")
        else:
            print(f"⚠️ Ruta no encontrada (se ignorará): {r}")

    if not rutas_validas:
        print("❌ ERROR: No se encontró ninguna de las rutas de red especificadas.")
        print("Verifique la conexión al servidor 192.168.3.70")
        return

    iniciar_monitoreo(rutas_validas)

if __name__ == "__main__":
    main()
