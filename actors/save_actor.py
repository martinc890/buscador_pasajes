import os
import pykka

class SaveActor(pykka.ThreadingActor):
    def on_receive(self, message):
        results = message.get('results')
        filename = 'results.txt'
        filepath = os.path.join(os.getcwd(), filename)
        
        if not results:
            return "No results to save"
        
        with open(filepath, 'w') as f:
            f.write("Comparación de vuelos\n")
            f.write("="*40 + "\n")
            for result in results:
                f.write(f"Aerolínea: {result['airline']}\n")
                f.write(f"Precio: {result['price']}\n")
                f.write(f"Hora de salida: {result['departure_time']}\n")
                f.write(f"Hora de llegada: {result['arrival_time']}\n")
                f.write(f"Escalas: {result['stops']}\n")
                f.write("-"*40 + "\n")
        
        return filepath
