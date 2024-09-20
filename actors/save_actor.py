import csv
import pykka

class SaveActor(pykka.ThreadingActor):

    def on_receive(self, message):
        flights = message.get('flights')
        
        # Guardar en archivo de texto
        self.save_to_text(flights)

        # Guardar en archivo CSV
        self.save_to_csv(flights)

        print("Resultados guardados correctamente en archivos de texto y CSV.")

    def save_to_text(self, flights):
        with open('vuelos_ordenados.txt', 'w', encoding='utf-8') as file:
            file.write("Vuelos ordenados por precio (menor a mayor):\n")
            for flight in flights:
                file.write(f"{flight['airline']} - Precio: {flight['price']}, Hora de salida: {flight['departure_time']}, Hora de llegada: {flight['arrival_time']}\n")

    def save_to_csv(self, flights):
        with open('vuelos_ordenados.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['airline', 'price', 'departure_time', 'arrival_time'])
            writer.writeheader()
            writer.writerows(flights)
