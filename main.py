import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import json
import time
from utils import diag_circle, see_stat, CUSTOMER, PRODUCT, ORDER, PRODUCTNAME, ORDER
    
class Sort_v1:
    def __init__(self):
        # Pandas
        self.customer_open = CUSTOMER() #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']   
        self.order_open = ORDER() #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date'] 
        self.product_open = PRODUCT() #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']   
        # Array
        self.customer_arr = self.customer_open.to_numpy()
        self.order_arr = self.order_open.to_numpy()
        self.product_arr = self.product_open.to_numpy()
        # Dict Graph
        self.customer_dict = self.func_return(self.customer_arr, 0)
        self.order_dict = self.func_return(self.order_arr, 0)
        self.product_dict = self.func_return(self.product_arr, 0)

        self.sort_dict = {}

    def func_unite(self, see=None):
        key_error = 0
        not_errot = 0
        # Прохожу циклом по покупкам ордер
        for i in range(self.order_arr.shape[0]):
            try:
                # Из получаю продукты исходя из покупки ордер
                gen_ls = [self.get_from_index(p) for p in self.product_dict[self.order_arr[i,0]]] #arr_p[arr_o[i,0]]

                # Получаю  индекс покупателя в массиве
                ID_customer = self.customer_dict[self.order_arr[i,1]][0]

                # По индексу получаю информацию о покупателе
                ID_customer = self.customer_arr[ID_customer,:].tolist()
                if see != None:
                    print ("Product in order", len(gen_ls))
                    print ("Customer ID", ID_customer, int(ID_customer[0]), self.order_arr[i,1])

                # Создаю словарь где ключ ID покупки ордера

                #sort_dict[arr_o[i,0]] = [[gen_ls, ID_customer]] # Новая
                T = self.func_repack(gen_ls)
                T.append({"DATE_ORDER":self.order_arr[i,-1], "Items_Count":self.order_arr[i,2], "price_before_discount":self.order_arr[i,3], 
                          "Amount_Charged": self.order_arr[i,5], "CONSENT":ID_customer[1],
                          "USER": ID_customer[0], "JCS":ID_customer[2], "CSS":ID_customer[3], "CSE":ID_customer[4],})
                self.sort_dict[self.order_arr[i,0]] = T
                not_errot += 1
            except KeyError:
                key_error += 1
        print (len(self.sort_dict), key_error, not_errot)

    def func_repack(self, x):
        list = []
        for i in x:
            list.append({"P_ID":i[1], "P_COUNT":i[2], "Total_Amount":i[3],"TotalDiscount":i[4]})
        return list

    def get_from_index(self, x):
        return self.product_arr[x,:].tolist()
    
    def save_data(self, x):
        with open(x, 'w') as js_file:
            json.dump(self.sort_dict, js_file)

    def open_data(self, x):
        with open(x) as json_file:
            data = json.load(json_file)
            return data
            #for ix, o in enumerate(list(data.keys())[:]):
                #print (data[o], ix, o)
                
        print ("DONE")

    def diag_product_0(self):
        # Количество покупок с одним товаром
        self.customer_dict = func_return(self.customer_arr, 0) #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']  
        self.order_dict = func_return(self.order_arr, 2) #['Order_Id', 'Branch_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date']
        #self.product_dict = self.func_return(self.product_arr, 0) #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']
        NO_ERROR = 0
        ERROR = 0
        print (len(self.customer_dict), len(self.order_dict))
        for i in self.order_dict :
            try:
                t = self.customer_dict[i][0] 
                if len(self.order_dict[i]) == 1:
                    #print (len(self.order_dict[i]), self.customer_arr[t,:].tolist())
                    NO_ERROR += 1
                else:
                    ERROR += 1
            except KeyError:
                pass
        print (len(self.customer_dict), len(self.order_dict), NO_ERROR, ERROR)
        diag_circle([NO_ERROR, ERROR], ["один товар","остальные"], [0,0], "Количество покупок с одним товаром", "github/order/diag_order_one_product_0.jpg")

    def diag_product_1(self):
        self.customer_dict = func_return(self.customer_arr, 0) #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']  
        self.order_dict = func_return(self.order_arr, 2) #['Order_Id', 'Branch_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date']
        fig, ax = plt.subplots(figsize=(10,10)) 
        M = {'01':0, '02':0, '03':0, '04':0, '05':0, '06':0, '07':0, '08':0, '09':0, '10':0, '11':0, '12':0}
        for i in list(self.order_dict.keys())[:20]:
                try:
                    idx_cust = self.customer_dict[i][0]  # idx в списке покупателя
                    _customet = self.customer_arr[idx_cust,:].tolist() # Информация о покупателе
                    order_list = self.order_dict[i] # 
                    for h in order_list:
                        _order = self.order_arr[h,:].tolist()
                        _date = _order[-1].split(" ")[0].split("-")[1]
                        M[str(_date)] += int(_order[3])
                    #ax.bar(list(M.keys()), list(M.values()), label = f"{_customet[0]}") 
                    ax.plot(list(M.keys()), list(M.values()), label = f"{_customet[0]}") 
                    ax.legend()
                except KeyError:
                    pass
        fig.savefig('github/order/count_order_per_year.png')

    # Разность покупки 'price_before_discount', 'Amount_Charged'
    def diag_product_2(self): # Total_Amount/TotalDiscount
        self.customer_dict = func_return(self.customer_arr, 0) #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']  
        self.order_dict = func_return(self.order_arr, 2) #['Order_Id', 'Branch_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date']
        fig, ax = plt.subplots(figsize=(10,10)) 
        M = {'01':0, '02':0, '03':0, '04':0, '05':0, '06':0, '07':0, '08':0, '09':0, '10':0, '11':0, '12':0}
        for i in list(self.order_dict.keys())[:20]:
                try:
                    idx_cust = self.customer_dict[i][0]  # idx в списке покупателя
                    _customet = self.customer_arr[idx_cust,:].tolist() # Информация о покупателе
                    order_list = self.order_dict[i] # 
                    for h in order_list:
                        _order = self.order_arr[h,:].tolist()
                        _date = _order[-1].split(" ")[0].split("-")[1]
                        M[str(_date)] += (int(_order[4])-int(_order[3]))
                    #ax.bar(list(M.keys()), list(M.values()), label = f"{_customet[0]}") 
                    ax.plot(list(M.keys()), list(M.values()), label = f"{_customet[0]}") 
                    ax.legend()
                except KeyError:
                    pass
        fig.savefig('github/order/difference_price_amount.png')

    def diag_category_0(self):
        NAME = PRODUCTNAME() # [ ID, Product_Id, LocalName, Category1_Id, Category1_Name, Category2_Id, Category2_Name] 
        name_arr = NAME.to_numpy() 
        CatID_1 = func_return(name_arr, 5) # cat2
        #CatID_1 = self.func_return(name_arr, 3) # cat

#############
        self.product_dict = func_return(self.product_arr, 1) #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']   
        #self.customer_dict = self.func_return(self.customer_arr, 0) #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']  
        self.order_dict = func_return(self.order_arr, 0) #['Order_Id', 'Branch_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date']
        fig, ax = plt.subplots(figsize=(10,10)) 
        dict_save = {}
        for i in CatID_1 :
            #M = {'01':[0,0], '02':[0,0], '03':[0,0], '04':[0,0], '05':[0,0], '06':[0,0], '07':[0,0], '08':[0,0], '09':[0,0], '10':[0,0], '11':[0,0], '12':[0,0]}
            M = {'01':0, '02':0, '03':0, '04':0, '05':0, '06':0, '07':0, '08':0, '09':0, '10':0, '11':0, '12':0}
            for o in CatID_1[i]:
                id_p = name_arr[o,1]
                try:
                    for k in range(len(self.product_dict[id_p])):
                        id_p_arr = self.product_dict[id_p][k]
                        F = self.product_arr[id_p_arr,:].tolist() 
                        price = F[3]
                        ord_id = F[0]
                        ord_id = self.order_dict[ord_id]
                        _order = self.order_arr[ord_id,:].tolist()[0]
                        _date = _order[-1].split(" ")[0].split("-")[1]
                        M[str(_date)] += price
                        #print (_order, ord_id, price, _date)
                except KeyError:
                    pass
                    #print (id_p)
            #PLOT
            if sum(M.values()) > 0:
                dict_save[i] = M
    #------------------------------------->
                plt.title(f'ID категории - {i}')
                plt.xlabel('Месяц')
                plt.ylabel('Количество продуктов')
                plt.bar(list(M.keys()), list(M.values()), color = (0.5,0.1,0.5,0.6))

                plt.plot(list(M.keys()), list(M.values()))  
                plt.savefig(f"github/cat2/{i}.jpg")  # cat/cat2
                plt.cla()
            with open('out/category2.json', 'w') as js_file:
                json.dump(dict_save, js_file)

###########
#  Популярные продукты в категории
#

if __name__ == "__main__":

    S = Sort_v1()
#----------------->
    #S.func_unite("see") # Подготовка
#----------------->
    #S.diag_product_0()  # Количество покупок с одним товаром ERROR
#----------------->
    #S.diag_product_1()  # Отношение покупателей к покупкам 
#----------------->
    #S.diag_product_2() # Разность покупки
#----------------->
    #S.diag_category_0() # Категории

