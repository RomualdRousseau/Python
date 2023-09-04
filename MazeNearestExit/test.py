import unittest
import itertools as it

from main import maze_to_graph, is_exit, is_connected, graph_bfs

class TestMazeFunctions(unittest.TestCase):
    def setUp(self):
        self.maze = [["+", "+", ".", "+"], [".", ".", ".", "+"], ["+", "+", "+", "."]]

    def test_is_exit(self):
        self.assertTrue(is_exit(self.maze, 0, 0))
        self.assertTrue(is_exit(self.maze, 3, 0))
        self.assertTrue(is_exit(self.maze, 0, 2))
        self.assertFalse(is_exit(self.maze, 1, 1))

    def test_is_connected(self):
        self.assertTrue(is_connected(self.maze, 0, 0, 1, 0))
        self.assertTrue(is_connected(self.maze, 1, 1, 1, 2))
        self.assertFalse(is_connected(self.maze, 1, 1, 2, 2))

    def test_maze_to_graph(self):
        expected_graph = [[
            (False, False, 0), (True, False, 1), (False, True, 1), (False, False, 0)
        ], [
            (True, False, 1), (False, False, 0), (True, False, 1), (False, True, 1)
        ], [
            (False, True, 1), (True, False, 1), (False, False, 0), (True, False, 1)
        ]]

        graph = maze_to_graph(self.maze)
        self.assertEqual(graph, expected_graph)

    def test_graph_bfs(self):
        graph = maze_to_graph(self.maze)
        result, hits = graph_bfs(graph, 3)
        self.assertEqual(result, 6)
        self.assertEqual(hits, 2)

if __name__ == '__main__':
    unittest.main()
