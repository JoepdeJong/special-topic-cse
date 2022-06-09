#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 17:35:30 2022

@author: ksyunetz
"""

import numpy as np
import matplotlib.pyplot as plt

df = np.zeros(9)
h_norm = np.zeros(9)

df = [0.6484486606656004,0.49170655425776283,0.6493251134927432,0.9875771574795098,0.0,0.5931852143475357,0.7769637680952811,0.8422294617050499,0.2704891764757655]
h_norm = [0.8470531223282445,0.8933479252134252	,0.825237012972247,0.0,1.0,0.9073973509169091,0.6823074532176571,0,0.969619215879966]
title = ['Connectome of the Rhesus brain','Connectome of a cat','Friendship among highschool students','Literary criticism network of Dutch writers in 1976','Roads Network in Eastern Massachusetts, USA','Neuronal network for a mouse brain','Friendship among college students in a leadership course','Neuronal network for Caenorhabditis elegans','International trade network of diplomatic exchanges']

fig = plt.figure()
ax = fig.add_subplot(111)
for i in range(9):
    ax.plot(df[i], h_norm[i], '.')

 
ax.legend(title, bbox_to_anchor=(0.77, 0.85))
plt.grid()
plt.title('Normalized entropy rate dependence \n on the network polarization in real-world networks')
plt.savefig('../fig2/normentr_df.png', dpi=300, bbox_inches = "tight")
plt.show()