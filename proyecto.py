import itertools as it
import random
import unittest
from utils import count_elapsed_time, gen_puntos_negativos
from time import time

import numpy as np

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

def prom_sin_outliers(datos, m = 2):
    data = np.array(datos)
    if (np.std(data) == 0):
        return datos[0]
    data = data[abs(data - np.mean(data)) < m * np.std(data)]
    prom =  np.mean(data)

    return prom


makeKDRTreeTiempo = count_elapsed_time(makeKDRTree)
makeKDTreeTiempo = count_elapsed_time(makeKDTree)
searchKDRTreeTiempo = count_elapsed_time(searchKDRTree)

def main():
    """Se realizan simulaciones para k en {5, 10, 15, 20}, r= 1..5, n = {10^5, 5 * 10^5, 10^6}
       Promediando los tiempos para 100 búsquedas positivas y 100 búsquedas negativas"""
    print("Preparando la simulación...")
    random.seed(759334)

    N_MAX = 10 ** 6

    arch = open("datos.csv", "w")
    arch.write("k;r;n;tipo;tiempo\n")
    for k in [5, 10, 15, 20]:
        print(f'Construyendo el conjunto de puntos para k={k}')
        conjunto_puntos_all = [tuple(random.randint(0, 100+1) for j in range(k)) for i in range(N_MAX)]
        for n in [10**5, 5 * 10**5, 10**6]:
            conjunto_puntos = conjunto_puntos_all[:n]
            for r in range(1, 5+1):
                print(f'Construyendo el árbol con r={r} y n={n}')
                tiempo, kdrTree = makeKDRTreeTiempo(conjunto_puntos[:n], r)
                arch.write(f'{k};{r};{n};arbolkdr;{tiempo}\n')

                tiempo, kdTree = makeKDTreeTiempo(conjunto_puntos[:n])
                arch.write(f'{k};{r};{n};arbolkd;{tiempo}\n')

                print("Realizando 100 búsquedas positivas...")
                tiempos = []
                for ign in range(100):
                    n_pos = random.choice(conjunto_puntos)
                    tiempo, val = searchKDRTreeTiempo(kdrTree, r, n_pos)
                    if not val:
                        assert False # Algo falló
                    tiempos.append(tiempo)
                arch.write(f'{k};{r};{n};buscar_pos;{prom_sin_outliers(tiempos)}\n')

                print("Realizando 100 búsquedas negativas...")
                tiempos = []
                for ign in range(100):
                    n_neg = tuple(random.randint(0, 100+1) for j in range(k))
                    while (n_neg in conjunto_puntos):
                        n_neg = tuple(random.randint(0, 100+1) for j in range(k))

                    tiempo, val = searchKDRTreeTiempo(kdrTree, r, n_neg)
                    if val:
                        assert False # Algo falló
                    tiempos.append(tiempo)
                arch.write(f'{k};{r};{n};buscar_neg;{prom_sin_outliers(tiempos)}\n')
    arch.close()


if __name__ == '__main__':
    main()