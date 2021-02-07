import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading


#def get_g(data, to_fig):
#    fig = plt.figure()
#    for ix in range(len(to_fig)):
#        ax = fig.add_subplot(len(to_fig)//2, len(to_fig)//2, ix+1)
#        ax.set_title(f'Т{ix}')
#        max_x = data[to_fig[ix][0]].max()
#        #min_x = data[to_fig[ix][0]].min()
#        max_y = data[to_fig[ix][1]].max()
#        #min_y = data[to_fig[ix][0]].max()
#        ax.set_xlim([0, max_x])
#        ax.set_ylim([0, max_y])
#        ax.set_xlabel(f'ось {to_fig[ix][0]}')
#        ax.set_ylabel(f'ось {to_fig[ix][1]}')   
#        ax.scatter(data[to_fig[ix][0]], data[to_fig[ix][1]], c = 'g', s = 14)
#    fig.set_figwidth(20)
#    fig.set_figheight(20)
#    plt.show()

#def similarity(vector1, vector2):
#    return np.dot(vector1, vector2.T) / np.dot(np.linalg.norm(vector1, axis=0, keepdims=True), np.linalg.norm(vector2.T, axis=0, keepdims=True))


def see_stat(x, y=0):
    if y == "list":
        print (x.columns.tolist())
    else:
        for c in  x.columns.tolist():
            print (f"###############\n{x[c].value_counts(dropna=False)}")


def CUSTOMER():
    f_open = pd.read_csv('B24_dbo_Crm_customers.csv', delimiter=',')
    f_open = f_open[['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']]
    f_open['join_club_success'] = f_open['join_club_success'].replace(np.nan, 2)
    f_open['Could_send_sms'] = f_open['Could_send_sms'].replace(np.nan, 0)
    f_open['Could_send_email'] = f_open['Could_send_email'].replace(np.nan, 0)
    f_open['consent'] = f_open['consent'].replace(np.nan, 0)
    return f_open


def PRODUCT():
    p_open = pd.read_csv('B24_dbo_Crm_product_in_order.csv', delimiter=',')
    p_open = p_open[['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']] 
#    vals, inverse, count = np.unique(arr_v[:,1], return_inverse=True, return_counts=True)
#    class_product = open("_class_product.txt", "w")
#    for i in range(len(count)):
#        print (vals[i], inverse[i], count[i])
#        class_product.write(f"{str(vals[i])},{str(count[i])}\n")
#    class_product.close()
    return p_open
    
def ORDER():
    o_open = pd.read_csv('B24_dbo_Crm_orders.csv', delimiter=',')
    o_open = o_open[['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged']]
    return o_open

def min_visual_product(_arr):
    x = range(0, _arr.shape[0])
#    #print (np.array(_arr).shape, f"ID product: {_arr[-1][0]} - count: {_arr[-1][1]}")
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
    
#Total Amount - итого
#Total Discount - Общая скидка
#    PRODUCT II
#    see_stat(p_open)
#    see_stat(p_open, "list")

    p_open = PRODUCT()
    p_arr = p_open.to_numpy()
    print (p_arr.shape)
    #print (p_open['Items_Count'].value_counts())
    vals, inverse, count = np.unique(p_arr[:,1], return_inverse=True, return_counts=True)
    print ("PRODUCT CLASS: ",len(count), max(count), min(count))
    _arr = []
    for ix, ixp in enumerate(count):
         #print (vals[ix],ixp)
         _arr.append([vals[ix],int(ixp)])
    _arr = np.array(_arr)
    _arr = _arr[_arr[:,1].argsort()]  
#---------------------->
    min_visual_product(_arr)
#---------------------->


#    ax.bar(x[:1000], _arr[:1000,1])
#    plt.title('P-stat\n', loc='left')
#    plt.ylabel('Procudct count')
#    plt.ylim(0, max(count))
#    plt.xlabel('Procudct ID')
#    plt.xlim(0, len(count))
#    #ax.set_axisbelow(True)
#    ax.xaxis.grid(color='gray', linestyle='dashed')
#    ax.autoscale(tight=True)
#    plt.show()
#    https://devpractice.ru/matplotlib-lesson-4-3-bar-pie/


