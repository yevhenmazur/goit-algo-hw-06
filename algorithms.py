import networkx as nx
from collections import deque


def dfs_recursive(graph, vertex, visited=None, dfs_tree=None):
    if visited is None:
        visited = set()
    if dfs_tree is None:
        dfs_tree = nx.DiGraph()

    visited.add(vertex)
    for neighbor in graph[vertex]:
        if neighbor not in visited:
            dfs_tree.add_edge(vertex, neighbor)
            dfs_recursive(graph, neighbor, visited, dfs_tree)

    return dfs_tree


def bfs_recursive(graph, vertex, visited=None, bfs_tree=None, queue=None):
    if visited is None:
        visited = set()
    if bfs_tree is None:
        bfs_tree = nx.DiGraph()
    if queue is None:
        queue = deque([vertex])

    if not queue:
        return bfs_tree

    vertex = queue.popleft()
    if vertex not in visited:
        visited.add(vertex)
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                bfs_tree.add_edge(vertex, neighbor)
                queue.append(neighbor)
    return bfs_recursive(graph, queue[0] if queue else None, visited, bfs_tree, queue)


def dijkstra(graph, start):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    unvisited = list(graph.keys())

    while unvisited:
        current_vertex = min(unvisited, key=lambda vertex: distances[vertex])

        if distances[current_vertex] == float('infinity'):
            break

        for neighbor, weight in graph[current_vertex].items():
            distance = distances[current_vertex] + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance

        unvisited.remove(current_vertex)

    return distances

# Виклик функції для вершини A
# print(dijkstra(graph, 'A'))
