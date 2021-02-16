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
    return o_open

def func_return(x, y):
    dict = {} 
    for i in range(x.shape[0]):
        try:
            dict[x[i,y]].append(i)
        except KeyError:
            dict[x[i,y]] = [i]
    return dict    

def get_i(x):
    #x = p_open[x,:].tolist()
    #dict = {"Order_ID":x[0], "Product_ID":x[1], "Items_Count":x[2]}
    return p_open[x,:].tolist()

def repack_func(x):
    list = []
    #{"P_ID":p_id[i], "P_COUNT":i_count[i], "P_USER": cus_id[IDX][0], "JCS":arr_jcs[IDX2][0], "CSS":arr_css[IDX2][0], "CSE":arr_cse[IDX2][0]}
    for i in x:
        list.append({"P_ID":i[1], "P_COUNT":i[2], "Total_Amount":i[3],"TotalDiscount":i[4]})
    return list

if __name__ == "__main__":
    c_open = CUSTOMER().to_numpy() #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']    
    arr_c = func_return(c_open, 0)

    o_open = ORDER().to_numpy() #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date'] 
    arr_o = o_open#func_return(o_open, 0)

    p_open = PRODUCT().to_numpy() #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']
    arr_p = func_return(p_open, 0)

    print (len(arr_o), o_open.shape, len(arr_p), p_open.shape)
    #10574427 (10574427, 5) 1760573 (12971900, 5)
    sort_dict = {}
    
    key_error = 0
    not_errot = 0
    # Прохожу циклом по покупкам ордер
    for i in range(arr_o.shape[0]):
        try:
            # Из получаю продукты исходя из покупки ордер
            gen_ls = [get_i(p) for p in arr_p[arr_o[i,0]]] #arr_p[arr_o[i,0]]

            # Получаю  индекс покупателя в массиве
            ID_customer = arr_c[arr_o[i,1]][0]

            # По индексу получаю информацию о покупателе
            ID_customer = c_open[ID_customer,:].tolist()

#            print ("Product in order", len(gen_ls))
#            print ("Customer ID", ID_customer, int(ID_customer[0]), arr_o[i,1])
 
            # Создаю словарь где ключ ID покупателя

#            if ID_customer[0] in sort_dict:
#                sort_dict[ID_customer[0]].append([gen_ls, ID_customer])
#                print ("Совпадение", ID_customer[0], ID_customer)
#            else:
#                sort_dict[ID_customer[0]] = [[gen_ls, ID_customer]]

            # Создаю словарь где ключ ID покупки ордера

#            sort_dict[arr_o[i,0]] = [[gen_ls, ID_customer]] # Новая
            l = repack_func(gen_ls) # Оригенал
            l.append({"DATE_ORDER":arr_o[i,-1], "Items_Count":arr_o[i,2], "price_before_discount":arr_o[i,3], "Amount_Charged": arr_o[i,4],
                      "USER": ID_customer[0], "JCS":ID_customer[2], "CSS":ID_customer[3], "CSE":ID_customer[4],})
            sort_dict[arr_o[i,0]] = l

            #{"P_ID":p_id[i], "P_COUNT":i_count[i], "P_USER": cus_id[IDX][0], "JCS":arr_jcs[IDX2][0], "CSS":arr_css[IDX2][0], "CSE":arr_cse[IDX2][0]}
            not_errot += 1
            #print ("----------------------->")
        except KeyError:
            key_error += 1
#    print (len(sort_dict),key_error, not_errot)
#    for i in sort_dict:
#        print (sort_dict[i])
#    print (len(sort_dict), key_error, not_errot)


    #9678606 1760573
    #229399 9678606 895821
    #229399 9678606 895821 sort_dict[ID_customer[0]] = [[gen_ls, ID_customer]]


    #dict_i[o_id[i]].append({"P_ID":p_id[i], "P_COUNT":i_count[i], "P_USER": cus_id[IDX][0], "JCS":arr_jcs[IDX2][0], "CSS":arr_css[IDX2][0], "CSE":arr_cse[IDX2][0]}) 
#    repack = {}
#    for i in sort_dict:
#        try:
#            repack [o_id[i]].append
#        except KeyError:
#                  
    
    with open('data_arr_v1.txt', 'w') as js_file:
        json.dump(sort_dict ,js_file)
    
    with open('data_arr_v1.txt') as json_file:
        data = json.load(json_file)
        for ix, o in enumerate(list(data.keys())[:]):
            print (data[o], ix)
    


