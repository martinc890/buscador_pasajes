from actors.search_actor import SearchActor
from actors.compare_actor import CompareActor
import pykka

if __name__ == "__main__":
    # Definir los detalles de búsqueda
    origin = "EZE"
    destination = "MIA"
    date = "2024-10-15"

    # Inicializar los actores
    search_actor_ref = SearchActor.start()
    compare_actor_ref = CompareActor.start()

    # Obtener los vuelos a través del SearchActor
    flights = search_actor_ref.ask({'origin': origin, 'destination': destination, 'date': date})

    # Enviar los vuelos al CompareActor para que los ordene
    sorted_flights = compare_actor_ref.ask({'flights': flights})

    # Imprimir los resultados ordenados
    print("Vuelos ordenados por precio (menor a mayor):")
    for flight in sorted_flights:
        print(f"{flight['airline']} - Precio: {flight['price']}, Hora de salida: {flight['departure_time']}, Hora de llegada: {flight['arrival_time']}")

    # Cerrar los actores después de usarlos
    search_actor_ref.stop()
    compare_actor_ref.stop()
