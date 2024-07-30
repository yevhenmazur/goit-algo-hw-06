import argparse
import sys
import networkx as nx
import matplotlib.pyplot as plt
import re
from anytree import Node, RenderTree
from algorithms import dfs_recursive, bfs_recursive, dijkstra


def parse_args():
    '''Describing the command line arguments'''
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-viz", "--vizualization",
                        action='store_true', help="Візуалізувати граф")
    parser.add_argument("-stat", "--statistic",
                        action='store_true', help="Вивести статистику графу")
    parser.add_argument("--dfs", action='store_true',
                        help="Відобразити дерево за допомогою обходу графа в глибину")
    parser.add_argument("--bfs", action='store_true',
                        help="Відобразити дерево за допомогою обходу графа в ширину")
    parser.add_argument("-d", "--dijkstra", type=str, nargs='?', const='graphical.target',
                        help="Відображає найкоротший шлях до вказаної ноди (за замовчуванням 'graphical.target')")
    if len(sys.argv) == 1:
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
    pos = nx.kamada_kawai_layout(graph)  # <- дуже прогресивний лейаут
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
    filtered_nodes = [(node, in_deg)
                      for node, in_deg in graph.in_degree() if node != "init.scope"]

    # Якщо всі вузли були відфільтровані, повертаємо None
    if not filtered_nodes:
        return None

    root_node = min(filtered_nodes, key=lambda x: x[1])[0]
    return root_node


def build_anytree(graph, algorithm):
    source = find_init_node(graph)
    if algorithm == "bfs":
        tree = bfs_recursive(graph, source)
    elif algorithm == "dfs":
        tree = dfs_recursive(graph, source)
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
    '''Print the tree in the terminal'''
    for pre, fill, node in RenderTree(tree_root):
        print("%s%s" % (pre, node.name))


def add_weights_to_edges(graph, dependency_weights):
    '''Function for adding weights to edges'''
    weighted_graph = nx.DiGraph()

    for u, v, data in graph.edges(data=True):
        dependency_type = data.get('dependency', 'Requires')
        weight = dependency_weights.get(dependency_type, 1)
        weighted_graph.add_edge(u, v, weight=weight)

    return weighted_graph


def main():

    # Зчитую граф з файлу DOT
    G = nx.drawing.nx_pydot.read_dot('dependency_graph.dot')

    DEPENDENCY_WEIGHTS = {
        'Requires': 1,
        'Wants': 3,
        'Before': 10,
        'After': 10,
        'Conflicts': 1000,
    }
    args = parse_args()
    if args.vizualization:
        visualize_graph(G)
    if args.statistic:
        print(G)
    if args.dfs:
        tree_root = build_anytree(G, algorithm='dfs')
        print_tree(tree_root)
    if args.bfs:
        tree_root = build_anytree(G, algorithm='bfs')
        print_tree(tree_root)
    if args.dijkstra:
        weighted_G = add_weights_to_edges(G, DEPENDENCY_WEIGHTS)
        #  Переводжу граф у формат словника, бо так треба для цієї реалізації алгоритму Дейкстри
        weighted_G_dict = {}
        for node in weighted_G.nodes():
            weighted_G_dict[node] = {neighbor: data['weight']
                                     for neighbor, data in weighted_G[node].items()}
        source = find_init_node(weighted_G)
        target_node = args.dijkstra
        shortest_paths = dijkstra(weighted_G_dict, source)
        print(f"Відстань між вершинами {source} та {
              target_node} - {shortest_paths[target_node]}")


if __name__ == "__main__":
    main()
