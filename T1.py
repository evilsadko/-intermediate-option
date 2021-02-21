import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import threading
import json
import time

def see_stat(x, y=0):
    if y == "list":
        print (x.columns.tolist())
    else:
        for c in  x.columns.tolist():
            print (f"###############\n{x[c].value_counts(dropna=False)}")


def diag_circle(vals, labels, myexplode, title, save_name, types=None):
    fig, ax = plt.subplots(figsize=(10,10))
    if myexplode != None:
        ax.pie(vals, explode=myexplode, labels=labels, autopct='%1.2f%%', startangle=90, pctdistance=0.85)
    else:
        ax.pie(vals, labels=labels, autopct='%1.2f%%', startangle=90, pctdistance=0.85)
    if types != None:
        centre_circle = plt.Circle((0,0),0.70,fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)

    ax.axis("equal")
    ax.set_title(title, pad=20)
    ax.legend(loc='best') #, bbox_to_anchor=(0.7, 0.7) 'upper left' bbox_to_anchor=(0.5, 0., 0.5, 0.5)
    plt.savefig(save_name)
    plt.cla()

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
    p_open = pd.read_csv('B24_dbo_Crm_product_in_order.csv', delimiter=',')
    p_open = p_open[['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']] 
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
        self.customer_open = CUSTOMER() #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']   
        self.order_open = ORDER() #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date'] 
        self.product_open = PRODUCT() #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']   
#        # Array
#        self.customer_arr = self.customer_open.to_numpy()
        self.order_arr = self.order_open.to_numpy()
        self.product_arr = self.product_open.to_numpy()
#        # Dict Graph
#        self.customer_dict = self.func_return(self.customer_arr, 0)
        self.order_dict = self.func_return(self.order_arr, 0)
        self.product_dict = self.func_return(self.product_arr, 0)

        self.sort_dict = {}

    def func_unite(self, see=None):
        key_error = 0
        not_errot = 0
        # Прохожу циклом по покупкам ордер
        for i in range(self.order_arr.shape[0]):
            try:
                # Из получаю продукты исходя из покупки ордер
                gen_ls = [self.get_from_index(p) for p in self.product_dict[self.order_arr[i,0]]] #arr_p[arr_o[i,0]]

                # Получаю  индекс покупателя в массиве
                ID_customer = self.customer_dict[self.order_arr[i,1]][0]

                # По индексу получаю информацию о покупателе
                ID_customer = self.customer_arr[ID_customer,:].tolist()
                if see != None:
                    print ("Product in order", len(gen_ls))
                    print ("Customer ID", ID_customer, int(ID_customer[0]), self.order_arr[i,1])

                # Создаю словарь где ключ ID покупки ордера

                #sort_dict[arr_o[i,0]] = [[gen_ls, ID_customer]] # Новая
                T = self.func_repack(gen_ls)
                T.append({"DATE_ORDER":self.order_arr[i,-1], "Items_Count":self.order_arr[i,2], "price_before_discount":self.order_arr[i,3], 
                          "Amount_Charged": self.order_arr[i,4], "CONSENT":ID_customer[1],
                          "USER": ID_customer[0], "JCS":ID_customer[2], "CSS":ID_customer[3], "CSE":ID_customer[4],})
                self.sort_dict[self.order_arr[i,0]] = T
                not_errot += 1
            except KeyError:
                key_error += 1
        print (len(self.sort_dict), key_error, not_errot)

    def func_repack(self, x):
        list = []
        for i in x:
            list.append({"P_ID":i[1], "P_COUNT":i[2], "Total_Amount":i[3],"TotalDiscount":i[4]})
        return list

    def func_return(self, x, y):
        dict = {} 
        for i in range(x.shape[0]):
            try:
                dict[x[i,y]].append(i)
            except KeyError:
                dict[x[i,y]] = [i]
        return dict    

    def get_from_index(self, x):
        return self.product_arr[x,:].tolist()
    
    def save_data(self, x):
        with open(x, 'w') as js_file:
            json.dump(self.sort_dict, js_file)

    def open_data(self, x):
        with open(x) as json_file:
            data = json.load(json_file)
            return data
            #for ix, o in enumerate(list(data.keys())[:]):
                #print (data[o], ix, o)
                
        print ("DONE")



## Сопутствующие товары
#    def diag_product_3(self):
## найти самые популярные товары
#        self.product_dict = self.func_return(self.product_arr, 0) #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount'] 
#        self.product_open = self.product_open.sort_values(['Items_Count'])
#        #see_stat(self.product_open)
#        # Узнать кол во ID продуктов
#        vals_prod = self.product_open.drop_duplicates("Product_ID")
#        vals_prod = vals_prod["Product_ID"]
#        #----------------------->
#        # Декодирование кодирование в словарь
#        dict_to_coding = {}
#        dict_to_encoding = {}
#        new_dict = {}
#        
#        for ix, ij in enumerate(vals_prod):
#            #print (ix, ij)
#            dict_to_coding[ij] = ix 
#            dict_to_encoding[ix] = ij
#            new_dict[ij] = 0
#        #------------------------->
#        arr = self.product_open.to_numpy()
#        
#        for p in range(1000): #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']  arr.shape[0]#arr.shape[0]
#            ord_id = arr[p,0] # Получаю ордер
#            pr_id = arr[p,1] # ID продукта
#            #_order = self.order_dict[ord_id] 
#            #_order = self.order_arr[_order,:].tolist() #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date'] 
#            Z = np.zeros((len(vals_prod)))
#            PR = self.product_dict[ord_id] #Товары в оредре
#            #print (PR, ord_id)
#            for k in PR:
#                if arr[k,1] != pr_id:
#                    #print (arr[k,1])
#                    #print (dict_to_coding[int(arr[k,1])])
#                    Z[dict_to_coding[int(arr[k,1])]] += 1
#                    #print (new_dict[pr_id][dict_to_coding[int(arr[k,1])]])
#                    #print ("-----------------------------------------")
#            new_dict[pr_id] = Z
#        print (len(new_dict)) 
#        for ic in new_dict:
#            t_d = {}
#            for iq, q in enumerate(new_dict[ic]):
#                 if q > 0:
#                    t_d[dict_to_encoding[iq]] = q
#                    #print (q, dict_to_encoding[iq])
#            print (len(t_d))

#            diag_circle(list(t_d.values()), list(t_d.keys()), None, ic, f"github/related_products/{ic}.jpg")

#            #plt.plot(list(t_d.keys()), list(t_d.values()))  
#            #plt.savefig(f"github/related_products/{i}.jpg") 
#            #plt.cla()
##       print (_order, ord_id, len(PR), pr_id)

    def diag_product_3(self):
# найти самые популярные товары
        self.product_dict = self.func_return(self.product_arr, 0) #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount'] 
        self.product_open = self.product_open.sort_values(['Items_Count'])
        #see_stat(self.product_open)
        # Узнать кол во ID продуктов
        vals_prod = self.product_open.drop_duplicates("Product_ID")
        vals_prod = vals_prod["Product_ID"]
        #----------------------->
        # Декодирование кодирование в словарь
        dict_to_coding = {}
        dict_to_encoding = {}
        new_dict = {}
        
        for ix, ij in enumerate(vals_prod):
            #print (ix, ij)
            dict_to_coding[ij] = ix 
            dict_to_encoding[ix] = ij
            new_dict[ij] = 0
        #------------------------->
        _product_dict = self.func_return(self.product_arr, 1) 
        arr = self.product_open.to_numpy()
        for j in vals_prod[:]:
            #print (len(_product_dict[j])) # Кол во покупок с этим товаром
            Z = np.zeros((len(vals_prod)))
            for k in _product_dict[j]:
                _id_o = arr[k,0]    #получаю ИД oredr и продукта
                #_order = self.order_arr[self.order_dict[_id_o],:].tolist()
                #self.product_dict[_id_o]
                #print (arr[k,:].tolist(), len(self.product_dict[_id_o]))
                for u in self.product_dict[_id_o]:
                     ix_z = int(arr[u,1])
                     if int(j) != int(ix_z): 
                        #print (arr[u,:].tolist()) 
                        
                        ix_z = dict_to_coding[ix_z]
                        Z[ix_z] += arr[u,2]
                        #
            new_dict[j] = Z
        for s in new_dict:
            t_d = {}
            try:
                for ix, m in enumerate(new_dict[s]):
                    if m > 1000:
                        #print (s, m, dict_to_encoding[ix])
                        t_d[dict_to_encoding[ix]] = m
                print (len(t_d))
                if len(t_d) > 1:
                    for N in t_d:
                        print (t_d[N], N)

                    #diag_circle(list(t_d.keys()), list(t_d.keys()), None, s, f"github/related_products/{s}.jpg")
            except TypeError:
                print (new_dict[s])
if __name__ == "__main__":
    #NAME = PRODUCTNAME()
    S = Sort_v1()
#----------------->
    S.diag_product_3()

#                try:
#                    idx_cust = self.customer_dict[i][0]  # idx в списке покупателя
#                    _customet = self.customer_arr[idx_cust,:].tolist() # Информация о покупателе
#                    order_list = self.order_dict[i] # 
#                    for h in order_list:
#                        _order = self.order_arr[h,:].tolist()
#                        _date = _order[-1].split(" ")[0].split("-")[1]
#                        M[str(_date)] += int(_order[3])
#                    #ax.bar(list(M.keys()), list(M.values()), label = f"{_customet[0]}") 
#                    ax.plot(list(M.keys()), list(M.values()), label = f"{_customet[0]}") 
#                    ax.legend()
#                except KeyError:
#                    pass
#35372 72994146
#35373 4033100098543
#35374 7290101958802
#35375 6186300

