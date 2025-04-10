"""
    Manejo de datos
                
   Expedientes Terminados del Tribunal Federal de Conciliación y Arbitraje          
Contiene el número de expedientes terminados por año y el motivo (causal) por el cual se ostentaron los conflictos laborales individuales o colectivos que se suscitan entre las dependencias de la Administración Pública Federal, del Gobierno del Distrito Federal, sus trabajadores y sus organizaciones sindicales.            
http://desc.scjn.gob.mx/exportacion/desca?field_demandante_quejoso=All&field_estado_miembro_target_id=All&field_reparaciones_de_garantias=All&field_reparaciones_de_indemnizacion=All&field_reparaciones_de_rehabilitacion=All&field_reparaciones_de_restitucion=All&field_reparaciones_de_satisfaccion=All&field_sentido_de_la_resolucion=All&field_tipo_de_via_judicial=All&page&_format=csv
    
    archivo de prueba: "terminados.csv"
• Leer y explorar el dataset (dimensiones, tipos de variables, valores faltantes).
• Limpiar la información (quitar duplicados, manejar valores nulos).
• Mostrar estadísticas descriptivas (media, mediana, percentiles, etc.).
• Crea un histograma y un boxplot para visualizar la distribución de una o dos
variables


"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Leer el dataset desde un archivo CSV
# Asegúrate de que el archivo 'terminados.csv' esté en la misma carpeta que tu script, o proporciona la ruta completa.
df = pd.read_csv('terminados.csv')

# 2. Exploración inicial
# Mostrar dimensiones (número de filas y columnas)
print(f'Dimensiones del dataset: {df.shape}')

# Mostrar los primeros 5 registros
print('\nPrimeros 5 registros del dataset:')
print(df.head())

# Mostrar tipos de variables
print('\nTipos de variables:')
print(df.dtypes)

# Verificar valores faltantes por columna
print('\nValores faltantes por columna:')
print(df.isnull().sum())

# 3. Limpiar los datos
# Eliminar duplicados (aunque en este dataset no parece haber duplicados)
df_cleaned = df.drop_duplicates()

# Manejar valores nulos (rellenamos con la mediana por cada columna)
df_cleaned = df_cleaned.fillna(df_cleaned.median())

# Confirmar que no hay valores nulos
print('\nValores faltantes después de limpieza:')
print(df_cleaned.isnull().sum())

# 4. Estadísticas descriptivas
# Mostrar estadísticas descriptivas
print('\nEstadísticas descriptivas:')
print(df_cleaned.describe())

# 5. Visualización
# Histograma para la columna '2014' (puedes elegir otro año si lo prefieres)
plt.figure(figsize=(10, 6))
sns.histplot(df_cleaned['2014'], kde=True)
plt.title('Distribución de Expedientes Terminados en 2014')
plt.xlabel('Cantidad de expedientes')
plt.ylabel('Frecuencia')
plt.show()

# Boxplot para la columna '2014'
plt.figure(figsize=(10, 6))
sns.boxplot(x=df_cleaned['2014'])
plt.title('Boxplot de Expedientes Terminados en 2014')
plt.xlabel('Cantidad de expedientes')
plt.show()


"""

instalación necesaria
    pip install pandas numpy matplotlib seaborn

"""