import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
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
    fig, ax = plt.subplots(figsize=(10,10), clear=True)
    if myexplode != None:
        #ax.pie(vals, explode=myexplode, labels=labels, autopct='%1.2f%%', startangle=90, pctdistance=0.85)
        ax.pie(vals, explode=myexplode, labels=labels, autopct='%.2f', startangle=90, pctdistance=0.85)
    else:
        #ax.pie(vals, labels=labels, autopct='%1.2f%%', startangle=90, pctdistance=0.85)
        ax.pie(vals, labels=labels, autopct='%.2f', startangle=0, pctdistance=0.85)
    if types != None:
        centre_circle = plt.Circle((0,0),0.70,fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)

    ax.axis("equal")
    ax.set_title(f"ID продукта: {title}", loc="left", pad=20)
    ax.legend(loc='lower right') #, bbox_to_anchor=(0.7, 0.7) 'upper left' bbox_to_anchor=(0.5, 0., 0.5, 0.5) 'best'
    fig.savefig(save_name)
    fig.clear(True)
    plt.close(fig)

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
    #see_stat(o_open)
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
#        # Array
#        self.customer_arr = self.customer_open.to_numpy()
        self.order_arr = self.order_open.to_numpy()
        self.product_arr = self.product_open.to_numpy()
#        # Dict Graph
#        self.customer_dict = self.func_return(self.customer_arr, 0)
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
                          "Amount_Charged": self.order_arr[i,4], "CONSENT":ID_customer[1],
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

    def func_return(self, x, y):
        dict = {} 
        for i in range(x.shape[0]):
            try:
                dict[x[i,y]].append(i)
            except KeyError:
                dict[x[i,y]] = [i]
        return dict    

    def get_from_index(self, x):
        return self.product_arr[x,:].tolist()
    
    def save_data(self, x):
        with open(x, 'w') as js_file:
            json.dump(self.sort_dict, js_file)

    def open_data(self, x):
        with open(x) as json_file:
            data = json.load(json_file)
            return data

    # Cопутствующий продукт создать файл для обработки
    def related_products(self):
        self.product_dict = self.func_return(self.product_arr, 0) #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount'] 
        self.product_open = self.product_open.sort_values(['Items_Count']) # Сортировка
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
        _product_dict = self.func_return(self.product_arr, 1)  #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount'] 
        arr = self.product_open.to_numpy()
        for j in vals_prod[:]:
            #print (len(_product_dict[j])) # Кол во покупок с этим товаром
            Z = np.zeros((len(vals_prod)))
            for k in _product_dict[j]:
                _id_o = arr[k,0]    #получаю ИД oredr и продукта
                for u in self.product_dict[_id_o]:
                     ix_z = int(arr[u,1])
                     if int(j) != int(ix_z): 
                        ix_z = dict_to_coding[ix_z]
                        Z[ix_z] += arr[u,2]

            new_dict[j] = Z.tolist()
        print ("END", time.time()-start, len(new_dict))

        #---------------------------------------->
        # Сохраняю файл
        with open("out/related_products.json", 'w') as js_file:
            json.dump(new_dict, js_file)

        #---------------------------------------->
# Сортировка сопутствующего товара
def related_product_sort():
        dict_to_encoding = json.load(open("dict_to_encoding.json",'r'))
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
                                        #t_d[ix] = o
                                        t_d[dict_to_encoding[str(ix)]] = o
                                        P1 = P1 - o
                            except:
                                   print (o, P1, i)   
                            
                    if P1 > 0:
                        t_d["остальные"] = P1
                        _dict[i] = t_d  
                        #diag_circle(list(t_d.values()), list(t_d.keys()) , None, i, f"github/related_products/{i}.jpg")
                    
        with open("out/sort_related_products.json",'w') as js_file:
                json.dump(_dict, js_file)

# Визуализация сопутствующего товара
def visual_related_product():
    F = open("out/sort_related_products.json", 'r')
    data = json.load(F)
    for i in data:
        diag_circle(list(data[i].values()), list(data[i].keys()) , None, i, f"github/related_products/{i}.jpg")
                 


# Сортировка сопутствующего товара по месяцам
# TO DO
###########
def visual_related_m():
    F = open("out/sort_related_products.json", 'r')
    data = json.load(F)
    for i in data:
        print (len(data[i]), i)


if __name__ == "__main__":
    #NAME = PRODUCTNAME()
    #S = Sort_v1()
#----------------->
    # Сопутствующие продукты
    #S.related_products()
    #related_product_sort()
    #visual_related_product()
#----------------->
    # Сортировка сопутствующего товара по месяцам
    #visual_related_m()
    



