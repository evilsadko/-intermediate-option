import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import threading
import json
import time
from scipy import stats
from utils import diag_circle, see_stat
import utils

def CUSTOMER():
    c_open = pd.read_csv('in/B24_dbo_Crm_customers.csv', delimiter=',')
    c_open = c_open[['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']]
    c_open['join_club_success'] = c_open['join_club_success'].replace(np.nan, 2)
    c_open['Could_send_sms'] = c_open['Could_send_sms'].replace(np.nan, 0)
    c_open['Could_send_email'] = c_open['Could_send_email'].replace(np.nan, 0)
    c_open['consent'] = c_open['consent'].replace(np.nan, 0)
    c_open = c_open.apply(lambda x: pd.to_numeric(x, errors='coerce')).dropna() # Убираю все строки
    return c_open

def PRODUCT():
    s = time.time()
#    p_open = pd.read_csv('B24_dbo_Crm_product_in_order.csv', delimiter=',')
#    p_open.to_pickle("B24_dbo_Crm_product_in_order.pk")
    
    p_open = pd.read_pickle("in/B24_dbo_Crm_product_in_order.pk")
#    see_stat(p_open)
    p_open = p_open[['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']] 
    print (time.time()-s)
    return p_open
    
def ORDER():
#    o_open = pd.read_csv('B24_dbo_Crm_orders.csv', delimiter=',')
#    o_open.to_pickle("B24_dbo_Crm_orders.pk")

    o_open = pd.read_pickle("in/B24_dbo_Crm_orders.pk")
#    see_stat(o_open)
    o_open = o_open[['Order_Id', 'Branch_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date']]
    o_open['price_before_discount'] = o_open['price_before_discount'].replace(np.nan, 0)
    o_open['Items_Count'] = o_open['Items_Count'].replace(np.nan, 0)
    return o_open.sort_values(by=['Order_Date'])

        
def PRODUCTNAME():
    p_open = pd.read_csv('in/B24_dbo_Products.csv', delimiter=',')
    #see_stat(p_open)
    return p_open

#def saveJSON(x):
#    with open("out/branch_product.json", 'w') as js_file:
#        json.dump(dict_branch_product, js_file)  

def branch_data():
    O = ORDER() # ['Order_Id', 'Batch', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date']
    O_arr = O.to_numpy()
    order_dict = utils.func_return(O_arr, 0)
    start = time.time()

    P = PRODUCT() # ['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount'] 
    P_arr = P.to_numpy()
    product_dict = utils.func_return(P_arr, 0)
    
    dict_branch = utils.func_return(O_arr, 1)
    for i in dict_branch:
        dict_branch[i] = {'01':[], '02':[], '03':[], '04':[], '05':[], '06':[], '07':[], '08':[], '09':[], '10':[], '11':[], '12':[]}
        
    for i in list(product_dict.keys())[:]:
        for v in product_dict[i]:
            L_product = P_arr[v,:].tolist()
            order_id = L_product[0]
            branch_id = O_arr[order_dict[order_id], 1][0]
            order_date = O_arr[order_dict[order_id], -1][0]
            customet_id = O_arr[order_dict[order_id], 2][0]
            M = order_date.split(" ")[0].split("-")[1]
            L_product += [customet_id, order_date]
            dict_branch[branch_id][M].append(L_product) 
            #print (L_product)     
            #dict_branch[branch_id][order_date].append(O_arr[order_dict[order_id], :].tolist())   
            
    for i in dict_branch:
        with open(f"out/branch/branch_product_{i}.json", 'w') as js_file:
            json.dump(dict_branch[i], js_file)  
    
#    dict_branch_product = {}
#    dict_branch = json.load(open("out/branch_order.json",'r'))  
#    for i in dict_branch:
#        dict_branch_product[i] = {'01':[], '02':[], '03':[], '04':[], '05':[], '06':[], '07':[], '08':[], '09':[], '10':[], '11':[], '12':[]}
#        for o in dict_branch[i]:
#            for d in range(len(dict_branch[i][o])):
#                id_order = dict_branch[i][o][d][0]
#                dict_branch_product[i][o].append(product_dict[id_order])
#        with open(f"out/branch/branch_product_{i}.json", 'w') as js_file:
#            json.dump(dict_branch_product[i], js_file)  
                
#    with open("out/branch_product.json", 'w') as js_file:
#        json.dump(dict_branch_product, js_file)  


if __name__ == "__main__":


#----------------------------------------------------->

#    branch_data()
 
    dict_branch = json.load(open("out/branch/branch_product_51.json",'r')) 
    for i in dict_branch:
        print (dict_branch[i], i, len(dict_branch[i]))
#---------------------------------->  
    
    
#    Сортировать продукты по магазинам посмотреть какой магазин больше всего продал продуктов 
#    какой больше всего принес прибыль

#    Выбрать самый популярный средний и самый не популярный магазин
#    сделать статистику продуктов по месяцам
#    популярные продукты
#    популярные категории
#
              
