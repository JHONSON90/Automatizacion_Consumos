import pandas as pd

df_noviembre = pd.read_excel('CONSUMO PACIENTES DEL MES DE NOVIEMBRE DE 2025.xlsx', sheet_name="Sheet1")
df_diciembre = pd.read_excel('CONSUMO PACIENTES DEL MES DE DICIEMBRE DE 2025.xlsx', sheet_name="Sheet1")
df_enero = pd.read_excel('CONSUMO PACIENTES DEL MES DE ENERO DE 2026.xlsx', sheet_name="Sheet1")
df_febrero = pd.read_excel('CONSUMO PACIENTES DEL MES DE FEBRERO DE 2026.xlsx', sheet_name="Sheet1")
df_marzo = pd.read_excel('CONSUMO PACIENTES DEL MES DE MARZO DE 2026.xlsx', sheet_name="Sheet1")

#['TipMovFiltro', 'FechaDesde', 'FechaHasta', 'Mes', 'fecha', 'TipDoc4',
    #    'DescTipDoc', 'NroMov', 'SecMov', 'BodegaMov', 'BOD4', 'NombreBod',
    #    'CentroMov', 'cc_Nombre', 'ScentroMov', 'scc_Nombre', 'MedicoCod',
    #    'MedicoNom', 'EspeCod', 'EspeNom', 'COD13', 'Unnamed: 21', 'Ref',
    #    'Producto', 'LinInv', 'Linea', 'GruInv', 'Grupo', 'CtaInv', 'CtaCruce',
    #    'dCantidad', 'dValor', 'costo promedio', 'Veces', 'origenMed',
    #    'IdPaciente', 'NomPaciente'],

df_noviembre["VUnit"] = df_noviembre['dValor'] / df_noviembre['dCantidad']
df_diciembre["VUnit"] = df_diciembre['dValor'] / df_diciembre['dCantidad']
df_enero["VUnit"] = df_enero['dValor'] / df_enero['dCantidad']
df_febrero["VUnit"] = df_febrero['dValor'] / df_febrero['dCantidad']
df_marzo["VUnit"] = df_marzo['dValor'] / df_marzo['dCantidad']

td_noviembre = df_noviembre.groupby('COD13')['VUnit'].mean().reset_index()
td_diciembre = df_diciembre.groupby('COD13')['VUnit'].mean().reset_index()
td_enero = df_enero.groupby('COD13')['VUnit'].mean().reset_index()
td_febrero = df_febrero.groupby('COD13')['VUnit'].mean().reset_index()
td_marzo = df_marzo.groupby('COD13')['VUnit'].mean().reset_index()

lista_reportes = [td_noviembre, td_diciembre, td_enero, td_febrero, td_marzo]

df_consolidado = pd.concat(lista_reportes, ignore_index=True)

df_consolidado = df_consolidado.groupby('COD13')['VUnit'].mean().reset_index()
df_consolidado.to_excel("para_unitarios.xlsx")
print("Hecho!!!")