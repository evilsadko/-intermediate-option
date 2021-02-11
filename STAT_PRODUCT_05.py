import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import json
import test_graph as TG


if __name__ == "__main__":

    p_open = TG.PRODUCT() #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']
    #TG.see_stat(p_open)   

    product_dict = {}
    p_arr = p_open.to_numpy()
    vals_prod = np.unique(p_arr[:,1])
    for ix, i in enumerate(vals_prod):
        product_dict[i] = ix

#    o_open = TG.ORDER() #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged']  
#    #TG.see_stat(o_open)
#    c_open = TG.CUSTOMER() #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']
#    TG.see_stat(c_open)

    product_data = {}
    
    with open('data_arr.txt') as json_file:
        data = json.load(json_file)
        for o in data:
            for i in range(len(data[o])):
                try:
                    product_data[data[o][i]["P_ID"]] += 1
                except KeyError:
                    product_data[data[o][i]["P_ID"]] = 0
    max_list = []
    max_list1 = []
    myexplode = []
    IX = 0
    OTHER = 0
    Product_20 = 8215277
    for o in product_data:
        IX += product_data[o]
        P = product_data[o] / Product_20 * 100
        #max_list.append([o, product_data[o]])
        if P > 0.5:
            max_list.append(product_data[o])
            max_list1.append(P)
            myexplode.append(0) 
            #print (o, product_data[o], P)
        else:
            OTHER += P
    print (IX)
    max_list.append("ALL")
    max_list1.append(OTHER)
    myexplode.append(0.2)
    #max_list = np.array(max_list)
    
    


#    Product_ID = len(vals_prod)
#    Product_ID_20 = max_list.shape[0]
#    print (max_list.shape, Product_ID)
#    P = Product_ID_20 / Product_ID * 100

    vals = np.array(max_list1)
    labels = max_list
    #myexplode = [0, 0.2]
    fig, ax = plt.subplots()
    ax.pie(vals, explode=myexplode, labels=labels, autopct='%1.2f%%')
    ax.axis("equal")
    ax.legend(loc='upper left', bbox_to_anchor=(0.9, 0.9))
    plt.show()






#    Product_ID = len(vals_prod)
#    Product_ID_20 = max_list.shape[0]
#    print (max_list.shape, Product_ID)
#    P = Product_ID_20 / Product_ID * 100
#    labels = ["Others customers", "Сustomers per year"]

#    vals = np.array([100-P, P])
#    labels = ["Not purchased products", "Purchased products per year"]
#    myexplode = [0, 0.2]
#    fig, ax = plt.subplots()
#    ax.pie(vals, explode=myexplode, labels=labels, autopct='%1.2f%%')
#    ax.axis("equal")
#    ax.legend(loc='upper left', bbox_to_anchor=(0.9, 0.9))
#    plt.show()








#    p_open = TG.PRODUCT() #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']
#    #TG.see_stat(p_open)   

#    product_dict = {}
#    p_arr = p_open.to_numpy()
#    vals_prod = np.unique(p_arr[:,1])
#    for ix, i in enumerate(vals_prod):
#        product_dict[i] = ix

#    o_open = TG.ORDER() #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged']  
#    #TG.see_stat(o_open)
#    c_open = TG.CUSTOMER() #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']
##    TG.see_stat(c_open)

#    user_data = {}
#    product_data = {}
#    idx = 0
#    with open('data_arr.txt') as json_file:
#        data = json.load(json_file)
#        for o in data:
#            idx += len(data[o])
#            for i in range(len(data[o])):
#                #print (data[o][i]["P_ID"], product_dict[data[o][i]["P_ID"]])
#                #product_data[data[o][i]["P_ID"]] = 0
#                
#                try:
#                    user_data[data[o][0]["P_USER"]].append(product_dict[data[o][i]["P_ID"]])
#                except KeyError:
#                    user_data[data[o][0]["P_USER"]] = [product_dict[data[o][i]["P_ID"]]]
#    max_list = []
#    for i in user_data:
#        max_list.append([i, len(user_data[i]), user_data[i]])
#        #print (i, len(user_data[i]))
#    max_list = np.array(max_list)
#    a = np.argsort(max_list[:,1])
#    #sort(max_list[:,:]) #max_list[:,1]
#    
#    for i in a:
#        print (max_list[i,0],max_list[i,1])
#    print (max_list.shape)
#    #(len(max_list), max(max_list), min(max_list))
#    #59843 26430 10


##    vals_сust = np.unique(c_open.to_numpy()[:,0])
##    print (f"Поиск повторяющиеся: {len(vals_сust)}")
