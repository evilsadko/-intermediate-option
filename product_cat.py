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
    p_open = pd.read_csv('in/B24_dbo_Products.csv', delimiter=',')
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
                
    def diag_category_0(self):
        NAME = PRODUCTNAME() # [ ID, Product_Id, LocalName, Category1_Id, Category1_Name, Category2_Id, Category2_Name] 
        name_arr = NAME.to_numpy() 
        #CatID_1 = self.func_return(name_arr, 5) # cat2
        CatID_1 = self.func_return(name_arr, 3) # cat
        self.product_dict = self.func_return(self.product_arr, 1) #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']   
        #self.customer_dict = self.func_return(self.customer_arr, 0) #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']  
        self.order_dict = self.func_return(self.order_arr, 0) #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date'] 
        fig, ax = plt.subplots(figsize=(10,10)) 
        dict_save = {}
        for i in CatID_1 :
            #M = {'01':[0,0], '02':[0,0], '03':[0,0], '04':[0,0], '05':[0,0], '06':[0,0], '07':[0,0], '08':[0,0], '09':[0,0], '10':[0,0], '11':[0,0], '12':[0,0]}
            M = {'01':0, '02':0, '03':0, '04':0, '05':0, '06':0, '07':0, '08':0, '09':0, '10':0, '11':0, '12':0}
            for o in CatID_1[i]:
                id_p = name_arr[o,1]
                try:
                    for k in range(len(self.product_dict[id_p])):
                        id_p_arr = self.product_dict[id_p][k]
                        F = self.product_arr[id_p_arr,:].tolist() 
                        price = F[3]
                        ord_id = F[0]
                        ord_id = self.order_dict[ord_id]
                        _order = self.order_arr[ord_id,:].tolist()[0]
                        _date = _order[-1].split(" ")[0].split("-")[1]
                        M[str(_date)] += price
                        #print (_order, ord_id, price, _date)
                except KeyError:
                    pass
                    #print (id_p)
            #PLOT
            with open('category2.json', 'w') as js_file:
                json.dump(dict_save, js_file)
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

    ax.set_title("Зависемость категорий")
    fig.tight_layout()
    #plt.show()
    fig.savefig(name)    

def func_return(x, y):
    dict = {} 
    for i in range(x.shape[0]):
        try:
            dict[x[i,y]].append(i)
        except KeyError:
            dict[x[i,y]] = [i]
    return dict    

def hard_heatmap_category():
    date_year = json.load(open("out/category.json", "r"))
    category = PRODUCTNAME().to_numpy() # [ ID, Product_Id, LocalName, Category1_Id, Category1_Name, Category2_Id, Category2_Name] 
    id_from_cat = func_return(category, 1) 
    cat_dict = {}
    with open("out/sort_related_products.json","r") as json_file:
        data = json.load(json_file)
        for i in data:
            try:
                _id = id_from_cat[int(float(i))]
                cat = category[_id, 3][0]
                cat_dict[cat] = []
                for p in data[i]:
                    if p != "остальные":
                        _id_1 = id_from_cat[int(float(p))]
                        cat_1 = category[_id_1, 3][0]
                        cat_dict[cat].append(cat_1)
            except KeyError:
                pass
    for o in cat_dict:
        try:
            T = np.array(list(date_year[str(o)].values()))
            T_data = []
            ID_s = []
            T_data.append(T)
            ID_s.append(o)
            for p in cat_dict[o]:
                T1 = np.array(list(date_year[str(p)].values()))
                ID_s.append(p)
                T_data.append(T1)
            T_data = np.array(T_data)     
            corr = np.corrcoef(T_data)
            heatmap_vis(corr, ID_s, f"github/correlation/category/cat_heatmap_{o}.jpg")     
        except KeyError:
            pass   

if __name__ == "__main__":
    date_year = json.load(open("out/category.json", "r"))
    for i in date_year:
        #print (i, date_year[i])
        list_t = []
        ID_s = []
        T1 = np.array(list(date_year[i].values()))
        ID_s.append(i)
        list_t.append(T1)
        for u in date_year:
            if u != i:
                
               T2 = np.array(list(date_year[u].values()))
               pearson_coef, p_value = stats.pearsonr(T1, T2)
               if pearson_coef > 0.8:
                   list_t.append(T2) 
                   ID_s.append(u)
        T_data = np.array(list_t)
        corr = np.corrcoef(T_data)
        heatmap_vis(corr, ID_s, f"github/correlation/category/cat_heatmap_{i}.jpg")                
#            T_data0 = []
#            T_data1 = []
#            T_data2 = []
#            ID_s = []
#            T = np.array(list(date_year[i].values()))
#            T_data0.append(T[:,0])
#            T_data1.append(T[:,1])
#            T_data2.append(T[:,2])
#            ID_s.append(i)
#            for o in data[i]:
#                if o != "остальные":
#                    T1 = np.array(list(date_year[o].values()))
#                    #pearson_coef, p_value = stats.pearsonr(I_C, I_C1)
#                    ID_s.append(o)
#                    T_data0.append(T1[:,0])
#                    T_data1.append(T1[:,1])
#                    T_data2.append(T1[:,2])
#            T_data0 = np.array(T_data0)
#            T_data1 = np.array(T_data1)
#            T_data2 = np.array(T_data2)
#            
#            corr_0 = np.corrcoef(T_data0)
#            heatmap_vis(corr_0, ID_s, f"github/correlation/Items_Count/ic_heatmap_{i}.jpg")
#            corr_1 = np.corrcoef(T_data1)
#            heatmap_vis(corr_1, ID_s, f"github/correlation/Total_Amount/ta_heatmap_{i}.jpg")
#            corr_2 = np.corrcoef(T_data2)
#            heatmap_vis(corr_2, ID_s, f"github/correlation/TotalDiscount/td_heatmap_{i}.jpg")
#            
#            corr_a = (corr_0+corr_1+corr_2)/3
#            heatmap_vis(corr_a, ID_s, f"github/correlation/test/a_heatmap_{i}.jpg")
            
            

