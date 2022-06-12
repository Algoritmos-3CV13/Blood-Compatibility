import math
import pydot
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout

def prim(w,n,s):
    v = []                          # arreglo de vertices
    for _ in range(n):              # añadir n verices con valor de 0
        v.append(0)
    v[s] = 1                        # el vertice s es por donde va a iniciar el arbol
    E = []                          # aristas
    suma = 0                        # suma
    for _ in range(n-1):            # para cada vertice
        minimo = inf                # inf es el limite
        agregar_vertice = 0         # check
        e = []                      # aux para guardar posiciones
        for j in range(n):          # para cada vertice
            if v[j] == 1:           # si el vertice fue visitado
                for k in range(n):  # para cada vertice
                    peso = w[j,k] if (j,k) in list(w) else inf
                    if v[k] == 0 and peso < minimo: # buscar arista con menor peso
                        agregar_vertice = k # agregar el vertice con arista más pequeña
                        e = [j,k]           # guardar posición
                        minimo = peso       # actualizar el peso minimo
        suma += w[e[0],e[1]]       # sumar peso
        v[agregar_vertice] = 1      # nodo ya visitado
        E.append(e)                 # agregar aristas
    return E,suma

def get_edges(personas,n):
    personas_key = [list(personas)[i] for i in range(n)]
    aristas = {}
    for i in range(n):
        key = personas_key[i]
        hijos = personas[key]["hijos"]
        indexes = [personas_key.index(hijos[i]) for i in range(len(hijos))]
        for j in range(len(indexes)):
            if len(indexes) > 0:
                aristas[(i,indexes[j])] = personas[key]["weight"][j]
                aristas[(indexes[j],i)] = personas[key]["weight"][j]
    return aristas

inf = math.inf

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
        "Yeager":{"edad":88,"tipo":"a+" ,"hijos":["Faye","Grisha"]       ,"weight":[50,50]},
        "Maria" :{"edad":99,"tipo":"o+" ,"hijos":["Faye","Grisha"]       ,"weight":[50,50]},
        "Jean"  :{"edad":84,"tipo":"b+" ,"hijos":["Carla"]               ,"weight":[50,50]},
        "Rose"  :{"edad":70,"tipo":"ab+","hijos":["Carla"]               ,"weight":[50,50]},
        "Faye"  :{"edad":32,"tipo":"a-" ,"hijos":[]                      ,"weight":[]},
        "Grisha":{"edad":37,"tipo":"o-" ,"hijos":["Zeke","Eren","Mikasa"],"weight":[75,50,50]},
        "Carla" :{"edad":43,"tipo":"b-" ,"hijos":["Eren","Mikasa"]       ,"weight":[50,50]},
        "Zeke"  :{"edad":16,"tipo":"a+" ,"hijos":[]                      ,"weight":[]},
        "Eren"  :{"edad":20,"tipo":"a+" ,"hijos":["Armin","Levi"]        ,"weight":[50,50]},
        "Mikasa":{"edad":18,"tipo":"b+" ,"hijos":[]                      ,"weight":[]},
        "Armin" :{"edad":2 ,"tipo":"ab+","hijos":[]                      ,"weight":[]},
        "Levi"  :{"edad":5 ,"tipo":"a-" ,"hijos":[]                      ,"weight":[]},
}

n = len(personas)
s = list(personas).index("Eren")
w = get_edges(personas,n)

E,suma = prim(w,n,s)
print(f"Despues de aplicar prim:\nAristas = {E}\nd = {suma}")

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
        peso = w[i,j] if (i,j) in list(w) else inf
        if peso < inf:
            g.add_edge(list(personas)[i],list(personas)[j],weight=w[i,j])

color_map = ["green" if i == 0 else "red" for i in range(n) ]

pos = graphviz_layout(g, prog="dot")

# dibujar todas las conexiones
nx.draw(g,
        pos,
        with_labels=True,
        node_color="tab:red",
        edge_color="tab:gray",
        node_size=500,
        width=1,
)

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
