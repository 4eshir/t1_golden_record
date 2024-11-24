import csv
import random
from Graph import *

class LoadWizard:
    @staticmethod
    def parse_csv(file_path, N = -1):
        vertices_list = []

        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            headers = next(csv_reader)  # Пропустить заголовок
            counter = 0
            for row in csv_reader:
                if counter >= N and N != -1:  # Проверка, достигли ли мы N записей
                    break
                counter += 1
                properties_list = []
                for header, value in zip(headers, row):
                    # Создаем объект Property и добавляем его в список
                    properties_list.append(Property(name=header, value=value))
                vertices_list.append(Vertex(str(counter), properties_list))

        return vertices_list

    @staticmethod
    def create_edges_and_hyperedges(graph: CombinedGraph, num_edges_per_vertex: int, vertices_per_hyperedge: int):
        vertices_list = list(graph.vertices)  # Преобразуем множество в список
        num_vertices = len(vertices_list)

        counter = 1
        # Генерация рёбер Edge
        for vertex in vertices_list:
            for _ in range(num_edges_per_vertex):
                # Выбираем случайную вершину, отличную от текущей
                vertex2 = random.choice([v for v in vertices_list if v != vertex])
                weight = random.randint(1, 10)  # Случайный вес
                edge = Edge(counter, vertex1=vertex, vertex2=vertex2, weight=weight)
                vertex.add_edge(edge)
                vertex2.add_edge(edge)
                graph.edges.append(edge)
                counter += 1

        # Генерация гиперрёбер Hyperedge
        all_vertices = list(vertices_list)
        random.shuffle(all_vertices)  # Перетасовываем все вершины

        # Создаем гиперрёбра
        for i in range(0, num_vertices, vertices_per_hyperedge):
            hyperedge_vertices = all_vertices[i:i + vertices_per_hyperedge]
            if len(hyperedge_vertices) < vertices_per_hyperedge:
                break  # Если недостаточно вершин для гиперребра, выходим

            agr_weight = random.randint(1, 10)  # Пример агрегатного веса
            mark = random.randint(1, 5)  # Пример отметки
            hyperedge = Hyperedge((i + 1), vertices=hyperedge_vertices, agr_weight=agr_weight, mark=mark)
            graph.hyperedges.append(hyperedge)