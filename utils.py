from time import time
import itertools as it
import random

def count_elapsed_time(f):
    """
    Execute the function and calculate the elapsed time.
    """
    def wrapper(*args):
        # Start counting.
        start_time = time()

        # Take the original function's return value.
        ret = f(*args)

        # Calculate the elapsed time.
        elapsed_time = time() - start_time
        return elapsed_time, ret

    return wrapper

def gen_puntos_negativos(k, conjunto_puntos):
    for ign in range(100):
        n_neg = tuple(random.randint(0, 100+1) for j in range(k))
        while (n_neg in conjunto_puntos):
            n_neg = tuple(random.randint(0, 100+1) for j in range(k))
        yield n_ne

def puntos_aleatorios(k, max_num = 100):
    return it.product(range(max_num+1), repeat = k)

def puntos_aleatorios_muestra(k, max_num):
    vals = set()
    while len(vals) <= max_num:
        vals.add(tuple(random.randint(0, 100+1) for j in range(k)))
    return list(vals)