import heapq

class Graph:
    def __init__(self):             # initializes the graph with incoming and outgoing nodes
        self.nodes = set()
        self.incoming = dict()
        self.outgoing = dict()
        self.edges = 0

    def add_node(self, node):
        if node in self.nodes:
            return
        self.nodes.add(node)
        self.incoming[node] = dict()
        self.outgoing[node] = dict()

    def add_edge(self, dest, begin, weight): 
        if dest not in self.nodes:
            self.add_node(dest)
        if begin not in self.nodes:
            self.add_node(begin)
        self.incoming[dest][begin] = weight
        self.outgoing[begin][dest] = weight
        self.edges += 1

    def return_edge_weight(self, dest, begin):
        if dest not in self.nodes:
            return -1
        if begin not in self.nodes:
            return -1
        if begin not in self.incoming[dest].keys():
            return -1
        return self.incoming[dest][begin]

    def return_outgoing_node(self, node):
        if node not in self.nodes:
            return []
        return self.outgoing[node].keys()

    def return_incoming_node(self, node):
        if node not in self.nodes:
            return []
        return self.incoming[node].keys()

class HeapEntry:
    def __init__(self, node, priority):
        self.node = node
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

def bidirectional_dij(source: int, destination: int, graph_object) -> int:
    """
    Bi-directional Dijkstra's algorithm.
    Args:
        source (int): Source stop id
        destination (int): destination stop id
        graph_object: python object containing network information
    Returns:
        shortest_path_distance (int): length of the shortest path.
    Warnings:
        If the destination is not reachable, function returns -1
    """
    shortest_path_distance = -1

    try:
        def traversal(target, outgoing):
            path = []
            while target:
                path.append(target)
                target = outgoing[target]
            return list(reversed(path))


        def reversal(n1, n1_outgoing, n2_outgoing):
            path = traversal(n1, n1_outgoing)
            n1 = n2_outgoing[n1]
            while n1:
                path.append(n1)
                n1 = n2_outgoing[n1]
            return path

        def bidirectional_dijkstra(graph, source, target):
            traversal_n1 = [HeapEntry(source, 0.0)]
            traversal_n2 = [HeapEntry(target, 0.0)]
            n1_visit = set()
            n2_visit = set()
            n1_outgoing = dict()
            n2_outgoing = dict()
            distance_from_n1 = dict()
            distance_from_n2 = dict()
            best_path_length = {'value': 1e9}
            n1 = {'value': None}
            n1_outgoing[source] = None
            n2_outgoing[target] = None
            distance_from_n1[source] = 0.0
            distance_from_n2[target] = 0.0


            def update_forward_frontier(node, node_weight):
                if node in n2_visit:
                    path_length = distance_from_n2[node] + node_weight

                    if best_path_length['value'] > path_length:
                        best_path_length['value'] = path_length
                        n1['value'] = node


            def update_backward_frontier(node, node_weight):
                if node in n1_visit:
                    path_length = distance_from_n1[node] + node_weight

                    if best_path_length['value'] > path_length:
                        best_path_length['value'] = path_length
                        n1['value'] = node


            def forward_frontier():
                current = heapq.heappop(traversal_n1).node
                n1_visit.add(current)
                for outgoing_node in graph.return_incoming_node(current):
                    if outgoing_node in n1_visit:
                        continue
                    
                    w1 = distance_from_n1[current] + graph.return_edge_weight(current, outgoing_node)
                    if outgoing_node not in distance_from_n1.keys() or w1 < distance_from_n1[outgoing_node]:
                        distance_from_n1[outgoing_node] = w1
                        n1_outgoing[outgoing_node] = current
                        heapq.heappush(traversal_n1, HeapEntry(outgoing_node, w1))
                        update_forward_frontier(outgoing_node, w1)


            def backward_frontier():
                current = heapq.heappop(traversal_n2).node
                n2_visit.add(current)
                for incoming_node in graph.return_outgoing_node(current):
                    if incoming_node in n2_visit:
                        continue

                    w1 = distance_from_n2[current] + graph.return_edge_weight(incoming_node, current)
                    if incoming_node not in distance_from_n2.keys() or w1 < distance_from_n2[incoming_node]:
                        distance_from_n2[incoming_node] = w1
                        n2_outgoing[incoming_node] = current
                        heapq.heappush(traversal_n2, HeapEntry(incoming_node, w1))
                        update_backward_frontier(incoming_node, w1)

            while traversal_n1 and traversal_n2:
                tmp = distance_from_n1[traversal_n1[0].node] + distance_from_n2[traversal_n2[0].node]
                if tmp >= best_path_length['value']:
                    return reversal(n1['value'], n1_outgoing, n2_outgoing)
                if len(traversal_n1) + len(n1_visit) < len(traversal_n2) + len(n2_visit):
                    forward_frontier()
                else:
                    backward_frontier()
            return []


        def path_cost(graph, path):
            cost = 0.0
            for i in range(len(path) - 1):
                dest = path[i]
                begin = path[i + 1]
                cost += graph.return_edge_weight(dest, begin)
            return cost


        graph = Graph()
        for node in range(1, len(graph_object)+1):
            for i in graph_object[node]:
                graph.add_edge(node, i[0], i[1])
        
        pathlen = bidirectional_dijkstra(graph, source, destination)
        shortest_path_distance = path_cost(graph, pathlen)
        return shortest_path_distance

    except:
        return shortest_path_distance

