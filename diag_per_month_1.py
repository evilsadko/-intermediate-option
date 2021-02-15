import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import create_arr as TG


def ORDER():
    o_open = pd.read_csv('B24_dbo_Crm_orders.csv', delimiter=',')
    o_open = o_open[['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date']]
    o_open['Items_Count'] = o_open['Items_Count'].replace(np.nan, 0)
    return o_open


if __name__ == "__main__":
    o_open = ORDER()  #['Order_Id', 'Customer_Id', ', 'price_before_discount', 'Amount_Charged', 'Order_Date']
    o_open = o_open.sort_values(by=['Order_Date']) #, inplace=True, ascending=False
    o_open = o_open.to_numpy()
    #cats = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun', 'Jul', 'Aug','Sep', 'Oct', 'Nov', 'Dec']
    
    dicts = {}
    dicts2 = {}
    for i in range(o_open.shape[0]):
        t = o_open[i,:].tolist()
        o_id = t[0]
        cust_id = t[1]
        items_count = t[2]
        date = t[-1]
        s_mon = date.split(" ")[0].split("-")[1]
        s_day = date.split(" ")[0].split("-")[-1]
        try:
            dicts[f"{s_mon}/{s_day}"] += 1
        except KeyError:
            dicts[f"{s_mon}/{s_day}"] = 1       
        try:
            dicts2[f"{s_mon}/{s_day}"] += int(items_count)
        except KeyError:
            dicts2[f"{s_mon}/{s_day}"] = int(items_count) 
        #print (o_id, items_count, date.split(" ")[0].split("-")[1])#, IDX[0], len(IDX[0].tolist()))   
    #print (list(dicts.keys()), list(dicts.values()))
#----------------------------->
    plt.plot(list(dicts.keys()), list(dicts.values()))
    plt.plot(list(dicts2.keys()), list(dicts2.values()))
    #plt.show()
    plt.savefig("test_img.jpg") 
##---------------------->
#Start -дата присоеденения к клубу
#End - когда заканчивается членство в клубе
#Renew - дата обновления членство в клубе
#Clubid - вид клуба при котором 15 это клуб клиентов
#8 клуб компаний
#5 клуб сотрудников/работников сети
#10 старый клуб-неработает
#Consent - подтверждения рассылки
#Items_Count - количество товаров в сделке
