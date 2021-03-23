import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import json
import utils as TG
import time

def similarity(vector1, vector2):
    return np.dot(vector1, vector2.T) / np.dot(np.linalg.norm(vector1, axis=0, keepdims=True), np.linalg.norm(vector2.T, axis=0, keepdims=True))

#def func_sort(ID):
#    if len(max_list) != 0:
#        for i in range(len(max_list)):
#            if ID not in G.keys():
#                    preds0 = max_list[i][1][0]
#                    #print (preds0, len(preds0))
#                    G[ID] = [max_list[i][0]]
#                    del max_list[i]
#            else:
#                try:
#                    preds1 = max_list[i][1][0]
#                    KEF = similarity(preds0, preds1)
#                    if KEF>tresh:
#                         G[ID].append(max_list[i][0])
#                         del max_list[i]
#                except IndexError: 
#                    if len(max_list) == 0:
#                         break
#                    ID += 1
#                    func_sort(ID)

#def func_rec(ID):
#    print (len(arr_list), len(arr.file), len(G.keys()))
#    for ix, i in enumerate(arr_list):
#        G[ID] = [arr.file[ix]]
#        del arr.file[ix]
#        del arr_list[ix]
#        for iix, ii in enumerate(arr_list):
#                KEF = similarity(i, ii)  
#                if KEF[0]>tresh:
#                   G[ID].append(arr.file[iix])
#                   del arr.file[iix]
#                   del arr_list[iix] 
#        ID += 1



if __name__ == "__main__":
    p_open = TG.PRODUCT() #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']
    product_arr = p_open.to_numpy()

#---------------------------------------------->
    # Создаю словарь ID продуктов
    ids_product = {}
    vals_prod = np.unique(product_arr[:,1])
    for ix, i in enumerate(vals_prod):
        ids_product[i] = ix
    num_ids = len(ids_product)
    print (num_ids)
    ids_product_order = TG.func_return(product_arr, 0)

##---------------------------------------------->    

    o_open = TG.ORDER() #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged']  
    order_arr = o_open.to_numpy()
    ids_order = TG.func_return(order_arr, 1)

    c_open = TG.CUSTOMER() #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']
    customer_arr = c_open.to_numpy()
    ids_customer = TG.func_return(customer_arr, 0)


#---------------------------------------------->
    """
    У меня есть вектор (48603, 1) в него ложу среднее кол во продуктов исходя из покупок
    Нужно получить кол покупок для каждого пользователя
    """
    ERROR = 0
    user_data = {}
#    file_arr_temp = open("out/file_arr_temp_v1.txt", "w")
    for i in ids_customer:
        try:
            Z = np.zeros((num_ids))
            for p in ids_order[int(i)]:
                o_id = order_arr[p][0]
                print (i, len(ids_product_order[o_id]), len(ids_order[int(i)]))
                for g in ids_product_order[o_id]:
                    Z[ids_product[product_arr[g][1]]] += 1
                    print (product_arr[g].tolist())
                print (product_arr[ids_product_order[o_id]].tolist())
                print(order_arr[p].tolist())
                print (sum(Z))
                print ("..................................")
            #if sum(customer_arr[ids_customer[i], 1:-1][0]) == 3.0:
                #print (customer_arr[ids_customer[i], 1:-1])
                #user_data[i] = Z
#                file_arr_temp.write(f"{i};{Z.tolist()}\n")
        except KeyError:
            ERROR += 1
            pass
    print (ERROR)
    print (len(user_data))
#    file_arr_temp.close()


#    file_arr_temp = open("out/file_arr_temp_v1.txt", "r")  
#    for i in file_arr_temp:
#        res = json.loads(i.split("\n")[0].split(";")[1])
#        print (len(res), sum(res))  
    
    
#    
#    with open('data_arr.txt') as json_file:
#        data = json.load(json_file)
#        start = time.time()
#        print (len(list(data.keys()))) #82705
#        for o in list(data.keys())[:100]:
#            IDX = np.where(o_arr[:,1] == data[o][0]["P_USER"])
#            tem_di = {}
#            # 35376 + 5  = 35381
#            Z = np.zeros((len(vals_prod)+5))
#            for i in data[o]:
#                id_arr_Z = product_dict[i['P_ID']]
#                Z[id_arr_Z] += 1
#            Z[35380] = data[o][0]['CSE']
#            Z[35379] = data[o][0]['CSS']
#            Z[35378] = data[o][0]['JCS']
#            Z[35377] = len(data[o]) # колво продуктов
#            Z[35376] = len(IDX[0]) # колво покупок
#            #print (data[o][0]["P_USER"], ">>>", Z[35376], Z[35377], Z[35378], Z[35379], Z[35380], Z.shape) 
#            #print (".....................................")
#            try:
#                    user_data[data[o][0]["P_USER"]].append(Z)
#            except KeyError:
#                    user_data[data[o][0]["P_USER"]] = [Z]
#        print (time.time()-start)  #21.18878984451294   19.416529893875122         

#    max_list = []
#    for k in user_data:
#        max_list.append(np.array([k, user_data[k]])) 
#    #print (max_list[0].shape)
#    G = {}
#    tresh = .96 # .32 - 1287
#    start = time.time()
#    func_sort(0)
#    print (len(list(G.keys()))) 
#    print (time.time()-start) #77.00579833984375
#    file_resave = open("resave.txt", "w")
#    for i in G:
#        st = ','.join(map(str,G[i]))
#        file_resave.write(f"{i},{st}\n")
#        #print (f"{i},{st}\n")
#    file_resave.close()
##        print (i, len(G[i]))
