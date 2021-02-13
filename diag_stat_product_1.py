import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import json, os
import create_arr as TG

def ORDER():
    o_open = pd.read_csv('B24_dbo_Crm_orders.csv', delimiter=',')
    o_open = o_open[['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date']]
    o_open['Items_Count'] = o_open['Items_Count'].replace(np.nan, 0)
    return o_open

class DATA(object):
   def __init__(self):
       self.file = {}
       self.label = {}

   def parseIMG(self, dir_name):
       path = dir_name+"/"
       print ("PARSING",path)
       for r, d, f in os.walk(path):
           for ix, file in enumerate(f):
                      if ".txt" in file:
                          self.label[file.split(".")[0]] = [os.path.join(r, file)]
if __name__ == "__main__":
    """
    o_open = ORDER()  #['Order_Id', 'Customer_Id', ', 'price_before_discount', 'Amount_Charged', 'Order_Date']
    o_open = o_open.sort_values(by=['Order_Date']) #, inplace=True, ascending=False
    o_open = o_open.to_numpy()
#    cats = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun', 'Jul', 'Aug','Sep', 'Oct', 'Nov', 'Dec']
    
    p_open = TG.PRODUCT() #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']
    p_open = p_open.to_numpy()
#----------------------------->
    #Граф ORDER ID - DATE
    dicts = {}
    for i in range(o_open.shape[0]):
            t = o_open[i,:].tolist()
            o_id = int(t[0])
            cust_id = int(t[1])
            items_count = int(t[2])
            dt = t[-1]
            short_dt = dt.split(" ")[0].split("-")[1]
            dicts[o_id] = short_dt
            #print (dt.split(" ")[0], o_id, short_dt)
#2020-01-18 189368945 01
#['Order_Id', 'Customer_Id', ', 'price_before_discount', 'Amount_Charged', 'Order_Date']
#----------------------------->
    #Граф PRODUCT ID - {ORDER ID, DATE, COUNT}
    product_data = {}
    for i in range(p_open.shape[0]):
        t = p_open[i,:].tolist()
        o_id = int(t[0])
        p_id = int(t[1])
        i_count = int(t[2])
        try:
            product_data[p_id].append({"o_id":o_id, "o_date":dicts[o_id], "i_count":i_count})
        except KeyError:
            product_data[p_id] = [{"o_id":o_id, "o_date":dicts[o_id], "i_count":i_count}]
        #print (o_id, p_id, i_count)
# 188861758 7290105500151 1.0     
#['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount'] 
#----------------------------->
    for i in product_data:
        file_ = open(f"graph/{i}.txt","w")
        for p in product_data[i]:
            o_id = p["o_id"]
            o_date = p["o_date"]
            i_count = p["i_count"]
            file_.write(f"{o_id},{o_date},{i_count}\n")
        file_.close()
    """
#----------------------------->
# OPEN
#graph_image
    D = DATA()
    D.parseIMG("graph")
    for i in D.label:
        file_ = open(D.label[i][0],"r").readlines()
        print (D.label[i][0])
        dict_ = {}
        for g in file_:
            a = g.split("\n")[0].split(",")
            try:
                dict_[a[1]] += int(a[-1])
            except KeyError:
                dict_[a[1]] = int(a[-1])
        #list(dict_.keys()), list(dict_.values())
        plt.plot(list(dict_.keys()), list(dict_.values()))  
        plt.savefig(f"graph_image/{i}.jpg") 
        plt.cla()
#----------------------------->
#    plt.show()
