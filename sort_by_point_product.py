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
import os


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

    
#    branch_data()
    
    D = DATA()
    D.parseIMG('out/branch')
    
    
    dict_popular_branch = {}
    
    for filename in D.file:
        branch_id = filename.split(".")[0].split("_")[-1]
#        print (filename, branch_)
        dict_branch = json.load(open(filename,'r')) 
        dict_popular_branch[branch_id] = {}
        for i in dict_branch:
            dict_popular_branch[branch_id][i] = {}
            for o in range(len(dict_branch[i])):
                id_product = dict_branch[i][o][1]
                count_product = dict_branch[i][o][2]
                try:
                    dict_popular_branch[branch_id][i][id_product] += count_product
                except KeyError:
                    dict_popular_branch[branch_id][i][id_product] = count_product
    #print (dict_popular_branch["51"]["02"])  
    sort_dict = {}   
    for i in dict_popular_branch:
        sort_dict[i] = {}
        try_m = {}
        list_ = []
        for o in dict_popular_branch[i]:
#            print (len(list(dict_popular_branch[i][o].keys())))
            sort_dict[i][o] = {}
            sum_all = sum(list(dict_popular_branch[i][o].values()))

            for r in dict_popular_branch[i][o]:
                P = dict_popular_branch[i][o][r] / int(sum_all) * 100
                if P > 0.5:
                    sort_dict[i][o][r] = dict_popular_branch[i][o][r]
                    #print (P, dict_popular_branch[i][o][r], r)  
                    list_.append(r)
                try:
                    try_m[r][o] = dict_popular_branch[i][o][r]
                except KeyError:
                    try_m[r] = {'01':0, '02':0, '03':0, '04':0, '05':0, '06':0, '07':0, '08':0, '09':0, '10':0, '11':0, '12':0}  
                    try_m[r][o] = dict_popular_branch[i][o][r]  
        #print (len(list(try_m.keys())))                                  
        fig, ax = plt.subplots(figsize=(10,10), clear=True)
        ax.set_title(f'ID точки - {i}')
        ax.set_xlabel('Месяц')
        ax.set_ylabel('Количество продуктов')
        for j in list_:
            #print (list(try_m[j].keys()), list(try_m[j].values()))
            ax.plot(list(try_m[j].keys()), list(try_m[j].values()), label = f"{j}") 
            ax.legend(loc='lower right')

        fig.savefig(f"github/branch_img/{i}.jpg")  # cat/cat2
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
              
#    Найти в каком магазине самые активные покупатели              
