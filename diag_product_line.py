import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import json
import create_arr as TG

 
def min_visual_product(_arr):
    x = range(0, _arr.shape[0])
    fig, ax = plt.subplots(1, figsize=(16, 6))# numerical x
    plt.bar(_arr[:,0], _arr[:,1], color = '#1D2F6F')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)# x y details
    plt.ylabel('количество продуктов в заказе')
    plt.xlabel('ID заказа')
    plt.xlim(-0.5, max(_arr[:,0]))# grid lines
    plt.ylim(-0.5, max(_arr[:,1]))
    ax.set_axisbelow(True)
    ax.yaxis.grid(color='gray', linestyle='dashed', alpha=0.2)# title and legend
    plt.title('Статистика заказов', loc ='left')
    plt.show()
   

if __name__ == "__main__":
    p_open = TG.PRODUCT() #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']
    #TG.see_stat(p_open)   

    p_arr = p_open.to_numpy()
    vals_prod = np.unique(p_arr[:,1])
    product_dict = {}
    for ix, i in enumerate(vals_prod):
        product_dict[i] = ix

    user_dict = {}
    product_data = {}
    idx = 0
    arr_vis = []
    with open('data_arr.txt') as json_file:
        data = json.load(json_file)
        for ix, o in enumerate(list(data.keys())[:1000]):
            user_dict[data[o][0]["P_USER"]] = ix
            idx = np.where(p_arr[:,0] == float(o))
            arr_vis.append([ix, len(data[o])])
            print (ix, len(data[o]), len(idx[0]))
    
    arr_vis = np.array(arr_vis)
    min_visual_product(arr_vis[:,:])
 
