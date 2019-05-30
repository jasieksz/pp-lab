#%%[markdown]
## Sprawozdanie - GPU
#----
## Środowisko tesotwe
#### GPU: 
# * Model: Nvidia GeForce GTX 750Ti
# * 640 CUDA Cores (5 x 128)
# * Global memory: 2002 MB 
# * GPU Clock rate: 1110 MHz
# * Memory Clock rate: 2700 MHz
# * Maximum number of thread per block: 1024
# * Maximum number of thread per multiprocessor: 2048 **(64 Warps)**
# * Shared memory per block: 49125 b
# * Max dimension size of thread block: (1024, 1024, 64)
# * CUDA Capability: 5.0
#
#### CPU:
# * Model: Intel i7-4600U
# * Frequency base(boost): 2.1 (3.3) GHz
# * Cores/Thread: 2 / 4
# * Cache: 4 MB
#
#----
## Pamięci tekstur
#
#
## Scheduler multiprocesora
#
#
#----
## Problem
# * Rozwiązywanie równania Laplace’a metodą różnic skończonych.
# * 3 warianty GPU wykorzystujące pamięć **globalną**, **współdzieloną**, **tekstur**
# * 1 wariant CPU
#
## Pomiar
# * Skrypt bash do uruchomienia algorymów z wybranymi parametrami
# * Wynik zapisawne do formatu *CSV*: ```grid,block,time,type```
# * Metryka ***achieved occupancy*** uzyskana za pomocą profilera nvprof
# 
### Parametry 
# * czas/delta symulacji: **0.5 / 0.00001**
# * Rozmiar Grid (N x N): **32, 64, 128, 256, 512**
# * Rozmiar Block (B x B): **2, 4, 8, 16, 32**
#
#----
## Wyniki 

#%%[markdown]
#### Zaagregowane wyniki dla ```type=texture```
by_type[0].describe()

#%%[markdown]
#### Zaagregowane wyniki dla ```type=global```
by_type[1].describe()

#%%[markdown]
#### Zaagregowane wyniki dla ```type=shared```
by_type[2].describe()

#%%[markdown]
#### Wpływ typu pamięci na wydajność - wykres łączony
showParametrized(data=df, x="grid", y="time", hue="type", palette="plasma", ticks=grids, title="Grid v Time", xax='Grid', yax="Time [s]")

#%%[markdown] 
##### Wykres przedstawia wszystkie wyniki, mimo to widać, że najlepsze czasy są dla pamięci tekstur. 

#%%[markdown]
#### Wpływ typu pamięci na wydajność, ze względu na rozmiar bloku
for i,b in enumerate(blocks):
    showParametrized(data=by_block[i], x="grid", y="time", hue="type", palette="plasma", ticks=grids, title="Grid v Time, for block="+str(b), xax='Grid', yax="Time [s]")
    plt.show()

#%%[markdown] 
##### Wniosek z poprzedniego wykresu potwierdził się, dodatkowo dla ```block=32``` wydajność dla pamięci globalnej i tekstur jest podobna.

#%%[markdown]
#### Wpływ rozmiaru bloku na czas wykonania, w zależności od typu pamięci
parameter_impact("grid", "time", "block", "Grid", grids)

#%%[markdown] 
##### Dla pamięci globalnej i tekstur najlepsze wyniki są dla ```block=32``` i ```block=16```, dla wspódzielonej tylko ```block=16```.
##### Rozmiary bloku poniżej 8 są znacząco gorsze.

#%%[markdown]
#### Dodatkowe porównanie wydajność GPU i CPU
showParametrized(data=b32_gpu_cpu, x="grid", y="time", hue="type", palette="plasma", ticks=grids, title="Grid v Time, for block=32", xax='Grid', yax="Time [s]")

#%%[markdown] 
##### Ten wykres bardzo dobrze pokazuje kwestię persektwy, nawet dla pamięci współdzielonej GPU jest znacząco szybsze od CPU

#%%[markdown]
#### Wpływ rozmiaru bloku na theoretical i achieved occupancy

#%%[markdown]
# 


#%%
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from collections import Counter
sns.set_style('darkgrid')

#%%
def showLess(data, x, y, title=None, xax=None, yax=None):
    sns.set(rc={'figure.figsize':(12, 8)})
    g = sns.scatterplot(x=x, y=y, data=data, s=80, legend='full')
    plt.title(title)
    plt.show()

def showParametrized(data, x, y, hue, ticks, title, xax, yax, palette):
    sns.set(rc={'figure.figsize':(8, 6)})
    g = sns.scatterplot(x=x, y=y, hue=hue, data=data, palette=palette, s=80, legend='full')
    g.set(xticks=ticks)
    plt.title(title)
    plt.ylabel(yax)
    plt.xlabel(xax)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.show()

def show(data, x='CPU', y='SpeedUp', hue='Bucket_CPU',\
        ticks=list(range(1,5)), title=None, xax=None, yax=None):
        showParametrized(data, x, y, hue, ticks, title, xax, yax)

def parameter_impact(x, y, hue, xlabel, ticks):
    g = sns.FacetGrid(df, col="type", hue=hue, palette=sns.color_palette("RdBu_r", len(ticks)), height=6, aspect=1.2, col_wrap=2)
    g = (g.map(plt.scatter, x, y, s=60, alpha=0.9)\
            .set(xticks=ticks)\
            .set_axis_labels(xlabel, "Time [s]")\
            .add_legend()
            )
    plt.show()

path = 'lab5-gpu/results/times.csv'
df = pd.read_csv(path)
df_cpu = pd.read_csv('lab5-gpu/results/cpu-times.csv')

blocks = [2,4,8,16,32]
grids = [32,64,128,256,512]
types = ['texture','global', 'shared']
by_block = [df[df['block']==b] for b in blocks] 
by_grid = [df[df['grid']==g] for g in grids]
by_type = [df[df['type']==t] for t in types]
b32_gpu_cpu = pd.concat([by_block[4], df_cpu])
