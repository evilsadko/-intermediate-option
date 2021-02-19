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
    fig, ax = plt.subplots(figsize=(50,50))
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
            #for ix, o in enumerate(list(data.keys())[:]):
                #print (data[o], ix, o)
                
        print ("DONE")


    def diag_product_2(self):
# Получить сумму всех продаж
        S = self.product_open['Total_Amount'].sum()
        self.order_dict = self.func_return(self.order_arr, 0) #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date'] 
        #amount_charged_sum= 1 573 811 359.5180595, price_before_discount_sum= 1 719 882 683.943696
       
# Разделить продукты на категории
#------------------------------------------->
        self.product_dict = self.func_return(self.product_arr, 1) #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount'] 
        Total = 0
        for i in range(self.product_arr.shape[0]):
            id_order = self.order_dict[self.product_arr[i,0]]
            Total += self.product_arr[i,3]
        print (int(Total), int(S), int(Total) == int(S))

        # 211 884 081.48872375
#------------------------------------------->
        NAME = PRODUCTNAME() # [ ID, Product_Id, LocalName, Category1_Id, Category1_Name, Category2_Id, Category2_Name] 
        print (len(NAME['Category1_Id']))
        name_arr = NAME.to_numpy() 

## Разложить продукты по категориям        
        CatID_1 = self.func_return(name_arr, 3)
        LEN_1 = 0
        for i in CatID_1 :
            #print (len(CatID_1[i]))
            LEN_1 += len(CatID_1[i])
            T_price = 0
            for o in CatID_1[i]:
                T = name_arr[o,:].tolist()
                id_p = T[1]
                try:
                    for k in range(len(self.product_dict[id_p])):
                        id_p_arr = self.product_dict[id_p][k]
                        F = self.product_arr[id_p_arr,:].tolist() 
                        T_price += F[-2]  
                    #print (len(self.product_dict[id_p]))
                except KeyError:
                    pass
            S -= T_price
            CatID_1[i] = T_price
        sorted_tuples = sorted(CatID_1.items(), key=lambda item: item[1])
        self.min_visual_product(np.array(sorted_tuples))
        L = []
        V = []
        M = []
        for i in CatID_1:
            print (CatID_1[i], i)
            if CatID_1[i] > 0:
                L.append(i)
                V.append(CatID_1[i])
                M.append(0)
        L.append("Other")
        V.append(S)
        M.append(0.2)
        #diag_circle(V, L, M,  "Анализ ID категорий", "C.jpg")
        diag_circle(V[:], L[:], M[:],  "Анализ ID категорий", "github/C.jpg")
        #myexplode.append(0.2)

#        
        #print(sorted_dict)  # {1: 1, 3: 4, 2: 9}
#------------------------------------------------
#        CatID_2 = self.func_return(name_arr, 5)
#        LEN_2 = 0    
#        for i in CatID_2:
#            #print (len(CatID_2[i]))
#            LEN_2 += len(CatID_2[i] )
#        print (len(CatID_1), LEN_1, len(CatID_2), LEN_2)   

    def min_visual_product(self, _arr):
        x = range(0, _arr.shape[0])
        fig, ax = plt.subplots(1, figsize=(16, 6))# numerical x
        plt.bar(x[:], _arr[:,1], width = 0.3)  #color = '#1D2F6F'
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)# x y details
        plt.ylabel('Сумма продаж')
        plt.xlabel('Категории')
#        plt.xlim(-0.5, len(count))# grid lines
#        plt.ylim(-0.5, max(count)/1000)
        ax.set_axisbelow(True)
        ax.yaxis.grid(color='gray', linestyle='dashed', alpha=0.2)# title and legend
        plt.title('Статистика продуктов по группам', loc ='left')
        plt.savefig("github/G.jpg")
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


#        #personal_data_user
#        self.customer_dict = self.func_return(self.customer_arr, 0) #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']  
#        self.order_dict = self.func_return(self.order_arr, 1) #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date'] 

#        #self.order_dict_ = self.func_return(self.order_arr, 0)
#        #self.product_dict = self.func_return(self.product_arr, 0) #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']   
#        fig, ax = plt.subplots(figsize=(10,10)) 
#        M = {'01':0, '02':0, '03':0, '04':0, '05':0, '06':0, '07':0, '08':0, '09':0, '10':0, '11':0, '12':0}
#        for i in list(self.order_dict.keys())[:30]:
#                try:
#                    idx_cust = self.customer_dict[i][0]  # idx в списке покупателя
#                    _customet = self.customer_arr[idx_cust,:].tolist() # Информация о покупателе

#                    #idx_order = self.order_dict[i]
#                    order_list = self.order_dict[i] # 

#                    date_dict_price = {}
#                    #price_list = []
#                    for h in order_list:
#                        _order = self.order_arr[h,:].tolist()
#                        _date = _order[-1]
##                        _item_count = _order[2]
##                        _price_before = _order[3]
##                        _amount_charge = _order[4]
#                        #date_list.append(_order[-1])
#                        #price_list.append(_order[3])

##                        try: 
##                            M[str(_date.split(" ")[0].split("-")[1])] += int(_order[3])
##                        except ValueError:
##                            print (_date, _order[3])

#                        #    print ("ERROR", _date)                    
#                        print (_order)
#                    #print (list(M.keys()), list(M.values()))
#                    #ax.bar(list(M.keys()), list(M.values()), label = f"{_customet[0]}") 
#                    ax.plot(list(M.keys()), list(M.values()), label = f"{_customet[0]}") 
#                    ax.legend()
#                    #ax.semilogy(list(date_dict_price.keys()), list(date_dict_price.values()), label = f"{_customet[0]}")                    
#                    print (len(order_list), _customet[0], "====================================")
#                    
#                except KeyError:
#                    pass
#         
#        #plt.show()
#        #plt.savefig("T.jpg")
#        fig.savefig('T.png')
#


#    def diag_product_2(self):
## Получить сумму всех продаж
##S = sum(self.product_open['Total_Amount'])
#        S = self.product_open['Total_Amount'].sum()
#        print (S)
##        S = self.order_open['price_before_discount'].sum()
##        print (S)


#        NAME = PRODUCTNAME() # [ ID, Product_Id, LocalName, Category1_Id, Category1_Name, Category2_Id, Category2_Name] 
#        print (len(NAME['Category1_Id']))
#        name_arr = NAME.to_numpy() 
#        self.product_dict = self.func_return(self.product_arr, 1)
## Разложить продукты по категориям        
#        CatID_1 = self.func_return(name_arr, 3)
#        LEN_1 = 0
#        ALL = 0
#        for i in CatID_1 :
#            #print (len(CatID_1[i]))
#            LEN_1 += len(CatID_1[i])
#            T_price = 0
#            for o in CatID_1[i]:
#                T = name_arr[o,:].tolist()
#                id_p = T[1]
#                try:
#                    id_order = self.order_dict[self.product_arr[i,0]]
#                    G = 0
#                    for k in range(len(self.product_dict[id_p])):
#                        id_p_arr = self.product_dict[id_p][k]
#                        F = self.product_arr[id_p_arr,:].tolist() 
#                        T_price += F[3] 
#                        ALL +=  F[3]
#                        G+=
#                        #print (F)
#                    print (len(self.product_dict[id_p]), self.order_arr[id_order,:].tolist())
#                except KeyError:
#                    pass
#            CatID_1[i] = T_price
#            #print (T_price)
#        print (S, ALL)
##------------------------------------------------
##        CatID_2 = self.func_return(name_arr, 5)
##        LEN_2 = 0    
##        for i in CatID_2:
##            #print (len(CatID_2[i]))
##            LEN_2 += len(CatID_2[i] )
##        print (len(CatID_1), LEN_1, len(CatID_2), LEN_2)   

