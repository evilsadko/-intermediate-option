import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import json
import time
from utils import diag_circle, see_stat

#def see_stat(x, y=0):
#    if y == "list":
#        print (x.columns.tolist())
#    else:
#        for c in  x.columns.tolist():
#            print (f"###############\n{x[c].value_counts(dropna=False)}")


#def diag_circle(vals, labels, myexplode, title, save_name, types=None):
#    fig, ax = plt.subplots(figsize=(50,50))
#    ax.pie(vals, explode=myexplode, labels=labels, autopct='%1.2f%%', startangle=90, pctdistance=0.85)

#    if types != None:
#        centre_circle = plt.Circle((0,0),0.70,fc='white')
#        fig = plt.gcf()
#        fig.gca().add_artist(centre_circle)

#    ax.axis("equal")
#    ax.set_title(title)
#    ax.legend(loc='best') #, bbox_to_anchor=(0.7, 0.7) 'upper left' bbox_to_anchor=(0.5, 0., 0.5, 0.5)
#    plt.savefig(save_name)


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
    p_open = pd.read_csv('in/B24_dbo_Crm_product_in_order.csv', delimiter=',')
    p_open = p_open[['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']] 
    return p_open
    
def ORDER():
    o_open = pd.read_csv('in/B24_dbo_Crm_orders.csv', delimiter=',')
    #see_stat(o_open)
    o_open = o_open[['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date']]
    o_open['price_before_discount'] = o_open['price_before_discount'].replace(np.nan, 0)
    return o_open.sort_values(by=['Order_Date'])

def PRODUCTNAME():
    p_open = pd.read_csv('B24_dbo_Products.csv', delimiter=',')
    #see_stat(p_open)
    return p_open

def chunks(lst, count):
    start = 0
    for i in range(count):
          stop = start + len(lst[i::count])
          yield lst[start:stop]
          start = stop     

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
            #for ix, o in enumerate(list(data.keys())[:]):
                #print (data[o], ix, o)
                
        print ("DONE")


# САМЫЕ ПОПУЛЯРНЫЕ КАТЕГОРИИ
    def diag_product_2(self):
#------------------------------------------->
# Получить сумму всех продаж
        S = self.product_open['Total_Amount'].sum()
        self.product_dict = self.func_return(self.product_arr, 1) #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount'] 
        print ("Общая продажа", S)
        
#------------------------------------------->
# Разделить продукты на категории
        # Категории
        NAME = PRODUCTNAME() # [ ID, Product_Id, LocalName, Category1_Id, Category1_Name, Category2_Id, Category2_Name] 
        name_arr = NAME.to_numpy() 

## Разложить продукты по категориям        
        #CatID_1 = self.func_return(name_arr, 3)  # Категория 1
        CatID_1 = self.func_return(name_arr, 5) # Категория 2 

        #Test_arr = [] #Можно использовать промежуточный список
        for i in CatID_1 :
            #print (len(CatID_1[i]))
            T_price = 0
            for o in CatID_1[i]:
                id_p = name_arr[o,1]
                try:
                    for id_p_arr in self.product_dict[id_p]:
                        F = self.product_arr[id_p_arr,:].tolist() 
                        T_price += F[-2]  
                except KeyError:
                    pass
            S -= T_price
            CatID_1[i] = T_price
            #Test_arr.append((i, T_price)) #промежуточный список
        sorted_tuples = sorted(CatID_1.items(), key=lambda item: item[1]) # Сортировка
        self.min_visual_product(np.array(sorted_tuples)) # <- Test_arr
#--------------------------->
        ty = chunks(list(sorted_tuples),9) # Разрезаю на части
        self.get_g(list(ty))
            
#---------------------------->
        L = []
        V = []
        M = []
        for i in CatID_1:
            #print (CatID_1[i], i)
            if CatID_1[i] > 0:
                L.append(i)
                V.append(CatID_1[i])
                M.append(0)
        # Добавить остаток
        L.append("Other")
        V.append(S)
        M.append(0.2)

        diag_circle(V[:], L[:], M[:],  "Популярные категории", "github/popular_categories.jpg")
        #print(sorted_dict)  # {1: 1, 3: 4, 2: 9}
#------------------------------------------------
#        CatID_2 = self.func_return(name_arr, 5)
#        LEN_2 = 0    
#        for i in CatID_2:
#            #print (len(CatID_2[i]))
#            LEN_2 += len(CatID_2[i] )
#        print (len(CatID_1), LEN_1, len(CatID_2), LEN_2)  

    def get_g(self, data):
        fig, ax = plt.subplots(len(data), figsize=(20, 20))        
        for ix in range(len(data)):
            A = np.array(data[ix])
            ax = fig.add_subplot(len(data)//3, len(data)//3, ix+1)
            max_y = np.amax(A[:,1])
            min_y = np.amin(A[:,1])
            ax.set_ylim([min_y, max_y])
            ax.bar(A[:,0], A[:,1], width = 0.3)  #color = '#1D2F6F'
        #fig.set_figwidth(20)
        #fig.set_figheight(20)
        plt.savefig("github/TEST.jpg") 


    def min_visual_product(self, _arr):
        x = range(0, _arr.shape[0])
        fig, ax = plt.subplots(1, figsize=(16, 6))# numerical x
        plt.bar(x[:], _arr[:,1], width = 0.3)  #color = '#1D2F6F'
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)# x y details
        plt.ylabel('Продажи')
        plt.xlabel('Категории')
        #ax.set_xticklabels(_arr[:,0])
#        plt.xlim(-0.5, len(count))# grid lines
#        plt.ylim(-0.5, max(count)/1000)
        ax.set_axisbelow(True)
        ax.yaxis.grid(color='gray', linestyle='dashed', alpha=0.2)# title and legend
        plt.title('Cтатистика продаж категорий', loc ='left', pad=20)
        plt.savefig("github/sort_stat_group.jpg")



if __name__ == "__main__":
    #NAME = PRODUCTNAME()
    S = Sort_v1()
#----------------->
    S.diag_product_2()
#

# Соптствующие товары !!!
# популярные продукты в отношении к категории !!!
# последние совпадающиесе цифры кредитной карты!!!
# Вывести категории

# покупку разделить на категории
# В разрезе на месяц в разрезе за квартал
# продукты в продукты есть ли подкатегории
# Послать остатки скалада 
# Что бы эти графики работали нужно в реальном времени воздействовать что бы они повышались
# Если они не изменяються учитывать охват магазина
# Что бы в магазин привлекать людей из далека нужен уникальный продукт характеристики цена состав этикетка


