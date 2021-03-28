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
import os

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
            
    for i in dict_branch:
        with open(f"out/branch/branch_product_{i}.json", 'w') as js_file:
            json.dump(dict_branch[i], js_file)  
    

class DATA(object):
   def __init__(self):
       self.file = []

   def parseIMG(self, dir_name):
       path = f"{dir_name}/"
       print ("PARSING",path)
       for r, d, f in os.walk(path):
           for ix, file in enumerate(f): 
                      if ".json" in file: 
                          self.file.append(os.path.join(r, file))


if __name__ == "__main__":

#----------------------------------------------------->

    C = CUSTOMER() #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']   
    C_arr = C.to_numpy()
    customet_dict = utils.func_return(C_arr, 0) 
    #print (customet_dict)
#    branch_data()
    
    D = DATA()
    D.parseIMG('out/branch')
    
    
    dict_popular_branch = {}
    #dict_count = {}
    for filename in D.file:
        branch_id = filename.split(".")[0].split("_")[-1]
#        print (filename, branch_)
        dict_branch = json.load(open(filename,'r')) 
        dict_popular_branch[branch_id] = {}
        #dict_count[branch_id] = [[],[]]
        for i in dict_branch:
            for o in range(len(dict_branch[i])):
                id_product = dict_branch[i][o][1]
                count_product = dict_branch[i][o][2]
                customet_id = dict_branch[i][o][-2]
                try:
                    cus = C_arr[customet_dict[float(customet_id)],:][0].tolist()
                except KeyError:
                    pass    
                    
                if sum(cus[1:]) == 4:
                    #print (i, o, sum(cus[1:]))
                    #dict_popular_branch[branch_id][i]
                    try:
                        dict_popular_branch[branch_id][customet_id][i] += count_product
                        #print (dict_popular_branch[branch_id][customet_id][i])
                    except KeyError:
                        dict_popular_branch[branch_id][customet_id] = {'01':0, '02':0, '03':0, '04':0, '05':0, '06':0, '07':0, '08':0, '09':0, '10':0, '11':0, '12':0}  
                        dict_popular_branch[branch_id][customet_id][i] += count_product  
   
#    for i in dict_popular_branch:
#        with open(f"out/branch_customer/branch_customer_{i}.json", 'w') as js_file:
#            json.dump(dict_popular_branch[i], js_file)  
                         
    print ("START")                    
    for i in dict_popular_branch:
        fig, ax = plt.subplots(figsize=(10,10), clear=True)
        ax.set_title(f'ID точки - {i}')
        ax.set_xlabel('Месяц')
        ax.set_ylabel('Покупатели/покупки')
        for j in dict_popular_branch[i]:
            #print (j)
            if int(j) != 0:
                Nul = 0
                for N in list(dict_popular_branch[i][j].values()):
                    if int(N) > 50:
                        Nul+=1
                if Nul == 12:
                    print (list(dict_popular_branch[i][j].values()))
                    ax.plot(list(dict_popular_branch[i][j].keys()), list(dict_popular_branch[i][j].values()), label = f"{j}") 
                    ax.legend(loc='lower right')

        fig.savefig(f"github/branch_customer/{i}.jpg")  # cat/cat2
        fig.clear(True)
        plt.close(fig)                        

#---------------------------------->    
#    Сортировать продукты по магазинам посмотреть какой магазин больше всего продал продуктов 
#    какой больше всего принес прибыль

#    Выбрать самый популярный средний и самый не популярный магазин
#    сделать статистику продуктов по месяцам
#    популярные продукты
#    популярные категории
#
              
#    Найти в каком магазине самые активные покупатели (оставили свои координаты) 

#Чт 09 июл 2020 15∶20∶11            
