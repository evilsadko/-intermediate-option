import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import json, os

"""
В этом файле присваиваю каждому продукту из файла B24_dbo_Crm_product_in_order.csv
дату продажи из файла B24_dbo_Crm_orders.csv
Это дает нам возможность выстраивать коллво проданных товаров по месяцам
ВАЖНО !!! Строит график только по тем месяцам в клоторых есть продажи
"""

def see_stat(x, y=0):
    if y == "list":
        print (x.columns.tolist())
    else:
        for c in  x.columns.tolist():
            print (f"###############\n{x[c].value_counts(dropna=False)}")

def PRODUCT():
    p_open = pd.read_csv('B24_dbo_Crm_product_in_order.csv', delimiter=',')
    see_stat(p_open)
    p_open = p_open[['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']] 
    return p_open

def ORDER():
    o_open = pd.read_csv('B24_dbo_Crm_orders.csv', delimiter=',')
    o_open = o_open[['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date']]
    o_open['Items_Count'] = o_open['Items_Count'].replace(np.nan, 0)
    return o_open


if __name__ == "__main__":
    #"""
    o_open = ORDER()  #['Order_Id', 'Customer_Id', ', 'price_before_discount', 'Amount_Charged', 'Order_Date']
    o_open = o_open.sort_values(by=['Order_Date']) #, inplace=True, ascending=False
    o_open = o_open.to_numpy()
#    cats = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun', 'Jul', 'Aug','Sep', 'Oct', 'Nov', 'Dec']
    
    p_open = PRODUCT() #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']
    p_open = p_open.to_numpy()
#----------------------------->
    #Граф ORDER ID - DATE
    dicts = {}
    print (o_open.shape[0], p_open.shape[0])
    for i in range(o_open.shape[0]):
            t = o_open[i,:].tolist()
            o_id = int(t[0]) 
            cust_id = int(t[1])
            items_count = int(t[2])
            date = t[-1]
            dicts[o_id] = date.split(" ")[0].split("-")[1] # Переношу месяц

#['Order_Id', 'Customer_Id', ', 'price_before_discount', 'Amount_Charged', 'Order_Date']
#----------------------------->
    #Граф PRODUCT ID - {ORDER ID, DATE, COUNT}
    product_data = {}
    for i in range(p_open.shape[0]):
        o_id = int(p_open[i,0]) # ID order из продукта
        p_id = int(p_open[i,1]) # ID продукта из ордера
        i_count = int(p_open[i,2])
        try:
            product_data[p_id].append({"o_id":o_id, "o_date":dicts[o_id], "i_count":i_count})
        except KeyError:
            product_data[p_id] = [{"o_id":o_id, "o_date":dicts[o_id], "i_count":i_count}]
        #print (o_id, p_id, i_count, dicts[o_id])

######## SAVE TO FILE
    with open('prod.json', 'w') as js_file:
            json.dump(product_data, js_file)

######## CREATE VISUAL 
    for i in product_data:
        print ("VISUAL")
        temp = {}
        for k in product_data[i]:
            #print (k)
            try:
                temp[k["o_date"]] += k["i_count"]
            except KeyError:
                temp[k["o_date"]] = k["i_count"]

        plt.plot(list(temp.keys()), list(temp.values()))  
        plt.savefig(f"graph/{i}.jpg") 
        plt.cla()

