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
#    c_open = c_open[['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']]
    c_open['join_club_success'] = c_open['join_club_success'].replace(np.nan, 2)
    c_open['Could_send_sms'] = c_open['Could_send_sms'].replace(np.nan, 0)
    c_open['Could_send_email'] = c_open['Could_send_email'].replace(np.nan, 0)
    c_open['consent'] = c_open['consent'].replace(np.nan, 0)
    c_open['Clubid'] = c_open['Clubid'].replace(np.nan, 100500)
#    c_open = c_open.apply(lambda x: pd.to_numeric(x, errors='coerce')).dropna() # Убираю все строки
    #see_stat(c_open)
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

def NAME():
    c_open = pd.read_csv('names - names.csv', delimiter=',')
    c_open = c_open[['1', '243995', 'היי', 'Unnamed: 3', '0 - женщины\n1 - мужчины']]
    c_open['Unnamed: 3'] = c_open['Unnamed: 3'].replace(np.nan, 2)
    return c_open

def func_return(x, y):
        dict = {} 
        for i in range(x.shape[0]):
            try:
                dict[x[i,y]].append(i)
            except KeyError:
                dict[x[i,y]] = [i]
        return dict    
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
        self.customer_dict = func_return(self.customer_arr, 0)
        self.order_dict = func_return(self.order_arr, 0)
        self.product_dict = func_return(self.product_arr, 0)

        self.sort_dict = {}


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

def user_per_m():
##----------------------->
    C = CUSTOMER() #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']   
    col = C.columns.tolist()
    arr_c = C.to_numpy()
    dict_cust_group = func_return(arr_c, 6)
    dict_cust_id = func_return(arr_c, 1)
##------------------------>
    O = ORDER() #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date'] 
    order_arr = O.to_numpy()
    dict_order_id_cust = func_return(order_arr, 1)
    
    for i in dict_order_id_cust:
        try:
            M = {'01':0, '02':0, '03':0, '04':0, '05':0, '06':0, '07':0, '08':0, '09':0, '10':0, '11':0, '12':0}
            for o in dict_order_id_cust[i]:
                data = order_arr[o,:].tolist()
                short_data = data[-1].split(" ")[0].split("-")[1]
                M[short_data] += data[3]
                #print (i, data, short_data)
                #print (i, data, arr_c[dict_cust_id[i],:].tolist())
             
            fig, ax = plt.subplots(figsize=(10,10), clear=True)
            ax.set_title(f'ID покупателя - {i}')
            ax.set_xlabel('Месяц')
            ax.set_ylabel('Потраченная сумма')
            ax.bar(list(M.keys()), list(M.values()), color = (0,0.2,1,0.6))

            ax.plot(list(M.keys()), list(M.values()))  
            fig.savefig(f"github/user_m/{i}.jpg") 
            fig.clear(True)
            plt.close(fig)  
              
        except KeyError:
            pass     

def sex_user_m():
    N = NAME()
    L = N.to_numpy()
    # Создаю граф пол
    dict_sex = {}
    for i in range(L.shape[0]):
        dict_sex[L[i,2]] = L[i,-2]
##----------------------->
    C = CUSTOMER() #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']   
    col = C.columns.tolist()
    print (col)
    arr_c = C.to_numpy()
#    dict_cust_group = func_return(arr_c, 6)
    dict_cust_id = func_return(arr_c, 1)

    O = ORDER() #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date'] 
    order_arr = O.to_numpy()
    dict_order_id_cust = func_return(order_arr, 1)
#   
    M0 = {'01':0, '02':0, '03':0, '04':0, '05':0, '06':0, '07':0, '08':0, '09':0, '10':0, '11':0, '12':0}
    M1 = {'01':0, '02':0, '03':0, '04':0, '05':0, '06':0, '07':0, '08':0, '09':0, '10':0, '11':0, '12':0}
    M2 = {'01':0, '02':0, '03':0, '04':0, '05':0, '06':0, '07':0, '08':0, '09':0, '10':0, '11':0, '12':0} 
    for i in dict_order_id_cust:
        try:

            for o in dict_order_id_cust[i]:
                 data = order_arr[o,:].tolist()
                 short_data = data[-1].split(" ")[0].split("-")[1]
                 #print (dict_cust_id[o])
                 #
                 id_ =  arr_c[dict_cust_id[o][0],10]
                 sex = dict_sex[id_]
                 if sex == 0.0:
                     M0[short_data] += data[3]
                 if sex == 1.0:
                     M1[short_data] += data[3]
                 if sex == 2.0:
                     M2[short_data] += data[3]
                 print (sex, short_data)
                 
        except KeyError:
                pass
                
    fig, ax = plt.subplots(figsize=(10,10), clear=True)
    ax.set_title(f'ID покупателя - {i}')
    ax.set_xlabel('Месяц')
    ax.set_ylabel('Потраченная сумма')
    ax.bar(list(M0.keys()), list(M0.values()), color = (0,0.5,1,0.6))
    ax.bar(list(M1.keys()), list(M1.values()), color = (0,0.4,1,0.6))
    ax.bar(list(M2.keys()), list(M2.values()), color = (0,0.3,1,0.6))
    #ax.plot(list(M.keys()), list(M.values()))  
    fig.savefig(f"github/user/sex.jpg") 
    fig.clear(True)
    plt.close(fig)       

if __name__ == "__main__":
    #S = Sort_v1()
    #S.diag_user() # Аналитика покупателя

    #user_per_m()
    sex_user_m()
    
    # 17 клубов если убираю NaN
    # 61984  если не убираю NaN  
    # 100500 - NaN
    # Пользователи за год с учетом пола
           
