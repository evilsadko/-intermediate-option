import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import threading
import json
import time
from scipy import stats
from utils import diag_circle, see_stat, CUSTOMER, PRODUCT, ORDER, PRODUCTNAME
import utils



if __name__ == "__main__":
#------------------------->
#    O = ORDER() # ['Order_Id', 'Batch', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date']
#    O_arr = O.to_numpy()
#    zero = np.zeros((O_arr.shape[0], 1))
#    O_arr = np.append(O_arr, zero, axis=1)
#    batch = func_return(O_arr, 1)
##    долго выполняеться много памяти
#------------------------->

    O = ORDER() # ['Order_Id', 'Batch', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date']
    O_arr = O.to_numpy()
    order_dict = utils.func_return(O_arr, 0)
#---------------------------------------->
# Тестирование
#    s = 0
#    for i in batch:
#        s += len(batch[i])
#    print(s, len(batch))
#---------------------------------------->
    start = time.time()
    
    P = PRODUCT() # ['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount'] 
    P_arr = P.to_numpy()
    product_dict = utils.func_return(P_arr, 0)
    
    dict_branch = utils.func_return(O_arr, 1)
    for i in dict_branch:
        dict_branch[i] = {'01':[0,0], '02':[0,0], '03':[0,0], '04':[0,0], '05':[0,0], '06':[0,0], '07':[0,0], '08':[0,0], '09':[0,0], '10':[0,0], '11':[0,0], '12':[0,0]}
    
    #dict_branch = {}
    for i in list(product_dict.keys())[:]:
       
        for v in product_dict[i]:
            #prod = P_arr[v,:]
            order_id = P_arr[v,0]
            branch_id = O_arr[order_dict[order_id], 1][0]
            order_date = O_arr[order_dict[order_id], -1][0].split(" ")[0].split("-")[1]
#            print (order_date)
            dict_branch[branch_id][order_date][0] += O_arr[order_dict[order_id], 3][0]
            dict_branch[branch_id][order_date][1] += O_arr[order_dict[order_id], 5][0]
#            try:
#                dict_branch[branch_id][0] += O_arr[order_dict[order_id], 3][0] #'Items_Count'
#                dict_branch[branch_id][1] += O_arr[order_dict[order_id], 5][0] #'Amount_Charged'
#            except KeyError:
#                dict_branch[branch_id] = [O_arr[order_dict[order_id], 3][0], O_arr[order_dict[order_id], 5][0]]  # count, Amount_Charged
                
            #print (dict_branch[branch_id])   
    
    #print (len(product_dict), time.time()-start)
    with open("out/sort_by_point.json", 'w') as js_file:
        json.dump(dict_branch, js_file)                        
     
#    F = json.load(open("out/sort_by_point.json",'r'))   
#    print (F)    
    L = []
    V = []
    M = [] 
    
    V0 = []
    for i in dict_branch:
        fig, ax = plt.subplots(figsize=(10,10), clear=True)
        ax.set_title(f'ID точки - {i}')
        ax.set_xlabel('Месяц')
        ax.set_ylabel('Количество продуктов')
        ax.bar(list(dict_branch[i].keys()), np.array(list(dict_branch[i].values()))[:,0], color = (0.2,0.7,0.6,0.6))

        ax.plot(list(dict_branch[i].keys()), np.array(list(dict_branch[i].values()))[:,0])  
        
#        for i, v in enumerate(np.array(list(dict_branch[i].values()))[:,0]):
#            ax.text(v + 3, i + .25, str(v), color='blue', fontweight='bold')
        fig.savefig(f"github/branch_0/{i}.jpg") 
        fig.clear(True)
        plt.close(fig)
 
 #------------------------------------->
        fig, ax = plt.subplots(figsize=(10,10), clear=True)
        ax.set_title(f'ID точки - {i}')
        ax.set_xlabel('Месяц')
        ax.set_ylabel('Сумма продаж')
        ax.bar(list(dict_branch[i].keys()), np.array(list(dict_branch[i].values()))[:,1], color = (0.2,0.7,0.6,0.6))

        ax.plot(list(dict_branch[i].keys()), np.array(list(dict_branch[i].values()))[:,1])  
        fig.savefig(f"github/branch_1/{i}.jpg") 
        fig.clear(True)
        plt.close(fig)   
        
        L.append(i)
        V.append(sum(np.array(list(dict_branch[i].values()))[:,0]))
        M.append(0)

        V0.append(sum(np.array(list(dict_branch[i].values()))[:,1]))
        
 
    
       
    diag_circle(V[:], L[:], M[:],  "Популярные точки", "github/popular_branch.jpg")    
    diag_circle(V0[:], L[:], M[:],  "Прибыльные точки", "github/profit_branch.jpg") 
#        print (np.array(list(dict_branch[i].values()))[:,0])
#        print (np.array(list(dict_branch[i].values()))[:,1])
        #print (np.array(list(dict_branch[i].values())).shape)
    
    
    
#    Сортировать продукты по магазинам посмотреть какой магазин больше всего продал продуктов 
#    какой больше всего принес прибыль

#    Выбрать самый популярный средний и самый не популярный магазин
#    сделать статистику продуктов по месяцам
#    популярные продукты
#    популярные категории
#
       
