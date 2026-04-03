"""
Algoritmo de Hierholzer para encontrar circuitos Eulerianos.

Um circuito Euleriano é um caminho que visita cada aresta exatamente uma vez
e retorna ao vértice de partida.

Pré-condições para um grafo dirigido ter um circuito Euleriano:
    1. Todos os vértices devem ter grau de entrada igual ao grau de saída
    2. O grafo deve ser conexo (todos vértices com arestas conectados)

Permite arestas múltiplas (multigrafo).

Complexidade:
    - Tempo: O(V + E)
    - Espaço: O(V + E)
"""

from digraph import Digraph
from directed_edge import DirectedEdge
from collections import defaultdict

class DirectedEulerianCycle:
    """
    Encontra um circuito Euleriano em um grafo não-dirigido usando
    o algoritmo de Hierholzer.
    
    Attributes:
        circuit: lista contendo o circuito Euleriano encontrado
        valid: boolean indicando se um circuito Euleriano existe
    """

    def __init__(self, digraph: Digraph):
        """
        Inicializa o algoritmo de Hierholzer.
        
        Args:
            digraph: objeto Digraph com lista de adjacência
        """
        self.digraph = digraph
        self.circuit = []
        self.valid = False
        self.subtours = []  # Para armazenar os subtours encontrados
        self._cost = 0
        
        # Criar cópia de trabalho das arestas como DirectedEdge
        # Permite rastrear arestas múltiplas corretamente
        self.working_adj = self._create_working_adjacency()
        
        self._find_circuit()

    def circuit_cost(self):
        return self._cost
    
    def _create_working_adjacency(self):
        """
        Cria uma cópia de trabalho das arestas do grafo como objetos DirectedEdge.
        Isso permite rastrear corretamente arestas múltiplas durante o algoritmo.
        
        Returns:
            list: lista de listas de DirectedEdge para cada vértice
        """
        working_adj = [[] for _ in range(self.digraph.V)]
        
        for v in range(self.digraph.V):
            for w, weight in self.digraph.adj[v]:
                edge = DirectedEdge(v, w, weight)
                working_adj[v].append(edge)
        
        return working_adj

    def _has_eulerian_circuit(self):
        """
        Verifica se o grafo tem um circuito Euleriano.
        
        Um grafo tem circuito Euleriano se:
        - Todos os vértices possuem grau par
        - O grafo é conexo (todos vértices com arestas estão conectados)
        
        Returns:
            bool: True se existe circuito Euleriano, False caso contrário
        """
        # Verificar se todos os vértices têm grau par
        for v in range(self.digraph.V):
            if self.digraph.out_degree(v) - self.digraph.in_degree(v) != 0:
                return False
        
        # Verificar se o grafo é conexo
        if not self._is_connected():
            return False
        
        return True

    def _is_connected(self):
        """
        Verifica se o grafo é conexo (todos vértices com arestas estão conectados).
        
        Returns:
            bool: True se o grafo é conexo, False caso contrário
        """
        # Encontrar um vértice com grau > 0
        start = -1
        for v in range(self.digraph.V):
            if self.digraph.out_degree(v) > 0:
                start = v
                break
        
        # Se nenhum vértice tem arestas, considerar como conexo
        if start == -1:
            return True
        
        # DFS a partir de um vértice com arestas
        visited = [False] * self.digraph.V
        self._dfs_connected(start, visited)
        
        # Verificar se todos os vértices com arestas foram visitados
        for v in range(self.digraph.V):
            if self.digraph.out_degree(v) > 0 and not visited[v]:
                return False
        
        return True

    def _dfs_connected(self, v, visited):
        """
        DFS auxiliar para verificar conectividade.
        
        Args:
            v: vértice atual
            visited: lista de vértices visitados
        """
        visited[v] = True
        for w, weight in self.digraph.adj[v]:
            if not visited[w]:
                self._dfs_connected(w, visited)

    def _find_circuit(self):
        """
        Encontra o circuito Euleriano usando o algoritmo de Hierholzer.
        
        Utiliza uma cópia de trabalho das arestas (DirectedEdge) que é modificada
        conforme as arestas são visitadas. Isso permite tratar corretamente
        arestas múltiplas entre os mesmos vértices.
        
        Segue o pseudo-código:
        BEGIN
          IF graph infeasible THEN END
          start ← suitable node
          tour ← {start}
          REPEAT
            current = start ← node in tour with unvisited edge
            subtour ← {start}
            DO
              {current, u} ← take unvisited edge
              subtour ← subtour ∪ {u}
              current ← u
            WHILE start ≠ current
            Integrate subtour in tour
          UNTIL tour is Eulerian path/cycle
        END
        """
        if not self._has_eulerian_circuit():
            self.valid = False
            return
        
        # Encontrar vértice inicial adequado
        start = 0
        for v in range(self.digraph.V):
            if self.digraph.out_degree(v) > 0:
                start = v
                break
        
        # Inicializar tour com o vértice inicial
        tour = [start]
        
        # Armazenar subtours encontrados (para visualização)
        self.subtours = []
        
        # REPEAT: continuar enquanto houver arestas não visitadas
        while True:
            # Procurar um nó em tour que tenha arestas não visitadas
            node_with_edge = None
            for node in tour:
                if self._has_unvisited_edge(node):
                    node_with_edge = node
                    break
            
            # Se nenhum nó em tour tem arestas não visitadas, tour é Euleriana
            if node_with_edge is None:
                break
            
            # Construir subtour começando do nó encontrado
            start_subtour = node_with_edge
            current = start_subtour
            subtour = [start_subtour]
            
            # DO-WHILE: construir subtour até retornar ao nó inicial
            while True:
                # Pegar uma aresta não visitada (current, u) e removê-la
                edge = self._get_and_remove_unvisited_edge(current)
                
                # Se não encontrou aresta, problema (não deveria acontecer)
                if edge is None:
                    break
                
                u = edge.To()
                self._cost += edge.weight
                
                # Adicionar u ao subtour
                subtour.append(u)
                current = u
                
                # Continuar enquanto start_subtour ≠ current
                if start_subtour == current:
                    break
            
            # Integrar subtour na tour
            tour = self._integrate_subtour(tour, subtour, start_subtour)
            
            # Armazenar subtour para visualização
            self.subtours.append(subtour.copy())
        
        self.circuit = tour
        self.valid = True
    
    def _has_unvisited_edge(self, node):
        """
        Verifica se um nó tem arestas não visitadas (ainda presentes no working_adj).
        
        Args:
            node: índice do vértice
            
        Returns:
            bool: True se o vértice tem arestas não visitadas
        """
        return len(self.working_adj[node]) > 0
    
    def _get_and_remove_unvisited_edge(self, node):
        """
        Obtém uma aresta não visitada de um vértice e a remove da adjacência de trabalho.
        Permite rastrear corretamente arestas múltiplas.
        
        Args:
            node: índice do vértice
            
        Returns:
            DirectedEdge: a aresta encontrada, ou None se não houver arestas
        """
        if len(self.working_adj[node]) > 0:
            edge = self.working_adj[node].pop()  # Remove e retorna a última aresta
            return edge
        return None
    
    def _integrate_subtour(self, tour, subtour, start_node):
        """
        Integra um subtour na tour.
        Encontra o start_node em tour e insere o subtour (sem repetir start_node).
        """
        # Encontrar posição do start_node na tour
        pos = tour.index(start_node)
        
        # Inserir subtour (sem repetir o start_node que já está em tour)
        # subtour = [start_node, ..., start_node]
        # Queremos inserir os nós intermediários em ordem
        integrated = tour[:pos+1] + subtour[1:] + tour[pos+1:]
        
        return integrated

    def has_circuit(self):
        """
        Retorna se um circuito Euleriano existe no grafo.
        
        Returns:
            bool: True se existe circuito Euleriano, False caso contrário
        """
        return self.valid

    def get_circuit(self):
        """
        Retorna o circuito Euleriano encontrado.
        
        Returns:
            list: lista de vértices no circuito, ou lista vazia se não existe
        """
        return self.circuit if self.valid else []
    
    def get_subtours(self):
        """
        Retorna os subtours encontrados durante a execução.
        
        Returns:
            list: lista de subtours, cada um é uma lista de vértices
        """
        return self.subtours

    def __str__(self):
        """Representação em string do circuito."""
        if not self.valid:
            return "Nenhum circuito Euleriano existe neste grafo."
        
        s = "Circuito Euleriano encontrado:\n"
        s += " → ".join(str(v.__str__().replace("0", "a").replace("1", "b").replace("2", "c").replace("3", "d").replace("4", "e").replace("5", "f")) for v in self.circuit)
        
        # Mostrar subtours também
        if self.subtours:
            s += f"\n\nSubtours integrados ({len(self.subtours)} total):\n"
            for i, subtour in enumerate(self.subtours):
                s += f"  Subtour {i+1}: {' → '.join(str(v.__str__().replace("0", "a").replace("1", "b").replace("2", "c").replace("3", "d").replace("4", "e").replace("5", "f")) for v in subtour)}\n"
        
        return s
