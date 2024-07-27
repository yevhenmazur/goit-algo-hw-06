import networkx as nx
import matplotlib.pyplot as plt
import re

def format_labels_for_viz(graph):
    '''This function removes uninformative parts of graph labels to simplify visualization'''
    formatted_labels = {}
    remove_words = ["service", "target", "device", "swap", "socket", "mount"]
    
    for node in graph.nodes:
        # Розділити лейбл вузла за роздільниками
        label_parts = re.split(r'[\\|:|@]', node)
        # Взяти останню частину після роздільника
        cleaned_label = label_parts[-1]
        # Видалити небажані слова
        for word in remove_words:
            cleaned_label = cleaned_label.replace(word, "")
            cleaned_label = cleaned_label.rstrip('.')
        # Видалити зайві пробіли
        cleaned_label = cleaned_label.strip()
        # Зберегти форматований лейбл
        formatted_labels[node] = cleaned_label
    
    return formatted_labels


# Зчитую граф з файлу DOT
G = nx.drawing.nx_pydot.read_dot('dependency_graph.dot')

plt.figure(figsize=(12, 12))
pos = nx.kamada_kawai_layout(G) # <- дуже прогресивний лейаут
labels = format_labels_for_viz(G)

options = {
    "node_color": "blue",
    "edge_color": "gray",
    "node_size": 100,
    "labels": labels,
    "alpha": 0.7,
    "with_labels": True,
    "font_size": 8,
    "font_color": "black"
}

nx.draw(G, pos, **options)
plt.show()

# print(G.number_of_nodes())
# print(G.number_of_edges())

