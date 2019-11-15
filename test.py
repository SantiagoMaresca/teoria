from proyecto import *

class TestKDTree(unittest.TestCase):
    def setUp(self):
        self.points = [
            (33, 23, 36, 47, 43),
            (12, 3, 31, 39, 4),
            (18, 32, 25, 32, 20),
            (35, 21, 40, 9, 27),
            (1, 19, 26, 11, 48),
            (30, 19, 24, 28, 19),
            (5, 23, 46, 13, 39),
            (49, 28, 29, 13, 6),
            (9, 4, 39, 21, 27),
            (41, 6, 25, 7, 18),
            (32, 1, 34, 14, 36)
        ]
        self.r = 2

    def test_large_tree(self):
        random.seed(8)
        print("Large point dataset...")
        many_points = [tuple(random.randint(0, 50) for j in range(20)) for i in range(1000)]
        print("Large tree...")
        many_r = 5
        kdrTree = makeKDRTree(many_points[:], many_r)
        print("Large search...")
        for point in many_points:
            self.assertTrue(searchKDRTree(kdrTree, many_r, point))
        for point in (tuple(random.randint(0, 50) for j in range(20)) for i in range(10000)):
            if point in many_points:
                self.assertTrue(searchKDRTree(kdrTree, many_r, point))
            else:
                self.assertFalse(searchKDRTree(kdrTree, many_r, point))


    def test_search_positive(self):
        kdrTree = makeKDRTree(self.points[:], self.r)
        for point in self.points:
            self.assertTrue(searchKDRTree(kdrTree, self.r, point))

    def test_search(self):
        kdrTree = makeKDRTree(self.points[:], self.r)
        random.seed(759334)
        for point in (tuple(random.randint(0, 50) for j in range(5)) for i in range(10000)):
            if point in self.points:
                self.assertTrue(searchKDRTree(kdrTree, self.r, point))
            else:
                self.assertFalse(searchKDRTree(kdrTree, self.r, point))

    def test_built_tree(self):
        kdTreeDone = makeKDRTree(self.points[:], self.r)
        self.assertEqual(kdTreeDone[0], [30, 19])
        self.assertEqual(kdTreeDone[1], makeKDRTree([self.points[i] for i in [1, 8]], self.r, dim=2))
        self.assertEqual(kdTreeDone[1][0], [39,39]) # puntos:[1, 8]], dim=2,3

        self.assertEqual(kdTreeDone[2], makeKDRTree([self.points[i] for i in [2, 4, 6]], self.r, dim=2))
        self.assertEqual(kdTreeDone[2][0], [26, 13]) # puntos:[2, 4, 6]], dim=2,3

        self.assertEqual(kdTreeDone[3], makeKDRTree([self.points[i] for i in [9, 10]], self.r, dim=2))
        self.assertEqual(kdTreeDone[3][0], [34, 14]) # puntos:[9, 10]], dim=2,3

        self.assertEqual(kdTreeDone[4], makeKDRTree([self.points[i] for i in [0, 3, 5, 7]], self.r, dim=2))
        self.assertEqual(kdTreeDone[4][0], [36, 28]) # puntos:[0, 3, 5, 7]], dim=2,3
        self.assertEqual(kdTreeDone[4][1], makeKDRTree([self.points[i] for i in [7]], self.r, dim=4))
        self.assertEqual(makeKDRTree([self.points[i] for i in [7]], self.r, dim=4), (self.points[7],))

        self.assertEqual(kdTreeDone[4][2], makeKDRTree([self.points[i] for i in [5]], self.r, dim=4))
        self.assertEqual(makeKDRTree([self.points[i] for i in [5]], self.r, dim=4), (self.points[5],))

        self.assertEqual(kdTreeDone[4][3], makeKDRTree([self.points[i] for i in [3]], self.r, dim=4))
        self.assertEqual(makeKDRTree([self.points[i] for i in [3]], self.r, dim=4), (self.points[3],))

        self.assertEqual(kdTreeDone[4][4], makeKDRTree([self.points[i] for i in [0]], self.r, dim=4))
        self.assertEqual(makeKDRTree([self.points[i] for i in [0]], self.r, dim=4), (self.points[0],))


if __name__ == '__main__':
    unittest.main()