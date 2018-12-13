import random as rand

# GRAPH DATA STRUCTURES

class LLNode:
    def __init__(self, data, pred=None, succ=None):
        self.data = data
        self.pred = pred
        self.succ = succ

class AdjList:
    def __init__(self, equal=lambda a,b: a == b):
        self.adjList = LLNode(data=None)
        self.tail = self.adjList
        self.equal = equal

    def has(self, val):
        node = self.adjList.succ
        t = (val,)
        while node:
            if self.equal(node.data, t):
                return True
            node = node.succ
        return False

    def insert(self, val):
        if not self.has(val):
            nnode = LLNode(val, pred=self.tail)
            self.tail.succ = nnode
            self.tail = nnode

    def remove(self, val):
        node = self.adjList.succ
        t = (val,)
        while node:
            if self.equal(node.data, t):
                if node.pred:
                    node.pred.succ = node.succ
                if node.succ:
                    node.succ.pred = node.pred
                if node == self.tail:
                    self.tail = node.pred
                break
            node = node.succ
    
    def get_edges(self):
        values = []
        node = self.adjList.succ
        while node:
            values.append(node.data)
            node = node.succ
        return values

class Graph:
    def __init__(self, directed):
        self.adjLists = {}
        self.directed = directed

    def create_vert(self, vert):
        if vert not in self.adjLists:
            self.adjLists[vert] = AdjList(equal=lambda a, b: a[0] == b[0])

    def insert(self, e1, e2, weight=1):
        if e1 not in self.adjLists:
            self.adjLists[e1] = AdjList(equal=lambda a, b: a[0] == b[0])
        self.adjLists[e1].insert((e2, weight))
        if not self.directed:
            if e2 not in self.adjLists:
                self.adjLists[e2] = AdjList(equal=lambda a, b: a[0] == b[0])
            self.adjLists[e2].insert((e1, weight))
    
    def remove(self, e1, e2):
        self.adjLists[e1].remove(e2)
        if not self.directed:
            self.adjLists[e2].remove(e1)

    def walk(self):
        for v, edgeList in self.adjLists.items():
            print("Vertex V", v, edgeList.get_edges())

def generate_graph(vert_count=10, density=0.5, derror=1, directed=True, weighted=False, min_weight=0, max_weight=10, allow_selfref=False):
    g = Graph(directed)
    verts = [i for i in range(vert_count)]
    allow_self = 0 if allow_selfref else 1
    if directed:
        for i in range(vert_count):
            src_v = verts[i]
            median = int((vert_count-1) * density)
            selected_verts = rand.sample(verts[:i] + verts[i+allow_self:], rand.randint(max(0, median-derror), min(vert_count-1, median+derror)))
            for v in selected_verts:
                g.insert(src_v, v, 1 if not weighted else rand.randint(min_weight, max_weight))
    if not directed:
        for i in range(vert_count):
            for j in range(i+allow_self, vert_count):
                if rand.random() <= density:
                    g.insert(verts[i], verts[j], 1 if not weighted else rand.randint(min_weight, max_weight))
    return g
