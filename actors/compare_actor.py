import pykka

class CompareActor(pykka.ThreadingActor):
    
    def on_receive(self, message):
        flights = message.get('flights')
        
        # Convertir precios a un formato numérico para ordenar
        for flight in flights:
            # Reemplazar punto por nada (para los miles) y coma por punto (para los decimales)
            price_cleaned = flight['price'].replace('.', '').replace(',', '.').replace('ARS', '').strip()
            flight['price'] = float(price_cleaned)
        
        # Ordenar los vuelos por precio (menor a mayor)
        flights_sorted = sorted(flights, key=lambda x: x['price'])
        
        # Imprimir los vuelos ordenados
        print("Vuelos ordenados por precio (menor a mayor):")
        for flight in flights_sorted:
            print(f"{flight['airline']} - Precio: {flight['price']}, Hora de salida: {flight['departure_time']}, Hora de llegada: {flight['arrival_time']}")
        
        return flights_sorted
