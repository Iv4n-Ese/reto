"""

script para obtener 
1.- Cien (100) juicios de tipo "civil", 
2.- Cuyo estado sea activo (True), 
3.- Y que tengan al menos un documento con el tipo "sentencia" emitido después del 01-01-2022.

Consideraciones:
a)Si el servidor de ElasticSearch está protegido por autenticación (como usuario y contraseña), agregar esos detalles en la conexión.
b)Asegúrate de que los datos en el índice juicios estén correctamente formateados y que los tipos de campo sean consistentes, especialmente con las fechas y los valores booleanos.
c)La consulta está limitada a 100 documentos con el parámetro size: 100. Si necesitas más documentos, puedes ajustar este número.

"""

from elasticsearch import Elasticsearch
from datetime import datetime

# Crear una instancia de conexión con ElasticSearch
es = Elasticsearch("http://38.348.39.19:9200")

# Definir el query
query = {
    "size": 100,  # Limitar la consulta a 100 juicios
    "query": {
        "bool": {
            "must": [
                {
                    "term": {
                        "tipo": "civil"  # Filtrar por tipo "civil"
                    }
                },
                {
                    "term": {
                        "estado": True  # Filtrar por estado activo (True)
                    }
                },
                {
                    "nested": {
                        "path": "documentos",  # Filtrar dentro del array "documentos"
                        "query": {
                            "bool": {
                                "must": [
                                    {
                                        "term": {
                                            "documentos.tipo_documento": "sentencia"  # Filtrar por tipo "sentencia"
                                        }
                                    },
                                    {
                                        "range": {
                                            "documentos.fecha": {
                                                "gte": "2022-01-01"  # Fecha después de 01-01-2022
                                            }
                                        }
                                    }
                                ]
                            }
                        }
                    }
                }
            ]
        }
    }
}

# Realizar la búsqueda en ElasticSearch
response = es.search(index="juicios", body=query)

# Procesar la respuesta y mostrar los juicios encontrados
juicios = response['hits']['hits']

# Mostrar información de los juicios encontrados
for juicio in juicios:
    print(f"ID Juicio: {juicio['_source']['id_juicio']}")
    print(f"Tipo: {juicio['_source']['tipo']}")
    print(f"Estado: {'Activo' if juicio['_source']['estado'] else 'Inactivo'}")
    print(f"Fecha de Inicio: {juicio['_source']['fecha_inicio']}")
    print("Documentos:")
    for doc in juicio['_source']['documentos']:
        print(f" - Tipo: {doc['tipo_documento']}, Fecha: {doc['fecha']}, URL: {doc['url']}")
    print("-" * 50)


"""

instalación
    pip install elasticsearch

"""