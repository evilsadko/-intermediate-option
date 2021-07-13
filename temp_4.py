import threading
from utils import *
import dbhandler
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import random
import tensorflow as tf
import numpy
import keras
import tensorflow as tf
slim = tf.contrib.slim

learn_rate=0.001
def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)


def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

def get_loss(y, y_):
    # Calculate the loss from digits being incorrect.  Don't count loss from
    # digits that are in non-present plates.
    digits_loss = tf.nn.softmax_cross_entropy_with_logits(
                                          logits=tf.reshape(y[:, 1:],
                                                     [-1, 100]),
                                          labels=tf.reshape(y_[:, 1:],
                                                     [-1, 100]))
    digits_loss = tf.reshape(digits_loss, [-1, 1])
    digits_loss = tf.reduce_sum(digits_loss, 1)
    digits_loss *= (y_[:, 0] != 0)
    digits_loss = tf.reduce_sum(digits_loss)

    # Calculate the loss from presence indicator being wrong.
    #presence_loss = tf.nn.sigmoid_cross_entropy_with_logits(logits=y[:, :1], labels=y_[:, :1])
    presence_loss = tf.nn.sigmoid_cross_entropy_with_logits(logits=y[:, :1], labels=y_[:, :1])
    presence_loss = 1 * tf.reduce_sum(presence_loss)

    return digits_loss, presence_loss, digits_loss + presence_loss


def net():
    strides = 1
    x_expanded = tf.placeholder(tf.float32, [None, 6, 3, 1])
    x = slim.conv2d(x_expanded, 32, (1,1), stride=strides, padding="SAME", activation_fn=tf.nn.relu) 
    x = slim.conv2d(x, 64, (3, 3), stride=strides, padding="SAME", activation_fn=tf.nn.relu) 
    x = slim.conv2d(x, 256, (3, 3), stride=strides, padding="VALID", activation_fn=tf.nn.relu)
    print (x.shape)
    W_fc1 = weight_variable([4 * 1 * 256, 2048])
    b_fc1 = bias_variable([2048])
    conv_layer_flat = tf.reshape(x, [-1, 4 * 1 * 256])
    h_fc1 = tf.nn.relu(tf.matmul(conv_layer_flat, W_fc1) + b_fc1)

    W_fc2 = weight_variable([2048, 1+1*100])
    b_fc2 = bias_variable([1+1*100])

    y = tf.matmul(h_fc1, W_fc2) + b_fc2
    print (y.shape)
    return x_expanded, y
    
x, y = net()
y_ = tf.placeholder(tf.float32, [None, 101])

digits_loss, presence_loss, loss = get_loss(y, y_)
train_step = tf.train.AdamOptimizer(learn_rate).minimize(loss)
best = tf.argmax(tf.reshape(y[:, 1:], [-1, 1, 100]), 2)
correct = tf.argmax(tf.reshape(y_[:, 1:], [-1, 1, 100]), 2)




#init = tf.initialize_all_variables()
#saver = tf.train.Saver()
#gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.70)
#with tf.Session(config=tf.ConfigProto(gpu_options=gpu_options)) as sess:
#    if initial_weights is not None:
#        saver.restore(sess, "model_slim/model.ckpt")
#    else:    
#        sess.run(init)



#### Даннаые

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
    #print (X[k_m][-1], X[k_m_before][-1])
    up = np.zeros(1)
    if X[k_m][-1] != 0 and X[k_m_before][-1] != 0:
        P = int(((X[k_m][-1]- X[k_m_before][-1])/ X[k_m][-1]*100))#round(((X[k_m][-1]- X[k_m_before][-1])/ X[k_m][-1]*100), 1)
        if P<= 0:
            up[0] = 0
        if P>0:
            up[0] = 1
        if (P*-1) > 100:
            P = 100
        return up, P
    else:
        return up, 0


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
    LIST_ARR_pred = []
    for Kx in p_list[:7]:
        T = DB.client.execute(f"""
                                SELECT
                                    SUM(Items_Count) as IC,
                                    SUM(Total_Amount) as TA,
                                    toMonth(Order_Date) as time
                                FROM test
                                WHERE test.Product_ID = {Kx[0]} 
                                GROUP BY time
                                """)         
        Z = np.array(T)[:,:]
        
        if (Z.shape[0]==12):
            
            temp_, D = func_corr(Z[:,0], Kx)
            M = {}
            for i in range(Z.shape[0]):
                IC = Z[i,0]
                TA = Z[i,1]
                if TA>IC:
                    price = TA/IC
#                    if price == 0:
#                        print (">>>>>>>>>>>", price)
                else:
                    price = 0.1    
                M[Z[i,-1]] = [IC, TA, price] #[price, TA, IC]   
            temp_list = list(M.keys())
            for A in temp_:
                corr_product_info = p_list[dict_pid[A]]
                for i in range(1, len(temp_list)):
                    k_m = temp_list[i]
                    k_m_before = temp_list[i-1]
                    #----------------------------------->
                    up1, P1 = func_helper(M, k_m, k_m_before)
                    up2, P2 = func_helper(D[A], k_m, k_m_before)
                    
                    print ("...........................")
                    print (f"ID PRODUCT ОСНОВНОЕ {Kx[0]} >>>>", up1, P1, ">>>>>>>>>>>>>", 
                            dict_pid[Kx[0]], dict_category1[Kx[1]], dict_category2[Kx[2]], M[k_m][-1], M[k_m_before], k_m, k_m_before) 
                    
                    print (f"ID PRODUCT КОРРЕЛИРУЮЩЕЕ {A} >>>>", up2, P2, ">>>>>>>>>>>>>", 
                            dict_pid[A], dict_category1[corr_product_info[1]], dict_category2[corr_product_info[2]], D[A][k_m][-1], D[A][k_m_before], k_m, k_m_before) 
                    print ("...........................")
                    
                    def char_to_vec(c):
                        y = numpy.zeros((100,))
                        #print c
                        y[c] = 1.0
                        return y
                    predict =  numpy.concatenate([up1, char_to_vec(P1)])
                    #predict = [up1, P1]
                    in_data = [dict_pid[Kx[0]], dict_category1[Kx[1]], dict_category2[Kx[2]], 
                               M[k_m_before][0],  M[k_m_before][1],  M[k_m_before][2],
                               k_m, k_m_before, M[k_m][-1],
                               dict_pid[A], dict_category1[corr_product_info[1]], dict_category2[corr_product_info[2]],
                               D[A][k_m_before][0], D[A][k_m_before][1], D[A][k_m_before][2],
                               k_m, k_m_before, D[A][k_m][-1]]
                    arr_ = np.array(in_data).reshape((6,3,1))
                    LIST_ARR.append(arr_)
                    predict = np.array(predict)
                    LIST_ARR_pred.append(predict)

                    #print (arr_, arr_.shape)
                    #LIST_ARR.append([[up1, P1],[dict_pid[Kx[0]], dict_category1[Kx[1]], dict_category2[Kx[2]], ]])
                #print ("\n")
    Array1 = np.array(LIST_ARR)
    Array2 = np.array(LIST_ARR_pred)
    print (Array1.shape, Array2.shape)
    init = tf.initialize_all_variables()
    saver = tf.train.Saver()
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.70)
    with tf.Session(config=tf.ConfigProto(gpu_options=gpu_options)) as sess:
        sess.run(init)
        for q in range(Array1.shape[0]):
            batch_xs = Array1[q,:,:,:].reshape((1,6,3,1))
            batch_ys = Array2[q,:].reshape((1,101))
            #print (batch_xs.shape, batch_ys.shape)
            sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
            r = sess.run([best,
                          correct,
                          loss],
                          feed_dict={x: batch_xs, y_: batch_ys})
            print (r)
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
