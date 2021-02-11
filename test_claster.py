import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import json
import test_graph as TG
import time

#with open('data.txt', 'r') as js_file:
#    json.dump(dict_i ,js_file)
    
def similarity(vector1, vector2):
    #print (vector1, vector2)
    return np.dot(vector1, vector2.T) / np.dot(np.linalg.norm(vector1, axis=0, keepdims=True), np.linalg.norm(vector2.T, axis=0, keepdims=True))

def func_sort(ID):
    if len(max_list) != 0:
        for i in range(len(max_list)):
            if ID not in G.keys():
                    preds0 = max_list[i][1][0]
                    #print (preds0, len(preds0))
                    G[ID] = [max_list[i][0]]
                    del max_list[i]
            else:
                try:
                    preds1 = max_list[i][1][0]
                    KEF = similarity(preds0, preds1)
                    if KEF>tresh:
                         G[ID].append(max_list[i][0])
                         del max_list[i]
                except IndexError: 
                    if len(max_list) == 0:
                         break
                    ID += 1
                    func_sort(ID)


if __name__ == "__main__":
    p_open = TG.PRODUCT() #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']
    #TG.see_stat(p_open)   

#---------------------------------------------->
    # Создаю словарь ID продуктов
    product_dict = {}
    p_arr = p_open.to_numpy()
    vals_prod = np.unique(p_arr[:,1])
    for ix, i in enumerate(vals_prod):
        product_dict[i] = ix
#---------------------------------------------->    

    o_open = TG.ORDER() #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged']  
    #TG.see_stat(o_open)
    o_arr = o_open.to_numpy()


    #c_open = TG.CUSTOMER() #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']
#    TG.see_stat(c_open)
#---------------------------------------------->
    """
    У меня есть вектор (35376, 1) в него ложу среднее кол во продуктов исходя из покупок
    Нужно получить кол покупок для каждого пользователя
    """
    user_data = {}
    
    with open('data_arr.txt') as json_file:
        data = json.load(json_file)
        start = time.time()
        print (len(list(data.keys()))) #82705
        for o in list(data.keys())[:4000]:
            IDX = np.where(o_arr[:,1] == data[o][0]["P_USER"])
            tem_di = {}
            # 35376 + 5  = 35381
            Z = np.zeros((len(vals_prod)+5))
            for i in data[o]:
                id_arr_Z = product_dict[i['P_ID']]
                Z[id_arr_Z] += 1
            Z[35380] = data[o][0]['CSE']
            Z[35379] = data[o][0]['CSS']
            Z[35378] = data[o][0]['JCS']
            Z[35377] = len(data[o]) # колво продуктов
            Z[35376] = len(IDX[0]) # колво покупок
            #print (data[o][0]["P_USER"], ">>>", Z[35376], Z[35377], Z[35378], Z[35379], Z[35380], Z.shape) 
            #print (".....................................")
            try:
                    user_data[data[o][0]["P_USER"]].append(Z)
            except KeyError:
                    user_data[data[o][0]["P_USER"]] = [Z]
        print (time.time()-start)  #21.18878984451294   19.416529893875122         

    max_list = []
    for k in user_data:
        max_list.append(np.array([k, user_data[k]])) 
    #print (max_list[0].shape)
    G = {}
    tresh = .96 # .32 - 1287
    start = time.time()
    func_sort(0)
    print (len(list(G.keys()))) 
    print (time.time()-start) #77.00579833984375
    file_resave = open("resave.txt", "w")
    for i in G:
        st = ','.join(map(str,G[i]))
        file_resave.write(f"{i},{st}\n")
        #print (f"{i},{st}\n")
    file_resave.close()
#        print (i, len(G[i]))
