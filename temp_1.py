import threading
from utils import *
import dbhandler
import matplotlib.pyplot as plt
import matplotlib.dates as dates
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

def heatmap_vis(x, y, name):
    fig, ax = plt.subplots()
    im = ax.imshow(x)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(y)))
    ax.set_yticks(np.arange(len(y)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(y)
    ax.set_yticklabels(y)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(x.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(x.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    # Loop over data dimensions and create text annotations.
    for z in range(len(y)):
        for j in range(len(y)):
            text = ax.text(j, z, round(x[z, j], 1), ha="center", va="center", color="w")

    ax.set_title("Зависемость продуктов")
    fig.tight_layout()
    #plt.show()
    fig.savefig(name)    
    fig.clear(True)
    plt.close(fig)
if __name__ == "__main__":
    
#    P = PRODUCT()
#    A = P.loc[P['Product_ID'] == 554815] #554815 #313528
#    O = ORDER()
#    
#    #554815
#    #print (A)
#    A = A.to_numpy()
#    cats = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
#    M = {'01':0, '02':0, '03':0, '04':0, '05':0, '06':0, '07':0, '08':0, '09':0, '10':0, '11':0, '12':0}
#    for i in A:
#        OID = i[0]
#        
#        O_t = O.loc[O['Order_Id'] == OID]
#        data = O_t.to_numpy()[0][-1]
#        s_mon = data.split(" ")[0].split("-")[1]
#        M[s_mon] += 1 #i[3]
#        print (i[1], OID, data, s_mon)
#        #print (OID,list(i), len(cats))
#    print (M)   

#    T = DB.client.execute(f"""
#            SELECT
#               count(columns.sum1) as s1,
#               columns.time
#            FROM
#            (SELECT
#            toMonth(Order_Date) as time,
#            count(Product_ID) as sum1
#            FROM my_table
#            WHERE Product_ID = 554815
#            GROUP BY Order_Date) columns
#            GROUP BY columns.time
#            ORDER BY columns.time
#            ASC    
#            """)  # test


#    T = DB.client.execute(f"""
#            SELECT
#                toMonth(Order_Date) as time
#            FROM test
#            WHERE Product_ID = 554815
#            """) #554815 #313528
#    #print (T)
#    #M = {'01':0, '02':0, '03':0, '04':0, '05':0, '06':0, '07':0, '08':0, '09':0, '10':0, '11':0, '12':0}
#    M = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}
#    for i in T:
#        #data = i[-3]
#        #s_mon = data.split(" ")[0].split("-")[1]
#        #print (data, s_mon)
#        s_mon = i[0]
#        M[s_mon] += 1#i[2]
#--------------------------------->
#    T = DB.client.execute(f"""
#            SELECT
#               count(columns.sum1) as s1,
#               columns.time
#            FROM
#            (SELECT
#            toMonth(Order_Date) as time,
#            count(Product_ID) as sum1
#            FROM test
#            WHERE Product_ID = 554815
#            GROUP BY Order_Date) columns
#            GROUP BY columns.time
#            ORDER BY columns.time
#            ASC    
#                                
#            """)      
#                                             SUM(Items_Count) as IC, 
#                                 SUM(Total_Amount) as TA, 
#                                 toMonth(Order_Date) as time






#    T = DB.client.execute(f"""
#             SELECT 
#                Items_Count,
#                Product_ID,
#                Order_ID,
#                toMonth(Order_Date) as time
#               FROM test
#               WHERE Items_Count > (
#                 SELECT AVG(Items_Count)
#                   FROM test
#                   WHERE Order_ID = Order_ID);
#                            """) 

    #Получить сопутствующий продукты
#    T = DB.client.execute(f"""
#                            SELECT
#                                 Order_ID, 
#                                 Product_ID, 
#                                 Items_Count, 
#                                 Total_Amount, 
#                                 Customer_Id,
#                                 toMonth(Order_Date) as time
#                            FROM test
#                            WHERE test.Product_ID = 554815
#                            """)   
######################################################################    
######################################################################    
######################################################################   
#    H = DB.client.execute(f"""
#                SELECT * FROM category1 
#                order by sum  
#                DESC
#                                                            
#                """)
#    print (H[0],len(H))
    
#    T = DB.client.execute(f"""
#                SELECT
#                     Category1_Id,
#                     SUM(Items_Count) as IC
#                FROM test
#                GROUP BY Category1_Id   
#                ORDER BY IC
#                DESC                                         
#                """)
#    T = DB.client.execute(f"""
#                SELECT
#                     Category1_Id,
#                     groupArray(time) AS eventstimes
#                FROM 
#                (
#                    SELECT
#                         Category1_Id,
#                         toMonth(Order_Date) as time
#                    FROM test
#                )
#                GROUP BY Category1_Id
#                """)#,toMonth(Order_Date) as time
#    T = DB.client.execute(f"""
#                    SELECT
#                        Category1_Id,
#                        SUM(Items_Count) AS IC,
#                        groupArray(toMonth(Order_Date)) AS eventstimes
#                    FROM test
#                    GROUP BY Category1_Id
#                """)
#    #print (T[2][0], len(T[2][1]), len(T))
#    print (T[0][0], T[0][1], T[0][2], len(T))

#    T = DB.client.execute(f"""
#                    SELECT
#                        Category1_Id,
#                        SUM(Items_Count) AS IC,
#                        groupArrayArray([toMonth(Order_Date), Items_Count]) AS eventstimes
#                    FROM test
#                    GROUP BY Category1_Id
#                """)


#    T = DB.client.execute(f"""
#                    SELECT
#                        Category1_Id,
#                        groupArray(Items_Count) AS IC,
#                        groupArray(toMonth(Order_Date)) AS eventstimes
#                    FROM test
#                    GROUP BY Category1_Id
#                """)

    T = DB.client.execute(f"""
                    SELECT
                        Category1_Id,
                        groupArray(Items_Count) AS IC,
                        groupArray(toMonth(Order_Date)) AS eventstimes
                    FROM test
                    GROUP BY Category1_Id
                """)

    #print (T[2][0], len(T[2][1]), len(T))
    print (T[0][0], len(T[0][1]), len(T[0][2]), len(T))


######################################################################    
######################################################################    
######################################################################    
#Регрессия

#    T = DB.client.execute(f"""
#                            SELECT
#                                SUM(Items_Count) as IC,
#                                toMonth(Order_Date) as time
#                            FROM test
#                            WHERE test.Product_ID = 554815 
#                            GROUP BY time
#                            """) 
#    Z = np.array(T)[:,0]
#    print (np.array(T)[:,0])
#                             
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
#    #8437646 554815
#    
#    
#    Data_1 = list(D[554815].values())
#    Data_2 = list(D[8437646].values())   
#    #print (Data_1, Data_2)   
#       
#       
#    rng = numpy.random

#    # Parameters
#    learning_rate = 0.001
#    training_epochs = 100000
#    display_step = 50


#    # Training Data
#    train_X = numpy.array(Data_2, dtype="float32")#.reshape((12, 1)) #f_list[100,0][2]#numpy.asarray([3.3,4.4,5.5,6.71,6.93,4.168,9.779,6.182,7.59,2.167,7.042,10.791,5.313,7.997,5.654,9.27,3.1])
#    train_Y = numpy.array(Data_1, dtype="float32")[:,:1]#.reshape((12, 1)) #f_list[100,1][0][2]#numpy.asarray([1.7,2.76,2.09,3.19,1.694,1.573,3.366,2.596,2.53,1.221,2.827,3.465,1.65,2.904,2.42,2.94,1.3])

#    print (train_X, train_Y)

#    n_samples = train_X.shape[0]
#    print (train_Y.shape, train_X.shape, n_samples)

#    # tf Graph Input
#    X = tf.placeholder("float")
#    Y = tf.placeholder("float")

#    # Set model weights
#    W = tf.Variable(rng.randn(), name="weight")
#    b = tf.Variable(rng.randn(), name="bias")

#    # Construct a linear model
#    pred = tf.add(tf.multiply(X, W), b)


#    # Mean squared error
#    cost = tf.reduce_sum(tf.pow(pred-Y, 2))/(2*n_samples)
#    # Gradient descent
#    #optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)
#    optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost)

#    # Initialize the variables (i.e. assign their default value)
#    init = tf.global_variables_initializer()

#    # Start training
#    with tf.Session() as sess:
#        sess.run(init)

#        # Fit all training data
#        for epoch in range(training_epochs):
#            for (x, y) in zip(train_X, train_Y):
#                sess.run(optimizer, feed_dict={X: x, Y: y})

#            #Display logs per epoch step
#            if (epoch+1) % display_step == 0:
#                c = sess.run(cost, feed_dict={X: train_X, Y:train_Y})
#                print ("Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(c), \
#                    "W=", sess.run(W), "b=", sess.run(b))

#        print ("Optimization Finished!")
#        training_cost = sess.run(cost, feed_dict={X: train_X, Y: train_Y})
#        print ("Training cost=", training_cost, "W=", sess.run(W), "b=", sess.run(b), '\n')
#        print ('Прогнозирование') 
#        y_pred_batch = sess.run(pred, {X: train_X})
#        print (y_pred_batch)
#        print (train_Y) #, train_X
#        #Graphic display
#        plt.plot(train_X, train_Y, 'ro', label='Original data')
#        plt.plot(train_X, sess.run(W) * train_X + sess.run(b), label='Fitted line')
#        plt.legend()
#        plt.show()                           
#    print (len(T))  
    
######################################################################    
######################################################################    
######################################################################    
    
                             
#    T = DB.client.execute(f"""
#            SELECT
#               count(columns.sum1) as s1,
#               columns.time
#            FROM
#            (SELECT
#            toMonth(Order_Date) as time,
#            count(Product_ID) as sum1
#            FROM my_table
#            WHERE Product_ID = 554815
#            GROUP BY Order_Date) columns
#            GROUP BY columns.time
#            ORDER BY columns.time
#            ASC    
#            """)  # test     

                       
#    WHERE Product_ID = 554815


#    G = {}
#    t_str = ""
#    t_count = 0
#    G[554815] = [0,0,0,0,0,0,0,0,0,0,0,0]
#    ixz = 0
#    LS = []
#    for batch_idx, i in enumerate(T):
#        if batch_idx % 100 == 0:
#            t_str += f"OR test.Order_ID = {i[0]}\n"
#            t_count += i[2]
#            G[554815][(i[-1])] += i[2]
#            ixz += 1
#            a = DB.client.execute(f"""
#                            SELECT
#                                 Order_ID, 
#                                 Product_ID, 
#                                 Items_Count, 
#                                 Total_Amount, 
#                                 Customer_Id,
#                                 toMonth(Order_Date) as time
#                            FROM test
#                            WHERE NOT test.Product_ID = 554815
#                            AND ({t_str[3:]})
#                            
#                            """)
#            LS += a 
#    a = LS                                            
#    dict_data = {}   
#    P1 = t_count   
#    for r in a:
#        try:
#            dict_data[r[1]][0][(r[-1])] += r[2]  
#            dict_data[r[1]][1] += r[2]
#        except KeyError:
#            dict_data[r[1]] = [[0,0,0,0,0,0,0,0,0,0,0,0], 0] 
#            dict_data[r[1]][0][(r[-1])] += r[2]
#            dict_data[r[1]][1] += r[2]  
#        #print (r[-1])  

#    for r in dict_data:
#        P2 = dict_data[r][1]
#        P = (P2/P1)*100  
#        if P > 5:  
#            G[r] = dict_data[r][0]  
            
             

#    


#https://www.sqlservertutorial.net/sql-server-basics/sql-server-correlated-subquery/
#https://coderoad.ru/1555051/SQL-%D0%BA%D0%BE%D1%80%D1%80%D0%B5%D0%BB%D1%8F%D1%86%D0%B8%D1%8F
#https://coderoad.ru/23415492/%D0%9A%D0%BE%D1%8D%D1%84%D1%84%D0%B8%D1%86%D0%B8%D0%B5%D0%BD%D1%82-%D0%9A%D0%BE%D1%80%D1%80%D0%B5%D0%BB%D1%8F%D1%86%D0%B8%D0%B8-%D0%9F%D0%B8%D1%80%D1%81%D0%BE%D0%BD%D0%B0-SQL-Server
#https://habr.com/ru/post/512304/
#https://github.com/linyue515/ClickHouse-1/blob/master/docs/en/query_language/agg_functions/reference.md


#https://github.com/ClickHouse/ClickHouse/issues/1777



#https://academy-of-capital.ru/blog/soputstvuyushchie-tovary/
#https://habr.com/ru/company/datawiz/blog/241738/
#https://habr.com/ru/company/retailrocket/blog/441366/

#https://github.com/mourner/simpleheat/blob/gh-pages/simpleheat.js

#https://stackoverflow.com/questions/3080421/javascript-color-gradient

#https://habr.com/ru/post/514818/

#https://habr.com/ru/company/ods/blog/322076/

#https://vc.ru/flood/43786-kak-uskorit-rabotu-redakcii-internet-magazina-v-10-raz-s-pomoshchyu-mashinnogo-obucheniya

#https://habr.com/ru/company/otus/blog/485972/

#https://doc.arcgis.com/ru/insights/latest/analyze/regression-analysis.htm

#https://dev-gang.ru/article/-prostyh-sposoba-normalizovat-dannye-v-python-7qqrhmlppl/

#https://www.machinelearningmastery.ru/predicting-sales-611cb5a252de/

#https://gist.github.com/karamanbk/fae78e4b0894cc0812812e4e600e5860

#https://habr.com/ru/company/ozontech/blog/431950/

#https://retail-loyalty.org/lr/trinity/

#https://towardsdatascience.com/predicting-sales-611cb5a252de

#https://www.kaggle.com/myster/eda-prophet-winning-solution-3-0
#https://www.kaggle.com/guidosalimbeni/regression-with-convolutional-neural-network-keras


#https://machinelearningmastery.com/regression-tutorial-keras-deep-learning-library-python/

#https://altinity.com/blog/harnessing-the-power-of-clickhouse-arrays-part-2

#Где именно спрятано машинное обучение

#Все представленные на рынке сервисы с машинным обучением решают два типа бизнес-задач:

#Прогнозирование продаж на уровне клиента
#Какая вероятность продажи конкретного товара в зависимости от истории покупок клиента на данном сайте или других сторонних сайтах, контекста запроса, цвета кнопки на сайте или канала, из которого пришел клиент. «Под капотом» решаются задачи бинарной классификации, коллаборативной фильтрации или вычисления сходства с уже купленными товарами (content-based рекомендации).
#Прогнозирование продаж на уровне товара и магазина
#Прогнозирование временных рядов.
#Таким образом, прогнозируется либо событие с двумя исходами (купит, не купит), либо временной ряд. Прогноз бинарного события в свое очередь сводится либо к стандартной задаче бинарной классификации, либо к задаче коллаборативной фильтрации.

#Обучение прогностических моделей, по всей видимости, происходит на данных той платформы, которая предоставляет сервис. После того, как модель обучена, сервис встраивается в интернет-магазин и вычисляет прогнозы, опираясь как на данные самой платформы, так и на данные продаж и поведение пользователя в интернет-магазине. Впоследствии возможно дообучение или обновление модели на новых данных.





#Какую архитектуру нейросети вы используете?
#Совсем технические детали: мы используем ансамбль нейросетей из сверточной сети над эмбеддингами слов для извлечения информации из названия и описания товара и сверточной сети resnet50 для извлечения информации из изображения, над которыми надстроен общий классификатор для результирующего предсказания.

#Итого
#Типовые задачи редакции интернет-магазина можно ускорить в 5-50 раз, если усилить редакцию с помощью машинного обучения.

#Категоризация товаров и присвоение товарам характеристик – это хорошо решаемая с помощью нейросетей задача. Первые хорошие результаты можно получить уже через неделю работы.

#Но совсем без редакции обойтись не получится: люди нужны для контроля работы нейросети и решения новых возникающих задач.



