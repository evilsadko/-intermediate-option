import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import json
import utils as TG
import time

#file_arr_temp = open("out/file_arr_temp_v3.txt", "r")  
file_arr_temp = open("out/1_create_file_arr.txt", "r").readlines()[:10000]#10000
tresh = .87#.68
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

    F = json.load(open(f"out/test_claster_10000_v4.json", 'r'))
#----------------------------------------->
# Найти доминирующий товар
# 
    for h in F:
        all_ = 0
        Sz = {}
        for i in F[h]:

            for o  in ids_order[int(float(i))]:
                OR = order_arr[o,:].tolist()
                #print (ids_product_order[OR[0]])
                for i in ids_product_order[OR[0]]:
                    #print (product_arr[i,:].tolist())
                    all_ += 1
                    try:
                        Sz[product_arr[i,1]][1].append(1)
                        Sz[product_arr[i,1]][0].append(i)
                    except KeyError:
#                        Sz[product_arr[i,1]] = 1
                        Sz[product_arr[i,1]] = [[i],[1]]
        print (Sz, all_)
#---------------------------------------------->    
    
#    id_list = []
#    val_list = []
#    for i in F:
#        id_list.append(i)
#        val_list.append(len(F[i]))
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

# V1
#def similarity(vector1, vector2):
#        return np.dot(vector1, vector2.T) / np.dot(np.linalg.norm(vector1, axis=1, keepdims=True), np.linalg.norm(vector2.T, axis=0, keepdims=True))
# V2
def similarity(vector1, vector2):
    return np.dot(vector1, vector2.T) / np.dot(np.linalg.norm(vector1, axis=0, keepdims=True), np.linalg.norm(vector2.T, axis=0, keepdims=True))

#------------------------------------------------------>
#def crt(i):
#        res = json.loads(i.split("\n")[0])
#        Z = np.zeros((12, 48603))
#        L1 = list(res.values())[0][0]
#        L2 = list(res.values())[0][1]
#        L3 = list(res.values())[0][2]
#        for i in range(len(L1)):
##             Z[L1[i],L2[i]] += 1  
#               Z[L1[i],L2[i]] += L3[i]  
#        Y = []
#        for o in range(Z.shape[0]):
#            Y.append(sum(Z[o,:])) 
#        return np.reshape(np.array(Y), (1,12)), list(res.keys())[0]
def crt(i):
        res = json.loads(i.split("\n")[0])
        Z = np.zeros(48603)
        L1 = list(res.values())[0][0]
        L2 = list(res.values())[0][1]
        L3 = list(res.values())[0][2]
        for i in range(len(L1)):
            Z[L2[i]] += L3[i]
            #print (L1[i],L2[i],L3[i])
        return Z, list(res.keys())[0]
#------------------------------------------------------>

def func_rec(ID):
    print (len(file_arr_temp))
    for ix, i in enumerate(file_arr_temp):
        Z0 = crt(i)
        G[ID] = [Z0[1]]
        del file_arr_temp[ix]
        for ix2, ii in enumerate(file_arr_temp):
            Z1 = crt(ii)
            KEF = similarity(Z0[0], Z1[0])
            # V1
#            if KEF[0]>tresh:
            # V2
            if KEF>tresh:
                G[ID].append(Z1[1])
                del file_arr_temp[ix2]
        ID += 1

def start_similarity():

    start = time.time()
    #file_arr_temp = open("out/1_create_file_arr.txt", "r").readlines()[:10000]
     
    func_rec(0)  
    print (time.time()-start, len(G))
    #print (G, len(file_arr_temp)) 
    with open(f"out/test_claster_10000_v4.json", 'w') as js_file:
        json.dump(G, js_file)  
        
 
def load_():
#     file_arr_temp = open("out/file_arr_temp_v3.txt", "r").readlines()
     file_arr_temp = open("out/1_create_file_arr.txt", "r").readlines()
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
    test()
    #----------------------------------------->
#Нюансы:
#Самый точная кластеризация для покупателя на векторе 12x48603
#12 - месяца
#48603 - классы продуктов в бд
#Из за такого размера вектора у нас 583236 параметров, так как алгоритм работает по принципу сравнения двух векторов, получаем большую вычислительную сложность, которую нужно оптимизировать.
#Нет времени для оптимизации, использовал идеи которые не отняли больше 2 часов на реализацию в коде:
#1 сделал min max кодирование, взял из полученного самый длинный вектор и учитывать его длину(остальные векторы приравнял длине самого длинного вектора, и заполнил нулями ).
#Эксперемент, получил не обьяснимю кластеризацию - не было пересечений продуктов в выявленных группах.
#2 использовал вектор размерности 12x1, 12 - месяца, в каждой позиции месяца было кол во продуктов купленных покумателем, обсалютно неудачный эксперемент
#3 испльзовал размерность вектора 1x48603 - в таком виде учитывал кол во купленных товаров за год, этот вариант использовал самым первым но получал ошибку, из за задчаи корреляции эта задача стала второстипенной. Для улучшения скорости, оптимезировал сортировку и хранение данных (создания вектора "на лету"), использовал подачу партиями по 10т.
#Этот эксперемент создал группы пользователей у которых есть пересечения товаров, что доказывает правильность данного направления.
#Доминирующий товар в группе, дает нам возможность предлагать пользователям группы, сопутствующий товар доминирующего, для повышения продаж этой пары.
#Выводы: для решения задачи "Повышения прибыльности за счет продаж", использовал алгоритмы: класстеризация, корреляция, регрессия 
#В класстеризации использован алгоритм косинусного расстояния, так же стоит проверить k-средних, EM-алгоритм, сети Кохонена. По моему мнению: покупательская активность за год предстваленная матрицей, самая точная характеристика покупателя. Данные о покупателе из бд использол для предворительной сортировки.
