import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import json
import time
import create_arr as TG


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
    p_open = TG.PRODUCT()
    p_arr = p_open.to_numpy()
    #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged']  
    o_open = TG.ORDER()
    o_arr = o_open.to_numpy()


    #print (len(vals_prod), class_arr.shape) 
    dict_arr_0 = {}
    dict_arr_1 = {}
    for ix, i in enumerate(p_arr[:, :]):
        ixx = np.where(o_arr[:,0] == i[0])
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

    


