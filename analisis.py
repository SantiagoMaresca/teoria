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
    df['tiempo'] = df['tiempo'] * 1000
    df_buscar_pos_kdr = df[df["tipo"] == BUSCAR_KDR_POS]
    df_buscar_pos_kd = df[df["tipo"] == BUSCAR_KD_POS]
    df_buscar_neg_kdr = df[df["tipo"] == BUSCAR_KDR_NEG]
    df_buscar_neg_kd = df[df["tipo"] == BUSCAR_KD_NEG]
    df_crear_kdr = df[df["tipo"] == CREAR_KDR]
    df_crear_kd = df[df["tipo"] == CREAR_KD]

    # Tiempo buscar positivo vs k
    for r in range(1, 5+1):
        ax = (
            df_buscar_pos_kdr[df_buscar_pos_kdr['r'] == r]
            .groupby(['k', 'n'], as_index=False)['tiempo']
            .mean()
            .pivot(index='k', columns='n', values='tiempo')
            .plot(style='.-')

        )
        ax.set_xlim([4,21])
        ax.set_ylabel('tiempo (ms)')
        ax.margins(.05)
        plt.suptitle(f'Tiempo de buscar positivo r={r}')
        plt.savefig(f'informe/img/buscar_pos_k_r{r}.png')

    # for n in [10**5, 5 * 10**5, 10**6]:
    #     (
    #         df_buscar_pos_kdr[df_buscar_pos_kdr['n'] == n]
    #         .groupby(['k', 'r'], as_index=False)['tiempo']
    #         .mean()
    #         .pivot(index='k', columns='r', values='tiempo')
    #         .plot(style='.-')
    #     )
    #     plt.savefig(f'fig/buscar_pos_k_n{n}.png')



    # (
    #     df_buscar_pos_kdr
    #     .groupby(['k'], as_index=False)
    #     .mean()
    #     .plot(x='k', y='tiempo', label='kdr', ax=ax)
    # )
    # (
    #     df_buscar_pos_kd
    #     .groupby(['k'], as_index=False)
    #     .mean()
    #     .plot(x='k', y='tiempo', ax=ax, label='kd')
    # )
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
    # plt.show()
