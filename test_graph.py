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
    o_open = o_open[['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged']]
    return o_open

def chunks(lst, count):
    start = 0
    for i in range(count):
          stop = start + len(lst[i::count, :])
          yield lst[start:stop, :]
          start = stop     

def T(p_arr, ord_id, o_id, arr_id_c, cus_id, p_id, i_count, arr_jcs, arr_css, arr_cse, dict_i):
    for i in range(p_arr.shape[0]):
              IDX = np.where(ord_id == o_id[i])
              IDX2 = np.where(arr_id_c == cus_id[IDX])
              if IDX2[0].shape[0] != 0:

                  try:
                     dict_i[o_id[i]].append({"P_ID":p_id[i], "P_COUNT":i_count[i], "P_USER": cus_id[IDX][0], "JCS":arr_jcs[IDX2][0], "CSS":arr_css[IDX2][0], "CSE":arr_cse[IDX2][0]}) 
                  except KeyError:
                     dict_i[o_id[i]] = [{"P_ID":p_id[i], "P_COUNT":i_count[i], "P_USER": cus_id[IDX][0], "JCS":arr_jcs[IDX2][0], "CSS":arr_css[IDX2][0], "CSE":arr_cse[IDX2][0]}]

if __name__ == "__main__":
#   ['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount'] 
    p_open = PRODUCT()
    #see_stat(p_open)
    #p_open = p_open[p_open[['Order_ID']].duplicated() == True]
    p_arr = p_open.to_numpy()
    #vals_prod, inverse_prod = np.unique(p_arr[:,1], return_index=True)
#    idx_class = range(0, len(vals_prod))
#    class_arr = np.zeros((len(vals_prod), 1))

    #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged']  
    o_open = ORDER()
    o_arr = o_open.to_numpy()


    #print (len(vals_prod), class_arr.shape) 
    dict_arr_0 = {}
    dict_arr_1 = {}
    for ix, i in enumerate(p_arr[:, :]):
        ixx = np.where(o_arr[:,0] == i[0])
        #print (i[1], o_arr[ixx[0],1][0])
#        ixx = np.where(o_arr == i[0])
#        print (i[1], ixx[0][0], ixx[1][0], o_arr[ixx[0][0],1])
        try:
           dict_arr_0[i[1]].append(o_arr[ixx[0],1][0])
           dict_arr_1[o_arr[ixx[0],1][0]].append(i[1])
        except KeyError:
           dict_arr_0[i[1]] = [o_arr[ixx[0],1][0]]
           dict_arr_1[o_arr[ixx[0],1][0]] = [i[1]]
    
    file0 = open("grap_0.txt", "w")
    for i in dict_arr_0:
        st = ','.join(map(str, dict_arr_0[i])) 
        file0.write(f"{i},{st}\n")
    file0.close()


    file1 = open("grap_1.txt", "w")
    for i in dict_arr_1:
        st = ','.join(map(str, dict_arr_1[i])) 
        file1.write(f"{i},{st}\n")
    file1.close()

    #print (dict_arr_1.keys(), len(list(dict_arr_0.keys())))
        #print (len(ixx), ixx[0].shape, ixx[1].shape)
        #print (ix, list(ixx[0]), list(ixx[1]))
    


