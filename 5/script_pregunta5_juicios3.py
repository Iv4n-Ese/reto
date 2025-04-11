"""

    Script para obtener obtener juicios de tipo civil
1.- Cien (100) juicios de tipo "civil", 
2.- Cuyo estado sea activo (True), 
3.- Y que tengan al menos un documento con el tipo "sentencia" emitido después del 01-01-2022.

Consideraciones:
a)Si el servidor de ElasticSearch está protegido por autenticación (como usuario y contraseña), agregar esos detalles en la conexión.
b)Asegúrate de que los datos en el índice juicios estén correctamente formateados y que los tipos de campo sean consistentes, especialmente con las fechas y los valores booleanos.
c)La consulta está limitada a 100 documentos con el parámetro size: 100. Si necesitas más documentos, puedes ajustar este número.

nota: Se ejecuto en local para hacer pruebas Elasticsearch la version 8 el cual ya necesita 
      usuario:elastic y contraseña: x32FoM8cwAevQt_=FXFW (para este ejemplo fue generada), 
      Para producción cambiar por http://38.348.39.19:9200 donde aplique
      reseteo de contraseña: elasticsearch-reset-password.bat -u elastic

"""

from elasticsearch import Elasticsearch
from datetime import datetime
import json
import csv

# ---------------------------------------------
# Conectar a Elasticsearch local
# ---------------------------------------------

es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic", "x32FoM8cwAevQt_=FXFW")
)

# ---------------------------------------------
# Crear el índice 'juicios' con su mapping
# ---------------------------------------------
if es.indices.exists(index="juicios"):
    es.indices.delete(index="juicios")

mapping = {
    "mappings": {
        "properties": {
            "id_juicio": {"type": "keyword"},
            "tipo": {"type": "keyword"},
            "estado": {"type": "boolean"},
            "fecha_inicio": {"type": "date"},
            "documentos": {
                "type": "nested",
                "properties": {
                    "tipo_documento": {"type": "keyword"},
                    "fecha": {"type": "date"},
                    "url": {"type": "keyword"}
                }
            }
        }
    }
}

es.indices.create(index="juicios", body=mapping)
print("✅ Índice 'juicios' creado.")

# ---------------------------------------------
# Insertar documentos de prueba
# ---------------------------------------------
docs = [
    {
        "id_juicio": "J001",
        "tipo": "civil",
        "estado": True,
        "fecha_inicio": "2023-03-15",
        "documentos": [
            {
                "tipo_documento": "sentencia",
                "fecha": "2023-07-10",
                "url": "http://localhost:9200/docs/J001-sentencia.pdf"
            },
            {
                "tipo_documento": "demanda",
                "fecha": "2023-03-10",
                "url": "http://localhost:9200/docs/J001-demanda.pdf"
            }
        ]
    },
    {
        "id_juicio": "J002",
        "tipo": "civil",
        "estado": True,
        "fecha_inicio": "2022-08-22",
        "documentos": [
            {
                "tipo_documento": "sentencia",
                "fecha": "2022-09-01",
                "url": "http://localhost:9200/docs/J002-sentencia.pdf"
            }
        ]
    },
    {
        "id_juicio": "J003",
        "tipo": "penal",
        "estado": True,
        "fecha_inicio": "2024-01-05",
        "documentos": [
            {
                "tipo_documento": "sentencia",
                "fecha": "2024-02-15",
                "url": "http://localhost:9200/docs/J003-sentencia.pdf"
            }
        ]
    }
]

for i, doc in enumerate(docs):
    es.index(index="juicios", id=i+1, document=doc)

print("✅ Documentos de prueba insertados.")

# ---------------------------------------------
# Ejecutar la consulta con filtro nested
# ---------------------------------------------
query = {
    "size": 100,
    "query": {
        "bool": {
            "must": [
                {"term": {"tipo": "civil"}},
                {"term": {"estado": True}},
                {
                    "nested": {
                        "path": "documentos",
                        "query": {
                            "bool": {
                                "must": [
                                    {"term": {"documentos.tipo_documento": "sentencia"}},
                                    {"range": {"documentos.fecha": {"gte": "2022-01-01"}}}
                                ]
                            }
                        }
                    }
                }
            ]
        }
    }
}

response = es.search(index="juicios", body=query)
juicios = response['hits']['hits']

# ---------------------------------------------
# Procesar y mostrar resultados filtrados
# ---------------------------------------------
print("\n📄 Resultados encontrados:")
resultados = []

for juicio in juicios:
    datos = juicio["_source"]
    documentos_filtrados = [
        doc for doc in datos["documentos"]
        if doc["tipo_documento"] == "sentencia" and doc["fecha"] >= "2022-01-01"
    ]

    if documentos_filtrados:
        print(f"\nID Juicio: {datos['id_juicio']}")
        print(f"Tipo: {datos['tipo']}")
        print(f"Estado: {'Activo' if datos['estado'] else 'Inactivo'}")
        print(f"Fecha de Inicio: {datos['fecha_inicio']}")
        print("Documentos (sentencia desde 2022-01-01):")
        for doc in documentos_filtrados:
            print(f" - Tipo: {doc['tipo_documento']}, Fecha: {doc['fecha']}, URL: {doc['url']}")

            # Agregar al resultado para exportar
            resultados.append({
                "id_juicio": datos["id_juicio"],
                "tipo": datos["tipo"],
                "estado": datos["estado"],
                "fecha_inicio": datos["fecha_inicio"],
                "tipo_documento": doc["tipo_documento"],
                "fecha_documento": doc["fecha"],
                "url": doc["url"]
            })

        print("-" * 50)

# ---------------------------------------------
# Exportar a CSV y JSON
# ---------------------------------------------
# Exportar CSV
with open("juicios_filtrados.csv", mode="w", newline="", encoding="utf-8") as file:
    fieldnames = ["id_juicio", "tipo", "estado", "fecha_inicio", "tipo_documento", "fecha_documento", "url"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(resultados)

# Exportar JSON
with open("juicios_filtrados.json", mode="w", encoding="utf-8") as file:
    json.dump(resultados, file, indent=4, ensure_ascii=False)

print("\n📁 Resultados exportados a 'juicios_filtrados.csv' y 'juicios_filtrados.json'")


"""

instalación
    pip install elasticsearch

"""