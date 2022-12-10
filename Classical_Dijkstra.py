from collections import defaultdict
import heapq
from time import time


def Dij_generator():
    """
    Returns:
    graph_object: variable containing network information.
    """
    try:
        filename = r'C:\Users\kesha\Documents\Projects\DAA_Sem 5\\ChicagoSketch_net.tntp'
        with open(filename, 'r') as file:
            lines = [line.rstrip() for line in file]

        data_lines = lines[9:]
        adjacency_list = defaultdict(list)


        for line in data_lines:
            if line:
                line_as_list = line.rsplit('\t')
                init_node = int(line_as_list[1])
                term_node = int(line_as_list[2])
                length = float(line_as_list[5])
                # print(f'{init_node} {term_node} {length}')
                if init_node in adjacency_list:
                    adjacency_list[init_node].append([term_node, length])
                else:
                    adjacency_list[init_node] = [[term_node, length]]
                # adjacency_matrix[init_node][term_node] = length
        ## adjacency list is the intended graph object for q1  
        graph_object = adjacency_list
        return graph_object
    except:
        return graph_object


def Q1_dijkstra(source: int, destination: int, graph_object) -> int:
    """
    Dijkstra's algorithm.

    Args:
        source (int): Source stop id
        destination (int): : destination stop id
        graph_object: python object containing network information

    Returns:
        shortest_path_distance (int): length of the shortest path.

    Warnings:
        If the destination is not reachable, function returns -1
    """
    
    shortest_path_distance = -1
    try:
        minHeap = [(0, source)]
        visit = set()
        while minHeap:
            w1, n1 = heapq.heappop(minHeap)
            if n1 == destination:
                shortest_path_distance =  w1
                return shortest_path_distance

            if n1 in visit:
                continue
            visit.add(n1)

            for n2, w2 in graph_object[n1]:
                if n2 not in visit: 
                    heapq.heappush(minHeap, (w1+w2, n2))
    except:
        return shortest_path_distance

graph_object = Dij_generator()


def evaluate_Q1(sample_input1):
    marks = 0
    avg_runtime = 1
    graph_object = None
    try:
        graph_object = Dij_generator()
        start_time = time()
        candidate_output = [round(Q1_dijkstra(source, destination, graph_object)) for source, destination in sample_input1]
        print(candidate_output)
        avg_runtime = avg_runtime + (time() - start_time) / len(sample_input1)
        if candidate_output == output_Q1Q2:
            print("Output verified. Source to destination is same as manually calculated.")
    except:
        pass
    return graph_object, avg_runtime

def main():
    print("Running Unidirectional Dijkstra: ")
    graph_object, avg_runtime = evaluate_Q1(input_Q1Q2)
    print(f"Avg Runtime in seconds for Q1: {avg_runtime}")


if __name__ == "__main__":
    input_Q1Q2 = [(253, 127), (139, 305), (148, 99), (363, 134), (778, 396), (650, 759), (724, 547), (788, 412), (105, 1)]
    output_Q1Q2 = [38, 59, 29, 76, 30, 70, 53, 59, 51]
    output3 = [2, 1, 0, 0, 1, 1]
    marksQ1, marksQ2, marksQ3 = 2, 4, 4
    main()
