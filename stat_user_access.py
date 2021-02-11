import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import json
import create_arr as TG


if __name__ == "__main__":

    p_open = TG.PRODUCT() #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']
    #TG.see_stat(p_open)   

    product_dict = {}
    p_arr = p_open.to_numpy()
    vals_prod = np.unique(p_arr[:,1])
    for ix, i in enumerate(vals_prod):
        product_dict[i] = ix

#    o_open = TG.ORDER() #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged']  
#    #TG.see_stat(o_open)
    c_open = TG.CUSTOMER() #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']
    TG.see_stat(c_open)

    product_data = {}
    FULLACCESS = 0
    ALL = 0
    with open('data_arr.txt') as json_file:
        data = json.load(json_file)
        ALL = len(list(data.keys()))
        for o in data:
            if data[o][0]["CSE"] == data[o][0]["CSS"] == data[o][0]["JCS"] == 1:
                 FULLACCESS += 1

    print(ALL, FULLACCESS)
    vals = np.array([FULLACCESS / ALL * 100, 100 - (FULLACCESS / ALL * 100)])
    labels = ["full_access", "not access"]
    myexplode = [0.05, 0.05]
    fig, ax = plt.subplots()
    ax.pie(vals, explode=myexplode, labels=labels, autopct='%1.2f%%', startangle=90, pctdistance=0.85)

    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)


    ax.axis("equal")
    ax.legend(loc='upper left', bbox_to_anchor=(0.9, 0.9))
    plt.show()  

