import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._nodes = []
        self._idMap = {}
        self._bestScore = 0
        self._bestPath = []


    def getAllCategories(self):
        return DAO.getAllCategories()


    def getDateRange(self):
        return DAO.getDateRange()


    def creaGrafo(self, categoria, inizio, fine):
        self._nodes = DAO.getProdottiCategoria(categoria)
        self._graph.clear()
        self._graph.add_nodes_from(self._nodes)

        self._idMap = {}
        for n in self._nodes:
            self._idMap[n.product_id] = n

        edges = DAO.getEdges(categoria, inizio, fine)
        for e1 in edges:
            for e2 in edges:
                if e1[0] != e2[0]:

                    if e1[1] < e2[1] and not self._graph.has_edge(self._idMap[e1[0]], self._idMap[e2[0]]): # se il primo nodo ha peso maggiore del secondo
                        self._graph.add_edge(self._idMap[e2[0]], self._idMap[e1[0]], weight=e1[1] + e2[1])

                    elif e1[1] == e2[1] and not self._graph.has_edge(self._idMap[e1[0]], self._idMap[e2[0]]):
                        self._graph.add_edge(self._idMap[e1[0]], self._idMap[e2[0]], weight=e1[1] + e2[1])
                        self._graph.add_edge(self._idMap[e2[0]], self._idMap[e1[0]], weight=e1[1] + e2[1])

                    else:
                        continue

        return self._nodes


    def getNumNodi(self):
        return len(self._graph.nodes)


    def getNumArchi(self):
        return len(self._graph.edges)


    def getBest5(self):
        lista_score = []

        for n in self._graph.nodes:
            punteggio = self._graph.out_degree(n, weight='weight') - self._graph.in_degree(n, weight='weight')
            lista_score.append((n, punteggio))

        lista_score.sort(key=lambda x: x[1], reverse=True)

        return lista_score[:5]


    def getCammino(self, partenza, arrivo, lunghezza):
        self._bestPath = []
        self._bestScore = 0

        if lunghezza == 0:
            return []

        parziale = [partenza]

        for n in self._graph.successors(partenza):
            parziale.append(n)
            self.ricorsione(parziale, arrivo, lunghezza)
            parziale.pop()

        return self._bestPath


    def ricorsione(self, parziale, arrivo, lunghezza):
        if len(parziale)-1 == lunghezza:
            if parziale[-1] == arrivo:
                costo = self.costoPercorso(parziale)
                if costo > self._bestScore:
                    self._bestScore = costo
                    self._bestPath = copy.deepcopy(parziale)

        else:
            for n in self._graph.successors(parziale[-1]):
                if n not in parziale:
                    parziale.append(n)
                    self.ricorsione(parziale, arrivo, lunghezza)
                    parziale.pop()


    def costoPercorso(self, percorso):
        costo = 0
        for i in range(len(percorso)-1):
            costo += self._graph[percorso[i]][percorso[i+1]]["weight"]
        return costo