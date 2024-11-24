import logging
from typing import Optional
from typing import List
import copy
from Graph import *

class GraphCommand:
    MERGE_COM = 'merge'
    SPLIT_COM = 'split'

    def __init__(self, command_type, vertices, graph_state=None):
        self.command_type = command_type  # 'merge' / 'split'
        self.vertices = vertices  # Вершины, участвующие в операции
        self.graph_state = graph_state  # Состояние графа до операции


class HistoryVertex:
    def __init__(self, hyperedge: Hyperedge, vertex: Vertex, prev_vertex_1: Optional[Vertex] = None, prev_vertex_2: Optional[Vertex] = None, new_edges = None, prev_edges = None):
        self.vertex = vertex
        self.prev_vertex_1 = prev_vertex_1
        self.prev_vertex_2 = prev_vertex_2
        if new_edges is None:
            self.new_edges = []
        else:
            self.new_edges = new_edges
        if prev_edges is None:
            self.prev_edges = []
        else:
            self.prev_edges = prev_edges
        self.hyperedge = hyperedge

    def __str__(self):
        return (f'V: {self.vertex} V1: {self.prev_vertex_1} V2: {self.prev_vertex_2}')


class HistoryManager:
    def __init__(self, graph: CombinedGraph):
        self.graph = graph
        self.base_state = copy.deepcopy(graph.get_state())
        self.history: List[HistoryVertex] = []
        self.current_step = -1

    def return_to_base_state(self):
        base_state_data = self.base_state
        self.graph.fill_vertices(base_state_data['vertices'])
        self.graph.fill_edges(base_state_data['edges'])
        self.graph.fill_hyperedges(base_state_data['hyperedges'])
        self.current_step = -1

    def write_step(self, vertex: HistoryVertex):
        self.history.append(vertex)
        self.current_step = len(self.history) - 1

    def next_step(self):
        if self.current_step >= len(self.history) - 1:
            return
        if self.current_step == -1:
            self.current_step = 0
        else:
            self.current_step += 1
        self.graph.add_vertex(self.history[self.current_step].vertex)
        self.graph.add_vertex_to_hyperedge(self.history[self.current_step].vertex, self.history[self.current_step].hyperedge)
        self.graph.remove_vertex(self.history[self.current_step].prev_vertex_1.name)
        self.graph.remove_vertex(self.history[self.current_step].prev_vertex_2.name)
        self.graph.remove_vertex_from_hyperedge(self.history[self.current_step].prev_vertex_1.name, self.history[self.current_step].hyperedge)
        self.graph.remove_vertex_from_hyperedge(self.history[self.current_step].prev_vertex_2.name, self.history[self.current_step].hyperedge)
        for new_edge in self.history[self.current_step].new_edges:
            self.graph.add_edge(new_edge)
        for prev_edge in self.history[self.current_step].prev_edges:
            self.graph.remove_edge(prev_edge)

    def prev_step(self):
        if self.current_step < 0:
            return
        if self.current_step == 0:
            self.return_to_base_state()
            return
        self.graph.remove_vertex(self.history[self.current_step].vertex.name)
        self.graph.remove_vertex_from_hyperedge(self.history[self.current_step].vertex.name, self.history[self.current_step].hyperedge)
        self.graph.add_vertex(self.history[self.current_step].prev_vertex_1)
        self.graph.add_vertex(self.history[self.current_step].prev_vertex_2)
        self.graph.add_vertex_to_hyperedge(self.history[self.current_step].prev_vertex_1, self.history[self.current_step].hyperedge)
        self.graph.add_vertex_to_hyperedge(self.history[self.current_step].prev_vertex_2, self.history[self.current_step].hyperedge)
        for prev_edge in self.history[self.current_step].prev_edges:
            self.graph.add_edge(prev_edge)
        for new_edge in self.history[self.current_step].new_edges:
            self.graph.remove_edge(new_edge)

        self.current_step -= 1


class LogManager:
    @staticmethod
    def setup_logging(log_file='graph_commands.log'):
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    @staticmethod
    def writeMerge(vertex1: Vertex, vertex2: Vertex, resultVertex: Vertex, datetime):
        log_message = f"Command: {GraphCommand.MERGE_COM:<10} | V1: {vertex1.name:<10} | V2: {vertex2.name:<10} | New_V: {resultVertex.name:<10} | Time: {datetime}"
        logging.info(log_message)

    @staticmethod
    def writeSplit(baseVertex: Vertex, vertex1: Vertex, vertex2: Vertex, datetime):
        log_message = f"Command: {GraphCommand.SPLIT_COM:<10} | Base V: {baseVertex.name:<10} | V1: {vertex1.name:<10} | V2: {vertex2.name:<10} | Time: {datetime}"
        logging.info(log_message)