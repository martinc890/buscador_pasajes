import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from actors.search_actor import SearchActor
from actors.compare_actor import CompareActor
from actors.save_actor import SaveActor
import pykka

# Lista de aeropuertos disponibles
aeropuertos = {
    'Ezeiza (EZE)': 'EZE',
    'Miami (MIA)': 'MIA',
    'Asunción (ASU)': 'ASU',
    'Madrid (MAD)': 'MAD',
}

def iniciar_busqueda():
    # Obtener los valores seleccionados
    origen = aeropuertos[origen_combo.get()]
    destino = aeropuertos[destino_combo.get()]
    fecha = fecha_entry.get_date().strftime("%Y-%m-%d")
    
    if origen == destino:
        messagebox.showerror("Error", "El aeropuerto de origen y destino no pueden ser iguales.")
        return

    # Inicializar los actores
    search_actor_ref = SearchActor.start()
    compare_actor_ref = CompareActor.start()
    save_actor_ref = SaveActor.start()

    # Obtener los vuelos a través del SearchActor
    flights = search_actor_ref.ask({'origin': origen, 'destination': destino, 'date': fecha})

    # Enviar los vuelos al CompareActor para que los ordene
    sorted_flights = compare_actor_ref.ask({'flights': flights})

    # Enviar los vuelos ordenados al SaveActor para que los guarde
    save_actor_ref.tell({'flights': sorted_flights})

    # Cerrar los actores después de usarlos
    search_actor_ref.stop()
    compare_actor_ref.stop()
    save_actor_ref.stop()

    # Mostrar mensaje de éxito
    messagebox.showinfo("Éxito", "Búsqueda completada y resultados guardados.")

# Crear la ventana principal
root = tk.Tk()
root.title("Buscador de Pasajes")

# Etiqueta para seleccionar el origen
tk.Label(root, text="Seleccione el aeropuerto de origen:").pack(pady=10)
origen_combo = ttk.Combobox(root, values=list(aeropuertos.keys()), state="readonly")
origen_combo.set("Ezeiza (EZE)")  # Valor por defecto
origen_combo.pack(pady=5)

# Etiqueta para seleccionar el destino
tk.Label(root, text="Seleccione el aeropuerto de destino:").pack(pady=10)
destino_combo = ttk.Combobox(root, values=list(aeropuertos.keys()), state="readonly")
destino_combo.set("Miami (MIA)")  # Valor por defecto
destino_combo.pack(pady=5)

# Selector de fecha
tk.Label(root, text="Seleccione la fecha del vuelo:").pack(pady=10)
fecha_entry = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='y-mm-dd')
fecha_entry.pack(pady=5)

# Botón para iniciar la búsqueda
tk.Button(root, text="Iniciar Búsqueda", command=iniciar_busqueda).pack(pady=20)

# Iniciar la interfaz gráfica
root.mainloop()
