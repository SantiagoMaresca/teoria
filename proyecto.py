import random
from utils import count_elapsed_time, gen_puntos_negativos, puntos_aleatorios_muestra
from time import time
import numpy as np

import kdstruct as kd


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

def gen_puntos_negativos(conjunto_puntos, k):
    for _ in range(100):
        n_neg = tuple(random.randint(0, 100+1) for j in range(k))
        while (n_neg in conjunto_puntos):
            n_neg = tuple(random.randint(0, 100+1) for j in range(k))
        yield n_neg



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
            puntos_positivos = list(random.choice(conjunto_puntos) for _ in range(100))
            puntos_negativos = list(gen_puntos_negativos(conjunto_puntos, k))
            tiempo, kdTree = makeKDTreeTiempo(conjunto_puntos[:n])
            arch.write(f'{k};-;{n};arbolkd;{tiempo}\n')

            tiemposKd = []
            for n_pos in puntos_positivos:
                tiempoKd, valKd = searchKDTreeTiempo(kdTree, n_pos)
                assert valKd
                tiemposKd.append(tiempoKd)
            arch.write(f'{k};-;{n};buscar_pos_kd;{prom_sin_outliers(tiemposKd)}\n')

            tiemposKd = []
            for n_neg in puntos_negativos:
                tiempoKd, valKd = searchKDTreeTiempo(kdTree, n_neg)
                assert not valKd
                tiemposKd.append(tiempoKd)
            arch.write(f'{k};-;{n};buscar_neg_kd;{prom_sin_outliers(tiemposKd)}\n')

            for r in range(1, 5+1):
                print(f'Construyendo el árbol con r={r} y n={n}')
                tiempo, kdrTree = makeKDRTreeTiempo(conjunto_puntos[:n], r)
                arch.write(f'{k};{r};{n};arbolkdr;{tiempo}\n')

                print("Realizando 100 búsquedas positivas...")
                tiempos = []
                for n_pos in puntos_positivos:
                    tiempo, val = searchKDRTreeTiempo(kdrTree, r, n_pos)
                    assert val
                    tiempos.append(tiempo)
                arch.write(f'{k};{r};{n};buscar_pos;{prom_sin_outliers(tiempos)}\n')

                print("Realizando 100 búsquedas negativas...")
                tiempos = []
                for n_neg in puntos_negativos:
                    tiempo, val = searchKDRTreeTiempo(kdrTree, r, n_neg)
                    assert not val
                    tiempos.append(tiempo)
                arch.write(f'{k};{r};{n};buscar_neg;{prom_sin_outliers(tiempos)}\n')

    arch.close()


if __name__ == '__main__':
    main()
