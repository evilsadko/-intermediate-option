import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import create_arr as TG



def min_visual_product(_arr):
    x = range(0, _arr.shape[0])
    fig, ax = plt.subplots(1, figsize=(16, 6))# numerical x
    plt.bar(x[:], _arr[:,1], width = 0.3, color = '#1D2F6F')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)# x y details
    plt.ylabel('Count product')
    plt.xlabel('ID product')
    plt.xlim(-0.5, len(count))# grid lines
    plt.ylim(-0.5, max(count)/1000)
    ax.set_axisbelow(True)
    ax.yaxis.grid(color='gray', linestyle='dashed', alpha=0.2)# title and legend
    plt.title('Procudct Stat', loc ='left')
    plt.show()

if __name__ == "__main__":
    
    p_open = TG.PRODUCT()
    p_arr = p_open.to_numpy()
    print (p_arr.shape)
    vals, inverse, count = np.unique(p_arr[:,1], return_inverse=True, return_counts=True)
    print ("PRODUCT CLASS: ",len(count), max(count), min(count))
    _arr = []
    for ix, ixp in enumerate(count[:1000]):
         _arr.append([vals[ix],int(ixp)])
    _arr = np.array(_arr)
    _arr = _arr[_arr[:,1].argsort()]  
#---------------------->
    min_visual_product(_arr)
#---------------------->

