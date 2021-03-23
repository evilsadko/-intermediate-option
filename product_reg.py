import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import threading
import json
import time
from scipy import stats
from utils import diag_circle, see_stat


def CUSTOMER():
    c_open = pd.read_csv('in/B24_dbo_Crm_customers.csv', delimiter=',')
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
    
    p_open = pd.read_pickle("in/B24_dbo_Crm_product_in_order.pk")
    #see_stat(p_open)
    p_open = p_open[['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']] 
    print (time.time()-s)
    return p_open
    
def ORDER():
#    o_open = pd.read_csv('B24_dbo_Crm_orders.csv', delimiter=',')
#    o_open.to_pickle("B24_dbo_Crm_orders.pk")

    o_open = pd.read_pickle("in/B24_dbo_Crm_orders.pk")
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
                #M = {'01':0, '02':0, '03':0, '04':0, '05':0, '06':0, '07':0, '08':0, '09':0, '10':0, '11':0, '12':0}
                M = {'01':[0,0,0], '02':[0,0,0], '03':[0,0,0], '04':[0,0,0], '05':[0,0,0], '06':[0,0,0], '07':[0,0,0], '08':[0,0,0], '09':[0,0,0], '10':[0,0,0], '11':[0,0,0], '12':[0,0,0]}
                for v in product_dict[i]:
                    temp = self.product_arr[v,:].tolist()
                    ord_id = temp[0] 
                    _date = self.order_arr[order_dict[ord_id],:].tolist()[0][-1].split(" ")[0].split("-")[1]
                    M[_date][0] += temp[2] #'Items_Count'
                    M[_date][1] += temp[3] #'Total_Amount'
                    M[_date][2] += temp[4] #'TotalDiscount'
                    
                    #print (i, v, _date, temp[3])
                temp_dict[i] = M
                #---------------------------->
#                fig, ax = plt.subplots(figsize=(10,10), clear=True)
#                ax.set_title(f'ID продукта - {i}')
#                ax.set_xlabel('Месяц')
#                ax.set_ylabel('Количество продуктов')
#                ax.bar(list(M.keys()), list(M.values()), color = (0.2,0.7,0.6,0.6))

#                ax.plot(list(M.keys()), list(M.values()))  
#                fig.savefig(f"github/products/{i}.jpg")  # cat/cat2
#                fig.clear(True)
#                plt.close(fig)
            with open("out/products_date_v1.json", 'w') as js_file:
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

def heatmap_product():
    product_open = PRODUCT() # ['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']
    pearson_coef, p_value = stats.pearsonr(product_open['Items_Count'], product_open['Total_Amount'])
    print("Items_Count <-> Total_Amount",pearson_coef, p_value)
    pearson_coef, p_value = stats.pearsonr(product_open['Items_Count'], product_open['TotalDiscount'])
    print("Items_Count <-> TotalDiscount",pearson_coef, p_value)
    G = product_open['Total_Amount']-product_open['TotalDiscount']
    pearson_coef, p_value = stats.pearsonr(product_open['Items_Count'], G)
    print("Items_Count <-> (Total_Amount-TotalDiscount)",pearson_coef, p_value) 
    corr = product_open.corr()
    
    print (product_open.corr())
    print (corr.to_numpy().shape, corr.columns)
    fig, ax = plt.subplots()
    corr_a = corr.to_numpy()
    im = ax.imshow(corr_a)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(corr.columns)))
    ax.set_yticks(np.arange(len(corr.columns)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(corr.columns)
    ax.set_yticklabels(corr.columns)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(corr.columns)):
        for j in range(len(corr.columns)):
            text = ax.text(j, i, round(corr_a[i, j], 1), ha="center", va="center", color="w")

    ax.set_title("Зависемость полей")
    fig.tight_layout()
    #plt.show()
    fig.savefig(f"github/correlation/heatmap_product.jpg")

def heatmap_order():
    product_open = ORDER() # ['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date']
    corr = product_open.corr()
    G = product_open['Amount_Charged']-product_open['price_before_discount']
    pearson_coef, p_value = stats.pearsonr(product_open['Items_Count'], G)
    print("Items_Count <-> (Amount_Charged-price_before_discount)",pearson_coef, p_value)
    print (product_open.corr())
    print (corr.to_numpy().shape, corr.columns)
    fig, ax = plt.subplots()
    corr_a = corr.to_numpy()
    im = ax.imshow(corr_a)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(corr.columns)))
    ax.set_yticks(np.arange(len(corr.columns)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(corr.columns)
    ax.set_yticklabels(corr.columns)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(corr.columns)):
        for j in range(len(corr.columns)):
            text = ax.text(j, i, round(corr_a[i, j], 1), ha="center", va="center", color="w")

    ax.set_title("Зависемость полей")
    fig.tight_layout()
    #plt.show()
    fig.savefig(f"github/correlation/heatmap_order.jpg")


#def visual_related_m_cor():
#    date_year = json.load(open("out/products_date_v1.json","r"))
#    with open("out/sort_related_products.json","r") as json_file:
#        data = json.load(json_file)
#        
#        for i in data:
##            print (i, date_year[i])
#            T_data = []
#            ID_s = []
#            T = np.array(list(date_year[i].values()))
#            #print (T.shape)
#            I_C = T[:,2]
#            T_data.append(I_C)
#            ID_s.append(i)
#            #print (I_C)
#            #print (len(data[i]))
#            for o in data[i]:
#                
#                if o != "остальные":
##                    print (o, date_year[o])
#                    T1 = np.array(list(date_year[o].values()))
#                    I_C1 = T1[:,2]
#                    
#                    #pearson_coef, p_value = stats.pearsonr(I_C, I_C1)
#                    ID_s.append(o)
#                    T_data.append(I_C1)
#                    #print (pearson_coef, p_value)
#            T_data = np.array(T_data)
#            corr_a = np.corrcoef(T_data)
#            fig, ax = plt.subplots()
#            im = ax.imshow(corr_a)

#            # We want to show all ticks...
#            ax.set_xticks(np.arange(len(ID_s)))
#            ax.set_yticks(np.arange(len(ID_s)))
#            # ... and label them with the respective list entries
#            ax.set_xticklabels(ID_s)
#            ax.set_yticklabels(ID_s)

#            # Rotate the tick labels and set their alignment.
#            plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
#                     rotation_mode="anchor")

#            for edge, spine in ax.spines.items():
#                spine.set_visible(False)

#            ax.set_xticks(np.arange(T_data.shape[1]+1)-.5, minor=True)
#            ax.set_yticks(np.arange(T_data.shape[0]+1)-.5, minor=True)
#            ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
#            ax.tick_params(which="minor", bottom=False, left=False)

#            # Loop over data dimensions and create text annotations.
#            for z in range(len(ID_s)):
#                for j in range(len(ID_s)):
#                    text = ax.text(j, z, round(corr_a[z, j], 1), ha="center", va="center", color="w")

#            ax.set_title("Зависемость продуктов")
#            fig.tight_layout()
#            #plt.show()
#            fig.savefig(f"github/correlation/TotalDiscount/heatmap_{i}.jpg")     

def heatmap_vis(x, y, name):
    fig, ax = plt.subplots()
    im = ax.imshow(x)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(y)))
    ax.set_yticks(np.arange(len(y)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(ID_s)
    ax.set_yticklabels(ID_s)

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

def heatmap_prep():
    date_year = json.load(open("out/products_date_v1.json","r"))
    with open("out/sort_related_products.json","r") as json_file:
        data = json.load(json_file)
        for i in data:
            T_data0 = []
            T_data1 = []
            T_data2 = []
            ID_s = []
            T = np.array(list(date_year[i].values()))
            T_data0.append(T[:,0])
            T_data1.append(T[:,1])
            T_data2.append(T[:,2])
            ID_s.append(i)
            for o in data[i]:
                if o != "остальные":
                    T1 = np.array(list(date_year[o].values()))
                    #pearson_coef, p_value = stats.pearsonr(I_C, I_C1)
                    ID_s.append(o)
                    T_data0.append(T1[:,0])
                    T_data1.append(T1[:,1])
                    T_data2.append(T1[:,2])
            T_data0 = np.array(T_data0)
            T_data1 = np.array(T_data1)
            T_data2 = np.array(T_data2)
            
            corr_0 = np.corrcoef(T_data0)
            heatmap_vis(corr_0, ID_s, f"github/correlation/Items_Count/ic_heatmap_{i}.jpg")
            corr_1 = np.corrcoef(T_data1)
            heatmap_vis(corr_1, ID_s, f"github/correlation/Total_Amount/ta_heatmap_{i}.jpg")
            corr_2 = np.corrcoef(T_data2)
            heatmap_vis(corr_2, ID_s, f"github/correlation/TotalDiscount/td_heatmap_{i}.jpg")
            
            corr_a = (corr_0+corr_1+corr_2)/3
            heatmap_vis(corr_a, ID_s, f"github/correlation/test/a_heatmap_{i}.jpg")

def dynamic_price():
    date_year = json.load(open("out/products_date_v1.json","r"))
    with open("out/sort_related_products.json","r") as json_file:
        data = json.load(json_file)
        for i in data:
            #print (date_year[i])
            ds = {}
            for o in date_year[i]:
                #print (date_year[i][o])
                try:
                    ds[o] = date_year[i][o][1]/date_year[i][o][0]
                except ZeroDivisionError:
                    #print (date_year[i][o])
                    ds[o] = 0
#            print (ds)  
            fig, ax = plt.subplots(figsize=(10,10), clear=True)
            ax.set_title(f'ID продукта - {i}')
            ax.set_xlabel('Месяц')
            ax.set_ylabel('Количество продуктов')
            ax.bar(list(ds.keys()), list(ds.values()), color = (0.8,0.2,0.1,0.6))
            ax.plot(list(ds.keys()), list(ds.values()), label = f"{o}")  
            ax.legend(loc='lower right')
            fig.savefig(f"github/dynamic_price/{i}.jpg")  # cat/cat2
            fig.clear(True)
            plt.close(fig)


def test():
    date_year = json.load(open("out/products_date_v1.json","r"))
    with open("out/sort_related_products.json","r") as json_file:
        data = json.load(json_file)
        f_list = []
        f_list_count = []
        for i in data:
            #print (date_year[i])
            ds = {}
            DSS = {}
            for o in date_year[i]:
                #print (date_year[i][o])
                try:
                    ds[o] = date_year[i][o][1]/date_year[i][o][0]
                except ZeroDivisionError:
                    #print (date_year[i][o])
                    ds[o] = 0
            DSS[i] = ds   
            T1 = np.array(list(date_year[i].values()))[:,0]   
            for o in data[i]:
                if o != "остальные":
                    T2 = np.array(list(date_year[o].values()))[:,1] 
                    pearson_coef, p_value = stats.pearsonr(T1, T2)
                    if pearson_coef > 0.8:
                        ds = {}
                        for om in date_year[o]:
                            try:
                                ds[om] = date_year[o][om][1]/date_year[o][om][0]
                            except ZeroDivisionError:
                                ds[o] = 0
                        DSS[o] = ds    
            f_list.append(DSS)  
        relist = []
        for ix, p in enumerate(f_list):   
            if len(list(p.keys())) > 1:   
                 relist.append(p)   
        for ix, p in enumerate(relist):   
            print (len(list(p.keys())))
def test2():
    date_year = json.load(open("out/products_date_v1.json","r"))
    F_LS = [] 
    with open("out/sort_related_products.json","r") as json_file:
        data = json.load(json_file)
        LS = []
        LS2 = []
        for i in data:
            T = np.array(list(date_year[i].values()))
            price_once = T[:,1]/T[:,0]
            where_are_NaNs = np.isnan(price_once)
            price_once[where_are_NaNs] = 0
            LS.append([i, T[:,0], price_once])
            #print (price_once)
            t_ls = []
            for o in data[i]:
                if o != "остальные":
                    
                    T2 = np.array(list(date_year[o].values()))
                    pearson_coef, p_value = stats.pearsonr(T[:,0], T2[:,0])
                    if pearson_coef > 0.8:
                        price_once2 = T2[:,1]/T2[:,0]
                        where_are_NaNs2 = np.isnan(price_once2)
                        price_once2[where_are_NaNs2] = 0
                        t_ls.append([o, T2[:,0], price_once2])
            LS2.append(t_ls)
        print (len(LS), len(LS2)) 
        for i in range(len(LS)):
            #print (len(LS[i]), len(LS2[i]))
            if len(LS2[i]) > 0:
                F_LS.append([LS[i], LS2[i]])
#    for i in F_LS:
#        print (i)   
    _array = np.array(F_LS)
    print (_array.shape)   
    train_array = _array[:,0].tolist()
    print (train_array)

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
#    heatmap_product()
#    heatmap_order()
#    heatmap_prep()

    """
    Буду использовать связанные продукты
    Мне нужен коэффициент который показывает как продукт влияют продукты из 
    Например кореляция цены на кол во покупок
    """
    date_year = json.load(open("out/products_date_v1.json","r"))
    data = json.load(open("out/sort_related_products.json","r")) 
    f_list = []
    for i in data:
        T1 = np.array(list(date_year[i].values()))
        price_once1 = T1[:,1]/T1[:,0]
        where_are_NaNs1 = np.isnan(price_once1)
        if not True in where_are_NaNs1:
#            print (T1)
            L = []
            for o in data[i]:
                if o != "остальные":
                    T2 = np.array(list(date_year[o].values()))
                    price_once2 = T2[:,1]/T2[:,0]
                    where_are_NaNs2 = np.isnan(price_once2)
                    if not True in where_are_NaNs2:
#                        print (T2)
                        L.append([o, T2[:,0], price_once2])
            if len(L) > 0:
#                print (L)  
                f_list.append([[i, T1[:,0], price_once1], L])    
    f_list = np.array(f_list)   
    #print (f_list[0,0][2], f_list[0,1][0][2])    
    print (f_list.shape)   
    import tensorflow as tf
    import numpy
    import matplotlib.pyplot as plt
    rng = numpy.random

    # Parameters
    learning_rate = 0.01
    training_epochs = 1000
    display_step = 50


    # Training Data
    train_X = f_list[100,0][2]#numpy.asarray([3.3,4.4,5.5,6.71,6.93,4.168,9.779,6.182,7.59,2.167,7.042,10.791,5.313,7.997,5.654,9.27,3.1])
    train_Y = f_list[100,1][0][2]#numpy.asarray([1.7,2.76,2.09,3.19,1.694,1.573,3.366,2.596,2.53,1.221,2.827,3.465,1.65,2.904,2.42,2.94,1.3])

    print (train_X, train_Y)

    n_samples = train_X.shape[0]
    print (train_Y.shape, train_X.shape)

    # tf Graph Input
    X = tf.placeholder("float")
    Y = tf.placeholder("float")

    # Set model weights
    W = tf.Variable(rng.randn(), name="weight")
    b = tf.Variable(rng.randn(), name="bias")

    # Construct a linear model
    pred = tf.add(tf.multiply(X, W), b)


    # Mean squared error
    cost = tf.reduce_sum(tf.pow(pred-Y, 2))/(2*n_samples)
    # Gradient descent
    optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)


    # Initialize the variables (i.e. assign their default value)
    init = tf.global_variables_initializer()

    # Start training
    with tf.Session() as sess:
        sess.run(init)

        # Fit all training data
        for epoch in range(training_epochs):
            for (x, y) in zip(train_X, train_Y):
                sess.run(optimizer, feed_dict={X: x, Y: y})

            #Display logs per epoch step
            if (epoch+1) % display_step == 0:
                c = sess.run(cost, feed_dict={X: train_X, Y:train_Y})
                print ("Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(c), \
                    "W=", sess.run(W), "b=", sess.run(b))

        print ("Optimization Finished!")
        training_cost = sess.run(cost, feed_dict={X: train_X, Y: train_Y})
        print ("Training cost=", training_cost, "W=", sess.run(W), "b=", sess.run(b), '\n')
        print ('Прогнозирование') 
        y_pred_batch = sess.run(pred, {X: train_X})
        print (y_pred_batch)
        print (train_Y)
        #Graphic display
        plt.plot(train_X, train_Y, 'ro', label='Original data')
        plt.plot(train_X, sess.run(W) * train_X + sess.run(b), label='Fitted line')
        plt.legend()
        plt.show()
        
# correlation          
#                    M[_date][0] += temp[2] #'Items_Count'
#                    M[_date][1] += temp[3] #'Total_Amount'
#                    M[_date][2] += temp[4] #'TotalDiscount'    
#               Items_Count  Total_Amount  TotalDiscount
#Items_Count    1.000000      0.129837       0.066624
#Total_Amount   0.129837      1.000000       0.392744
#TotalDiscount  0.066624      0.392744       1.000000       

# Кол во товаров от колва цены
# кол во товаров от цены сопутствующего
# Кол вл ьлваолв от кол ва сопутствующего
#let IMG = document.querySelector("#rc-imageselector-target > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > div.rc-image-tile-wrapper > img")
#короляция товаров, что счем покупают, что приводит к увиличанию корзины.
#что лучше предлагать клиентам и/или клиенту персонально
#что лучше рекламировать - и почему.
