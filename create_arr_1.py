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
    for i in range(arr_o.shape[0]):
        try:
            arr_p[arr_o[i,0]]
            not_errot += 1
            gen_ls = [get_i(p) for p in arr_p[arr_o[i,0]]]
            #print (gen_ls)
            #print ("Product in order", len(arr_p[arr_o[i,0]]))
            ID_customer = arr_c[arr_o[i,1]][0]
            ID_customer = c_open[ID_customer,:].tolist()
            #print ("Customer ID", ID_customer)
            sort_dict[ID_customer[0]] = [gen_ls, ID_customer]
            #print ("----------------------->")
        except KeyError:
            key_error += 1
    print (len(sort_dict),key_error, not_errot)
    #9678606 1760573


#    with open('data_arr.txt', 'w') as js_file:
#        json.dump(dict_i ,js_file)
    

    


