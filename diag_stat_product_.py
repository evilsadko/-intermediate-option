import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import json
import create_arr as TG

def ORDER():
    o_open = pd.read_csv('B24_dbo_Crm_orders.csv', delimiter=',')
    o_open = o_open[['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date']]
    o_open['Items_Count'] = o_open['Items_Count'].replace(np.nan, 0)
    return o_open


if __name__ == "__main__":

#    p_open = TG.PRODUCT() #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']
#    product_dict = {}
#    p_arr = p_open.to_numpy()
#    vals_prod = np.unique(p_arr[:,1])
#    for ix, i in enumerate(vals_prod):
#        product_dict[i] = ix

    product_data = {}
    
    with open('data_arr.txt') as json_file:
        data = json.load(json_file)
        for o in data:
            for i in range(len(data[o])):
                try:
                    product_data[data[o][i]["P_ID"]].append(int(float(o)))
                except KeyError:
                    product_data[data[o][i]["P_ID"]] = [int(float(o))]

        print (len(list(product_data.keys())), len(list(product_data.values())))
        val_list = []
        #id_list = []
        Product_20 = 8215277
        
        for o in product_data:
            P = len(product_data[o])/ Product_20 * 100
            #max_list.append([o, product_data[o]])
            if P > 0.5:
                 val_list.append([product_data[o], o])
                 #id_list.append(str(o))
                 #print (o, product_data[o], P, len(product_data[o]))
        o_open = ORDER()  #['Order_Id', 'Customer_Id', ', 'price_before_discount', 'Amount_Charged', 'Order_Date']
        #TG.see_stat(o_open)
        o_open = o_open.sort_values(by=['Order_Date']) #, inplace=True, ascending=False
        o_open = o_open.to_numpy()
    ##    
        print (len(val_list), o_open.shape[0])
        dicts = {}
        for i in range(o_open.shape[0]):
            t = o_open[i,:].tolist()
            o_id = t[0]
            cust_id = t[1]
            items_count = t[2]
            dt = t[-1]
            short_dt = dt.split(" ")[0].split("-")[1]
            #print (dt.split(" ")[0], o_id, short_dt != "01", short_dt)
            dicts[o_id] = dt.split(" ")[0].split("-")[-1]
#            try:
#                print (dt.split(" ")[0], len(data[str(float(o_id))])) #str(float(o_id))
#            except KeyError:
#                pass
        print (len(list(dicts.keys())))                  
        fig, ax = plt.subplots()
        for p in range(len(val_list)):
            f_dict = {}
            for o in val_list[p][0]:
                 
                 #IDX = np.where(o_open[:,0] == int(o)) o_open[IDX].tolist()
                 #if dicts[o] != '01':
                 print (len(val_list[p]), o, dicts[o])
                 try:
                    f_dict[dicts[o]] += 1
                 except KeyError:
                    f_dict[dicts[o]] = 1
            ax.plot(list(f_dict.keys()), list(f_dict.values()), label = f"{val_list[p][1]}")   
        ax.legend()    
        plt.show()
    #        try:
    #            dicts[date.split(" ")[0].split("-")[1]] += 1 #int(items_count)
    #        except KeyError:
    #            dicts[date.split(" ")[0].split("-")[1]] = 1 #int(items_count) 
        #print (len(list(f_dict.keys())))
    #    plt.plot(list(f_dict.keys()), list(f_dict.values()))
    #    plt.show()
