import unittest

from simulation.model import CommunicationNetwork
from simulation.model import EntityNotFound
from simulation.minimal_paths import single_source_dijkstra_vertices, single_source_dijkstra_hyperedges, DistanceType


class MinimalPath(unittest.TestCase):
    cn = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})

    
    ### vertex tests ###

    def test_shortest_path_vertex(self):
        self.assertEqual(single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0), {'v2': 1, 'v3': 2, 'v4': 3})

    def test_fastest_path_vertex(self):
        self.assertEqual(single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.FASTEST, min_timing=0), {'v2': 0, 'v3': 1, 'v4': 2})

    def test_foremost_path_vertex(self):
        self.assertEqual(single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.FOREMOST, min_timing=0), {'v2': 1, 'v3': 2, 'v4': 3})

    ### hyperedge tests ###

    def test_shortest_path_hyperedge(self):
        self.assertEqual(single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0), {'v2': 1, 'v3': 2, 'v4': 3})

    def test_fastest_path_hyperedge(self):
        self.assertEqual(single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.FASTEST, min_timing=0), {'v2': 0, 'v3': 1, 'v4': 2})

    def test_foremost_path_hyperedge(self):
        self.assertEqual(single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.FOREMOST, min_timing=0), {'v2': 1, 'v3': 2, 'v4': 3})

    ### equivalence tests ###

    def test_equivalence_shortest_path_implementation(self):
        result_1 = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')

    def test_equivalence_fastest_path_implementation(self):
        result_1 = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.FASTEST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.FASTEST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')

    def test_equivalence_foremost_path_implementation(self):
        result_1 = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.FOREMOST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.FOREMOST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')

    ### edge-case/error handling tests ###

    def test_none_communication_network(self):
        with self.assertRaises(AttributeError):
            single_source_dijkstra_vertices(None, 'v1', DistanceType.SHORTEST, min_timing=0)

    def test_nonexistent_start_vertex(self):
        with self.assertRaises(EntityNotFound):
            single_source_dijkstra_vertices(MinimalPath.cn, 'v5', DistanceType.SHORTEST, min_timing=0)

    def test_nonexistent_path(self):
        no_path_to_v5 = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4'], 'h4': ['v5']}, {'h1': 1, 'h2': 2, 'h3': 3, 'h4': 4})
        self.assertNotIn("v5", single_source_dijkstra_vertices(no_path_to_v5, 'v1', DistanceType.SHORTEST, min_timing=0))

    def test_invalid_distance_type(self):
        with self.assertRaises(UnboundLocalError):
            single_source_dijkstra_vertices(MinimalPath.cn, 'v1', "InvalidDistanceType", min_timing=0)
