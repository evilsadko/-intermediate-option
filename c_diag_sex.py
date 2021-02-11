import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import json
import create_arr as TG

def NAME():
    c_open = pd.read_csv('names - names.csv', delimiter=',')
    c_open = c_open[['1', '243995', 'היי', 'Unnamed: 3', '0 - женщины\n1 - мужчины']]
    #c_open['היי'] = c_open['היי'].replace(np.nan, 2)
    c_open['Unnamed: 3'] = c_open['Unnamed: 3'].replace(np.nan, 2)
    #c_open['Could_send_email'] = c_open['Could_send_email'].replace(np.nan, 0)
    #c_open = c_open.apply(lambda x: pd.to_numeric(x, errors='coerce')).dropna() # Убираю все строки
    return c_open

def CUSTOMER():
    c_open = pd.read_csv('B24_dbo_Crm_customers.csv', delimiter=',')
    #TG.see_stat(c_open) 
    c_open = c_open[['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email', 'first_name_delivery']]
    c_open['join_club_success'] = c_open['join_club_success'].replace(np.nan, 2)
    c_open['Could_send_sms'] = c_open['Could_send_sms'].replace(np.nan, 0)
    c_open['Could_send_email'] = c_open['Could_send_email'].replace(np.nan, 0)
    c_open['consent'] = c_open['consent'].replace(np.nan, 0)
    #c_open = c_open.apply(lambda x: pd.to_numeric(x, errors='coerce')).dropna() # Убираю все строки
    return c_open

if __name__ == "__main__":
    N = NAME()
    #TG.see_stat(N) 
    L = N.to_numpy()
    dict_sex = {}
    for i in range(L.shape[0]):
        dict_sex[L[i,2]] = L[i,-2]
        #print (L[i,-2], L[i,1], L[i,2])
    c_open = CUSTOMER()
    arr_c = c_open.to_numpy() 
    men = 0 #1
    women = 0 #0
    ALL = 0
    with open('data_arr.txt') as json_file:
        data = json.load(json_file)
        ALL = len(list(data.keys()))
        for o in data:
            IDX = np.where(arr_c[:,0] == data[o][0]["P_USER"])
            try:
                if dict_sex[str(arr_c[IDX, -1][0][0])] == 1:
                     men += 1
                     print ("MEN",arr_c[IDX, -1][0][0], dict_sex[str(arr_c[IDX, -1][0][0])])
                if dict_sex[str(arr_c[IDX, -1][0][0])] == 0:
                     women += 1
                     print ("WOMEN",arr_c[IDX, -1][0][0], dict_sex[str(arr_c[IDX, -1][0][0])])
            except KeyError:
                pass
            except IndexError:
                pass
    vals = np.array([men / ALL * 100, women / ALL * 100, 100 - ((men / ALL * 100) + (women / ALL * 100))])
    labels = ["man", "female", "undefined"]
    myexplode = [0.05, 0.05, 0.05]
    fig, ax = plt.subplots()
    ax.pie(vals, explode=myexplode, labels=labels, autopct='%1.2f%%', startangle=90, pctdistance=0.85)

    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    ax.axis("equal")
    ax.legend(loc='upper left', bbox_to_anchor=(0.9, 0.9))
    plt.show()  

