import os
import glob
import pandas as pd
import numpy as np
os.chdir("Crm_product_in_order23")
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

def see_stat(x, y=0):
    if y == "list":
        print (x.columns.tolist())
    else:
        for c in  x.columns.tolist():
            print (f"###############\n{x[c].value_counts(dropna=False)}")


def PRODUCT(x):
    p_open = pd.read_csv(x, delimiter=',')
    #see_stat(p_open)
    return p_open

all_filenames = sorted(all_filenames)
print (all_filenames)

list_ = [] 
for f in all_filenames:
    H = PRODUCT(f)#.to_numpy()
    list_.append(H.values)
    
list_ = np.concatenate(list_)
column_values = ['#', 'Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']
index_values = range(list_.shape[0])
df = pd.DataFrame(data = list_,  
                  index = index_values,  
                  columns = column_values) 
df.to_csv('B24_dbo_Crm_product_in_order.csv')
print (len(df.values))
#print("==================================")

#PRODUCT("B24_dbo_Crm_product_in_order.csv")
