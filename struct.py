def at(point, i):
    return point[i % len(point)]

def searchKDTree(kdTree, point, dim = 0):
    if not kdTree:
        return False
    elif len(kdTree) == 1:
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
    points_d = list(set(map(lambda p: p[dim], points)))
    points_d.sort()
    median = points_d[len(points_d) // 2]
    nextDim = (dim + 1) % len(points[0])
    left = [p for p in points if p[dim] < median]
    right = [p for p in points if p[dim] >= median]
    return (median, makeKDTree(left, nextDim), makeKDTree(right, nextDim))

def getMedians(points, r, dim):
    """Se obtienen las r medianas desde dim"""
    medians = [None] * r
    for i in range(r):
        points_d = list(set(map(lambda p: at(p, dim+i), points)))
        points_d.sort()
        medians[i] = points_d[len(points_d) // 2]
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

def makeKDRTree(points, r, dim = 0, level = 0):
    """La lista `points` no puede contener duplicados"""
    if not points:
        return None # Empty trees are None
    elif len(points) == 1:
        return tuple(points) # Leaf nodes have one point.

    # if (level > 40):
    #     print(f"level={level},n={points},dim={dim}")

    # Obtenemos las r medianas, para las dimensiones dim, dim+1, ..., dim+(r-1)
    medians = getMedians(points, r, dim)
    partitions = [None] * (2**r + 1) # Tendremos 2**r particiones (hijos)
    partitions[0] = medians
    partitions_points = []
    criterias = list(it.product([False, True], repeat = r))
    for criteria in criterias:  # 2^r iteraciones
        partitions_points.append([p for p in points if matches_criteria(criteria, medians, p, dim)]) # n iteraciones
        # if (level > 40):
        #     print(f"CHILD{len(partitions_points)}={partitions_points[-1]}")

    for i in range(len(partitions_points)):
        new_dim = (dim+r) % len(points[0])
        partitions[i+1] = makeKDRTree(partitions_points[i], r, new_dim, level+1)

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
