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

    def open_dat(self, x):
        with open(x) as json_file:
            data = json.load(json_file)
            return data
            #for ix, o in enumerate(list(data.keys())[:]):
                #print (data[o], ix, o)
                
        print ("DONE")

    def diag_user(self):
        duplicat = self.customer_open.drop_duplicates('Customer_Id') 
        A = len(duplicat)
        B = (duplicat['consent'] == 1.0).sum()
        vals  = [A-B, B]
        myexplode = [0, 0.2]
        labels = ["Не подтверждено", "Согласны на рассылку"]
        diag_circle(vals, labels, myexplode, "Для всех покупателей", "github/user/diag_user_consent_0_0.jpg") #vals, labels, myexplode, title, save_name
        #----------------------------------->
        duplicat  = self.customer_open[self.customer_open[['Customer_Id']].duplicated() == True]
        duplicat = duplicat.drop_duplicates('Customer_Id') 
        A = len(duplicat)
        B = (duplicat['consent'] == 1.0).sum()
        vals  = [A-B, B]
        myexplode = [0, 0.2]
        labels = ["Не подтверждено", "Согласны на рассылку"]
        diag_circle(vals, labels, myexplode, "Для покупателей совершивших больше одной покупки", "github/user/diag_user_consent_0_1.jpg")
        #----------------------------------->
        #C = duplicat[duplicat[]== 1.0]
        duplicat = self.customer_open.drop_duplicates('Customer_Id') 
        A = len(duplicat)
        C = (duplicat['join_club_success'] == 1.0).sum()
        D = (duplicat['Could_send_sms'] == 1.0).sum()
        I = (duplicat['Could_send_email'] == 1.0).sum()
        A = A-(C+D+I)
        vals = [C, D, I, A]
        labels = ["join_club_success", "Could_send_email", "Could_send_sms", "not access"]
        myexplode = [0.05, 0.05, 0.05, 0.05]
        diag_circle(vals, labels, myexplode, "Для всех покупателей", "github/user/diag_user_consent_1_0.jpg", True)
        #------------------------------------->
        # Для тех кто совершил больше 2 покупок
        duplicat  = self.customer_open[self.customer_open[['Customer_Id']].duplicated() == True]
        duplicat = duplicat.drop_duplicates('Customer_Id') 
        A = len(duplicat['Customer_Id'])
        C = (duplicat['join_club_success'] == 1.0).sum()
        D = (duplicat['Could_send_sms'] == 1.0).sum()
        I = (duplicat['Could_send_email'] == 1.0).sum()
        A = A-(C+D+I)
        vals = [C, D, I, A]
        labels = ["join_club_success", "Could_send_email", "Could_send_sms", "not access"]
        myexplode = [0.05, 0.05, 0.05, 0.05]
        diag_circle(vals, labels, myexplode, "Для покупателей совершивших больше одной покупки", "github/user/diag_user_consent_1_1.jpg", True)
        #---------------------------------------->
        duplicat = self.customer_open.drop_duplicates('Customer_Id') 
        C = ((duplicat['join_club_success']  == 1.0) & (duplicat['Could_send_sms'] == 1.0) & (duplicat['Could_send_email'] == 1.0)).sum()
        vals = [C, len(duplicat['Customer_Id'])-C]
        labels = ["полный доступ", "остальные"]
        myexplode = [0.05, 0.05]
        diag_circle(vals, labels, myexplode, "Для всех покупателей", "github/user/diag_user_consent_2.jpg", True)
        #---------------------------------------->
        # Покупатели скупились больше чем 1 раз
        customer_dup = self.customer_open[self.customer_open[['Customer_Id']].duplicated() == True]
        customer_dup = customer_dup.drop_duplicates('Customer_Id')
        not_duplicat = len(customer_dup['Customer_Id'])
        duplicat = len(self.customer_open.drop_duplicates('Customer_Id')) 
        P = not_duplicat / duplicat * 100
        vals  = [duplicat, not_duplicat]
        myexplode = [0, 0.2]
        labels = ["Остальные", "Покупатели совершившие покупки больше 1 раза"]
        diag_circle(vals, labels, myexplode, "Анализ всех ID", "github/user/diag_user_0.jpg")

    
    def diag_product_0(self):
        # Количество покупок с одним товаром
        self.customer_dict = self.func_return(self.customer_arr, 0) #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']  
        self.order_dict = self.func_return(self.order_arr, 1) #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date'] 
        #self.product_dict = self.func_return(self.product_arr, 0) #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']
        NO_ERROR = 0
        ERROR = 0
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
        fig.savefig('T.png')

    def diag_product_2(self):
        #personal_data_user
        self.customer_dict = self.func_return(self.customer_arr, 0) #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']  
        self.order_dict = self.func_return(self.order_arr, 1) #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date'] 

        #self.order_dict_ = self.func_return(self.order_arr, 0)
        #self.product_dict = self.func_return(self.product_arr, 0) #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']   
        fig, ax = plt.subplots(figsize=(10,10)) 
        M = {'01':0, '02':0, '03':0, '04':0, '05':0, '06':0, '07':0, '08':0, '09':0, '10':0, '11':0, '12':0}
        for i in list(self.order_dict.keys())[:30]:
                try:
                    idx_cust = self.customer_dict[i][0]  # idx в списке покупателя
                    _customet = self.customer_arr[idx_cust,:].tolist() # Информация о покупателе

                    #idx_order = self.order_dict[i]
                    order_list = self.order_dict[i] # 

                    date_dict_price = {}
                    #price_list = []
                    for h in order_list:
                        _order = self.order_arr[h,:].tolist()
                        _date = _order[-1]
#                        _item_count = _order[2]
#                        _price_before = _order[3]
#                        _amount_charge = _order[4]
                        #date_list.append(_order[-1])
                        #price_list.append(_order[3])

#                        try: 
#                            M[str(_date.split(" ")[0].split("-")[1])] += int(_order[3])
#                        except ValueError:
#                            print (_date, _order[3])

                        #    print ("ERROR", _date)                    
                        print (_order)
                    #print (list(M.keys()), list(M.values()))
                    #ax.bar(list(M.keys()), list(M.values()), label = f"{_customet[0]}") 
                    ax.plot(list(M.keys()), list(M.values()), label = f"{_customet[0]}") 
                    ax.legend()
                    #ax.semilogy(list(date_dict_price.keys()), list(date_dict_price.values()), label = f"{_customet[0]}")                    
                    print (len(order_list), _customet[0], "====================================")
                    
                except KeyError:
                    pass
         
        #plt.show()
        #plt.savefig("T.jpg")
        fig.savefig('T.png')


if __name__ == "__main__":

    S = Sort_v1()
#----------------->
    #S.func_unite("see") # Подготовка
    #S.save_data("data_arr_v1.txt") # Сохранение
    #S.open_dat("data_arr_v1.txt") # Открыть
#----------------->
    #S.diag_user() # Аналитика покупателя
#----------------->
    #S.diag_product_0()  # Количество покупок с одним товаром
#----------------->
    #S.diag_product_1()  # Отношение покупателей к покупкам  В РАБОТЕ!!!
#----------------->
    S.diag_product_2()
#
# последние совпадающиесе цифры кредитной карты!!!
# Вывести категории

# покупку разделить на категории
# В разрезе на месяц в разрезе за квартал
# продукты в продукты есть ли подкатегории
# Послать остатки скалада 

# Соптствующие товары !!!
# популярные продукты в отношении к категории !!!
