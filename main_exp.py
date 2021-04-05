import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import json
import time
from utils import func_return, diag_circle, see_stat, CUSTOMER, PRODUCT, ORDER, PRODUCTNAME



def chunks(lst, count):
    start = 0
    for i in range(count):
          stop = start + len(lst[i::count])
          yield lst[start:stop]
          start = stop     

class Sort_v1:
    def __init__(self):
        # Pandas
        self.product_open = PRODUCT() #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']   
#        # Array
        self.product_arr = self.product_open.to_numpy()
#        # Dict Graph
        self.product_dict = func_return(self.product_arr, 0)
# САМЫЕ ПОПУЛЯРНЫЕ КАТЕГОРИИ
    def diag_product_2(self):
#------------------------------------------->
# Получить сумму всех продаж
        S = self.product_open['Total_Amount'].sum()
        self.product_dict = func_return(self.product_arr, 1) #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount'] 
        print ("Общая продажа", S)
        
#------------------------------------------->
# Разделить продукты на категории
        # Категории
        NAME = PRODUCTNAME() # [ ID, Product_Id, LocalName, Category1_Id, Category1_Name, Category2_Id, Category2_Name] 
        name_arr = NAME.to_numpy() 

## Разложить продукты по категориям        
        #CatID_1 = func_return(name_arr, 3)  # Категория 1
        CatID_1 = func_return(name_arr, 5) # Категория 2 

        #Test_arr = [] #Можно использовать промежуточный список
        for i in CatID_1 :
            #print (len(CatID_1[i]))
            T_price = 0
            for o in CatID_1[i]:
                id_p = name_arr[o,1]
                try:
                    for id_p_arr in self.product_dict[id_p]:
                        F = self.product_arr[id_p_arr,:].tolist() 
                        T_price += F[-2]  
                except KeyError:
                    pass
            S -= T_price
            CatID_1[i] = T_price
            #Test_arr.append((i, T_price)) #промежуточный список
        sorted_tuples = sorted(CatID_1.items(), key=lambda item: item[1]) # Сортировка
        self.min_visual_product(np.array(sorted_tuples)) # <- Test_arr
#--------------------------->
        ty = chunks(list(sorted_tuples),9) # Разрезаю на части
        self.get_g(list(ty))
            
#---------------------------->
        L = []
        V = []
        M = []
        for i in CatID_1:
            #print (CatID_1[i], i)
            if CatID_1[i] > 0:
                L.append(i)
                V.append(CatID_1[i])
                M.append(0)
        # Добавить остаток
        L.append("Other")
        V.append(S)
        M.append(0.2)

        diag_circle(V[:], L[:], M[:],  "Популярные категории", "github/categories/popular_categories.jpg")
        #print(sorted_dict)  # {1: 1, 3: 4, 2: 9}
#------------------------------------------------
#        CatID_2 = func_return(name_arr, 5)
#        LEN_2 = 0    
#        for i in CatID_2:
#            #print (len(CatID_2[i]))
#            LEN_2 += len(CatID_2[i] )
#        print (len(CatID_1), LEN_1, len(CatID_2), LEN_2)  

    def get_g(self, data):
        fig, ax = plt.subplots(len(data), figsize=(20, 20))        
        for ix in range(len(data)):
            A = np.array(data[ix])
            ax = fig.add_subplot(len(data)//3, len(data)//3, ix+1)
            max_y = np.amax(A[:,1])
            min_y = np.amin(A[:,1])
            ax.set_ylim([min_y, max_y])
            ax.bar(A[:,0], A[:,1], width = 0.3)  #color = '#1D2F6F'
        #fig.set_figwidth(20)
        #fig.set_figheight(20)
        plt.savefig("github/categories/TEST.jpg") 


    def min_visual_product(self, _arr):
        x = range(0, _arr.shape[0])
        fig, ax = plt.subplots(1, figsize=(16, 6))# numerical x
        plt.bar(x[:], _arr[:,1], width = 0.3)  #color = '#1D2F6F'
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)# x y details
        plt.ylabel('Продажи')
        plt.xlabel('Категории')
        #ax.set_xticklabels(_arr[:,0])
#        plt.xlim(-0.5, len(count))# grid lines
#        plt.ylim(-0.5, max(count)/1000)
        ax.set_axisbelow(True)
        ax.yaxis.grid(color='gray', linestyle='dashed', alpha=0.2)# title and legend
        plt.title('Cтатистика продаж категорий', loc ='left', pad=20)
        plt.savefig("github/categories/sort_stat_group.jpg")



if __name__ == "__main__":
    S = Sort_v1()
#----------------->
    S.diag_product_2()
#




