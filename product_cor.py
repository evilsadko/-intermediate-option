import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import threading
import json
import time
from scipy import stats

def see_stat(x, y=0):
    if y == "list":
        print (x.columns.tolist())
    else:
        for c in  x.columns.tolist():
            print (f"###############\n{x[c].value_counts(dropna=False)}")


def diag_circle(vals, labels, myexplode, title, save_name, types=None):
    fig, ax = plt.subplots(figsize=(10,10), clear=True)
    if myexplode != None:
        ax.pie(vals, explode=myexplode, labels=labels, autopct='%.2f', startangle=90, pctdistance=0.85)
    else:
        ax.pie(vals, labels=labels, autopct='%.2f', startangle=0, pctdistance=0.85) # startangle=90 autopct='%1.2f%%',
    if types != None:
        centre_circle = plt.Circle((0,0),0.70,fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)

    ax.axis("equal")
    ax.set_title(f"ID продукта: {title}", loc="left", pad=20)
    ax.legend(loc='lower right') #, bbox_to_anchor=(0.7, 0.7) 'upper left' bbox_to_anchor=(0.5, 0., 0.5, 0.5) 'best'
    fig.savefig(save_name)
    fig.clear(True)
    plt.close(fig)

def CUSTOMER():
    c_open = pd.read_csv('B24_dbo_Crm_customers.csv', delimiter=',')
    c_open = c_open[['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']]
    c_open['join_club_success'] = c_open['join_club_success'].replace(np.nan, 2)
    c_open['Could_send_sms'] = c_open['Could_send_sms'].replace(np.nan, 0)
    c_open['Could_send_email'] = c_open['Could_send_email'].replace(np.nan, 0)
    c_open['consent'] = c_open['consent'].replace(np.nan, 0)
    c_open = c_open.apply(lambda x: pd.to_numeric(x, errors='coerce')).dropna() # Убираю все строки
    return c_open

def PRODUCT():
    s = time.time()
#    p_open = pd.read_csv('B24_dbo_Crm_product_in_order.csv', delimiter=',')
#    p_open.to_pickle("B24_dbo_Crm_product_in_order.pk")
    
    p_open = pd.read_pickle("B24_dbo_Crm_product_in_order.pk")
    see_stat(p_open)
    p_open = p_open[['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']] 
    print (time.time()-s)
    return p_open
    
def ORDER():
    o_open = pd.read_csv('B24_dbo_Crm_orders.csv', delimiter=',')
    #see_stat(o_open)
    o_open = o_open[['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date']]
    o_open['price_before_discount'] = o_open['price_before_discount'].replace(np.nan, 0)
    return o_open.sort_values(by=['Order_Date'])

def PRODUCTNAME():
    p_open = pd.read_csv('B24_dbo_Products.csv', delimiter=',')
    #see_stat(p_open)
    return p_open


class Sort_v1:
    def __init__(self):
        # Pandas
        #self.customer_open = CUSTOMER() #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']   
        self.order_open = ORDER() #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date'] 
        self.product_open = PRODUCT() #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']   
#        # Array
#        self.customer_arr = self.customer_open.to_numpy()
        self.order_arr = self.order_open.to_numpy()
        self.product_arr = self.product_open.to_numpy()
        self.sort_dict = {}


    def func_return(self, x, y):
        dict = {} 
        for i in range(x.shape[0]):
            try:
                dict[x[i,y]].append(i)
            except KeyError:
                dict[x[i,y]] = [i]
        return dict    

    # Cопутствующий продукт создать файл для обработки
    def related_products(self):
        product_dict = self.func_return(self.product_arr, 0) #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount'] 
        product_open = self.product_open.sort_values(['Items_Count']) # Сортировка
        vals_prod = self.product_open.drop_duplicates("Product_ID") # Убрать дубликаты
        vals_prod = vals_prod["Product_ID"] 
        print (len(vals_prod)) # Узнать кол во ID продуктов
        #----------------------->
        # Декодирование кодирование в словарь
        dict_to_coding = {}
        dict_to_encoding = {}
        for ix, ij in enumerate(vals_prod):
            dict_to_coding[ij] = ix 
            dict_to_encoding[ix] = ij
        
        #------------------------------------->
        # Обработка файлов
        start = time.time()
        new_dict = {}
        _product_dict = self.func_return(self.product_arr, 1)  #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount'] 
        for j in vals_prod[:]:
            #print (len(_product_dict[j])) # Кол во покупок с этим товаром
            Z = np.zeros((len(vals_prod)))
            for k in _product_dict[j]:
                _id_o = self.product_arr[k,0]    #получаю ИД oredr и продукта
                for u in product_dict[_id_o]:
                     ix_z = int(self.product_arr[u,1])
                     if int(j) != int(ix_z): 
                        ix_z = dict_to_coding[ix_z]
                        Z[ix_z] += self.product_arr[u,2]

            new_dict[j] = Z.tolist()
        print ("END", time.time()-start, len(new_dict))

        #---------------------------------------->
        # Сохраняю файл
        with open("out/related_products.json", 'w') as js_file:
            json.dump(new_dict, js_file)
        #---------------------------------------->
        with open("out/dict_to_encoding.json", 'w') as js_file:
            json.dump(dict_to_encoding, js_file)

    # Сортировка сопутствующего товара по месяцам
    # TO DO
    ###########
    def products_date(self):
            #dict_to_encoding = json.load(open("out/dict_to_encoding.json",'r'))
            product_dict = self.func_return(self.product_arr, 1) #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount'] 
            order_dict = self.func_return(self.order_arr, 0) #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date']
            temp_dict = {}
            for i in product_dict:
                M = {'01':0, '02':0, '03':0, '04':0, '05':0, '06':0, '07':0, '08':0, '09':0, '10':0, '11':0, '12':0}
                for v in product_dict[i]:
                    temp = self.product_arr[v,:].tolist()
                    ord_id = temp[0]
                    _date = self.order_arr[order_dict[ord_id],:].tolist()[0][-1].split(" ")[0].split("-")[1]
                    M[_date] += temp[3]
                    #print (i, v, _date, temp[3])
                temp_dict[i] = M
                #---------------------------->
                fig, ax = plt.subplots(figsize=(10,10), clear=True)
                ax.set_title(f'ID продукта - {i}')
                ax.set_xlabel('Месяц')
                ax.set_ylabel('Количество продуктов')
                ax.bar(list(M.keys()), list(M.values()), color = (0.2,0.7,0.6,0.6))

                ax.plot(list(M.keys()), list(M.values()))  
                fig.savefig(f"github/products/{i}.jpg")  # cat/cat2
                fig.clear(True)
                plt.close(fig)
            with open("out/products_date.json", 'w') as js_file:
                json.dump(temp_dict, js_file)                        
                
# Сортировка сопутствующего товара
def related_product_sort():
        dict_to_encoding = json.load(open("out/dict_to_encoding.json",'r'))
        _dict = {}
        with open("out/related_products.json","r") as json_file:
                data = json.load(json_file)
                for i in data:
                    P1 = sum(data[i])
                    t_d = {}
                    for ix, o in enumerate(data[i]):
                            try:
                                if o > 0:
                                    P = o / int(P1) * 100
                                    if P > 0.5:
                                        #t_d[ix] = o
                                        t_d[dict_to_encoding[str(ix)]] = o
                                        P1 = P1 - o
                            except:
                                   print (o, P1, i)   
                            
                    if P1 > 0:
                        t_d["остальные"] = P1
                        _dict[i] = t_d  
                        #diag_circle(list(t_d.values()), list(t_d.keys()) , None, i, f"github/related_products/{i}.jpg")
                    
        with open("out/sort_related_products.json",'w') as js_file:
                json.dump(_dict, js_file)

# Визуализация сопутствующего товара
def visual_related_product():
    F = open("out/sort_related_products.json", 'r')
    data = json.load(F)
    for i in data:
        diag_circle(list(data[i].values()), list(data[i].keys()) , None, i, f"github/related_products/{i}.jpg")
                 

def visual_related_m():
            data_related = json.load(open("out/sort_related_products.json", 'r'))
            date_sort_m = json.load(open("out/products_date.json",'r'))
            for i in data_related:
                fig, ax = plt.subplots(figsize=(10,10), clear=True)
                #print (i, date_sort_m[i])
                #print ("-------------")
                ax.set_title(f'ID продукта - {i}')
                ax.set_xlabel('Месяц')
                ax.set_ylabel('Количество продуктов')
                ax.bar(list(date_sort_m[i].keys()), list(date_sort_m[i].values()), color = (0.2,0.7,0.6,0.6))
                for o in data_related[i]:
                    if o != "остальные":
                        #print (o, date_sort_m[o]) 
                        #print ("----------")                                   
                        ax.plot(list(date_sort_m[o].keys()), list(date_sort_m[o].values()), label = f"{o}")  
                        ax.legend(loc='lower right')
                fig.savefig(f"github/related_products_m/{i}.jpg")  # cat/cat2
                fig.clear(True)
                plt.close(fig)

#def visual_related_m_cor():
#            data_related = json.load(open("out/sort_related_products.json", 'r'))
#            date_sort_m = json.load(open("out/products_date.json",'r'))
#            for i in data_related:
#                for o in data_related[i]:
#                    if o != "остальные":
#                        print (o, date_sort_m[o].keys(), date_sort_m[o].values()) 



if __name__ == "__main__":
    #NAME = PRODUCTNAME()
    #S = Sort_v1()
#----------------->
    # Сопутствующие продукты
    #S.related_products()
    #related_product_sort()
    #visual_related_product()
#----------------->
    # Сортировка сопутствующего товара по месяцам
    #S.products_date()
    #visual_related_m()
    
#------------------------------------------->
#    кореляция
#    visual_related_m_cor()
        
    """
    Буду использовать связанные продукты
    Мне нужен коэффициент который показывает как продукт влияют продукты из 
    Например кореляция цены на кол во покупок
    """
    product_open = PRODUCT() # ['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']
#35.73815846443176
#70.14598345756531
# Если не хотите использовать бд 
# Запускаю процесс в вечный цикл с файлом
# Записываю в текстовый документ номер процесса и запускаю
# Нужный скрип и читаю процесс, так исбавлюсь от постоянной загрузки файла
    
#    print (product_open.corr())
#    
#    pearson_coef, p_value = stats.pearsonr(product_open['Items_Count'], product_open['Total_Amount'])
#    print("Items_Count <-> Total_Amount",pearson_coef, p_value)
#    pearson_coef, p_value = stats.pearsonr(product_open['Items_Count'], product_open['TotalDiscount'])
#    print("Items_Count <-> TotalDiscount",pearson_coef, p_value)
#    G = product_open['Total_Amount']-product_open['TotalDiscount']
#    pearson_coef, p_value = stats.pearsonr(product_open['Items_Count'], G)
#    print("Items_Count <-> (Total_Amount-TotalDiscount)",pearson_coef, p_value) 
       
#    product_dict = self.func_return(self.product_arr, 1) #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount'] 
#    product_arr = product_open.to_numpy()
#    new_dict = {}
#    with open("out/sort_related_products.json","r") as json_file:
#        data = json.load(json_file)
#        for i in data:
#            print (i, data[i])
#       
     
#               Items_Count  Total_Amount  TotalDiscount
#Items_Count    1.000000      0.129837       0.066624
#Total_Amount   0.129837      1.000000       0.392744
#TotalDiscount  0.066624      0.392744       1.000000       
            
#https://habr.com/ru/company/datawiz/blog/264217/
#https://habr.com/ru/post/241967/
#https://habr.com/ru/post/240323/
#https://neurohive.io/ru/tutorial/primer-reshenija-realnoj-zadachi-po-mashinnomu-obucheniju-na-python/
#https://coderoad.ru/3949226/Вычисление-корреляции-Пирсона-и-значимости-в-Python
#http://chel-center.ru/python-yfc/2020/02/13/opisatelnaya-statistika-na-python-chast-2/
#https://habr.com/ru/post/206306/
#https://www.machinelearningmastery.ru/simple-and-multiple-linear-regression-with-python-c9ab422ec29c/
#https://overcoder.net/q/как-рассчитать-r-квадрат-используя-python-и-numpy
#https://proglib.io/p/linear-regression
#http://statistica.ru/theory/koeffitsient-determinatsii-i-lineynaya-regressiya/   
#https://pythonru.com/biblioteki/osnovnye-funkcii-pandas-pd-4 
#https://habr.com/ru/post/350500/
#https://habr.com/ru/post/329334/
#https://habr.com/ru/post/491622/
#https://habr.com/ru/company/billing/blog/334738/
# ТЕПЛОВАЯ КАРТА 
#https://towardsdatascience.com/histograms-and-density-plots-in-python-f6bda88f5ac0   
#https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html   
# ONE HOT ENCODING
# https://machinelearningmastery.com/how-to-one-hot-encode-sequence-data-in-python/
#https://stackoverflow.com/questions/33282368/plotting-a-2d-heatmap-with-matplotlib 
#https://pythonru.com/biblioteki/seaborn-plot
#Серелизация
#https://towardsdatascience.com/the-best-format-to-save-pandas-data-414dca023e0d
#https://stackoverflow.com/questions/17098654/how-to-store-a-dataframe-using-pandas
            
