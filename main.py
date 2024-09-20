from actors.search_actor import SearchActor
from actors.compare_actor import CompareActor
from actors.save_actor import SaveActor
import pykka

if __name__ == "_main_":
    # Definir los detalles de búsqueda
    origin = "EZE"
    destination = "MIA"
    date = "2024-10-15"

    # Inicializar los actores
    search_actor_ref = SearchActor.start()
    compare_actor_ref = CompareActor.start()
    save_actor_ref = SaveActor.start()

    # Obtener los vuelos a través del SearchActor
    flights = search_actor_ref.ask({'origin': origin, 'destination': destination, 'date': date})

    # Enviar los vuelos al CompareActor para que los ordene
    sorted_flights = compare_actor_ref.ask({'flights': flights})

    # Enviar los vuelos ordenados al SaveActor para que los guarde
    save_actor_ref.tell({'flights': sorted_flights})

    # Cerrar los actores después de usarlos
    search_actor_ref.stop()
    compare_actor_ref.stop()
    save_actor_ref.stop()