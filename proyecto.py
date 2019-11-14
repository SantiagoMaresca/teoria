import itertools as it
import random

import unittest

def at(point, i):
    return point[i % len(point)]

def searchKDTree(kdTree, point, dim = 0):
    if len(kdTree) == 1:
        return kdTree[0] == point
    nodeValue, left, right = kdTree
    nextDim = (dim + 1) % len(point)
    nextTree = left if point[dim] < nodeValue else right
    return searchKDTree(nextTree, point, nextDim)

def makeKDTree(points, dim = 0):
    if not points:
        return None # Empty trees are None
    elif len(points) == 1:
        return tuple(points) # Leaf nodes have one point.
    points.sort(key = lambda p: p[dim])
    medianIndex = len(points) // 2
    median = points[medianIndex][dim]
    nextDim = (dim + 1) % len(points[medianIndex])
    left = [p for p in points if p[dim] < median]
    right = [p for p in points if p[dim] >= median]
    return (median, makeKDTree(left, nextDim), makeKDTree(right, nextDim))

def getMedians(points, r, dim):
    """Se obtienen las r medianas desde dim"""
    medians = [None] * r
    for i in range(r):
        points.sort(key = lambda p: at(p, dim+i))
        medians[i] = at(points[len(points) // 2], dim+i)
    return medians

def matches_criteria(criteria, medians, point, dim):
    for i, c in enumerate(criteria):
        leq = at(point, dim+i) < medians[i]
        # Si con c=False queremos < a mediana.
        # No hay match si queremos < y es > o al revés.
        # Esto coincide con c == leq
        if (c == leq):
            return False
    return True

def makeKDRTree(points, r, dim = 0):
    if not points:
        return None # Empty trees are None
    elif len(points) == 1:
        return tuple(points) # Leaf nodes have one point.

    # Obtenemos las r medianas, para las dimensiones dim, dim+1, ..., dim+(r-1)
    medians = getMedians(points, r, dim)

    partitions = [None] * (2**r + 1) # Tendremos 2**r particiones (hijos)
    partitions[0] = medians
    i = 1
    for criteria in it.product([False, True], repeat = r):  # 2^r iteraciones
        partition = [p for p in points if matches_criteria(criteria, medians, p, dim)] # n iteraciones
        partitions[i] = makeKDRTree(partition, r, (dim+r) % len(points[0]))
        i += 1

    return tuple(partitions)

def searchKDRTree(kdrTree, r, point, dim = 0):
    if (kdrTree is None):
        return False
    elif len(kdrTree) == 1:
        return kdrTree[0] == point

    medians = kdrTree[0]
    i = 1
    for criteria in it.product([False, True], repeat = r):  # 2^r iteraciones
        if (matches_criteria(criteria, medians, point, dim)):
            # go to this subtree
            chosen_subtree = kdrTree[i]
            return searchKDRTree(chosen_subtree, r, point, (dim+r) % len(point))
        i += 1

    return False


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
        many_points = [tuple(random.randint(0, 50) for j in range(20)) for i in range(1000)]
        many_r = 5
        kdrTree = makeKDRTree(many_points[:], many_r)
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


def main():
    """Se realizan simulaciones para k en {5, 10, 15, 20}, r= 1..5, n = {10^5, 5 * 10^5, 10^6}
       Promediando los tiempos para 100 búsquedas positivas y 100 búsquedas negativas"""
    print("Preparando la simulación...")
    random.seed(759334)

    N_MAX = 10 ** 2


    for k in [5, 10, 15, 20]:
        print(f'Construyendo el conjunto de puntos para k={k}')
        conjunto_puntos_all = [tuple(random.randint(0, 100+1) for j in range(k)) for i in range(N_MAX)]
        for n in [10**2]:
        # for n in [10**5, 5 * 10**5, 10**6]:
            conjunto_puntos = conjunto_puntos_all[:n]
            for r in range(1, 5+1):
                print(f'Construyendo el árbol con r={r} y n={n}')
                kdrTree = makeKDRTree(conjunto_puntos[:n], r)

                print("Realizando 100 búsquedas positivas...")
                for ign in range(100):
                    n_pos = random.choice(conjunto_puntos)
                    assert searchKDRTree(kdrTree, r, n_pos)

                print("Realizando 100 búsquedas negativas...")
                for ign in range(100):
                    n_neg = conjunto_puntos[0]
                    while (n_neg in conjunto_puntos):
                        n_neg = tuple(random.randint(0, 100+1) for j in range(k))

                    assert not searchKDRTree(kdrTree, r, n_neg)


if __name__ == '__main__':
    # unittest.main()
    main()