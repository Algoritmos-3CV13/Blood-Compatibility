import math
import pydot
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout

def prim(w,n,s):
    v = []                          # arreglo de vertices
    for i in range(n):              # añadir n verices con valor de 0
        v.append(0)
    v[s] = 1                        # el vertice s es por donde va a iniciar el arbol
    E = []                          # aristas
    suma = 0                        # suma
    for i in range(n-1):            # para cada vertice
        minimo = inf                # inf es el limite
        agregar_vertice = 0         # check
        e = []                      # aux para guardar posiciones
        for j in range(n):          # para cada vertice
            if v[j] == 1:           # si el vertice fue visitado
                for k in range(n):  # para cada vertice
                    if v[k] == 0 and w[j][k] < minimo: # buscar arista con menor peso
                        agregar_vertice = k # agregar el vertice con arista más pequeña
                        e = [j,k]           # guardar posición
                        minimo = w[j][k]    # actualizar el peso minimo
        suma += w[e[0]][e[1]]       # sumar peso
        v[agregar_vertice] = 1      # nodo ya visitado
        E.append(e)                 # agregar aristas
    return E,suma

inf = math.inf
s = 2
w = [
        # 0   1   2   3   4   5   6   7
        [inf, 4 , 2 ,inf, 3 ,inf,inf,inf], # 0
        [ 4 ,inf,inf,inf,inf,inf,inf,inf], # 1
        [ 2 ,inf,inf, 1 ,inf,inf, 1 , 1 ], # 2
        [inf,inf, 1 ,inf,inf,inf,inf,inf], # 3
        [ 3 ,inf,inf,inf,inf, 2 ,inf,inf], # 4
        [inf,inf,inf,inf, 2 ,inf,inf,inf], # 5
        [inf,inf, 1 ,inf,inf,inf,inf,inf], # 6
        [inf,inf, 1 ,inf,inf,inf,inf,inf], # 7
]

n = len(w)
E,suma = prim(w,n,s)
print(E,suma)

compatibilidad = {
        "a+": {"recibe":["a+","a-","o+","o-"]},
        "o+": {"recibe":["o+","o-"]},
        "b+": {"recibe":["b+","b-","o+","o-"]},
        "ab+":{"recibe":["a+","o+","b+","ab+","a-","o-","b","ab"]},
        "a-": {"recibe":["a-","o-"]},
        "o-": {"recibe":["o-"]},
        "b":  {"recibe":["b-","o-"]},
        "ab": {"recibe":["ab-","a-","b-","o-"]},
};

personas = {
        "Ymir"  :{"edad":82,"tipo":"a+" },
        "Shina" :{"edad":48,"tipo":"o+" },
        "Maria" :{"edad":39,"tipo":"b+" },
        "Levi"  :{"edad":25,"tipo":"ab+"},
        "Rose"  :{"edad":50,"tipo":"a-" },
        "Eren"  :{"edad":50,"tipo":"o-" },
        "Mikasa":{"edad":10,"tipo":"b-" },
        "Armin" :{"edad":17,"tipo":"ab-"},
}

sangre_receptor = personas[list(personas)[s]]["tipo"]
print(f"\nPersona receptora: {list(personas)[s]} {personas[list(personas)[s]]}\n")

E_nombres = [[list(personas)[E[i][0]],list(personas)[E[i][1]]] for i in range(len(E))]
print("Nombres de donadores:")
j = 0
for i in range(len(E_nombres)):
    nombre_donador = E_nombres[i][1]
    edad = personas[nombre_donador]["edad"]
    sangre = personas[nombre_donador]["tipo"]
    if(18 <= edad <= 65 and sangre in compatibilidad[sangre_receptor]["recibe"]):
        j += 1
        print(f"{j} {nombre_donador} {personas[nombre_donador]}")

g = nx.Graph()
for i in range(n):
    for j in range(n):
        if w[i][j] < inf:
            g.add_edge(list(personas)[i],list(personas)[j],weight=w[i][j])

color_map = ["green" if i == 0 else "red" for i in range(n) ]

pos = graphviz_layout(g, prog="dot")

# dibujar todas las conexiones
#nx.draw(g,
#        pos,
#        with_labels=True,
#        node_color="tab:red",
#        edge_color="tab:gray",
#        node_size=500,
#        width=1,
#)

# dibujar arbol de prim pintando nodo inicial de verde
nx.draw(nx.Graph(E_nombres),
        pos,
        with_labels=True,
        node_color=color_map,
        edge_color="tab:blue",
        node_size=500,
        width=3,
)

# dibujar pesos en aristas
edge_labels = nx.get_edge_attributes(g, "weight")
nx.draw_networkx_edge_labels(g, pos, edge_labels)

# desplegar grafo en pantalla
plt.draw()
plt.show()
