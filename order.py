import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import json
import time

def see_stat(x, y=0):
    if y == "list":
        print (x.columns.tolist())
    else:
        for c in  x.columns.tolist():
            print (f"###############\n{x[c].value_counts(dropna=False)}")


def diag_circle(vals, labels, myexplode, title, save_name, types=None):
    fig, ax = plt.subplots(figsize=(10,10))
    ax.pie(vals, explode=myexplode, labels=labels, autopct='%1.2f%%', startangle=90, pctdistance=0.85)

    if types != None:
        centre_circle = plt.Circle((0,0),0.70,fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)

    ax.axis("equal")
    ax.set_title(title)
    ax.legend(loc='best') #, bbox_to_anchor=(0.7, 0.7) 'upper left' bbox_to_anchor=(0.5, 0., 0.5, 0.5)
    plt.savefig(save_name)

def CUSTOMER():
    c_open = pd.read_csv('B24_dbo_Crm_customers.csv', delimiter=',')
    c_open = c_open[['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']]
    c_open['join_club_success'] = c_open['join_club_success'].replace(np.nan, 2)
    c_open['Could_send_sms'] = c_open['Could_send_sms'].replace(np.nan, 0)
    c_open['Could_send_email'] = c_open['Could_send_email'].replace(np.nan, 0)
    c_open['consent'] = c_open['consent'].replace(np.nan, 0)
    c_open = c_open.apply(lambda x: pd.to_numeric(x, errors='coerce')).dropna() # Убираю все строки
    return c_open

def PRODUCT():
    p_open = pd.read_csv('B24_dbo_Crm_product_in_order.csv', delimiter=',')
    p_open = p_open[['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']] 
    return p_open
    
def ORDER():
    o_open = pd.read_csv('B24_dbo_Crm_orders.csv', delimiter=',')
    o_open = o_open[['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date']]
    o_open['price_before_discount'] = o_open['price_before_discount'].replace(np.nan, 0)
    return o_open.sort_values(by=['Order_Date'])

def PRODUCTNAME():
    p_open = pd.read_csv('B24_dbo_Products.csv', delimiter=',')
    #see_stat(p_open)
    return p_open


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
 
    def func_return(self, x, y):
        dict = {} 
        for i in range(x.shape[0]):
            try:
                dict[x[i,y]].append(i)
            except KeyError:
                dict[x[i,y]] = [i]
        return dict    
   
    def diag_product_0(self):
        # Количество покупок с одним товаром
        self.customer_dict = self.func_return(self.customer_arr, 0) #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']  
        self.order_dict = self.func_return(self.order_arr, 1) #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date'] 
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
        self.customer_dict = self.func_return(self.customer_arr, 0) #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']  
        self.order_dict = self.func_return(self.order_arr, 1) #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date'] 
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
        self.customer_dict = self.func_return(self.customer_arr, 0) #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']  
        self.order_dict = self.func_return(self.order_arr, 1) #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date'] 
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
        CatID_1 = self.func_return(name_arr, 5) # cat2
        #CatID_1 = self.func_return(name_arr, 3) # cat

#############
        self.product_dict = self.func_return(self.product_arr, 1) #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']   
        #self.customer_dict = self.func_return(self.customer_arr, 0) #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']  
        self.order_dict = self.func_return(self.order_arr, 0) #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date'] 
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
            with open('category2.json', 'w') as js_file:
                json.dump(dict_save, js_file)

###########
#  Популярные продукты в категории
#
    def popular_product_category(self):
        NAME = PRODUCTNAME() # [ ID, Product_Id, LocalName, Category1_Id, Category1_Name, Category2_Id, Category2_Name] 
        name_arr = NAME.to_numpy() 
        #CatID_1 = self.func_return(name_arr, 5) # cat2
        CatID_1 = self.func_return(name_arr, 3) # cat

#############
        self.product_dict = self.func_return(self.product_arr, 1) #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']   
        self.order_dict = self.func_return(self.order_arr, 0) #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date'] 
        dict_save = {}
        for i in CatID_1:

            
            dict_save[i] = []
            for o in CatID_1[i]:
                id_p = name_arr[o,1]
                try:
                    dict_save[i].append([id_p, len(self.product_dict[id_p])])
                    print (len(self.product_dict[id_p]))
                except KeyError:
                    pass

        with open('out/popular_product_category.json', 'w') as js_file:
                json.dump(dict_save, js_file)

def popular_product_category_vis():
        data = json.load(open('out/popular_product_category.json', 'r'))
        for i in data:
            arr = data[i]
            #print (i, arr.shape)
            try:
                if len(arr) > 0:
                    fig, ax = plt.subplots(figsize=(10,10), clear=True)
                    ax.set_title(f'ID категории - {i}')
                    ax.set_xlabel('ID продукта')
                    ax.set_ylabel('Количество продуктов')
                    for o in range(len(arr)):
                            #print (len(arr))
                            #ax.plot([o], [arr[o][1]], label = f"{arr[o][0]}")  
                            ax.bar([o], [arr[o][1]], label = f"{arr[o][0]}")
                    ax.legend(loc='lower right')
                    #print (arr)
                    fig.savefig(f"github/popular_category/{i}.jpg")  # cat/cat2
                    fig.clear(True)
                    plt.close(fig)
                    #print ("OK")
            except IndexError:
                pass
# ID продукта, сумма продаж или колво проданных едениц            


if __name__ == "__main__":

    #S = Sort_v1()
#----------------->
    #S.diag_product_0()  # Количество покупок с одним товаром ERROR
#----------------->
    #S.diag_product_1()  # Отношение покупателей к покупкам 
#----------------->
    #S.diag_product_2() # Разность покупки
#----------------->
    #S.diag_category_0() # Категории
#----------------->

    #S.popular_product_category() # Самый популярный продукт в категории
    popular_product_category_vis()
   

