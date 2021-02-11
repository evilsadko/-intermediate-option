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
    
    c_open = CUSTOMER() #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']
    arr_c = c_open.to_numpy() # Преобразовываю в масив
    arr_id_c, arr_jcs, arr_css, arr_cse = arr_c[:,0], arr_c[:,2], arr_c[:,3], arr_c[:,4]
    o_open = ORDER() #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged'] 
    arr_o = o_open.to_numpy()
    ord_id, cus_id, i_count = arr_o[:,0], arr_o[:,1], arr_o[:,2]
    p_open = PRODUCT() #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']
    p_open = p_open[p_open[['Order_ID']].duplicated() == True]
    p_arr = p_open.to_numpy()
    o_id, p_id, i_count = p_arr[:,0], p_arr[:,1], p_arr[:,2]
    dict_i = {}


    ty = chunks(p_arr[:,:],10)
    threads = []
    for f_list in ty:
       my_thread = threading.Thread(target=T, args=(f_list, ord_id, o_id, arr_id_c, cus_id, p_id, i_count, arr_jcs, arr_css, arr_cse, dict_i))
       threads.append(my_thread)
       my_thread.start()
    flag = 1
    while (flag):
        for t in threads:
            if t.isAlive():
                flag = 1
            else:
                flag = 0


    time.sleep(20)

    with open('data_arr.txt', 'w') as js_file:
        json.dump(dict_i ,js_file)
    

    


