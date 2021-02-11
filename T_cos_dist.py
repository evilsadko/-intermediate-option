import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import json
import test_graph as TG

#with open('data.txt', 'r') as js_file:
#    json.dump(dict_i ,js_file)
    
def similarity(vector1, vector2):
    #print (vector1, vector2)
    return np.dot(vector1, vector2.T) / np.dot(np.linalg.norm(vector1, axis=0, keepdims=True), np.linalg.norm(vector2.T, axis=0, keepdims=True))

def func_sort(ID):
    if len(max_list) != 0:
        for i in range(len(max_list)):
            if ID not in G.keys():
                    preds0 = max_list[i]#[0]
                    G[ID] = [[preds0, max_list[i][0]]]
                    del max_list[i]
            else:
                try:
                    preds1 = max_list[i]#[0]
                    KEF = similarity(preds0, preds1)
                    if KEF>tresh:
                         G[ID].append([preds1, max_list[i][0]])
                         del max_list[i]
                except IndexError: 
                    if len(max_list) == 0:
                         break
                    ID += 1
                    func_sort(ID)


if __name__ == "__main__":
    p_open = TG.PRODUCT() #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']
    #TG.see_stat(p_open)   

    product_dict = {}
    p_arr = p_open.to_numpy()
    vals_prod = np.unique(p_arr[:,1])
    for ix, i in enumerate(vals_prod):
        product_dict[i] = ix

    o_open = TG.ORDER() #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged']  
    #TG.see_stat(o_open)
    c_open = TG.CUSTOMER() #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']
#    TG.see_stat(c_open)

    user_data = {}
    product_data = {}
    idx = 0
    with open('data_arr.txt') as json_file:
        data = json.load(json_file)
        for o in data:
            idx += len(data[o])
            for i in range(len(data[o])):
                #print (data[o][i]["P_ID"], product_dict[data[o][i]["P_ID"]])
                #product_data[data[o][i]["P_ID"]] = 0
                
                try:
                    user_data[data[o][0]["P_USER"]].append(product_dict[data[o][i]["P_ID"]])
                except KeyError:
                    user_data[data[o][0]["P_USER"]] = [product_dict[data[o][i]["P_ID"]]]
    max_list = []
    for i in user_data:
        max_list.append(np.array([i, len(user_data[i])])) #np.array(user_data[i])
        #print (i, len(user_data[i]))
#    max_list = np.array(max_list)
#    a = np.argsort(max_list[:,1])
#    #sort(max_list[:,:]) #max_list[:,1]
#    
#    for i in a:
#        print (max_list[i,0],max_list[i,1])
#    print (max_list.shape)
    G = {}
    tresh = .96
    func_sort(0)
    print (len(list(G.keys())))
    for i in G:
        print (G[i])
    #(len(max_list), max(max_list), min(max_list))
    #59843 26430 10


#    vals_сust = np.unique(c_open.to_numpy()[:,0])
#    print (f"Поиск повторяющиеся: {len(vals_сust)}")
