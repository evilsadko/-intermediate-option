import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import json
import utils as TG
import time

#file_arr_temp = open("out/file_arr_temp_v3.txt", "r")  
file_arr_temp = open("out/1_create_file_arr.txt", "r").readlines()[:10000]
tresh = .68
G = {}

def test():
    # TEST
    
    p_open = TG.PRODUCT() #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']
    product_arr = p_open.to_numpy()
    ids_product_order = TG.func_return(product_arr, 0)
##---------------------------------------------->
    # Создаю словарь ID продуктов
    ids_product = {}
    vals_prod = np.unique(product_arr[:,1])
    for ix, i in enumerate(vals_prod):
        ids_product[i] = ix
    num_ids = len(ids_product)

##---------------------------------------------->    

    o_open = TG.ORDER() #['Order_Id', 'Branch_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date']  
    order_arr = o_open.to_numpy()
    ids_order = TG.func_return(order_arr, 2)
#    for i in ids_order:
#        print (i, type(i))
    
    c_open = TG.CUSTOMER() #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']
    customer_arr = c_open.to_numpy()
    ids_customer = TG.func_return(customer_arr, 0)
    print (num_ids, len(ids_customer))

    F = json.load(open(f"out/test_claster_10000_v2.json", 'r'))
    id_list = []
    val_list = []
    for i in F:
        id_list.append(i)
        val_list.append(len(F[i]))
#        print (i, len(F[i]))
#    print (max(val_list), val_list.index(max(val_list)), F[str(val_list.index(max(val_list)))])  
#    print (min(val_list), val_list.index(min(val_list)), F[str(val_list.index(min(val_list)))])  
    #-------------------------------------------
#    for h in F:
#        Sum = 0
#        Con = 0
#        SA = 0
#        for i in F[h]:
#            #print (i, ids_order[int(float(i))])
#            for o  in ids_order[int(float(i))]:
#                OR = order_arr[o,:].tolist()
#                Sum += OR[4]
#                Con += OR[3]
#                SA += 1
#        print (Sum, Con, Sum/Con, SA, Sum/SA, Con/SA, "USER IN GROUP:", len(F[h]))    
    
#    Sum = 0
#    Con = 0
#    for i in F[str(val_list.index(max(val_list)))]:
#        #print (i, ids_order[int(float(i))])
#        for o  in ids_order[int(float(i))]:
#            OR = order_arr[o,:].tolist()
#            Sum += OR[4]
#            Con += OR[3]
#    print (Sum, Con, len(F[str(val_list.index(max(val_list)))]))
#
#----------------------------------------->
# Найти доминирующий товар
# 
#    for h in F:
#        all_ = 0
#        Sz = {}
#        for i in F[h]:

#            for o  in ids_order[int(float(i))]:
#                OR = order_arr[o,:].tolist()
#                #print (ids_product_order[OR[0]])
#                for i in ids_product_order[OR[0]]:
#                    all_ += 1
#                    try:
#                        Sz[i] += 1
#                    except KeyError:
#                        Sz[i] = 1
#        print (Sz, all_)


def get_batch():
    L = []
    for i in file_arr_temp:
            res = json.loads(i.split("\n")[0])
            Z = np.zeros((12, num_ids))
            L1 = list(res.values())[0][0]
            L2 = list(res.values())[0][1]
            for i in range(len(L1)):
                 Z[L1[i],L2[i]] += 1  
            L.append(Z)
            if len(L) == 32:
                yield np.array(L)
                L = []       

#    for i in range(100000):
#        for o in get_batch():
#            print (o.shape)   

def plot_user():
    start = time.time()
    file_arr_temp = open("out/file_arr_temp_v3.txt", "r") 
    ix = 0 
    for i in file_arr_temp:
        res = json.loads(i.split("\n")[0])
        Z = np.zeros((12, 48603))
        L1 = list(res.values())[0][0]
        L2 = list(res.values())[0][1]
        for i in range(len(L1)):
             Z[L1[i],L2[i]] += 1    
        ix += 1 
        
        fig, ax = plt.subplots(figsize=(10,10), clear=True)
        A = []
        B = []
        for o in range(Z.shape[0]):
            A.append(o)
            B.append(sum(Z[o,:]))
        plt.plot(A, B, label = f"{o}")    
        fig.savefig(f"temp/{i}.jpg")  # cat/cat2
        fig.clear(True)
        plt.close(fig) 
        
    print (time.time()-start, ix) 

def imgs_v(x):
      cv2.imshow('Rotat', np.array(x))
      cv2.waitKey(0)
      cv2.destroyAllWindows()


def similarity(vector1, vector2):
        return np.dot(vector1, vector2.T) / np.dot(np.linalg.norm(vector1, axis=1, keepdims=True), np.linalg.norm(vector2.T, axis=0, keepdims=True))

#def crt(i):
#        res = json.loads(i.split("\n")[0])
#        Z = np.zeros((12, 48603))
#        L1 = list(res.values())[0][0]
#        L2 = list(res.values())[0][1]
#        for i in range(len(L1)):
#             Z[L1[i],L2[i]] += 1  
#               
#        Y = []
#        for o in range(Z.shape[0]):
#            if sum(Z[o,:]) > 0:
#                Y.append(1) 
#            if sum(Z[o,:]) == 0:
#                Y.append(0)      
#        return np.reshape(np.array(Y), (1,12)), list(res.keys())[0]
def crt(i):
        res = json.loads(i.split("\n")[0])
        Z = np.zeros((12, 48603))
        L1 = list(res.values())[0][0]
        L2 = list(res.values())[0][1]
        L3 = list(res.values())[0][2]
        for i in range(len(L1)):
#             Z[L1[i],L2[i]] += 1  
               Z[L1[i],L2[i]] += L3[i]  
        Y = []
        for o in range(Z.shape[0]):
            Y.append(sum(Z[o,:])) 
        return np.reshape(np.array(Y), (1,12)), list(res.keys())[0]



def func_rec(ID):
    print (len(file_arr_temp))
    for ix, i in enumerate(file_arr_temp):
        Z0 = crt(i)
        G[ID] = [Z0[1]]
        del file_arr_temp[ix]
        for ix2, ii in enumerate(file_arr_temp):
            Z1 = crt(ii)
            KEF = similarity(Z0[0], Z1[0])
            if KEF[0]>tresh:
                G[ID].append(Z1[1])
                del file_arr_temp[ix2]
        ID += 1

def start_similarity():

    start = time.time()
    file_arr_temp = open("out/1_create_file_arr.txt", "r").readlines()[:10000]
    print (time.time()-start) 
    func_rec(0)  
    print (G, len(file_arr_temp)) 
    with open(f"out/test_claster_10000_v2.json", 'w') as js_file:
        json.dump(G, js_file)  
        
 
def load_():
#     file_arr_temp = open("out/file_arr_temp_v3.txt", "r").readlines()
     file_arr_temp = open("out/_create_file_arr.txt", "r").readlines()
     print (len(file_arr_temp))
     for i in file_arr_temp:
        res = json.loads(i.split("\n")[0])
        for p in res:
            #print (res[p][0], res[p][1])
            D = {}
            for g in res[p][1]:
                try:
                    D[g] += 1
                except KeyError:
                    D[g] = 1
            print (D)


if __name__ == "__main__":
    #----------------------------------------->
    #load_() 
    #start_similarity()
    #----------------------------------------->

                        
