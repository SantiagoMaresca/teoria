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

    fig = plt.figure(figsize=(10,10))
    # Tiempo buscar positivo vs k
    for i, r in enumerate(range(1, 5+1)):
        ax = fig.add_subplot(f'32{i+1}')
        (
            df_buscar_pos_kdr[df_buscar_pos_kdr['r'] == r]
            .groupby(['k', 'n'], as_index=False)['tiempo']
            .mean()
            .pivot(index='n', columns='k', values='tiempo')
            .plot(style='.-', ax=ax)
        )
        ax.set_xlim([10**5 - 10**4, 10**6 + 10**4])
        ax.set_ylabel('tiempo (ms)')
        ax.set_xticks([10**5, 5 * 10**5, 10**6])
        ax.margins(.05)
        ax.title.set_text(f'r={r}')
        ax.get_legend().remove()
        handles, labels = ax.get_legend_handles_labels()
        fig.legend(handles, labels, loc=(0.7, 0.2))
    fig.tight_layout()
    plt.savefig(f'informe/img/buscar_pos_n.png')

    fig = plt.figure(figsize=(10,10))
    # Tiempo buscar positivo vs k
    for i, r in enumerate(range(1, 5+1)):
        ax = fig.add_subplot(f'32{i+1}')
        (
            df_buscar_neg_kdr[df_buscar_neg_kdr['r'] == r]
            .groupby(['k', 'n'], as_index=False)['tiempo']
            .mean()
            .pivot(index='n', columns='k', values='tiempo')
            .plot(style='.-', ax=ax)
        )
        ax.set_xlim([10**5 - 10**4, 10**6 + 10**4])
        ax.set_ylabel('tiempo (ms)')
        ax.set_xticks([10**5, 5 * 10**5, 10**6])
        ax.margins(.05)
        ax.title.set_text(f'r={r}')
        ax.get_legend().remove()
        handles, labels = ax.get_legend_handles_labels()
        fig.legend(handles, labels, loc=(0.7, 0.2))
    fig.tight_layout()
    plt.savefig(f'informe/img/buscar_neg_n.png')

    fig = plt.figure(figsize=(10,10))
    # Tiempo buscar positivo vs k
    for i, k in enumerate([5, 10, 15, 20]):
        ax = fig.add_subplot(f'22{i+1}')
        (
            df_buscar_pos_kdr[df_buscar_pos_kdr['k'] == k]
            .groupby(['r', 'n'], as_index=False)['tiempo']
            .mean()
            .pivot(index='n', columns='r', values='tiempo')
            .plot(style='.-', ax=ax)
        )
        (
            df_buscar_neg_kdr[df_buscar_neg_kdr['k'] == k]
            .groupby(['r', 'n'], as_index=False)['tiempo']
            .mean()
            .pivot(index='n', columns='r', values='tiempo')
            .plot(style='x-', ax=ax)
        )
        ax.set_xlim([10**5 - 10**4, 10**6 + 10**4])
        ax.set_ylabel('tiempo (ms)')
        ax.set_xticks([10**5, 5 * 10**5, 10**6])
        ax.margins(.05)
        ax.title.set_text(f'k={k}')
        ax.get_legend().remove()
        handles, labels = ax.get_legend_handles_labels()
        fig.legend(handles, labels, loc=(0.45, 0.45))
    fig.tight_layout()
    plt.savefig(f'informe/img/buscar_n.png')

    fig = plt.figure(figsize=(10,10))
    # Tiempo buscar positivo vs k
    for i, r in enumerate(range(1, 5+1)):
        ax = fig.add_subplot(f'32{i+1}')
        (
            df_buscar_pos_kdr[df_buscar_pos_kdr['r'] == r]
            .groupby(['k', 'n'], as_index=False)['tiempo']
            .mean()
            .pivot(index='n', columns='k', values='tiempo')
            .plot(style='.-', ax=ax)
        )
        (
            df_buscar_pos_kd
            .groupby(['k', 'n'], as_index=False)['tiempo']
            .mean()
            .pivot(index='n', columns='k', values='tiempo')
            .plot(style='x-', ax=ax)
        )
        ax.set_xlim([10**5 - 10**4, 10**6 + 10**4])
        ax.set_ylabel('tiempo (ms)')
        ax.set_xticks([10**5, 5 * 10**5, 10**6])
        ax.margins(.05)
        ax.title.set_text(f'r={r}')
        ax.get_legend().remove()
        handles, labels = ax.get_legend_handles_labels()
        fig.legend(handles, labels, loc=(0.7, 0.1))
    fig.tight_layout()
    plt.savefig(f'informe/img/buscar_pos_kd_n.png')

    fig = plt.figure(figsize=(10,10))
    # Tiempo buscar positivo vs k
    for i, r in enumerate(range(1, 5+1)):
        ax = fig.add_subplot(f'32{i+1}')
        (
            df_buscar_neg_kdr[df_buscar_neg_kdr['r'] == r]
            .groupby(['k', 'n'], as_index=False)['tiempo']
            .mean()
            .pivot(index='n', columns='k', values='tiempo')
            .plot(style='.-', ax=ax)
        )
        (
            df_buscar_neg_kd
            .groupby(['k', 'n'], as_index=False)['tiempo']
            .mean()
            .pivot(index='n', columns='k', values='tiempo')
            .plot(style='x-', ax=ax)
        )
        ax.set_xlim([10**5 - 10**4, 10**6 + 10**4])
        ax.set_ylabel('tiempo (ms)')
        ax.set_xticks([10**5, 5 * 10**5, 10**6])
        ax.margins(.05)
        ax.title.set_text(f'r={r}')
        ax.get_legend().remove()
        handles, labels = ax.get_legend_handles_labels()
        fig.legend(handles, labels, loc=(0.7, 0.1))
    fig.tight_layout()
    plt.savefig(f'informe/img/buscar_neg_kd_n.png')

