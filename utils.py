import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import time


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
    ax.set_title(f"ID: {title}", loc="left", pad=20)
    ax.legend(loc='lower right') #, bbox_to_anchor=(0.7, 0.7) 'upper left' bbox_to_anchor=(0.5, 0., 0.5, 0.5) 'best'
    fig.savefig(save_name)
    fig.clear(True)
    plt.close(fig)

def func_return(x, y):
        dict = {} 
        for i in range(x.shape[0]):
            try:
                dict[x[i,y]].append(i)
            except KeyError:
                dict[x[i,y]] = [i]
        return dict    
        
        
        
def func_date():
    o_open = ORDER()  #['Order_Id', 'Customer_Id', ', 'price_before_discount', 'Amount_Charged', 'Order_Date']
    o_open = o_open.sort_values(by=['Order_Date']) #, inplace=True, ascending=False
    o_open = o_open.to_numpy()
    p_open = PRODUCT() #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']
    p_open = p_open.to_numpy()
#----------------------------->
    #Граф ORDER ID - DATE
    dicts = {}
    print (o_open.shape[0], p_open.shape[0])
    for i in range(o_open.shape[0]):
            t = o_open[i,:].tolist()
            o_id = int(t[0]) 
            cust_id = int(t[1])
            items_count = int(t[2])
            date = t[-1]
            dicts[o_id] = date.split(" ")[0].split("-")[1] # Переношу месяц
#----------------------------->
    #Граф PRODUCT ID - {ORDER ID, DATE, COUNT}
    product_data = {}
    for i in range(p_open.shape[0]):
        o_id = int(p_open[i,0]) # ID order из продукта
        p_id = int(p_open[i,1]) # ID продукта из ордера
        i_count = int(p_open[i,2])
        try:
            product_data[p_id].append({"o_id":o_id, "o_date":dicts[o_id], "i_count":i_count})
        except KeyError:
            product_data[p_id] = [{"o_id":o_id, "o_date":dicts[o_id], "i_count":i_count}]
        #print (o_id, p_id, i_count, dicts[o_id])

######## SAVE TO FILE
    with open('prod.json', 'w') as js_file:
            json.dump(product_data, js_file)

######## CREATE VISUAL 
    for i in product_data:
        print ("VISUAL")
        temp = {}
        for k in product_data[i]:
            #print (k)
            try:
                temp[k["o_date"]] += k["i_count"]
            except KeyError:
                temp[k["o_date"]] = k["i_count"]

        plt.plot(list(temp.keys()), list(temp.values()))  
        plt.savefig(f"graph/{i}.jpg") 
        plt.cla()        
#-----------------------------------------------------------------_>
def convert_to_pk(name):
    c_open = pd.read_csv(name, delimiter=',')
    c_open.to_pickle(f"{name.split('.')[0]}.pk")


def CUSTOMER():
    c_open = pd.read_pickle("in/B24_dbo_Crm_customers.pk")
    c_open = c_open[['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']]
    c_open['join_club_success'] = c_open['join_club_success'].replace(np.nan, 2)
    c_open['Could_send_sms'] = c_open['Could_send_sms'].replace(np.nan, 0)
    c_open['Could_send_email'] = c_open['Could_send_email'].replace(np.nan, 0)
    c_open['consent'] = c_open['consent'].replace(np.nan, 0)
    c_open = c_open.apply(lambda x: pd.to_numeric(x, errors='coerce')).dropna() # Убираю все строки
#    see_stat(c_open)
    return c_open

def PRODUCT():
    p_open = pd.read_pickle("in/B24_dbo_Crm_product_in_order.pk")
    p_open = p_open[['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']] 
#    see_stat(c_open)
    return p_open
    
def ORDER():
    o_open = pd.read_pickle("in/B24_dbo_Crm_orders.pk")
    o_open = o_open[['Order_Id', 'Branch_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date']]
    o_open['price_before_discount'] = o_open['price_before_discount'].replace(np.nan, 0)
    o_open['Items_Count'] = o_open['Items_Count'].replace(np.nan, 0)
    return o_open.sort_values(by=['Order_Date'])

def PRODUCTNAME():
    p_open = pd.read_csv('in/B24_dbo_Products.csv', delimiter=',')
#    see_stat(p_open)
    return p_open
    
def NAME():
    c_open = pd.read_csv('in/names - names.csv', delimiter=',')
    c_open = c_open[['1', '243995', 'היי', 'Unnamed: 3', '0 - женщины\n1 - мужчины']]
    c_open['Unnamed: 3'] = c_open['Unnamed: 3'].replace(np.nan, 2)
    return c_open    
