#Agregue mejora para que castigue la perdida de puntos, y que seleccione el camino 
import tkinter as tk #biblioteca para interfaz grafica 
from heapq import heappop, heappush #funciones para trabajar con colas de prioridad necesarias para algoritmo a*

# Define los colores y castigos de movimiento segun terrenos
terrenos = {
    "01": {"color": "lightgreen", "costo_pasos": 2},  # Césped
    "02": {"color": "darkgreen", "costo_pasos": 4},  # Bosque
    "04": {"color": "darkblue", "costo_pasos": 6},   # Agua profunda
    "05": {"color": "darkgray", "costo_pasos": 50},   # Muro
    }

# Inicializa el mapa de 10x10 con césped
mapa = [["01" for _ in range(10)] for _ in range(10)]

# Función para obtener el costo en pasos
def obtener_costo_pasos(codigo):
    return terrenos[codigo]["costo_pasos"]

# Algoritmo A* para encontrar la ruta más eficiente en términos de costo en pasos segun terrenos recorridos
def a_star(inicio, fin):#algoritmo a* no sigue solo un camino sino que explora multiples caminos a la vez 
    filas, columnas = len(mapa), len(mapa[0])
    vecinos = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    open_set = [] #cola de priodidad, nodos explorando, ordenados estimacion costo total, inicia en costo 0
    heappush(open_set, (0, inicio))
    g_score = {inicio: 0} #suma los costos del nodo inicial a cada nodo del grafo
    f_score = {inicio: obtener_costo_pasos(mapa[inicio[1]][inicio[0]])} #calcula costo desde el nodo inicial, al final pasando por el actual
    came_from = {} #diccionario que guarda el nodo previo optimo que llevo al nodo actual

    while open_set: #mientras no este vacio sigue buscando 
        _, current = heappop(open_set)
        
        if current == fin: #si es el nodo objetivo, reconstruye el camino desde ahi hasta el inicial
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(inicio)
            return path[::-1]

        for d in vecinos: #calcula los costos adicionales tentativos al nodo vecino, si el costo es el menor, agrega a came from, para indiicar mejor fuente 
            vecino = (current[0] + d[0], current[1] + d[1])
            if 0 <= vecino[0] < filas and 0 <= vecino[1] < columnas:
                tentative_g_score = g_score[current] + obtener_costo_pasos(mapa[vecino[1]][vecino[0]])
                if vecino not in g_score or tentative_g_score < g_score[vecino]:
                    came_from[vecino] = current
                    g_score[vecino] = tentative_g_score
                    f_score[vecino] = tentative_g_score
                    heappush(open_set, (f_score[vecino], vecino))

    return []

# Función para encontrar y resaltar la ruta, actualiza saldo segun recorrido
def encontrar_ruta():
    inicio = (int(inicio_y.get()), int(inicio_x.get()))
    fin = (int(fin_y.get()), int(fin_x.get()))
    ruta = a_star(inicio, fin)
    
    for fila in celdas:
        for celda in fila:
            canvas.itemconfig(celda, outline="black")
    
    saldo = int(saldo_pasos.get())

    for x, y in ruta:
        costo_pasos = obtener_costo_pasos(mapa[y][x])
        saldo -= costo_pasos
        canvas.itemconfig(celdas[y][x], outline="yellow", width=2)

    saldo_pasos.set(saldo)
    etiqueta_saldo.config(text=f"Saldo de pasos: {saldo}")

# Función para actualizar el tipo de terreno en una celda segun las coordenadas instruidas por el usuario
def actualizar_terreno(terreno):
    coords = [(int(coord[1]), int(coord[0])) for coord in terrenos_coords[terreno]]
    for x, y in coords:
        mapa[y][x] = terreno
        canvas.itemconfig(celdas[y][x], fill=terrenos[terreno]["color"])

def agregar_coordenada(terreno):
    x = int(coordenada_x.get())
    y = int(coordenada_y.get())
    terrenos_coords[terreno].append((x, y))
    lista_coordenadas[terreno].insert(tk.END, f"({x}, {y})")

# Configuración de la interfaz gráfica y sus elementos visuales, entrada salida, terrenos y recorrido
root = tk.Tk()
root.title("Calculadora de Rutas")

canvas = tk.Canvas(root, width=400, height=400)
canvas.grid(row=0, column=0, rowspan=10, columnspan=10)

celdas = [[None for _ in range(10)] for _ in range(10)]
for y in range(10):
    for x in range(10):
        celdas[y][x] = canvas.create_rectangle(x*40, y*40, x*40+40, y*40+40, fill=terrenos["01"]["color"], outline="black")

# Controles para entrada de coordenadas de inicio y fin
tk.Label(root, text="Inicio X:").grid(row=10, column=0)
inicio_x = tk.Entry(root, width=3)
inicio_x.grid(row=10, column=1)
tk.Label(root, text="Y:").grid(row=10, column=2)
inicio_y = tk.Entry(root, width=3)
inicio_y.grid(row=10, column=3)

tk.Label(root, text="Fin X:").grid(row=10, column=4)
fin_x = tk.Entry(root, width=3)
fin_x.grid(row=10, column=5)
tk.Label(root, text="Y:").grid(row=10, column=6)
fin_y = tk.Entry(root, width=3)
fin_y.grid(row=10, column=7)

tk.Button(root, text="Encontrar Ruta", command=encontrar_ruta).grid(row=10, column=8, columnspan=2)

# Controles para entrada de coordenadas de terrenos
terrenos_coords = {
    "02": [],
    "04": [],
    "05": []
}

tk.Label(root, text="Terreno X:").grid(row=11, column=0)
coordenada_x = tk.Entry(root, width=3)
coordenada_x.grid(row=11, column=1)
tk.Label(root, text="Y:").grid(row=11, column=2)
coordenada_y = tk.Entry(root, width=3)
coordenada_y.grid(row=11, column=3)

tk.Button(root, text="Agregar Bosque", command=lambda: agregar_coordenada("02")).grid(row=11, column=4, columnspan=2)
tk.Button(root, text="Agregar Agua Profunda", command=lambda: agregar_coordenada("04")).grid(row=11, column=6, columnspan=2)
tk.Button(root, text="Agregar Muro", command=lambda: agregar_coordenada("05")).grid(row=11, column=8, columnspan=2)

lista_coordenadas = {
    "02": tk.Listbox(root, height=6, width=20),
    "04": tk.Listbox(root, height=6, width=20),
    "05": tk.Listbox(root, height=6, width=20)
}

lista_coordenadas["02"].grid(row=12, column=0, columnspan=3)
lista_coordenadas["04"].grid(row=12, column=4, columnspan=3)
lista_coordenadas["05"].grid(row=12, column=8, columnspan=3)

tk.Button(root, text="Actualizar Bosque", command=lambda: actualizar_terreno("02")).grid(row=13, column=0, columnspan=3)
tk.Button(root, text="Actualizar Agua Profunda", command=lambda: actualizar_terreno("04")).grid(row=13, column=4, columnspan=3)
tk.Button(root, text="Actualizar Muro", command=lambda: actualizar_terreno("05")).grid(row=13, column=8, columnspan=3)

# Controles para el saldo de pasos despues del recorrido
tk.Label(root, text="Saldo de pasos:").grid(row=14, column=0)
saldo_pasos = tk.StringVar(value="200")
entrada_saldo = tk.Entry(root, textvariable=saldo_pasos, width=5)
entrada_saldo.grid(row=14, column=1)
etiqueta_saldo = tk.Label(root, text="Saldo de pasos: 200")
etiqueta_saldo.grid(row=14, column=2, columnspan=4)

root.mainloop()
