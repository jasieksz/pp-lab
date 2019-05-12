#%%[markdown]
## Sprawozdanie - Równoległe sortowanie kubełkowe
#----
## Środowisko tesotwe
# vnode-03 - maszyna z 4 rdzeniami    
#
## Struktury danych użyte w algorytmie 
# * Wygenerowane dane wejściowe - float[]
# * Posortowane dane wynikowe - float[]
# * Kubełki - float[][]
# * Indeksy w kubełkach - int[]
# * Indeksy użyte przy scalaniu - int[] - każdy element oznacza indeks początku rejonu, w którym powinny się znaleźć kubełki danego proces
# * Globalna tablica czasów - int[]
#
## Istotne wspólne elementy algorytmów
### Generowanie danych
# ``` 
# #pragma omp parallel
# {
#     unsigned int seed = omp_get_thread_num();
#     #pragma omp for private (i)
#     for (i = 0; i < n; i++) {
#         data[i] = ((double) rand_r(&seed)) / RAND_MAX;
#     }
# } 
# ```
# * Liczby losowe - osobny *seed* dla każdego wątku
# * Mechanizmy *OMP parallel* oraz *OMP for*
#
### Sortowanie poszczególnych kubełków
# ```
# pragma omp parallel
# {
#   int i;
#   int bucketStart = buckPerProc * omp_get_thread_num();
#   int bucketStop = bucketStart + buckPerProc - 1;

#   for (i = bucketStart; i <= bucketStop; i++) {
#       sort(buckets[i], buckets[i] + bucketsIndexes[i]);
#   }
# }
#
# ```
# * Każdy proces sortuje przypisane sobie kubełki
# 
### Scalanie kubełków
# ```
# int index;
# float* res = new float[n];
# #pragma omp parallel shared(res) private(index)
# {
#     int bucketStart = buckPerProc * omp_get_thread_num();
#     int bucketStop = bucketStart + buckPerProc - 1;

#     index = divideIndexes[omp_get_thread_num()];
#     for (int i = bucketStart; i <= bucketStop; i++) {
#         for (int j = 0; j < bucketsIndexes[i]; j++) {
#             res[index++] = buckets[i][j];
#         }
#     }
# }
# ```
# 
### Rozdzielanie danych między kubełki - algorytm 1 
# ```
# #pragma omp parallel
# {
#     int i;
#     unsigned int bucketStart = buckPerProc * omp_get_thread_num();
#     unsigned int bucketStop = bucketStart + buckPerProc - 1;

#     for (i = 0; i < n; i++)
#     {
#         int bi = numberOfBuckets * data[i]; // Index in bucket
#         if (bi == numberOfBuckets) { bi--; } // Hack to handle 1
#         if (bi >= bucketStart && bi <= bucketStop) {
#             buckets[bi][bucketsIndexes[bi]++] = data[i];
#         }
#     }
# }
# ``` 
# * Proces ma przypisane do siebie kubełki i tylko do nich pisze
#  
### Rozdzielanie danych między kubełki - algorytm 2
# ```
# #pragma omp parallel
# {
#     unsigned int seed = omp_get_thread_num();
#     for (int i = 0; i < n; i++)
#     {        
#         float data = ((double) rand_r(&seed)) / RAND_MAX;
#         int bi = numberOfBuckets * data;
#         if (bi == numberOfBuckets) {bi--;} 
#         #pragma omp critical 
#         {
#             buckets[bi][bucketsIndexes[bi]] = data;
#             bucketsIndexes[bi]++;
#         }
#     }
# }
# ```
# * Proces ma przypisany do siebie fragment tablicy i zapisuje do współdzielonych kubełków
# * Synchronizacja za pomocą mechanizmu ```#pragma omp critical```
#
## Pomiar
# * Mierzenie czasu poprzez ```omp_get_wtime()```
# * Skrypt bash do uruchomienia algorymów z wybranymi parametrami
# * wynik zapisawne do formatu *CSV*
# 
### Parametry 
# * liczba danych: **10,000,000**
# * zakres danych: **[0,1)**
# * rdzenie procesora: **1-4**
# * kubełki per rdzeń: **1,2,4,6,8,12,15,20,25,30,35,45,60,80,100,150,200,500,1000,2500**
#
### Dodatkowy pomiar wpływu liczby kubełków na metrykę *Speedup*
# * liczba danych: **10,000,000**
# * rdzenie procesora: **4**
# * kubełki per rdzeń: **1,2,5,10,15,20,40,60,100,250,600,1000,1500,3500,9000,12000,25000,70000,150000,250000**
#----
## Wyniki 
# 
### Format 
# * CPU	- liczba rdzeni procesora
# * Bucket_CPU - liczba kubełków na 1 rdzeń
# * Data_Gen - czas generowania danych (s)
# * Init - czas inicjalizacji struktur danych (s)
# *	Split - czas rozdzielania danych do kubełków (s)
# *	Sort - czas sortowania kubełków (s)
# *	Merge - czas scalania kubełków (s)
# *	Total - suma czasów (s)
# *	Serial - suma czasów dla 1 rdzenia (s)
# *	SpeedUp - metryka przyspieszenia
# 
# 
#%% [markdown]
### Przykładowe wyniki pomiarów
results[0].head(5)

#%% [markdown]
### Zaagregowane wyniki pomiarów

#%%
results[0].describe()[['CPU', 'Bucket_CPU', 'SpeedUp']]

#%%
results[1].describe()[['CPU', 'Bucket_CPU', 'SpeedUp']]

#%%
results[2].describe()[['Bucket_CPU', 'SpeedUp']]

#%%
results[3].describe()[['Bucket_CPU', 'SpeedUp']]


#%% [markdown]
### Średnia proporcja rozkładu czasu pomiędzy kolejnymi etapmi programu

labels = ['Data_Gen', 'Init', 'Split', 'Sort', 'Merge']
pies = [results[i].mean()[2:7] for i in range(2)]
pies[0] *= 10
pies[1] *= 10

sns.set(rc={'figure.figsize': (4, 4)})
plt.pie(pies[0], labels=labels, colors=['g', 'm', 'orange', 'r', 'm'])
plt.title('Alg. 1, n=10^7')
plt.show()

plt.pie(pies[1], labels=labels, colors=['g', 'm', 'orange', 'r', 'm'])
plt.title('Alg. 2, n=10^7')
plt.show()

#%% [markdown]
### Wyniki pomiarów dla algorytmu 1

#%%
show(results[0], 'CPU', 'SpeedUp', 'Bucket_CPU', title='SpeedUp - CPU, alg. 1')

#%%
showLess(results[2], 'Bucket_CPU', 'SpeedUp', title='SpeedUp - Buckets, alg. 1')

#%% [markdown]
#### Maksimum jest osiągane dla Bucket_CPU = 25000

#%% [markdown]
### Wyniki pomiarów dla algorytmu 2

#%%
show(results[1], 'CPU', 'SpeedUp', 'Bucket_CPU', title='SpeedUp - CPU, alg. 2')

#%%
showLess(results[3], 'Bucket_CPU', 'SpeedUp', title='SpeedUp - Buckets, alg. 2')


#%% [markdown]
## Wnioski
#
#
#
#
## Funkcje pomocnicze

#%%
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from collections import Counter
sns.set_style('darkgrid')

def getSpeedUp(data, cpus):
    serial = [max(data[data['CPU']==cpu]['Total']) for cpu in cpus]
    data['Serial'] = data['CPU'].apply(lambda c: serial[0])
    data['SpeedUp'] = data['Serial'] / data['Total']

def showLess(data, x, y, title=None, xax=None, yax=None):
    sns.set(rc={'figure.figsize':(12, 8)})
    g = sns.scatterplot(x=x, y=y, data=data, s=80, legend='full')
    plt.title(title)
    plt.show()

def showParametrized(data, x, y, hue, ticks, title, xax, yax):
    sns.set(rc={'figure.figsize':(12, 8)})
    g = sns.scatterplot(x=x, y=y, hue=hue, data=data, palette=sns.color_palette("RdBu_r", len(Counter(data[hue]))), s=80, legend='full')
    g.set(xticks=ticks)
    plt.title(title)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.show()

def show(data, x='CPU', y='SpeedUp', hue='Bucket_CPU',\
        ticks=list(range(1,5)), title=None, xax=None, yax=None):
        showParametrized(data, x, y, hue, ticks, title, xax, yax)

#%% 
base = 'bucket-sort/results/'
paths = ['alg1_e7.csv', 'alg2_e7.csv', 'b_alg1_e7.csv', 'b_alg2_e7.csv']
results = [pd.read_csv(base + path) for path in paths]
for result in results[:2]:
    getSpeedUp(result, [1,2,3,4])

for result in results[2:]:
    getSpeedUp(result, [4])
