from MergeWizard import *
from Visualization import *
from History import *
from LoadAdapter import *
import time

def test():
    graph = CombinedGraph()
    A = Vertex('A')
    B = Vertex('B')
    C = Vertex('C')
    D = Vertex('D')
    E = Vertex('E')
    vertices_arr = [A, B, C, D, E]
    edgeAB = Edge(1, A, B, 2)
    edgeAC = Edge(2, A, C, 1)
    edgeCB = Edge(3, C, B, 3)
    edgeCD = Edge(4, C, D, 5)
    edgeCE = Edge(5, C, E, 4)
    edgeEB = Edge(6, E, B, 6)
    edgeED = Edge(7, E, D, 8)
    edgeBD = Edge(8, B, D, 7)
    edges_arr = [edgeAB, edgeAC, edgeCB, edgeCD, edgeCE, edgeEB, edgeED, edgeBD]
    hyperedges_arr = []
    hyperedges_arr.append(Hyperedge(1, [A, C, D]))
    hyperedges_arr.append(Hyperedge(2, [B, E]))
    GraphVisual.graph_output(
        GraphVisual.vertex_adapter(vertices_arr),
        GraphVisual.edge_adapter(edges_arr),
        GraphVisual.hyperedge_adapter(hyperedges_arr)
    )

    graph.fill_vertices([A, B, C, D, E])
    graph.fill_edges({edgeAB, edgeAC, edgeCB, edgeCD, edgeCE, edgeEB, edgeED, edgeBD})
    graph.fill_hyperedges(hyperedges_arr)
    print(graph)

    '''
    graph.collapse_hyperedge(graph.hyperedges[0])
    print(graph)

    '''
    history = HistoryManager(graph)

    historyDE = MergeWizard.MergeWizard.merge_pair_vertices(D, E, graph)
    history.write_step(historyDE)
    print(graph)

    historyCDE = MergeWizard.MergeWizard.merge_pair_vertices(historyDE.vertex, C, graph)
    history.write_step(historyCDE)
    print(graph)

    historyDECA = MergeWizard.MergeWizard.merge_pair_vertices(historyCDE.vertex, A, graph)
    history.write_step(historyDECA)
    print(graph)

    '''
    history.prev_step()
    history.prev_step()
    history.prev_step()
    print(graph)
    history.next_step()
    history.next_step()
    history.next_step()
    print(graph)
    '''

def dataset_test():
    v_count = 5000
    e_count = 10
    he_count = 500

    graph = CombinedGraph()
    start_time = time.time()
    vertices = LoadWizard.parse_csv('15k.csv', v_count)
    end_time = time.time()
    print(f'Время парсинга файла: {end_time - start_time}с.')


    start_time = time.time()
    graph.fill_vertices(vertices)
    LoadWizard.create_edges_and_hyperedges(graph, e_count, he_count)
    end_time = time.time()
    print(f'Время создания {v_count} вершин, генерации {e_count * v_count} ребер и {round(v_count / he_count)} гиперребер: {end_time - start_time}с.')

    count = 4000
    start_time = time.time()
    MergeWizard.fake_merges(graph, count)
    end_time = time.time()
    print(f'Время тестового мерджа {count} вершин: {end_time - start_time}с.')


if __name__ == '__main__':
    LogManager.setup_logging()
    test()
    #dataset_test()
