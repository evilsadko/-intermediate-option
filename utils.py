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
    ax.set_title(f"ID продукта: {title}", loc="left", pad=20)
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
    #o_open = o_open[['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date']]
    o_open = o_open[['Order_Id', 'Branch_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date']]
    o_open['price_before_discount'] = o_open['price_before_discount'].replace(np.nan, 0)
    o_open['Items_Count'] = o_open['Items_Count'].replace(np.nan, 0)
    return o_open.sort_values(by=['Order_Date'])

def PRODUCTNAME():
    p_open = pd.read_csv('in/B24_dbo_Products.csv', delimiter=',')
#    see_stat(p_open)
    return p_open
    
def NAME():
    c_open = pd.read_csv('names - names.csv', delimiter=',')
    c_open = c_open[['1', '243995', 'היי', 'Unnamed: 3', '0 - женщины\n1 - мужчины']]
    c_open['Unnamed: 3'] = c_open['Unnamed: 3'].replace(np.nan, 2)
    return c_open    
    
