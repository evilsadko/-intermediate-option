import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import json
import test_graph as TG

#with open('data.txt', 'r') as js_file:
#    json.dump(dict_i ,js_file)
    

if __name__ == "__main__":
    p_open = TG.PRODUCT() #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']
    #TG.see_stat(p_open)   

    product_dict = {}
    p_arr = p_open.to_numpy()
    vals_prod = np.unique(p_arr[:,1])
    for ix, i in enumerate(vals_prod):
        product_dict[i] = ix
        
    o_open = TG.ORDER() #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged']  
    o_arr = o_open.to_numpy()
#    
    user_data = {}
    product_data = {}
    idx = 0
    with open('data_arr.txt') as json_file:
        data = json.load(json_file)
        for o in data:
            idx += len(data[o])
            for i in range(len(data[o])):
                
                IDX = np.where(p_arr[:,1] == data[o][i]["P_ID"])
                #print (len(IDX))#(data[o][i]["P_ID"], product_dict[data[o][i]["P_ID"]]) 
                #
                try:    
                    product_data[data[o][i]["P_ID"]] += 1
                except KeyError:
                    product_data[data[o][i]["P_ID"]] = 0
            user_data[data[o][0]["P_USER"]] = 0
            #print (o, len(data[o]), data[o][0]["P_USER"])
        print (f"""Наименования продуктов которые покупались: {len(list(product_data.keys()))}\n 
                   Количество покупателей: {len(list(user_data.keys()))}\n
                   Количество покупок: {len(list(data.keys()))}\n
                   Количество продуктов: {idx}\n
                   Среднее количество продуктов в покупке: {idx/len(list(data.keys()))}\n 
                """)
    for K in product_data.keys():
         print (product_data[K])
# Создать диаграмму покупаемых продуктов



#https://medium.com/@kvnamipara/a-better-visualisation-of-pie-charts-by-matplotlib-935b7667d77f
#https://medium.com/swlh/python-data-visualization-with-matplotlib-for-absolute-beginner-part-iii-three-dimensional-8284df93dfab
#https://jakevdp.github.io/PythonDataScienceHandbook/04.12-three-dimensional-plotting.html
#https://towardsdatascience.com/the-art-of-effective-visualization-of-multi-dimensional-data-6c7202990c57


#Наименования продуктов которые покупались: 24290
# 
#                   Количество покупателей: 59843

#                   Количество покупок: 82705

#                   Количество продуктов: 8239567

#                   Среднее количество продуктов в покупке: 99.62598391874735


#![Иллюстрация к проекту](https://github.com/evilsadko/social-network/blob/master/media/skr4.png)

#Victor, [09.02.21 13:41]
#json ключи покупатели, вложения продукты

#Victor, [09.02.21 13:43]
#82705 - покупок

#Victor, [09.02.21 13:55]
#8239567 - продуктов


#Victor, [09.02.21 14:01]
#59843 - пользователей которые есть в базе


#Victor, [09.02.21 14:11]
#59843 покупателя совершили 82705 покупок купив 8239567

#Victor, [09.02.21 14:11]
#Средняя покупка содержит 99.6 товаров

#Victor, [09.02.21 14:54]
#Почему получилось 59843 - это индивидуальные ID, остальное в мусор так как это не клубные клиенты их в статистику не берем

#Victor, [09.02.21 15:12]
#из 35376 наименований продуктов, 59843 покупателями куплено 24290 наименования

#Victor, [09.02.21 15:15]
#через 40 минут на прогулку, к этому времени попытаюсь подготовить векторы к кластеризации

