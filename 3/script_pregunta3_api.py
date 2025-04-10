"""
    Flujo básico para consumir una API desde una fuente de datos abierta: 
        https://api.datos.gob.mx/v1/gobmx.facts

1.- Muestra cómo realizarías un requests a ese endpoint en python, 
2.- Manipula la respuesta y 
3.- Resume la información: cuenta cuántos registros tiene, filtra por alguna categoría, entre otros

"""

import requests

# Nueva URL del endpoint
url = "https://api.datos.gob.mx/v1/gobmx.facts"

# Realizando el request GET
response = requests.get(url)

# Verificando el estado de la respuesta
if response.status_code == 200:
    data = response.json()  # Parsear la respuesta JSON
    print("Datos obtenidos correctamente")
else:
    print(f"Error al obtener datos: {response.status_code}")

# Manipulando la respuesta
if response.status_code == 200:
    data = response.json()

    # Mostrar la respuesta completa (solo para ver qué contiene)
    print("Respuesta completa:")
    print(data)
else:
    print(f"Error al obtener datos: {response.status_code}")

# Resumiendo la información obtenida
if response.status_code == 200:
    data = response.json()

    # Accediendo a la lista de hechos (suponiendo que esté bajo 'data')
    facts = data.get('data', [])

    # Contando el número de hechos
    total_facts = len(facts)
    print(f"Total de hechos encontrados: {total_facts}")

    # Mostrar los primeros 5 hechos como ejemplo
    for i, fact in enumerate(facts[:5]):
        print(f"{i + 1}. Hecho: {fact['fact']}")
        print(f"   Fuente: {fact['source']}\n")
else:
    print(f"Error al obtener datos: {response.status_code}")


"""

instalación 
    pip install requests

"""