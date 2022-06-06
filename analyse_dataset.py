from matplotlib import pyplot as plt
import pandas as pd


filename = 'dataset/prices_model_seed1313_m3_k01_initial_nodes1.csv'

data = pd.read_csv(filename)

n_nodes = data['n'].unique()
reciprocal_threshold = data['reciprocal_threshold'].unique()

## Normalized entropy
plt.figure()
for n in n_nodes:
    data_n_p = data[data['n'] == n].groupby('reciprocal_threshold')
    plt.plot(reciprocal_threshold, data_n_p['normalized_entropy'].mean(), label='n = ' + str(n))

plt.title('Normalized entropy of prices model')
plt.xlabel('Reciprocal threshold')
plt.ylabel('Normalized entropy')
# plt.yscale('log')
plt.xscale('log')
plt.legend()

## Henrici
plt.figure()
for n in n_nodes:
    data_n_p = data[data['n'] == n].groupby('reciprocal_threshold')
    plt.plot(reciprocal_threshold, data_n_p['df'].mean(), label='n = ' + str(n))

plt.title('Henrici of prices model')
plt.xlabel('Reciprocal threshold')
plt.ylabel('Henrici')
# plt.yscale('log')
plt.xscale('log')
plt.legend()

## Spectral Scaling
plt.figure()
for n in n_nodes:
    data_n_p = data[data['n'] == n].groupby('reciprocal_threshold')
    plt.plot(reciprocal_threshold, data_n_p['spectral_scaling'].mean()/n, label='n = ' + str(n))

plt.title('Spectral Scaling of prices model')
plt.xlabel('Reciprocal threshold')
plt.ylabel('Spectral Scaling / n')
# plt.yscale('log')
# plt.xscale('log')
plt.legend()

## Spectral Gap
plt.figure()
for n in n_nodes:
    data_n_p = data[data['n'] == n].groupby('reciprocal_threshold')
    plt.plot(reciprocal_threshold, data_n_p['spectral_gap'].mean(), label='n = ' + str(n))

plt.title('Spectral Gap of prices model')
plt.xlabel('Reciprocal threshold')
plt.ylabel('Spectral Gap')
# plt.yscale('log')
# plt.xscale('log')
plt.legend()

plt.show()