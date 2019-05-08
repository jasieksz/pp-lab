#%%
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
sns.set_style('darkgrid')

#%%
df1 = pd.read_csv('bucket-sort/results/alg1_e7.csv')
df2 = pd.read_csv('bucket-sort/results/alg2_e7.csv')

#%%
df1.describe()

#%%
df2.describe()

#%%
sns.set(rc={'figure.figsize':(12, 8)})
g = sns.scatterplot(x='CPU', y='Total', hue='Bucket_CPU', data=df1, palette='viridis', s=80, legend='full')
g.set(xticks=list(range(1,5)))
plt.show()

#%%
labels = ['Data_Gen', 'Init', 'Split', 'Sort', 'Merge']
times = [0.129277, 0.000183, 0.849584, 2.343296, 0.101942]
plt.pie(times, labels=labels, colors=['g', 'm', 'orange', 'r', 'm'])
plt.show()
