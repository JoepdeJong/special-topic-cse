#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 03:53:28 2022

@author: ksyunetz
"""
import numpy as np
from matplotlib import cm
#from colorspacious import cspace_converter
from hierarchy import *

def getvalue(val):
    return list(val.values())[0]

def levels_struct(G):
    k = len(G.nodes)
    h = hierarchy(G)
    levels = np.zeros(k)
    for key, value in h.items():
        levels[key-1] = getvalue(value)
    hier_numb = np.unique(levels, return_counts=True) #2d list of hierarchical numbers + number of nodes on each level
    nodes = [[[] for i in range(0)] for j in range(len(hier_numb[0]))]
    nodes[0] = leader_nodes(G)
    for key, value in h.items():
        nodes[getvalue(value)].append(key) #multidimensional list with nodes of each hierarchical numbers
    return nodes

def colouring(G):
    levs = levels_struct(G)
    red = [[[] for i in range(0)] for j in range(len(levs))] 
    red_num = np.zeros(len(levs))
    blue = [[[] for i in range(0)] for j in range(len(levs))]
    blue_num = np.zeros(len(levs))
    green = [[[] for i in range(0)] for j in range(len(levs))]
    green_num = np.zeros(len(levs))
    for k in range(len(levs)-1):
        for j in levs[k]:
            for l in levs[k+1]:
                if G.has_edge(l,j) == True:
                    blue[k].append([l,j])
        blue_num[k] = len(blue[k])
    for k in range(1, len(levs)):
        for j in levs[k]:
            count = 0
            while (k + count + 1 <= len(levs) - 1):
                for l in levs[k+count+1]:
                    if G.has_edge(j,l) == True:
                        red[k].append([j,l])
                count += 1                
        red_num[k] = len(red[k])
    for k in range(1, len(levs)):
        for l in levs[k]:
            for m in levs[k]:
                if G.has_edge(m,l) == True:
                    green[k].append([m,l])
        green_num[k] = len(green[k])
    return  blue_num, red_num, green_num

def hier_lvl_shift(G):
    levs = levels_struct(G)
    ans = np.zeros((len(levs),len(levs)))
    for k in range(len(levs)-1):
        for j in levs[k]:
            for l in levs[k+1]:
                if G.has_edge(l,j) == True:
                    ans[k+1,k] += 1
    for k in range(1, len(levs)):
        for j in levs[k]:
            count = 0
            while (k + count + 1 <= len(levs) - 1):
                for l in levs[k+count+1]:
                    if G.has_edge(j,l) == True:
                        ans[k,k+count+1] += 1
                count += 1
    for k in range(1, len(levs)):
        for l in levs[k]:
            for m in levs[k]:
                if G.has_edge(m,l) == True:
                    ans[k,k] += 1
    return  ans

if __name__ == '__main__':
    from import_literature1976 import *
    G = import_draw_literature (draw=False)
    A = G.adjacency()
    l = leader_nodes(G)
    h = hierarchy(G)
    if len(l)>0:
        col = np.array(colouring(G))
        levs = levels_struct(G)
        edges_num = np.zeros(3)
        lens = np.arange(0,len(levs),1)
        for j in range(3):
            edges_num[j] = np.sum(col[j,:])
        hier_struct = np.zeros((3,len(levs)))
        s = 0
        for j in range(len(levs)):
            for i in range(3):
                hier_struct[i,j] = col[i,j]/edges_num[i]
        hier_shift = np.array(hier_lvl_shift(G))
        hier_lvl_frac = np.zeros((len(levs),len(levs)))
        for i in range(1,len(levs)):
            for j in range(len(levs)):
                hier_lvl_frac[j,i] = hier_shift[i,j]/sum(edges_num)
        plt.figure(figsize=(3,3))
        plt.imshow(hier_lvl_frac, interpolation='none', aspect='equal', cmap=cm.Blues, alpha = 1)
        plt.colorbar()
        plt.xticks(np.arange(0,4,1))
        plt.yticks(np.arange(0,4,1))
        plt.xlabel('$Hierarchical~number$')
        plt.ylabel('$Hierarchical~number$')
        plt.savefig('../fig4/hiershift.png', dpi=300, bbox_inches = "tight")
        
        plt.figure(figsize=(5,3))
        plt.plot(lens, hier_struct[0,:], 'b.-', alpha = 0.5)
        plt.plot(lens, hier_struct[1,:], 'r.-', alpha = 0.5)
        labels = ('Upwards', 'Downwards')
        plt.legend(labels, loc = 'upper right')
        plt.xlabel('Hierarchical number')
        plt.ylabel('Fraction of Edges in Direction')
        plt.title('Literary criticism network of Dutch writers in 1976')
        plt.savefig('../fig4/hiernumb.png', dpi=300, bbox_inches = "tight")
        
        width = 0.75
        fig = plt.figure(figsize=(5,4))
        ax = fig.add_axes([0,0,0.5,0.5])
        ax.bar(1, edges_num[0], width, color='b')
        ax.bar(2, edges_num[1], width, color='r')
        ax.bar(1, edges_num[2], width,bottom=edges_num[0], color='g')
        ax.set_ylabel('Sum of edges')
        ax.set_xlabel('Types') 
        ax.set_title('Total weight of edges')
        ax.set_yticks(np.arange(0, edges_num[0]+edges_num[2], 10))
        ax.set_xticks([1,2],('$upwards+$\n$neutral$', '$downwards$'))
        plt.savefig('../fig4/redbluegreen_barchart.png', dpi=300, bbox_inches = "tight")
    else:
        print('No leader nodes in the network')

   
        
