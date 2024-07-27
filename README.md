# goit-algo-hw-06
Homework: Graphs
У якості об'єктного графу я згенерував граф залежностей systemd юнітів на робочій ОС свого комп'ютера за допомогою команд `systemd-analyze dot | dot -Tsvg > dependency_graph.svg` і `systemd-analyze dot > dependency_graph.dot`

dependency_graph.dot перетворюю у структуру данних python за допомогою networkx 

Утворений граф містить 203 вузли і 1395 ребер
Це складний для візуалізації граф, тому я написав функцію format_labels_for_viz(graph), яка видаляє неінформативні частини лейьлів, щоб вони не загромаджували візуалізацію.

Для того щоб побачити візуалізацію запустіть скрипт з ключем `-viz` або `--vizualization`
`python ./main.py -viz`

Для виведення короткого опису графу використовуйте ключ `-s` або `--statistic`
`python ./main.py -s`