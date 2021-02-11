import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import json
import create_arr as TG

    

if __name__ == "__main__":

    #c_open = TG.CUSTOMER() #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']
    #TG.see_stat(c_open)
    Customer_Id = 1446480 #100%
    Customer_Id_20 = 59843 
    P = Customer_Id_20 / Customer_Id * 100
    print (P, 100-P)

    vals = np.array([100-P, P])
    labels = ["Others customers", "Сustomers per year"]
    myexplode = [0, 0.2]
    fig, ax = plt.subplots()
    ax.pie(vals, explode=myexplode, labels=labels, autopct='%1.2f%%')
    ax.axis("equal")
    ax.legend(loc='upper left', bbox_to_anchor=(0.9, 0.9))
    plt.show()



