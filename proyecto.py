import itertools as it
import random
import unittest
from utils import count_elapsed_time, gen_puntos_negativos, puntos_aleatorios_muestra
from time import time
import numpy as np

import struct as kd


def prom_sin_outliers(datos, m = 2):
    data = np.array(datos)
    if (np.std(data) == 0):
        return datos[0]
    data = data[abs(data - np.mean(data)) < m * np.std(data)]
    prom =  np.mean(data)

    return prom


makeKDRTreeTiempo = count_elapsed_time(kd.makeKDRTree)
makeKDTreeTiempo = count_elapsed_time(kd.makeKDTree)
searchKDRTreeTiempo = count_elapsed_time(kd.searchKDRTree)
searchKDTreeTiempo = count_elapsed_time(kd.searchKDTree)

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
        conjunto_puntos_all = puntos_aleatorios_muestra(k, N_MAX)
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
                tiemposKd = []
                for ign in range(100):
                    n_pos = random.choice(conjunto_puntos)
                    tiempo, val = searchKDRTreeTiempo(kdrTree, r, n_pos)
                    tiempoKd, valKd = searchKDTreeTiempo(kdrTree, n_pos)
                    if (not val) or (not val):
                        assert False # Algo falló
                    tiempos.append(tiempo)
                    tiemposKd.append(tiempoKd)
                arch.write(f'{k};{r};{n};buscar_pos;{prom_sin_outliers(tiempos)}\n')
                arch.write(f'{k};{r};{n};buscar_pos_kd;{prom_sin_outliers(tiemposKd)}\n')

                print("Realizando 100 búsquedas negativas...")
                tiempos = []
                tiemposKd = []
                for ign in range(100):
                    n_neg = tuple(random.randint(0, 100+1) for j in range(k))
                    while (n_neg in conjunto_puntos):
                        n_neg = tuple(random.randint(0, 100+1) for j in range(k))

                    tiempo, val = searchKDRTreeTiempo(kdrTree, r, n_neg)
                    tiempoKd, valKd = searchKDTreeTiempo(kdrTree, n_neg)
                    if val or val:
                        assert False # Algo falló
                    tiempos.append(tiempo)
                    tiemposKd.append(tiempoKd)
                arch.write(f'{k};{r};{n};buscar_neg;{prom_sin_outliers(tiempos)}\n')
                arch.write(f'{k};{r};{n};buscar_neg_kd;{prom_sin_outliers(tiemposKd)}\n')
    arch.close()


if __name__ == '__main__':
    main()