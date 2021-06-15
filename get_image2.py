import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import json
from utils import func_return, diag_circle, see_stat, CUSTOMER, PRODUCT, ORDER, PRODUCTNAME

def ORDER():
#    o_open = pd.read_csv('B24_dbo_Crm_orders.csv', delimiter=',')
#    o_open.to_pickle("B24_dbo_Crm_orders.pk")

    o_open = pd.read_pickle("in/B24_dbo_Crm_product_in_order.pk")
    print (o_open.head())
    #see_stat(o_open)
#    o_open = o_open[['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date']]
#    o_open['price_before_discount'] = o_open['price_before_discount'].replace(np.nan, 0)
#    return o_open.sort_values(by=['Order_Date'])

if __name__ == "__main__":

    pn = PRODUCTNAME()
    
    print (pn.columns)
    pn = pn.to_numpy()
    a = func_return(pn, 2)
    print (len(a), pn.shape)
    for i in a:
        print (i)
#        for ii in a[i]:
#            print (o[ii,:])#(a[i], ii)
            
#def func_return(x, y):
#        dict = {} 
#        for i in range(x.shape[0]):
#            try:
#                dict[x[i,y]].append(i)
#            except KeyError:
#                dict[x[i,y]] = [i]
#        return dict  
