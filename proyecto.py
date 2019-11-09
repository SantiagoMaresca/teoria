import itertools as it

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
        partitions[i] = makeKDRTree(partition, r, (dim+r) % len(points))
        i += 1

    return tuple(partitions)

if __name__ == '__main__':
    t = makeKDRTree([(0, 1, 2), (4, 2, 3)], 2)
    print(t)

