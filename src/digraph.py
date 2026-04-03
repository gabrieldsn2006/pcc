from bag import Bag


class Digraph:

    def __init__(self, v=0):
        self.V = v
        self.E = 0
        self.adj = [Bag() for _ in range(self.V)]
        self._indegree = [0] * (v)

    def __str__(self):
        s = "%d vertices, %d edges\n" % (self.V, self.E)
        s += "\n".join("%d: %s" % (v, " ".join(str(w) for w in self.adj[v])) for v in range(self.V))
        return s

    def add_edge(self, v, w, weight):
        v, w, weight = int(v), int(w), int(weight)
        self.adj[v].add((w, weight))
        self.E += 1
        self._indegree[w] += 1

    def out_degree(self, v):
        return self.adj[v].size()

    def in_degree(self, v):
        return self._indegree[v]

    def max_degree(self):
        max_deg = 0
        for v in range(self.V):
            max_deg = max(max_deg, self.degree(v))
        return max_deg

    def number_of_self_loops(self):
        count = 0
        for v in range(self.V):
            for w, weight in self.adj[v]:
                if w == v:
                    count += 1
        return count

    def reverse(self):
        R = Digraph(self.V)
        v = 0
        while v < self.V:
            for w, weight in self.adj[v]:
                R.add_edge(w, v, weight)
            v += 1
        return R

