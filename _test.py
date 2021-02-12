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

def min_visual_product(_arr):
    x = range(0, _arr.shape[0])
    fig, ax = plt.subplots(1, figsize=(16, 6))# numerical x
    plt.bar(x[:], _arr[:,1], width = 0.3, color = '#1D2F6F')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)# x y details
    plt.ylabel('Count product')
    plt.xlabel('ID product')
    plt.xlim(-0.5, len(count))# grid lines
    plt.ylim(-0.5, max(count)/1000)
    ax.set_axisbelow(True)
    ax.yaxis.grid(color='gray', linestyle='dashed', alpha=0.2)# title and legend
    plt.title('Procudct Stat', loc ='left')
    plt.show()

if __name__ == "__main__":
    o_open = ORDER()  #['Order_Id', 'Customer_Id', ', 'price_before_discount', 'Amount_Charged', 'Order_Date']
    o_open = o_open.sort_values(by=['Order_Date']) #, inplace=True, ascending=False
    o_open = o_open.to_numpy()
    cats = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun', 'Jul', 'Aug','Sep', 'Oct', 'Nov', 'Dec']
    
    dicts = {}
    for i in range(o_open.shape[0]):
        t = o_open[i,:].tolist()
        o_id = t[0]
        cust_id = t[1]
        items_count = t[2]
        date = t[-1]
        #IDX = np.where(p_open[:,0] == o_id)
        try:
            dicts[date.split(" ")[0].split("-")[1]] += 1 #int(items_count)
        except KeyError:
            dicts[date.split(" ")[0].split("-")[1]] = 1 #int(items_count) 
        #print (dicts[date.split(" ")[0].split("-")[1]])      
        #print (o_id, items_count, date.split(" ")[0].split("-")[1])#, IDX[0], len(IDX[0].tolist()))   
    #print (list(dicts.keys()), list(dicts.values()))
#----------------------------->
    plt.plot(list(dicts.keys()), list(dicts.values()))
    plt.show()
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
