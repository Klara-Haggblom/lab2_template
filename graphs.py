class Graph:
    def __init__(self, start=None, values = None, directed=False):
        self._adjlist = {}
        if values is None:
            values = {}
        self._valuelist = values
        self._isdirected = directed
        # plus some code for building a graph from a ’start’ object
        # such as a list of edges
        # here are some of the public methods to implement
    def vertices(self):
        return list(self._adjlist.keys())
    def edges(self):
        vertices = []
        edges = []
        for elements in list(self._adjlist.keys()):
            vertices.append(elements)
            for i in range(len(vertices)):
                for j in range(i+1,len(vertices)):
                    edges.append((vertices[i],vertices[j]))

    def neighbours(self,v):
        if v not in self._adjlist:
            return None
        else:
            return self._adjlist[v]
    def add_edge(self,a,b):
        if a not in self._adjlist:
            self._adjlist[a] = []
        self._adjlist[a].append(b)
    def add_vertex(self,a):
        if a not in self._adjlist:
            self._adjlist[a] = []
    def is_directed(self):
        if self._isdirected == True:
            return self.is_directed()

    def remove_vertex(self, v):
        if v in self._adjlist:
            self._adjlist.pop(v)

        for vertex in self._adjlist:
            new_neighbors = []
            for neighbor in self._adjlist[vertex]:
                if neighbor != v:
                    new_neighbors.append(neighbor)
            self._adjlist[vertex] = new_neighbors

    def remove_edge(self, a,b):
        if a in self._adjlist and b in self._adjlist:
            new_neighbors_a = []
            for neighbor in self._adjlist[a]:
                if neighbor != b:
                    new_neighbors_a.append(neighbor)
            self._adjlist[a] = new_neighbors_a
    def get_vertex_value(self, v):
        if v in self._adjlist:
            return self._adjlist[v]
        else:
            return None
    def set_vertex_value(self, v, x):
        if v in self._adjlist:
            self._adjlist[v] = x

class WeightedGraph(Graph): #weight dictionary som attribut. Mellan 2 noder kommer vi spara kostnaden mellan två noder. Tid eller distans. Olika dictionaries beroende på. Men bygger så det funka på bägge
    def __init__(self):
        super().__init__() #skapar allt från klassen ovanifrån, skapa allt där. ALla attribut och metoder
        self.weight = {} #sparar alla vikter mellan två noder
    def set_weight(self, a, b, w):
        if a not in self.weight and b not in self.weight:
            self.weight[a] = {b:w}
        elif a not in self.weight:
            self.weight[b][a] = w
        else:
            self.weight[a][b] = w

    def get_weight(self, a, b):
        if a not in self.weight and b not in self.weight:
            return None
        elif a not in self.weight:
            return self.weight[b][a]
        else:
            return self.weight[a][b]
    def dijkstra(self, graph, source, cost = lambda u,v: 1): #när vi ska gå till granne hämtar vi kostnaden mellan den vi är på nu
        #avståndet mellan u och v är 1 om inget annat anges. Kan hämta distance beroende på vad vi skickar in
        #source är där vi börjar
        unvisited = {n: float('inf') for n in graph.keys()}#ska iterera över unvisited, ska gå till granne med kortast avstånd
        unvisited[source] = 0
        visited = {}
        while unvisited:
            minNode = min(unvisited, key = unvisited.get)
            visited[minNode] = unvisited[minNode]

            for neighbor in graph.get(minNode).keys():
                if neighbor in visited:
                    continue
                tempDist = unvisited[minNode] + graph[minNode][neighbor]
                if tempDist < unvisited[neighbor]:
                    unvisited[neighbor] = tempDist
            unvisited.pop(minNode)







