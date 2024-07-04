#agregue otros terrenos, y que no tenga limite de 6 celdas por tipo de terreno
import tkinter as tk
from heapq import heappop, heappush

# Define los colores y factores de movimiento de los terrenos
terrenos = {
    "01": {"color": "lightgreen", "factor": 1.0},  # Césped
    "02": {"color": "darkgreen", "factor": 0.75},  # Bosque
    "03": {"color": "lightblue", "factor": 0.5},   # Agua poco profunda
    "04": {"color": "darkblue", "factor": 0.25},   # Agua profunda
    "05": {"color": "darkgray", "factor": 0.1},    # Muro
    "06": {"color": "brown", "factor": 0.8}        # Puente de madera
}

# Inicializa el mapa de 10x10 con césped
mapa = [["01" for _ in range(10)] for _ in range(10)]

# Función para obtener el costo de movimiento
def obtener_costo(codigo):
    return 1.0 / terrenos[codigo]["factor"]

# Algoritmo A* para encontrar la ruta más eficiente
def a_star(inicio, fin):
    filas, columnas = len(mapa), len(mapa[0])
    vecinos = [(0,1), (0,-1), (1,0), (-1,0)]
    
    open_set = []
    heappush(open_set, (0, inicio))
    g_score = {inicio: 0}
    came_from = {}

    while open_set:
        _, current = heappop(open_set)
        
        if current == fin:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(inicio)
            return path[::-1]

        for d in vecinos:
            vecino = (current[0] + d[0], current[1] + d[1])
            if 0 <= vecino[0] < filas and 0 <= vecino[1] < columnas:
                tentative_g_score = g_score[current] + obtener_costo(mapa[vecino[0]][vecino[1]])
                if vecino not in g_score or tentative_g_score < g_score[vecino]:
                    came_from[vecino] = current
                    g_score[vecino] = tentative_g_score
                    heappush(open_set, (tentative_g_score, vecino))

    return []

# Función para encontrar y resaltar la ruta
def encontrar_ruta():
    inicio = (int(inicio_y.get()), int(inicio_x.get()))
    fin = (int(fin_y.get()), int(fin_x.get()))
    ruta = a_star(inicio, fin)
    
    for fila in celdas:
        for celda in fila:
            canvas.itemconfig(celda, outline="black")
    
    for x, y in ruta:
        canvas.itemconfig(celdas[y][x], outline="yellow", width=2)

# Función para actualizar el tipo de terreno en una celda
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

# Configuración de la interfaz gráfica
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

root.mainloop()
