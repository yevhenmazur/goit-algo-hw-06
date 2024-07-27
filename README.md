# goit-algo-hw-06
Homework: Graphs
У якості об'єктного графу я згенерував граф залежностей systemd юнатів на своєму комп'ютері за допомогою команд systemd-analyze dot | dot -Tsvg > dependency_graph.svg і systemd-analyze dot > dependency_graph.dot

dependency_graph.dot перетворюю у структуру данних python за допомогою networkx 