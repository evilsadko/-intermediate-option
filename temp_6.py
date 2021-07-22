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
import sys
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
#    digits_loss = tf.nn.softmax_cross_entropy_with_logits(
#                                          logits=tf.reshape(y[:, 1:],
#                                                     [-1, 100]),
#                                          labels=tf.reshape(y_[:, 1:],
#                                                     [-1, 100]))
#    digits_loss = tf.reshape(digits_loss, [-1, 1])
#    digits_loss = tf.reduce_sum(digits_loss, 1)
#    digits_loss *= (y_[:, 0] != 0)
#    digits_loss = tf.reduce_sum(digits_loss)

#    # Calculate the loss from presence indicator being wrong.
#    presence_loss = tf.nn.sigmoid_cross_entropy_with_logits(logits=y[:, :1], labels=y_[:, :1])
#    presence_loss = 1 * tf.reduce_sum(presence_loss)

#    return digits_loss, presence_loss, digits_loss + presence_loss
    presence_loss = tf.nn.sigmoid_cross_entropy_with_logits(logits=y[:, :1], labels=y_[:, :1])
    presence_loss = 1 * tf.reduce_sum(presence_loss)
    return presence_loss

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

#digits_loss, presence_loss, loss = get_loss(y, y_)
loss = get_loss(y, y_)
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
        P = abs(P)
        if P > 100:
            P = 99
        #print (P, X[k_m][-1], X[k_m_before][-1])
        return up, P
    else:
        
        return up, 0

def train(initial_weights):    
    init = tf.initialize_all_variables()
    saver = tf.train.Saver()
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.70)
    with tf.Session(config=tf.ConfigProto(gpu_options=gpu_options)) as sess:
        if initial_weights is not None:
            saver.restore(sess, "model_slim/model.ckpt")
        else:    
            sess.run(init)
        try:
            for q in range(Array1.shape[0]):
                batch_xs = Array1[q,:,:,:].reshape((1,6,3,1))
                batch_ys = Array2[q,:].reshape((1,101))
                #print (batch_xs.shape, batch_ys.shape)
                sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
                
                
                
                batch_test_x = Array1_test[10,:,:,:].reshape((1,6,3,1))
                batch_test_y = Array2_test[10,:].reshape((1,101))                
                r = sess.run([best,
                              correct,
                              tf.greater(y[:, 0], 0),
                              y_[:, 0],
                              loss],
                              feed_dict={x: batch_test_x, y_: batch_test_y})
                print (r, "Проверка: ", batch_test_y[:,0])
        except KeyboardInterrupt:
             save_path = saver.save(sess, "model_slim/model.ckpt")
             print("Model saved in path: %s" % save_path)

def chunks(lst, count):
    start = 0
    for i in range(count):
          stop = start + len(lst[i::count, :])
          yield lst[start:stop, :]
          start = stop     

def create_data():
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
#----------------------------------------->
# Создать массив категорий для кодирования
    dict_category1 = {}
    T = DB.client.execute(f"""
                            SELECT
                                DISTINCT Category1_Id
                            FROM test
                            ORDER BY Category1_Id
                            """)    

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
# Нужно получить все продукты и все сопуствующие этих продуктов с корреляцией 

    LIST_ARR = []
    LIST_ARR_pred = []
    
    LIST_ARR_test = []
    LIST_ARR_pred_test = []

    for ikx, Kx in enumerate(p_list[:100]):
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
            
            temp_corr, D = func_corr(Z[:,0], Kx) 
            if len(temp_corr) != 0:
                M = {}
                for i in range(Z.shape[0]):
                    IC = Z[i,0]
                    TA = Z[i,1]
                    if IC==0 and TA==0:
                        price = 0
                    else:
                        price = TA/IC
                    M[Z[i,-1]] = [IC, TA, price]   
                    print (M[Z[i,-1]])
                    
                temp_list = list(M.keys())
                #print (temp_list, list(M.values()))
                for A in temp_corr[:3]:
                    corr_product_info = p_list[dict_pid[A]]
                    for i in range(0, len(temp_list)):
                        k_m = temp_list[i]
                        k_m_before = temp_list[i-1]
                        #----------------------------------->
                        print (">>>>>>>>>>", M, k_m, k_m_before)
                        up1, P1 = func_helper(M, k_m, k_m_before)
                        up2, P2 = func_helper(D[A], k_m, k_m_before)
                        
#                        print ("...........................")
#                        print (f"ID PRODUCT ОСНОВНОЕ {Kx[0]} >>>>", up1, P1, ">>>>>>>>>>>>>", 
#                                dict_pid[Kx[0]], dict_category1[Kx[1]], dict_category2[Kx[2]], M[k_m][-1], M[k_m_before], k_m, k_m_before) 
#                        
#                        print (f"ID PRODUCT КОРРЕЛИРУЮЩЕЕ {A} >>>>", up2, P2, ">>>>>>>>>>>>>", 
#                                dict_pid[A], dict_category1[corr_product_info[1]], dict_category2[corr_product_info[2]], D[A][k_m][-1], D[A][k_m_before], k_m, k_m_before) 
#                        print ("...........................")
                        
                        def to_vec(c):
                            y = numpy.zeros((100,))
                            y[c] = 1.0
                            return y
                        predict =  numpy.concatenate([up1, to_vec(P1)])
                        #predict = [up1, P1]
                        in_data = [dict_pid[Kx[0]], dict_category1[Kx[1]], dict_category2[Kx[2]], 
                                   M[k_m_before][0],  M[k_m_before][1],  M[k_m_before][2],
                                   k_m, k_m_before, M[k_m][-1],
                                   dict_pid[A], dict_category1[corr_product_info[1]], dict_category2[corr_product_info[2]],
                                   D[A][k_m_before][0], D[A][k_m_before][1], D[A][k_m_before][2],
                                   k_m, k_m_before, D[A][k_m][-1]]
                        arr_ = np.array(in_data).reshape((6,3,1))
                        predict = np.array(predict)
                        #K = random.choice(range(1, len(temp_list)))
                        #print (K)
                        if i % 11 == 0:
                            LIST_ARR_test.append(arr_)
                            LIST_ARR_pred_test.append(predict)                        
                        else:
                            LIST_ARR.append(arr_)
                            LIST_ARR_pred.append(predict)
                        
    Array1 = np.array(LIST_ARR)
    Array2 = np.array(LIST_ARR_pred)
    print (Array1.shape, Array2.shape)
    Array1_test = np.array(LIST_ARR_test)
    Array2_test = np.array(LIST_ARR_pred_test)
    print (Array1_test.shape, Array2_test.shape)
    
#    OK = 0
#    NOK = 0
#    for k in range(Array2.shape[0]):
#        print (Array2[k,0])
#        if Array2[k,0] == 0:
#            NOK += 1
#        else:
#            OK += 1
#    print (OK, NOK)
#    #---------------------------------->
#    init = tf.initialize_all_variables()
#    saver = tf.train.Saver()



#    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.70)
#    with tf.Session(config=tf.ConfigProto(gpu_options=gpu_options)) as sess:
#        if initial_weights is not None:
#            saver.restore(sess, "model_slim/model.ckpt")
#        else:    
#            sess.run(init)
#        try:
#            for a in range(20):
#                for q in range(Array1.shape[0]):
#                    batch_xs = Array1[q,:,:,:].reshape((1,6,3,1))
#                    batch_ys = Array2[q,:].reshape((1,101))
#                    #print (batch_xs.shape, batch_ys.shape)
#                    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
#                    
#                    
#                    
#                    batch_test_x = Array1_test[-10:,:,:,:].reshape((10,6,3,1))
#                    batch_test_y = Array2_test[-10:,:].reshape((10,101))                
#                    r = sess.run([best,
#                                  correct,
#                                  tf.greater(y[:, 0], 0),
#                                  y_[:, 0],
#                                  loss],
#                                  feed_dict={x: batch_test_x, y_: batch_test_y})
#                    #r_short = (r[0][:190], r[1][:190])  
#                    r_short = (r[0][:190], r[1][:190], r[2][:190], r[3][:190])            
#                    for b, c, pb, pc in zip(*r_short):
#                        print ("{} {} <-> {} {}".format(c, pc, b, float(pb)))  
#                                  
#                    print ("Потеря: ", r[-1])
#        except KeyboardInterrupt:
#             save_path = saver.save(sess, "model_slim/model.ckpt")
#             print("Model saved in path: %s" % save_path)

if __name__ == "__main__":

    if len(sys.argv) > 1:
       initial_weights = sys.argv
    else:
       initial_weights = None
    create_data()



