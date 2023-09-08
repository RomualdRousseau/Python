import unittest
import itertools as it


def is_exit(maze, x, y):
    m = len(maze)
    n = len(maze[0])
    return x == 0 or x == (n - 1) or y == 0 or y == (m - 1)


def is_connected(maze, x1, y1, x2, y2):
    m = len(maze)
    n = len(maze[0])
    e1 = maze[y1][x1]
    e2 = maze[y2][x2]
    if e1 != "." or e2 != ".":
        return False
    else:
        return abs(x2 - x1) == 1 and y1 == y2 or abs(y2 - y1) == 1 and x1 == x2


def maze_to_graph(maze):
    m = len(maze)
    n = len(maze[0])
    return [
        [
            (is_connected(maze, a[1], a[0], b[1], b[0]), is_exit(maze, b[1], b[0]))
            for b in it.product(range(m), range(n))
        ]
        for a in it.product(range(m), range(n))
    ]


def graph_bfs(graph, s):
    n = len(graph)

    res = []
    hits = [0 for i in range(n)]

    queue = []
    visited = [False for i in range(n)]

    queue.append(s)
    visited[s] = True

    while len(queue) > 0:
        i = queue.pop(0)
        for j in range(n):
            if graph[i][j][0] and not visited[j]:
                hits[j] = max(hits[i] + 1, hits[j])
                if graph[i][j][1]:
                    res.append(j)
                queue.append(j)
                visited[j] = True

    if len(res) > 0:
        return res[0], hits[res[0]]
    else:
        return -1, -1


def nearest_exit(maze, s):
    n = len(maze[0])
    x = s[0] * n + s[1]
    _, s = graph_bfs(maze_to_graph(maze), x)
    return s


class Test_NearestExit(unittest.TestCase):
    def test_example1(self):
        input = [["+", "+", ".", "+"], [".", ".", ".", "+"], ["+", "+", "+", "."]]
        entrance = (1, 2)
        expected = 1
        result = nearest_exit(input, entrance)
        self.assertEqual(result, expected)

    def test_example2(self):
        maze = [["+", "+", "+"], [".", ".", "."], ["+", "+", "+"]]
        entrance = (1, 0)
        expected = 2
        result = nearest_exit(maze, entrance)
        self.assertEqual(result, expected)

    def test_example3(self):
        maze = [[".", "+"]]
        entrance = (0, 0)
        expected = -1
        result = nearest_exit(maze, entrance)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
