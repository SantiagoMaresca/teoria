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


    # Tiempo buscar positivo vs k
    (
        df_buscar_pos_kdr
        .groupby(['k'], as_index=False)
        .mean()
        .plot(x='k', y='tiempo')
    )

    # plot
    plt.show()