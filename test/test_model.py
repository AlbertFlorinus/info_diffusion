import unittest

try:
    from simulation.model import CommunicationNetwork, EntityNotFound
    
except ModuleNotFoundError:
    # Add simulation to path, coverage test/test_model from workspace dir otherwise might fail
    import sys
    sys.path.insert(1, 'simulation')
    from model import CommunicationNetwork
    from model import EntityNotFound

class ModelTest(unittest.TestCase):

    cn = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})
    def test_vertices(self):
        self.assertEqual(len(ModelTest.cn.vertices()), 4)
        self.assertEqual(ModelTest.cn.vertices('h1'), {'v1', 'v2'})
        self.assertEqual(ModelTest.cn.vertices('h2'), {'v2', 'v3'})
        self.assertEqual(ModelTest.cn.vertices('h3'), {'v3', 'v4'})

    def test_hyperedges(self):
        self.assertEqual(len(ModelTest.cn.hyperedges()), 3)
        self.assertEqual(ModelTest.cn.hyperedges('v1'), {'h1'})
        self.assertEqual(ModelTest.cn.hyperedges('v2'), {'h1', 'h2'})
        self.assertEqual(ModelTest.cn.hyperedges('v3'), {'h2', 'h3'})

    def test_check_if_hypergrah(self):
        self.assertIsInstance(ModelTest.cn, CommunicationNetwork)
    
    def test_correct_parameter(self):
        self.assertEqual(ModelTest.cn.__dict__["_hedges"].keys(), ModelTest.cn.__dict__["_timings"].keys())

    def test_d_regular(self):
        self.assertEqual(len(ModelTest.cn.hyperedges('v2')), 2)
        self.assertEqual(len(ModelTest.cn.hyperedges('v1')), 1)

    def test_2_colorable(self):
        pass

    def test_k_uniform(self):
        self.assertEqual(len(ModelTest.cn.vertices('h1')), 2)
        self.assertEqual(len(ModelTest.cn.vertices('h2')), 2)
        self.assertEqual(len(ModelTest.cn.vertices('h3')), 2)

    def test_raise_exceptions_vertices_wrong_hedge(self):
        
        with self.assertRaises(EntityNotFound):
            ModelTest.cn.hyperedges('hej')

    def test_raise_exceptions_vertices_no_hedge(self):
        cn_no_hedge = {'h1':[], 'h2':[]}
        with self.assertRaises(EntityNotFound) as k:
            ModelTest.cn.vertices('hej')
        
    

class ModelDataTest(unittest.TestCase):
    def test_model_with_data(self):
        communciation_network = CommunicationNetwork.from_json('./data/networks/microsoft.json')
        self.assertEqual(len(communciation_network.participants()), 37103)
        self.assertEqual(len(communciation_network.channels()), 309740)

        self.assertEqual(len(communciation_network.vertices()), 37103)
        self.assertEqual(len(communciation_network.hyperedges()), 309740)
