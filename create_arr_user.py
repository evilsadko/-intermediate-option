import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import json
import utils as TG
import time

file_arr_temp = open("out/file_arr_temp_v3.txt", "r")  
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



def imgs_v(x):
      cv2.imshow('Rotat', np.array(x))
      cv2.waitKey(0)
      cv2.destroyAllWindows()


def test_data_arr():
    start = time.time()
    file_arr_temp = open("out/file_arr_temp_v3.txt", "r") 
    ix = 0 
    Y = {}
    for i in file_arr_temp:
        res = json.loads(i.split("\n")[0])
        Z = np.zeros((12, 48603))
        L1 = list(res.values())[0][0]
        L2 = list(res.values())[0][1]
        for i in range(len(L1)):
             Z[L1[i],L2[i]] += 1    
        ix += 1 
        Y[list(res.keys())[0]] = []
        for o in range(Z.shape[0]):
            #print (sum(Z[o,:])) 
            if sum(Z[o,:]) > 0:
                Y[list(res.keys())[0]].append(1) 
            if sum(Z[o,:]) == 0:
                Y[list(res.keys())[0]].append(0) 
        print (list(res.keys())[0], Y[list(res.keys())[0]], "--------------------------")
#        print (list(res.keys())[0], (Z.shape[0]*Z.shape[1])/2, Z.shape)  
    print (time.time()-start, ix) 


def create_file_arr():
    p_open = TG.PRODUCT() #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']
    product_arr = p_open.to_numpy()

##---------------------------------------------->
    # Создаю словарь ID продуктов
    ids_product = {}
    vals_prod = np.unique(product_arr[:,1])
    for ix, i in enumerate(vals_prod):
        ids_product[i] = ix
    num_ids = len(ids_product)
    ids_product_order = TG.func_return(product_arr, 0)

##---------------------------------------------->    

    o_open = TG.ORDER() #['Order_Id', 'Branch_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date']  
    order_arr = o_open.to_numpy()
    ids_order = TG.func_return(order_arr, 2)

    c_open = TG.CUSTOMER() #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']
    customer_arr = c_open.to_numpy()
    ids_customer = TG.func_return(customer_arr, 0)
    print (num_ids, len(ids_customer))

#---------------------------------------------->
    """
    У меня есть вектор (48603, 1) в него ложу среднее кол во продуктов исходя из покупок
    Нужно получить кол покупок для каждого пользователя
    """
    MZ = {'01':0, '02':1, '03':2, '04':3, '05':4, '06':5, '07':6, '08':7, '09':8, '10':9, '11':10, '12':11} 
    ERROR = 0
    
    file_arr_temp = open("out/1_create_file_arr.txt", "w")
    for i in ids_customer:
        try:
#            Z = np.zeros((12, num_ids))
            user_data = {}
            user_data[i] = [[],[],[]]
            
            #print (Z.shape)
            for p in ids_order[int(i)]:
                o_id = order_arr[p][0]
                order_date = order_arr[p][-1]
                M = order_date.split(" ")[0].split("-")[1]
                #print (i, order_arr[p], len(ids_product_order[o_id]), len(ids_order[int(i)]), order_date, M, Z[MZ[M],:].shape)
                for g in ids_product_order[o_id]:
                    #Z[MZ[M], ids_product[product_arr[g][1]]] += product_arr[g][2]
                    
                    user_data[i][0].append(MZ[M])
                    user_data[i][1].append(ids_product[product_arr[g][1]])
                    user_data[i][2].append(product_arr[g][2])
                    

                    #print (product_arr[g].tolist())
                    
#                print (product_arr[ids_product_order[o_id]].tolist())
#                print(order_arr[p].tolist())
#                print (sum(Z))
#                print ("..................................")
            #if sum(customer_arr[ids_customer[i], 1:-1][0]) > 2.0:
                #print (customer_arr[ids_customer[i], 1:-1])
                
            #user_data[i] = Z.tolist()
            
            temp_json = json.dumps(user_data)
            file_arr_temp.write(f"{temp_json}\n")
        except KeyError:
            ERROR += 1
    print ("ERROR", ERROR)
    file_arr_temp.close()


if __name__ == "__main__":
    create_file_arr()
    
    #test_data_arr()
    
#### TEST BATCH       
#    for i in range(100000):
#        for o in get_batch():
#            print (o.shape)        
#        
    
