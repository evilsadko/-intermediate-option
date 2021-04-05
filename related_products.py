import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import threading
import json
import time
from utils import func_return, diag_circle, see_stat, CUSTOMER, PRODUCT, ORDER, PRODUCTNAME


    
def ORDER():
    #o_open = pd.read_csv('in/B24_dbo_Crm_orders.csv', delimiter=',')
    o_open = pd.read_pickle("in/B24_dbo_Crm_orders.pk")
    #see_stat(o_open)
    o_open = o_open[['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date']]
    o_open['price_before_discount'] = o_open['price_before_discount'].replace(np.nan, 0)
    return o_open.sort_values(by=['Order_Date'])





class Sort_v1:
    def __init__(self):
        # Pandas
        self.order_open = ORDER() #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date'] 
        self.product_open = PRODUCT() #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']   
        # Array
        self.order_arr = self.order_open.to_numpy()
        self.product_arr = self.product_open.to_numpy()

    # Cопутствующий продукт создать файл для обработки
    def related_products(self):
        product_dict = func_return(self.product_arr, 0) #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount'] 
        product_open = self.product_open.sort_values(['Items_Count']) # Сортировка
        vals_prod = self.product_open.drop_duplicates("Product_ID") # Убрать дубликаты
        vals_prod = vals_prod["Product_ID"] 
        print (len(vals_prod)) # Узнать кол во ID продуктов
        #----------------------->
        # Декодирование кодирование в словарь
        dict_to_coding = {}
        dict_to_encoding = {}
        for ix, ij in enumerate(vals_prod):
            dict_to_coding[ij] = ix 
            dict_to_encoding[ix] = ij
        #------------------------------------->
        # Обработка файлов
        start = time.time()
        new_dict = {}
        _product_dict = func_return(self.product_arr, 1)  #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount'] 
        for j in vals_prod[:]:
            #print (len(_product_dict[j])) # Кол во покупок с этим товаром
            Z = np.zeros((len(vals_prod)))
            for k in _product_dict[j]:
                _id_o = self.product_arr[k,0]    #получаю ИД oredr и продукта
                for u in product_dict[_id_o]:
                     ix_z = int(self.product_arr[u,1])
                     if int(j) != int(ix_z): 
                        ix_z = dict_to_coding[ix_z]
                        Z[ix_z] += self.product_arr[u,2]

            new_dict[j] = Z.tolist()
        print ("END", time.time()-start, len(new_dict))

        #---------------------------------------->
        # Сохраняю файлы
        with open("out/related_products.json", 'w') as js_file:
            json.dump(new_dict, js_file)
        
        with open("out/dict_to_encoding.json", 'w') as js_file:
            json.dump(dict_to_encoding, js_file)
        #---------------------------------------->
    
    # Сортировка товара по месяцам
    def products_date(self):
            product_dict = func_return(self.product_arr, 1) #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount'] 
            order_dict = func_return(self.order_arr, 0) #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date']
            temp_dict = {}
            for i in product_dict:
                M = {'01':0, '02':0, '03':0, '04':0, '05':0, '06':0, '07':0, '08':0, '09':0, '10':0, '11':0, '12':0}
                for v in product_dict[i]:
                    temp = self.product_arr[v,:].tolist()
                    ord_id = temp[0]
                    _date = self.order_arr[order_dict[ord_id],:].tolist()[0][-1].split(" ")[0].split("-")[1]
                    M[_date] += temp[3]
                temp_dict[i] = M
                #---------------------------->
                fig, ax = plt.subplots(figsize=(10,10), clear=True)
                ax.set_title(f'ID продукта - {i}')
                ax.set_xlabel('Месяц')
                ax.set_ylabel('Количество продуктов')
                ax.bar(list(M.keys()), list(M.values()), color = (0.2,0.7,0.6,0.6))

                ax.plot(list(M.keys()), list(M.values()))  
                fig.savefig(f"github/products/{i}.jpg") 
                fig.clear(True)
                plt.close(fig)
            #---------------------------------------->
            # Сохраняю файлы
            with open("out/products_date.json", 'w') as js_file:
                json.dump(temp_dict, js_file)                        
                
# Сортировка сопутствующего товара
def related_product_sort():
        dict_to_encoding = json.load(open("out/dict_to_encoding.json",'r'))
        _dict = {}
        with open("out/related_products.json","r") as json_file:
                data = json.load(json_file)
                for i in data:
                    P1 = sum(data[i])
                    t_d = {}
                    for ix, o in enumerate(data[i]):
                            try:
                                if o > 0:
                                    P = o / int(P1) * 100
                                    if P > 0.5:
                                        t_d[dict_to_encoding[str(ix)]] = o
                                        P1 = P1 - o
                            except:
                                   print (o, P1, i)   
                            
                    if P1 > 0:
                        t_d["остальные"] = P1
                        _dict[i] = t_d  
                    
        with open("out/sort_related_products.json",'w') as js_file:
                json.dump(_dict, js_file)

# Визуализация сопутствующего товара
def visual_related_product():
    F = open("out/sort_related_products.json", 'r')
    data = json.load(F)
    for i in data:
        diag_circle(list(data[i].values()), list(data[i].keys()) , None, i, f"github/related_products/{i}.jpg")
                 

def visual_related_m():
            data_related = json.load(open("out/sort_related_products.json", 'r'))
            date_sort_m = json.load(open("out/products_date.json",'r'))
            for i in data_related:
#                print (i, date_sort_m[i])
#                print ("-------------")
            
                fig, ax = plt.subplots(figsize=(10,10), clear=True)
                ax.set_title(f'ID продукта - {i}')
                ax.set_xlabel('Месяц')
                ax.set_ylabel('Количество продуктов')
                ax.bar(list(date_sort_m[i].keys()), list(date_sort_m[i].values()), color = (0.2,0.7,0.6,0.6))
                for o in data_related[i]:
                    if o != "остальные":
                        #print (o, date_sort_m[o]) 
                        #print ("----------")                                   
                        ax.plot(list(date_sort_m[o].keys()), list(date_sort_m[o].values()), label = f"{o}")  
                        ax.legend(loc='lower right')
                fig.savefig(f"github/related_products_m/{i}.jpg") 
                fig.clear(True)
                plt.close(fig)


if __name__ == "__main__":
    #NAME = PRODUCTNAME()
    S = Sort_v1()
#----------------->
    # Сопутствующие продукты
    S.related_products()
    #related_product_sort()
    #visual_related_product()
#----------------->
    # Сортировка сопутствующего товара по месяцам
    #S.products_date()
    #visual_related_m()



