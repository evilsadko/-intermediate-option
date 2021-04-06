import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import json
import utils as TG
import time

def create_file_arr():
    p_open = TG.PRODUCT() #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']
    product_arr = p_open.to_numpy()

#---------------------------------------------->
    # Создаю словарь ID продуктов
    ids_product = {}
    vals_prod = np.unique(product_arr[:,1])
    for ix, i in enumerate(vals_prod):
        ids_product[i] = ix
    num_ids = len(ids_product)
    ids_product_order = TG.func_return(product_arr, 0)

##---------------------------------------------->    

    o_open = TG.ORDER() #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged']  
    order_arr = o_open.to_numpy()
    ids_order = TG.func_return(order_arr, 1)

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
    file_arr_temp = open("out/file_arr_temp_v2.txt", "w")
    for i in ids_customer:
        try:
            Z = np.zeros((12, num_ids))
            #print (Z.shape)
            for p in ids_order[int(i)]:
                o_id = order_arr[p][0]
                order_date = order_arr[p][-1]
                M = order_date.split(" ")[0].split("-")[1]
                for g in ids_product_order[o_id]:
                    Z[MZ[M], ids_product[product_arr[g][1]]] += 1
            if sum(customer_arr[ids_customer[i], 1:-1][0]) == 3.0:
                file_arr_temp.write(f"{i};{Z.tolist()}\n")
        except KeyError:
            ERROR += 1
    print (ERROR)
    file_arr_temp.close()

def test_data_arr():
    file_arr_temp = open("out/file_arr_temp_v2.txt", "r")  
    for i in file_arr_temp:
        res = json.loads(i.split("\n")[0].split(";")[1])
        print (len(res), sum(res))  

if __name__ == "__main__":
    test_data_arr()



    
#Metacommerce проводит мониторинг как в интернете, так и в розничных торговых точках конкурентов для сравнения с своими данными и дальнейшего анализа и принятия решений
# -общая статистика
# -статистика точек - не уверен
# -анализа покупателей нет

#Мы пытаемся повысить прибыль увеличивая собственную эффективность, конечно хорошо смотреть что у конкурентов но это следующий этап
# -общая статистика
# -статистика точек реализации
# -анализ покупателей по покупкам

#Если покупатель не зарегестрирован это не означает что он для нас безполезная информация.
#После класттеризации индифицированных покупателей можем создать определенные паттерны каждой группы.
#Из этих данных создать модель которая по одной покупке на кассе сможет отнести покупателя к одной из групп,
#если группа в которую он попал являеться приоритетной, нужно попытаться еще до выхода из точки, получить его данные для дальнейшей индефикации ( акция, скидка с обязательной индефикацией документы/номер телефона/смс ). Такой подход поможет в микроманипуляции.
#В моем понимании микроманипуляция - когда мы знаем колерирующиеся товары, с помощью регрессии приблизительно понимать что товар "А" при снижении цены увеличит продажу товара "Б".
#После класстеризации покупателей мы будем знать в какой группе какой товар доменирует и этот товар с чем то коррелируеться в общих масштабах, это может увеличить прибыльность
#за счет повышения эффективности рекламы в рассылке. Этот подход похож на google, он не всегда бывает точным но все же работает. По мимо сбора цен у конкурентов, хотим реализовать сбор характеристик и фото продуктов для анализа. Мы попытаемся найти закономерности между продажами и цветовым решением упаковки/характеристиками.

# 
