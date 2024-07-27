import networkx as nx

# Зчитування графу з файлу DOT
graph = nx.drawing.nx_pydot.read_dot('dependency_graph.dot')

# Конвертація у формат JSON
data = nx.node_link_data(graph)

# Запис у файл JSON
import json
with open('dependency_graph.json', 'w') as f:
    json.dump(data, f, indent=4)