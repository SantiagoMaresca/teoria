import pandas as pd
from datetime import datetime
import csv
import matplotlib.pyplot as plt

CREAR_KDR = 'arbolkdr'
CREAR_KD = 'arbolkd'
BUSCAR_KDR_POS = 'buscar_pos'
BUSCAR_KD_POS = 'buscar_pos_kd'
BUSCAR_KDR_NEG = 'buscar_neg'
BUSCAR_KD_NEG = 'buscar_neg_kd'


if __name__ == '__main__':
    headers = ['k','r','n', 'tipo', 'tiempo']
    df = pd.read_csv('datos.csv',names=headers, sep=';', header=0)
    df_buscar_pos_kdr = df[df["tipo"] == BUSCAR_KDR_POS]
    df_buscar_pos_kd = df[df["tipo"] == BUSCAR_KD_POS]
    df_buscar_neg_kdr = df[df["tipo"] == BUSCAR_KDR_NEG]
    df_buscar_neg_kd = df[df["tipo"] == BUSCAR_KD_NEG]
    df_crear_kdr = df[df["tipo"] == CREAR_KDR]
    df_crear_kd = df[df["tipo"] == CREAR_KD]

    fig, ax = plt.subplots(1, 1)

    # Tiempo buscar positivo vs k
    fig.suptitle('Tiempo de buscar positivo')
    (
        df_buscar_pos_kdr
        .groupby(['k'], as_index=False)
        .mean()
        .plot(x='k', y='tiempo', label='kdr', ax=ax)
    )
    (
        df_buscar_pos_kd
        .groupby(['k'], as_index=False)
        .mean()
        .plot(x='k', y='tiempo', ax=ax, label='kd')
    )
    # TODO: Agrupar para cada valor de k, n y r

    # Tiempo buscar positivo vs r
    # (
    #     df_buscar_pos_kdr
    #     .groupby(['r'], as_index=False)
    #     .mean()
    #     .plot(x='r', y='tiempo')
    # )
    # (
    #     df_buscar_pos_kd
    #     .groupby(['r'], as_index=False)
    #     .mean()
    #     .plot(x='r', y='tiempo')
    # )

    # # Tiempo buscar positivo vs n
    # (
    #     df_buscar_pos_kdr
    #     .groupby(['n'], as_index=False)
    #     .mean()
    #     .plot(x='n', y='tiempo')
    # )
    # (
    #     df_buscar_pos_kd
    #     .groupby(['n'], as_index=False)
    #     .mean()
    #     .plot(x='n', y='tiempo')
    # )

    # plot
    plt.show()