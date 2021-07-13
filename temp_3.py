import threading
from utils import *
import dbhandler
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import random
#import tensorflow as tf
#import numpy
#import keras
#from keras.layers import Dense
#from keras.models import Sequential
#from keras.optimizers import Adam 
#from keras.callbacks import EarlyStopping
#from keras.utils import np_utils
#from keras.layers import LSTM
#from sklearn.model_selection import KFold, cross_val_score, train_test_split



DB = dbhandler.DataBase()

def func_corr(Z, Kx):  
    T = DB.client.execute(f"""
             SELECT 
                Items_Count,
                Total_Amount,
                Product_ID,
                Order_ID,
                toMonth(Order_Date) as time
               FROM test              
               WHERE Order_ID IN (                        
                            SELECT
                                 Order_ID
                            FROM test
                            WHERE test.Product_ID = {Kx[0]}
                           )
                            """)    
    D = {}  
    for k in T:
        if k[0] > 0:
            try:
                #print (k[1], k[0])
                D[k[2]][k[-1]][0] += k[0]
                D[k[2]][k[-1]][1] += k[1]
                D[k[2]][k[-1]][2] = k[1]/k[0]
                
            except KeyError:
                #D[k[2]] = {1:[0,0], 2:[0,0], 3:[0,0], 4:[0,0], 5:[0,0], 6:[0,0], 7:[0,0], 8:[0,0], 9:[0,0], 10:[0,0], 11:[0,0], 12:[0,0]}
                D[k[2]] = {1:[0,0,0], 2:[0,0,0], 3:[0,0,0], 4:[0,0,0], 5:[0,0,0], 6:[0,0,0], 7:[0,0,0], 8:[0,0,0], 9:[0,0,0], 10:[0,0,0], 11:[0,0,0], 12:[0,0,0]}
                D[k[2]][k[-1]][0] += k[0]
                D[k[2]][k[-1]][1] += k[1]
            
    #print (len(D), D)
    T_data0 = []
    ID_s = []
    
    T_data0.append(Z)
    ID_s.append(Kx[0])
    for k in D:
        P = np.mean(np.array(list(D[k].values()))[:,0]) / np.mean(Z) * 100.
#        P = np.mean(np.array(list(D[k].values()))) / np.mean(Z) * 100.
        if P > 10:
            #print (np.array(list(D[k].values()))[:,0], Z, P) #np.mean(Z), 
            T_data0.append(np.array(list(D[k].values()))[:,0])
            ID_s.append(k) 
    T_data0 = np.array(T_data0)
    #print (Z.shape, T_data0.shape)
    corr_0 = np.corrcoef(T_data0) 
    #heatmap_vis(corr_0, ID_s, f"ic_heatmap_554815.jpg")   
    #print (corr_0.shape, len(ID_s))
    
    temp_list = []
    for x in range(corr_0.shape[0]):
        for y in range(corr_0.shape[1]):
            if corr_0[x,y] >= 0.9:
                if ID_s[x] != ID_s[y]:
                    #print (ID_s[x], ID_s[y], corr_0[x,y])   
                    temp_list.append(ID_s[y])
    return temp_list, D       

def func_helper(X, k_m, k_m_before):
    P = round(((X[k_m][-1]- X[k_m_before][-1])/ X[k_m][0]*100), 1)
    up = np.zeros(2)
    if P<0:
        up[0] = 1
    if P>0:
        up[1] = 1
    return up, P


if __name__ == "__main__":
# Создать массив классов продуктов из магазина


    p_list = DB.client.execute(f"""
                            SELECT
                                DISTINCT Product_ID,
                                Category1_Id, 
                                Category2_Id
                            FROM test
                            ORDER BY Product_ID
                            """)     
    dict_pid = {}
    for ix, o in enumerate(p_list):
        dict_pid[o[0]] = ix
    #class_array = np.zeros((len(p_list),1))
    #print (class_array.shape)
#----------------------------------------->
# Создать массив категорий для кодирования

    T = DB.client.execute(f"""
                            SELECT
                                DISTINCT Category1_Id
                            FROM test
                            ORDER BY Category1_Id
                            """)    
    dict_category1 = {}
    for ix, o in enumerate(T):
        dict_category1[o[0]] = ix
    
    dict_category2 = {}
    T = DB.client.execute(f"""
                            SELECT
                                DISTINCT Category2_Id
                            FROM test
                            ORDER BY Category2_Id
                            """)       
                            
    for ix, o in enumerate(T):
        dict_category2[o[0]] = ix  
                               
    #print (dict_category2[5704])

#----------------------------------------->
# Создать массив месяцов

#    month_array = np.zeros((12,1))

# Нужно получить все продукты и все сопуствующие этих продуктов с корреляцией 

    LIST_ARR = []
    for Kx in p_list[:20]:
        T = DB.client.execute(f"""
                                SELECT
                                    SUM(Items_Count) as IC,
                                    SUM(Total_Amount) as TA,
                                    toMonth(Order_Date) as time
                                FROM test
                                WHERE test.Product_ID = {Kx[0]} 
                                GROUP BY time
                                """)         
        Z = np.array(T)[:,:]#[:,:]
        
        if (Z.shape[0]==12):
            
            temp_, D = func_corr(Z[:,0], Kx)
            #ID_corr_product = random.choice(temp_)
            #print (Kx[0], Z.shape, len(temp_), ID_corr_product, D[ID_corr_product])
            M = {}
            for i in range(Z.shape[0]):
                IC = Z[i,0]
                TA = Z[i,1]
                if TA>IC:
                    price = TA/IC
                else:
                    price = 0.1    
                M[Z[i,-1]] = [IC, TA, price] #[price, TA, IC]   
            #print (Kx, T, M)
            temp_list = list(M.keys())
            for A in temp_:
                #print (A, D[A])
                corr_product_info = p_list[dict_pid[A]]
                #print (f"ID PRODUCT {A} >>>>>>>>>>>>>>>>>", dict_pid[A], dict_category1[corr_product_info[1]], dict_category2[corr_product_info[2]])
                for i in range(1, len(temp_list)):
                    k_m = temp_list[i]
                    k_m_before = temp_list[i-1]
                    
                    #P = round(((M[k_m][-1]-M[k_m_before][-1])/M[k_m][0]*100), 1)#int((temp_list[i]-temp_list[i-1])/temp_list[i]*100)
                    up1, P1 = func_helper(M, k_m, k_m_before)
                    
                    up2, P2 = func_helper(D[A], k_m, k_m_before)
#                    P = round(((D[A][k_m][-1]- D[A][k_m_before][-1])/ D[A][k_m][0]*100), 1)
#                    up = np.zeros(2)
#                    if P<0:
#                        up[0] = 1
#                    if P>0:
#                        up[1] = 1
                    print ("...........................")#, k_m, M[k_m_before])
                    print (f"ID PRODUCT {Kx[0]} >>>>", up1, P1, ">>>>>>>>>>>>>", 
                            dict_pid[Kx[0]], dict_category1[Kx[1]], dict_category2[Kx[2]], M[k_m][-1], M[k_m_before], k_m, k_m_before) 
                    
                    print (f"ID PRODUCT {A} >>>>", up2, P2, ">>>>>>>>>>>>>", 
                            dict_pid[A], dict_category1[corr_product_info[1]], dict_category2[corr_product_info[2]], D[A][k_m][-1], D[A][k_m_before], k_m, k_m_before) 
                    #Product_ID
                    #predict = [up1, P1]
                    #in_data = [dict_pid[Kx[0]], dict_category1[Kx[1]], dict_category2[Kx[2]], ]
                    #LIST_ARR.append([[up1, P1],[dict_pid[Kx[0]], dict_category1[Kx[1]], dict_category2[Kx[2]], ]])
                print ("\n")
#

#Какойто из месяцов будет брать в тестовую выборку


            
####             Код поиска корреляции

        #print (Z.tolist())
 



#                               
#        #-------------------->
#        
#        for x in range(corr_0.shape[0]):
#            for y in range(corr_0.shape[1]):
#                if corr_0[x,y] >= 0.9:
#                    print (ID_s[x], ID_s[y], corr_0[x,y])    
#------------------------------------->
            
            
            
            
            
            
#        temp_list = list(M.keys())
#        for i in range(len(temp_list)):
#            #print (temp_list[i], temp_list[i-1])
#            P = round(((temp_list[i]-temp_list[i-1])/temp_list[i]*100), 1)#int((temp_list[i]-temp_list[i-1])/temp_list[i]*100)
#            # Создать массив вверх/вниз
#            up = np.zeros(2)
#            if P<0:
#                up[0] = 1
#            if P>0:
#                up[1] = 1
#            print (up, P, k, i+1, M)    
#            print (k[0], dict_category2[k[2]], dict_category1[k[1]], M[i+1])
#            #print (up, P, ">>>>>>>>>" ,temp_list[i], temp_list[i-1], ">>>>>>>>> price", temp_list[i] - temp_list[i-1])
            
            
#    T = DB.client.execute(f"""
#                            SELECT
#                                SUM(Items_Count) as IC,
#                                SUM(Total_Amount) as TA,
#                                toMonth(Order_Date) as time
#                            FROM test
#                            WHERE test.Product_ID = 554815 
#                            GROUP BY time
#                            """) 
#    Z = np.array(T)#[:,:]
#    #print (np.array(T)[:,:].tolist())
#    M = {}
#    AVG = 0
#    for i in range(Z.shape[0]):
#        IC = Z[i,0]
#        TA = Z[i,1]
#        price = TA/IC
#        AVG += price
#        M[Z[i,-1]] = price   
#    print (M, AVG/Z.shape[0])
#    temp_list = list(M.values())
#    for i in range(Z.shape[0]):
#        P = int((temp_list[i]-temp_list[i-1])/temp_list[i]*100)
#        # Создать массив вверх/вниз
#        up = np.zeros(2)
#        if P<0:
#            #print (temp_list[i], temp_list[i-1], temp_list[i] - temp_list[i-1], P)   
#            up[0] = 1
#        else:
#            up[1] = 1
#        print (up, temp_list[i], temp_list[i-1], temp_list[i] - temp_list[i-1], P)




                             
#    T = DB.client.execute(f"""
#             SELECT 
#                Items_Count,
#                Total_Amount,
#                Product_ID,
#                Order_ID,
#                toMonth(Order_Date) as time
#               FROM test              
#               WHERE Order_ID IN (                        
#                            SELECT
#                                 Order_ID
#                            FROM test
#                            WHERE test.Product_ID = 554815
#                           )
#                            """)    
#    D = {}  
#    #print (T)                       
#    for k in T:
#        try:
#            D[k[2]][k[-1]][0] += k[0]
#            #print (k[1], D[k[1]])
#        except KeyError:
#            D[k[2]] = {1:[0,0], 2:[0,0], 3:[0,0], 4:[0,0], 5:[0,0], 6:[0,0], 7:[0,0], 8:[0,0], 9:[0,0], 10:[0,0], 11:[0,0], 12:[0,0]}
#            D[k[2]][k[-1]][0] += k[0]
#            D[k[2]][k[-1]][1] += k[1]
#    #print (len(D), D)
#    T_data0 = []
#    ID_s = []
#    
#    T_data0.append(Z)
#    ID_s.append(554815)
#    for k in D:
#        #print (np.mean(Z), np.mean(np.array(list(D[k].values()))))
#        P = np.mean(np.array(list(D[k].values()))) / np.mean(Z) * 100.
#        if P > 10:
#            print (Z, np.array(list(D[k].values())), np.mean(Z), np.mean(np.array(list(D[k].values()))))
#            T_data0.append(np.array(list(D[k].values()))[:,0])
#            ID_s.append(k)        
#    T_data0 = np.array(T_data0)
#    corr_0 = np.corrcoef(T_data0) 
#    #heatmap_vis(corr_0, ID_s, f"ic_heatmap_554815.jpg")   
#    print (corr_0.shape, len(ID_s))
#                           
#    #-------------------->
#    
#    for x in range(corr_0.shape[0]):
#        for y in range(corr_0.shape[1]):
#            if corr_0[x,y] >= 0.9:
#                print (ID_s[x], ID_s[y], corr_0[x,y])    
