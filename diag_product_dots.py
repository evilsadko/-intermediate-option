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


def min_visual_product(_arr):
    x = range(0, _arr.shape[0])
#    #print (np.array(_arr).shape, f"ID product: {_arr[-1][0]} - count: {_arr[-1][1]}")
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
        
#    o_open = TG.ORDER() #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged']  

#    o_arr = o_open.to_numpy()
#    vals_orde = np.unique(o_arr[:,0])  
#    order_dict = {}
#    for ix, i in enumerate(vals_orde):
#        order_dict[i] = ix

#    c_open = TG.CUSTOMER() #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']
#    с_arr = c_open.to_numpy()  
#    vals_user = np.unique(с_arr[:,0])    
#    print (len(vals_user))
#    user_dict = {}
#    for ix, i in enumerate(vals_user):
#        user_dict[i] = ix

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
            #arr_vis.append([ix, len(data[o]), len(idx[0])])
            arr_vis.append([ix, len(data[o])])
            print (ix, len(data[o]), len(idx[0]))# order_dict[o], len(data[o]) #user_dict[data[o][0]["P_USER"]]
            #print (ix,len(data[o]), data[o][0]["P_USER"]) # ID покупки, количество продуктов в покупке
    
    arr_vis = np.array(arr_vis)
    #min_visual_product(arr_vis[:,:])
    get_g(arr_vis[:,:])
 

