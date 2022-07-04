import math
import pydot
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout

def prim(w,n,s):
    v = []                          # vertices
    for _ in range(n):              # set every vertice as 0
        v.append(0)
    v[s] = 1                        # the tree starts at the recipient
    E = []                          # edges
    cost = 0
    for _ in range(n-1):
        min_ = inf
        vertice_index = 0
        e = []                      # edge
        for j in range(n):          # for every edge
            if v[j] == 1:           # if vertice was visited
                for k in range(n):  # for every edge
                    weight = w[j,k] if (j,k) in list(w) else inf
                    if v[k] == 0 and weight < min_: # search the shorter edge
                        vertice_index = k # save the index of the shorter edge
                        e = [j,k]         # save position
                        min_ = weight     # update min_
        cost += w[e[0],e[1]]        # increse cost
        v[vertice_index] = 1        # set node as visited
        E.append(e)
    return E,cost

def get_edges(family_tree,n):
    family_tree_keys = list(family_tree)
    edges = {}
    for i in range(n):
        donor_name = family_tree_keys[i]
        children = family_tree[donor_name]["children"] # get array of children
        indexes  = [family_tree_keys.index(children[i]) for i in range(len(children))] # get indexes of children
        for j in range(len(indexes)):
            if len(indexes) > 0:
                edges[(i,indexes[j])] = family_tree[donor_name]["weight"][j]   # create edges with tuples as index
                edges[(indexes[j],i)] = family_tree[donor_name]["weight"][j]   # and store the weight
    return edges

def find_donors(family_tree,recipient):
    n = len(family_tree)                   # vertices lenght
    s = list(family_tree).index(recipient) # recipient index
    w = get_edges(family_tree,n)
    
    E,cost = prim(w,n,s)
    # print(f"After apply Prim's Algorithm:\nEdges = {E}\nCost = {cost}")
    
    blood_recipient = family_tree[recipient]["blood"]
    print(f"""Recipient:\n{list(family_tree)[s]} {family_tree[list(family_tree)[s]]}\n""")
    
    edges_by_name = [[list(family_tree)[E[i][0]],list(family_tree)[E[i][1]]] for i in range(len(E))]
    print("Potential donors:")
    j = 0

    potential_donors = []
    for i in range(len(edges_by_name)):                 # apply filters
        donor_name  = edges_by_name[i][1]
        donor_age   = family_tree[donor_name]["age"]    # the donor must be over 18 years old.
        donor_blood = family_tree[donor_name]["blood"]  # the donor's blood type must be compatible
        if(18 <= donor_age <= 65 and donor_blood in blood_compatibility[blood_recipient]["donors"]):
            j += 1
            potential_donors.append(i)
            print(f"{j} {donor_name} {family_tree[donor_name]}")
    
    g = nx.Graph()
    for i in range(n):
        for j in range(n):
            weight = w[i,j] if (i,j) in list(w) else inf
            if weight < inf:
                g.add_edge(list(family_tree)[i],list(family_tree)[j],weight=w[i,j])   # add edge with weight
    
    color_map = ["red" for i in range(n) ]          # default vertice color is red
    color_map[0] = "green"                          # the recipient is green
    for i in range(len(potential_donors)):
        color_map[potential_donors[i]+1] = "orange" # potential donors are orange

    print("""
Graph information:
Node green  <--> Recipient
Node orange <--> Potential donor
Node red    <--> Default""")
    
    # set graph style
    pos = graphviz_layout(g, prog="dot")
    
    # draw graph with node names
    nx.draw(g,
            pos,
            with_labels=True,
            node_color="tab:red",
            edge_color="tab:gray",
            node_size=2000,
            width=1,
    )
    
    # draw graph with node names and indicative colors
    nx.draw(nx.Graph(edges_by_name),
            pos,
            with_labels=True,
            node_color=color_map,
            edge_color="tab:blue",
            node_size=2000,
            width=3,
    )
    
    # draw weight on graph
    edge_labels = nx.get_edge_attributes(g, "weight")
    nx.draw_networkx_edge_labels(g, pos, edge_labels)
    
    # show graph
    plt.draw()
    plt.show()

inf = math.inf

blood_compatibility = {
        "a+": {"donors":["a+","a-","o+","o-"]},
        "o+": {"donors":["o+","o-"]},
        "b+": {"donors":["b+","b-","o+","o-"]},
        "ab+":{"donors":["a+","o+","b+","ab+","a-","o-","b","ab"]},
        "a-": {"donors":["a-","o-"]},
        "o-": {"donors":["o-"]},
        "b":  {"donors":["b-","o-"]},
        "ab": {"donors":["ab-","a-","b-","o-"]},
};

family_tree = {
        "Yeager":{"age":88,"blood":"a+" ,"children":["Faye","Grisha"]       ,"weight":[50,50]},
        "Maria" :{"age":99,"blood":"o+" ,"children":["Faye","Grisha"]       ,"weight":[50,50]},
        "Jean"  :{"age":84,"blood":"b+" ,"children":["Carla"]               ,"weight":[50,50]},
        "Rose"  :{"age":70,"blood":"ab+","children":["Carla"]               ,"weight":[50,50]},
        "Faye"  :{"age":32,"blood":"a-" ,"children":[]                      ,"weight":[]},
        "Grisha":{"age":37,"blood":"o-" ,"children":["Zeke","Eren","Mikasa"],"weight":[75,50,50]},
        "Carla" :{"age":43,"blood":"b-" ,"children":["Eren","Mikasa"]       ,"weight":[50,50]},
        "Zeke"  :{"age":16,"blood":"a+" ,"children":[]                      ,"weight":[]},
        "Eren"  :{"age":20,"blood":"a+" ,"children":["Armin","Levi"]        ,"weight":[50,50]},
        "Mikasa":{"age":18,"blood":"b+" ,"children":[]                      ,"weight":[]},
        "Armin" :{"age":2 ,"blood":"ab+","children":[]                      ,"weight":[]},
        "Levi"  :{"age":5 ,"blood":"a-" ,"children":[]                      ,"weight":[]},
}

find_donors(family_tree,"Eren")
