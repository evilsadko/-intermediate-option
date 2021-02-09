import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import json
import test_graph as TG

#with open('data.txt', 'r') as js_file:
#    json.dump(dict_i ,js_file)
    

if __name__ == "__main__":
    p_open = TG.PRODUCT() #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']
    #TG.see_stat(p_open)   

    product_dict = {}
    p_arr = p_open.to_numpy()
    vals_prod = np.unique(p_arr[:,1])
    for ix, i in enumerate(vals_prod):
        product_dict[i] = ix

    #o_open = TG.ORDER() #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged']  
    
    #c_open = TG.CUSTOMER() #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']

    
    user_data = {}
    product_data = {}
    idx = 0
    with open('data_arr.txt') as json_file:
        data = json.load(json_file)
        for o in data:
            idx += len(data[o])
            for i in range(len(data[o])):
                print (data[o][i]["P_ID"], product_dict[data[o][i]["P_ID"]])
                product_data[data[o][i]["P_ID"]] = 0
                

            user_data[data[o][0]["P_USER"]] = 0
            #print (o, len(data[o]), data[o][0]["P_USER"])
        print (f"""Наименования продуктов которые покупались: {len(list(product_data.keys()))}\n 
                   Количество покупателей: {len(list(user_data.keys()))}\n
                   Количество покупок: {len(list(data.keys()))}\n
                   Количество продуктов: {idx}\n
                   Среднее количество продуктов в покупке: {idx/len(list(data.keys()))}\n 
                """)
