import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import json
import test_graph as TG

#with open('data.txt', 'r') as js_file:
#    json.dump(dict_i ,js_file)
    

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
            arr_vis.append([ix, len(data[o]), len(idx[0])])
            print (ix, len(data[o]), len(idx[0]))# order_dict[o], len(data[o]) #user_dict[data[o][0]["P_USER"]]
            #print (ix,len(data[o]), data[o][0]["P_USER"]) # ID покупки, количество продуктов в покупке

 
    arr_vis = np.array(arr_vis)
    print (arr_vis.shape)
    x = arr_vis[:,0]
    y = arr_vis[:,1]
    z = arr_vis[:,2]
    ax = plt.axes(projection='3d')
    ax.scatter(x, y, z, c=z, cmap='viridis', linewidth=0.5);
    plt.show()


#    for K in product_data.keys():
#         print (product_data[K])
# Создать диаграмму покупаемых продуктов
#             user_data[data[o][0]["P_USER"]] = 0
#            Z[35380] = data[o][0]['CSE']
#            Z[35379] = data[o][0]['CSS']
#            Z[35378] = data[o][0]['JCS']
#            Z[35377] = len(data[o]) # колво продуктов
#            Z[35376] = len(IDX[0]) # колво покупок
             #arr_vis.append([ix,len(data[o])])


#https://medium.com/@kvnamipara/a-better-visualisation-of-pie-charts-by-matplotlib-935b7667d77f
#https://medium.com/swlh/python-data-visualization-with-matplotlib-for-absolute-beginner-part-iii-three-dimensional-8284df93dfab
#https://jakevdp.github.io/PythonDataScienceHandbook/04.12-three-dimensional-plotting.html
#https://towardsdatascience.com/the-art-of-effective-visualization-of-multi-dimensional-data-6c7202990c57


#Наименования продуктов которые покупались: 24290
# 
#                   Количество покупателей: 59843

#                   Количество покупок: 82705

#                   Количество продуктов: 8239567

#                   Среднее количество продуктов в покупке: 99.62598391874735

