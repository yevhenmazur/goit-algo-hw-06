import argparse
import sys
import networkx as nx
import matplotlib.pyplot as plt
import re

def parse_args():
    '''Describing the command line arguments'''
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-viz", "--vizualization", action='store_true', help="Візуалізувати граф")
    parser.add_argument("-s", "--statistic", action='store_true', help="Вивести статистику графу")
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

def graph_basic_stats(graph):
    
    # nodes_count = graph.number_of_nodes()
    # edges_count = graph.number_of_edges()
    # result = f"Grapf {graph} has: \n {nodes_count} nodes \n {edges_count} edges"
    result = f"{graph}"
    return result

def main():
    
    # Зчитую граф з файлу DOT
    G = nx.drawing.nx_pydot.read_dot('dependency_graph.dot')
    args = parse_args()
    if args.vizualization:
        visualize_graph(G)
    elif args.statistic:
        print(G)
    

if __name__ == "__main__":
    main()