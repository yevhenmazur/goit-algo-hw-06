import argparse
import sys
import networkx as nx
import matplotlib.pyplot as plt
import re
from anytree import Node, RenderTree

def parse_args():
    '''Describing the command line arguments'''
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-viz", "--vizualization", action='store_true', help="Візуалізувати граф")
    parser.add_argument("-stat", "--statistic", action='store_true', help="Вивести статистику графу")
    parser.add_argument("--dfs", action='store_true', help="Обхід графа за допомогою пошуку в глибину")
    parser.add_argument("--bfs", action='store_true', help="Обхід графа за допомогою пошуку в ширину")
    parser.add_argument("-t", "--test", action='store_true', help="test")
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    return parser.parse_args()

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
        # Зберегти форматований лейбл
        formatted_labels[node] = cleaned_label
    
    return formatted_labels

def visualize_graph(graph):
    '''Builds a visualization of the graph'''

    plt.figure(figsize=(12, 12))
    pos = nx.kamada_kawai_layout(graph) # <- дуже прогресивний лейаут
    labels = format_labels_for_viz(graph)

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
    
    nx.draw(graph, pos, **options)
    plt.show()
    return True

def find_init_node(graph):
    '''Bootstrapping starts from the node pointed to by the minimum number of edges. This function returns this node.'''
    # Фільтруємо вузли, щоб ігнорувати "init.scope"
    filtered_nodes = [(node, in_deg) for node, in_deg in graph.in_degree() if node != "init.scope"]
    
    # Якщо всі вузли були відфільтровані, повертаємо None або інше значення за замовчуванням
    if not filtered_nodes:
        return None

    root_node = min(filtered_nodes, key=lambda x: x[1])[0]
    return root_node

# def dfs(graph):
#     source = find_init_node(graph)
#     dfs_tree = nx.dfs_tree(graph, source=source)
#     return dfs_tree

# def bfs(graph):
#     source = find_init_node(graph)
#     bfs_tree = nx.bfs_tree(graph, source=source)
#     return bfs_tree

# def graph_traversal(graph, algorithm):
#     source = find_init_node(graph)
#     if algorithm == "bfs":
#         tree = nx.bfs_tree(graph, source=source)
#     if algorithm == "dfs":
#         tree = nx.dfs_tree(graph, source=source)
#     else:
#         tree = None
#     return tree

def build_anytree(graph, algorithm):
    source = find_init_node(graph)
    if algorithm == "bfs":
        tree = nx.bfs_tree(graph, source=source)
    elif algorithm == "dfs":
        tree = nx.dfs_tree(graph, source=source)
    else:
        return None

    # Створюємо вузли для дерева
    nodes = {}
    for node in tree.nodes:
        if node not in nodes:
            nodes[node] = Node(node)
        for child in tree.successors(node):
            if child not in nodes:
                nodes[child] = Node(child, parent=nodes[node])
            else:
                nodes[child].parent = nodes[node]

    # Повертаємо кореневий вузол
    return nodes[find_init_node(graph)]

def print_tree(tree_root):
    # Друкуємо дерево у терміналі
    for pre, fill, node in RenderTree(tree_root):
        print("%s%s" % (pre, node.name))

def main():
    
    # Зчитую граф з файлу DOT
    G = nx.drawing.nx_pydot.read_dot('dependency_graph.dot')

    args = parse_args()
    if args.vizualization:
        visualize_graph(G)
    if  args.statistic:
        print(G)
    if args.dfs:
        tree_root = build_anytree(G, algorithm='dfs')
        print_tree(tree_root)
    if args.bfs:
        tree_root = build_anytree(G, algorithm='bfs')
        print_tree(tree_root)

if __name__ == "__main__":
    main()