import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import json
import create_arr as TG

def get_g(data):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title(f'Статистика заказов')
    ax.set_xlim([0, max(data[:,0])+100])
    ax.set_ylim([0, max(data[:,1])+100])
    ax.set_xlabel(f'ID заказа')
    ax.set_ylabel(f'количество продуктов в заказе')   
    ax.scatter(data[:,0], data[:,1], c = '#1D2F6F', s = 14)
    fig.set_figwidth(20)
    fig.set_figheight(20)
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
    #user_data = {}
    product_data = {}
    idx = 0
    arr_vis = []
    with open('data_arr.txt') as json_file:
        data = json.load(json_file)
        for ix, o in enumerate(list(data.keys())[:]):
            user_dict[data[o][0]["P_USER"]] = ix
            idx = np.where(p_arr[:,0] == float(o))
            arr_vis.append([ix, len(data[o])])
            print (ix, len(data[o]), len(idx[0]))
    
    arr_vis = np.array(arr_vis)
    #min_visual_product(arr_vis[:,:])
    get_g(arr_vis[:,:])
 

