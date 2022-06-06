from matplotlib import pyplot as plt
import pandas as pd

n = 100
filename = f'output/mutations_m3_k01_initial_nodes1_n{n}.csv'

filename2 = f'dataset/prices_model_seed1313_m3_k01_initial_nodes1.csv'

data = pd.read_csv(filename)
original = pd.read_csv(filename2)
original_n = original[original['n'] == n].groupby('reciprocal_threshold')

mutations = data['mutation'].unique()
steps = data['step'].unique()
reciprocal_threshold = data['reciprocal_threshold'].unique()

## Normalized entropy
for mutation in mutations:
    plt.figure()
    plt.plot(reciprocal_threshold, original_n['normalized_entropy'].mean(), label='original')

    for step in steps:
        df = data[(data['mutation'] == mutation) & (data['step'] == step)].groupby(['reciprocal_threshold'])
        plt.plot(reciprocal_threshold, df['normalized_entropy'].mean(), label=f'steps={step}')

    plt.title(f'Normalized entropy of prices model \nN = {n}, mutator: {mutation}')
    plt.xlabel('Reciprocal threshold')
    plt.ylabel('Normalized entropy')
    plt.xscale('log')
    plt.legend()

    # Save figure
    plt.savefig(f'plots/normalized_entropy_n{n}_{mutation}.png')
plt.show()

## Henrici
for mutation in mutations:
    plt.figure()
    plt.plot(reciprocal_threshold, original_n['df'].mean(), label='original')

    for step in steps:
        df = data[(data['mutation'] == mutation) & (data['step'] == step)].groupby(['reciprocal_threshold'])
        plt.plot(reciprocal_threshold, df['df'].mean(), label=f'steps={step}')

    plt.title(f'Henrici of prices model \nN = {n}, mutator: {mutation}')
    plt.xlabel('Reciprocal threshold')
    plt.ylabel('Henrici')
    plt.xscale('log')
    plt.legend()

    # Save figure
    plt.savefig(f'plots/henrici_n{n}_{mutation}.png')
plt.show()

## Spectral Scaling
for mutation in mutations:
    plt.figure()
    plt.plot(reciprocal_threshold, original_n['spectral_scaling'].mean()/n, label='original')

    for step in steps:
        df = data[(data['mutation'] == mutation) & (data['step'] == step)].groupby(['reciprocal_threshold'])
        plt.plot(reciprocal_threshold, df['spectral_scaling'].mean()/n, label=f'steps={step}')

    plt.title(f'Spectral Scaling of prices model \nN = {n}, mutator: {mutation}')
    plt.xlabel('Reciprocal threshold')
    plt.ylabel('Spectral Scaling / n')
    plt.legend()

    # Save figure
    plt.savefig(f'plots/spectral_scaling_n{n}_{mutation}.png')
plt.show()

## Spectral Gap
for mutation in mutations:
    plt.figure()
    plt.plot(reciprocal_threshold, original_n['spectral_gap'].mean(), label='original')

    for step in steps:
        df = data[(data['mutation'] == mutation) & (data['step'] == step)].groupby(['reciprocal_threshold'])
        plt.plot(reciprocal_threshold, df['spectral_gap'].mean(), label=f'steps={step}')

    plt.title(f'Spectral Gap of prices model \nN = {n}, mutator: {mutation}')
    plt.xlabel('Reciprocal threshold')
    plt.ylabel('Spectral Gap')
    plt.legend()

    # Save figure
    plt.savefig(f'plots/spectral_gap_n{n}_{mutation}.png')
plt.show()