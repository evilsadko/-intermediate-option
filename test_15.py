import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import json

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

if __name__ == "__main__":
    


#---------------------------------->
#   ['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']
#    CUSTOMER

    c_open = CUSTOMER()
#    #see_stat(c_open, "list")

    arr_c = c_open.to_numpy() # Преобразовываю в масив
    arr_id_c, arr_jcs, arr_css, arr_cse = arr_c[:,0], arr_c[:,2], arr_c[:,3], arr_c[:,4]
#    vals0, inverse0, count0 = np.unique(arr_c[:,0], return_inverse=True, return_counts=True) # Получаю повторяющиеся элементы
#    print ("CUSTOMER ORIG:", len(c_open), len(vals0))


#---------------------------------->
#   ['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged']  
#    ORDER

    o_open = ORDER()
    #see_stat(o_open, "list")

    arr_o = o_open.to_numpy()
    ord_id, cus_id, i_count = arr_o[:,0], arr_o[:,1], arr_o[:,2]
#    vals1, inverse1, count1 = np.unique(arr_o[:,1], return_index=True, return_counts=True)
#    print ("ORDER CLASS: ", len(count1), len(o_open), len(ord_id))

#---------------------------------->
#   ['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount'] 
#    PRODUCT
# Сколько раз покупали продукт
    p_open = PRODUCT()
    #see_stat(p_open)
    p_open = p_open[p_open[['Order_ID']].duplicated() == True]
    p_arr = p_open.to_numpy()
    #vals, inverse, count = np.unique(p_arr[:,1], return_inverse=True, return_counts=True)
    #print ("PRODUCT CLASS: ",len(vals), "MAX:", max(count), "MIN:", min(count)) #p_open[p_open[['Order_ID']].duplicated() == True], 
    print ("SHAPE:", p_arr.shape[0])
    o_id, p_id, i_count = p_arr[:,0], p_arr[:,1], p_arr[:,2]
#    

#    print (o_id[:3], p_id[:3], i_count[:3])
    dict_i = {}
#    #p_arr.shape[0]
#    
    #ord_id = list(ord_id) !!!<< IDX
    IDDD = 0
#p_arr.shape[0]
    for ix, i in enumerate(p_arr[:100,:]):
               #print (ix, i[0])
               #print ("PRODUCT->>>", o_id[ix], p_id[ix], i_count[ix], i[0])

               IDX = np.where(ord_id == o_id[ix]) # Получаю ID ордера из бд ордера по ID продукта
               #print (list(ord_id).index(int(i[0])))
               #print ("ORDER->>>", IDX[0], ord_id[IDX[0]][0], cus_id[IDX][0], i_count[IDX][0])
#              
               IDX2 = np.where(arr_id_c == cus_id[IDX]) # Получаю ID покупателя из бд покупатя по ID пользователя
#              IDDD += 1
               if IDX2[0].shape[0] != 0:
                  try:
                     dict_i[o_id[ix]].append({"P_ID":p_id[ix], "P_COUNT":i_count[ix], "P_USER": cus_id[IDX][0], "JCS":arr_jcs[IDX2][0], "CSS":arr_css[IDX2][0], "CSE":arr_cse[IDX2][0]}) 
                  except KeyError:
                     #print ({"P_ID":p_id[ix], "P_COUNT":i_count[ix], "P_USER": cus_id[IDX][0], "JCS":arr_jcs[IDX2][0], "CSS":arr_css[IDX2][0], "CSE":arr_cse[IDX2][0]})
                     dict_i[o_id[ix]] = [{"P_ID":p_id[ix], "P_COUNT":i_count[ix], "P_USER": cus_id[IDX][0], "JCS":arr_jcs[IDX2][0], "CSS":arr_css[IDX2][0], "CSE":arr_cse[IDX2][0]}]
    with open('data_arr.txt', 'w') as js_file:
        json.dump(dict_i ,js_file)
    
#import numpy as np

#A = np.array([[2,4],
#          [6,2]])
#index= np.nonzero(A>1)
#       OR
#(A>1).nonzero()
    


