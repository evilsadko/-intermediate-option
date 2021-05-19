import threading
from utils import *
from dbhandler_2 import *



## Cопутствующий продукт создать файл для обработки
#def related_products(self):
#    product_dict = self.func_return(self.product_arr, 0) #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount'] 
#    product_open = self.product_open.sort_values(['Items_Count']) # Сортировка
#    vals_prod = self.product_open.drop_duplicates("Product_ID") # Убрать дубликаты
#    vals_prod = vals_prod["Product_ID"] 
#    print (len(vals_prod)) # Узнать кол во ID продуктов
#    #----------------------->
#    # Декодирование кодирование в словарь
#    dict_to_coding = {}
#    dict_to_encoding = {}
#    for ix, ij in enumerate(vals_prod):
#        dict_to_coding[ij] = ix 
#        dict_to_encoding[ix] = ij
#    
#    #------------------------------------->
#    # Обработка файлов
#    start = time.time()
#    new_dict = {}
#    _product_dict = self.func_return(self.product_arr, 1)  #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount'] 
#    for j in vals_prod[:]:
#        #print (len(_product_dict[j])) # Кол во покупок с этим товаром
#        Z = np.zeros((len(vals_prod)))
#        for k in _product_dict[j]:
#            _id_o = self.product_arr[k,0]    #получаю ИД oredr и продукта
#            for u in product_dict[_id_o]:
#                 ix_z = int(self.product_arr[u,1])
#                 if int(j) != int(ix_z): 
#                    ix_z = dict_to_coding[ix_z]
#                    Z[ix_z] += self.product_arr[u,2]

#        new_dict[j] = Z.tolist()
#    print ("END", time.time()-start, len(new_dict))

#    #---------------------------------------->
#    # Сохраняю файл
#    with open("out/related_products.json", 'w') as js_file:
#        json.dump(new_dict, js_file)
#    #---------------------------------------->
#    with open("out/dict_to_encoding.json", 'w') as js_file:
#        json.dump(dict_to_encoding, js_file)

## Сортировка сопутствующего товара по месяцам
## TO DO
############
#def products_date(self):
#        product_dict = self.func_return(self.product_arr, 1) #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount'] 
#        order_dict = self.func_return(self.order_arr, 0) #['Order_Id', 'Branch_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date']
#        temp_dict = {}
#        for i in product_dict:
#            M = {'01':[0,0,0], '02':[0,0,0], '03':[0,0,0], '04':[0,0,0], '05':[0,0,0], '06':[0,0,0], '07':[0,0,0], '08':[0,0,0], '09':[0,0,0], '10':[0,0,0], '11':[0,0,0], '12':[0,0,0]}
#            for v in product_dict[i]:
#                temp = self.product_arr[v,:].tolist()
#                ord_id = temp[0] 
#                _date = self.order_arr[order_dict[ord_id],:].tolist()[0][-1].split(" ")[0].split("-")[1]
#                M[_date][0] += temp[2] #'Items_Count'
#                M[_date][1] += temp[3] #'Total_Amount'
#                M[_date][2] += temp[4] #'TotalDiscount'
#            temp_dict[i] = M
#            #---------------------------->
#        with open("out/products_date_v1.json", 'w') as js_file:
#            json.dump(temp_dict, js_file)    


#def heatmap_prep():
#    date_year = json.load(open("out/products_date_v1.json","r"))
#    with open("out/sort_related_products.json","r") as json_file:
#        data = json.load(json_file)
#        d_ict = {}
#        for i in data:
#            T_data0 = []
#            ID_s = []
#            T = np.array(list(date_year[i].values()))
#            T_data0.append(T[:,0])
#            ID_s.append(i)
#            for o in data[i]:
#                if o != "остальные":
#                    T1 = np.array(list(date_year[o].values()))
#                    #pearson_coef, p_value = stats.pearsonr(I_C, I_C1)
#                    ID_s.append(o)
#                    T_data0.append(T1[:,0])
#                    
#            T_data0 = np.array(T_data0)
#            corr_0 = np.corrcoef(T_data0)
#            d_ict[f"corr_{i}"] = [ID_s, corr_0.tolist()]
#            #heatmap_vis(corr_0, ID_s, f"github/correlation/Items_Count/ic_heatmap_{i}.jpg")
#        with open("out/correlation_products.json",'w') as js_file:
#                json.dump(d_ict, js_file)

# Cопутствующий продукт
"""
Получить ИД продуктов
Словарь
Для И во всех ИД продуктов:
    получить Список покупок c И
    Для ИИ в Списке покупок:
        Если ИД продукта не равно И:
            Словарь[]

Нужно сгруппировать а затем 

"""





if __name__ == "__main__":
    D = DataBase()
    #D.get_all_data("my_table") 
    #D.show_tables()
    #D.info_1()
    #D.info_2()
    
    #Количество ID классов
#    _temp = D.client.execute("""
#    SELECT DISTINCT Product_ID
#    FROM my_table
#    """)

#    _temp = D.client.execute("""
#        SELECT SUM(Total_Amount) FROM my_table group by Product_ID
#    """)   
        
#    _temp = D.client.execute("""
#        SELECT
#          DISTINCT my_table.Product_ID as IDS
#        FROM my_table 
#    """)
#----------------------------------------->

     #Количество покупок
#    _temp = D.client.execute("""
#        SELECT  DISTINCT Order_ID AS Product_num FROM my_table GROUP BY Order_ID
#    """)  
#      
#    _temp = D.client.execute("""
#        SELECT Product_ID as IDS FROM my_table WHERE Order_ID IN (SELECT Order_ID AS Product_num FROM my_table GROUP BY Order_ID)
#    """)    


#---------------------------------->

#    _temp = D.client.execute("""
#        SELECT Product_ID, Order_ID FROM my_table GROUP BY Product_ID, Order_ID;
#    """)    

#-------------------------------------->
#    SLOW
#    _temp = D.client.execute("""
#        SELECT DISTINCT Product_ID FROM my_table
#    """)        
#    Str = f""
#    
#    for i in _temp:
#        ZS = D.client.execute(f"""   
#                                        SELECT
#                                          my_table.Order_ID
#                                        FROM my_table
#                                        WHERE my_table.Product_ID = {i[0]}
#                                    """)
#        print (i[0], len(ZS))
#Category1_Id Category2_Id 
#    _temp = D.client.execute("""
#        SELECT DISTINCT Category1_Id FROM my_table
#    """) 
    
    
    _temp = D.client.execute("""
        SELECT DISTINCT Customer_Id FROM my_table
    """)      

    # Count category
#    def func_return(x, y):
#        dict = {} 
#        for i in range(x.shape[0]):
#            try:
#                dict[x[i,y]].append(i)
#            except KeyError:
#                dict[x[i,y]] = [i]
#        return dict     
             
    Str = f""
    print (len(_temp))
    for i in _temp:
    # WORK !!!
#        ZS = D.client.execute(f"""   
#                                        SELECT
#                                          SUM(Items_Count) as sum1, 
#                                          SUM(Total_Amount) as sum2,
#                                          Category1_Id
#                                        FROM my_table
#                                        WHERE my_table.Customer_Id = {i[0]} GROUP BY Category1_Id
#                                        ORDER BY sum2
#                                    """)
                                    
#        ZS = D.client.execute(f"""   
#                                        SELECT
#                                          SUM(Items_Count) as sum1, 
#                                          SUM(Total_Amount) as sum2,
#                                          Category1_Id
#                                        FROM my_table
#                                        WHERE my_table.Customer_Id = {i[0]} 
#                                        AND my_table.Category1_Id = 402 
#                                        GROUP BY Category1_Id
#                                    """)                                    




        ZS = D.client.execute(f"""   
                                        SELECT
                                          SUM(Items_Count) as sum1, 
                                          SUM(Total_Amount) as sum2,
                                          Order_Date
                                        FROM test
                                        WHERE test.Customer_Id = {i[0]} 
                                        AND test.Category1_Id = 402
                                        GROUP BY Order_Date
                                    """)   
                                    #  
#        ZS1 = D.client.execute(f"""   
#                                        SELECT
#                                          SUM(Items_Count) as sum1, 
#                                          SUM(Total_Amount) as sum2,
#                                          Order_Date
#                                        FROM my_table
#                                        WHERE my_table.Customer_Id = {i[0]} 
#                                        AND my_table.Category1_Id = 402
#                                        GROUP BY Order_Date
#                                    """) 
#        ZS = np.array(ZS) 
#        A = func_return(ZS, -1) 
#        for o in range(ZS.shape[0]):
#            print (ZS[o,2:5], ZS[o,2:5]) 
        #temp_dict = {}
        M = {'01':[0,0,0], '02':[0,0,0], '03':[0,0,0], '04':[0,0,0], '05':[0,0,0], '06':[0,0,0], '07':[0,0,0], '08':[0,0,0], '09':[0,0,0], '10':[0,0,0], '11':[0,0,0], '12':[0,0,0]} 
        for op in range(len(ZS)):
            try:   
                temp_idx = str(ZS[op][-1]).split(" ")[0].split("-")[1]
                M[temp_idx][0] += ZS[op][0]
                M[temp_idx][1] += ZS[op][1]                  
                #print (len(ZS), M[temp_idx], ZS[op][0], ZS[op][1])#, ZS[-1]) #ZS[10, 1:2]  ZS[:, :] ZS[10]
            except IndexError:
                print (ZS)
        print ("ID=", i[0],"...........................", M)
        
        a = np.array(list(M.values())).reshape((12, 3))#list(JS[o].keys())[:-1] 
        #sum 
        #b = JS[o]#list(JS[o].values())[:-1] 
        
        print (a.shape, sum(a[:, 0]), sum(a[:, 1]))
        s1, s2 = a[:, 0].tolist(), a[:, 1].tolist()
        print (s1, s2)
        
 #    _temp = D.client.execute("""
#       SELECT SUM(Customer_Id), Order_Date, SUM(Total_Amount) FROM test GROUP BY Order_Date ORDER BY Order_Date
#    """)        
        
# OUT
#user[o] = {
#"id_cat" [ 2, 323, 323 ,323 ...]
#"sum" [0 0 0 0 ... ]
#}
#                                (Order_ID Int64, 
#                                 Product_ID Int64, 
#                                 Items_Count Float64, 
#                                 Total_Amount Float64, 
#                                 TotalDiscount Float64, 
#                                 Branch_Id Int64, 
#                                 Customer_Id Int64,
#                                 Order_Date DateTime64,
#                                 Category1_Id Int64, 
#                                 Category2_Id Int64)

#    _temp = D.client.execute("""
#        SELECT Category1_Id as IDS FROM my_table WHERE Order_ID IN (SELECT Order_ID AS Product_num FROM my_table GROUP BY Order_ID)
#    """)    


#-------------------------------------->        
  #(194469565, 8437646, 1.0, 0.1, 0.0, 79, 2852748, '2020-07-04 17:20:00.000', 160, 1605),     
   #.................................. 
#   # Кол во проданных продуктов
#    _temp = D.client.execute("""
#    SELECT Product_ID, SUM(Items_Count) as sum FROM my_table GROUP BY Product_ID
#    """)
#   # Сумма проданных продуктов
#    _temp = D.client.execute("""
#    SELECT Product_ID, SUM(Total_Amount) as sum FROM my_table GROUP BY Product_ID ORDER BY sum
#    """)
    
#    # Сумма потраченных средств покупателем
#    _temp = D.client.execute("""
#    SELECT Customer_Id, SUM(Total_Amount) as sum FROM my_table GROUP BY Customer_Id
#    """)
#    
#    # Сумма покупок по точкам 
#    _temp = D.client.execute("""
#    SELECT Branch_Id, SUM(Total_Amount) as sum FROM my_table GROUP BY Branch_Id ORDER BY sum
#    """)     

#    # Сумма покупок по месяцам
    #D.show_count_tables("test")#
#    _temp = D.client.execute("""
#       SELECT SUM(Customer_Id), Order_Date, SUM(Total_Amount) FROM test GROUP BY Order_Date ORDER BY Order_Date
#    """)  

#    _temp = D.client.execute("""
#       SELECT Customer_Id, Order_Date FROM test ORDER BY Order_Date
#    """)  

#6188069    
#    _temp = D.client.execute("""
#       SELECT Product_ID, Order_ID, month(Order_Date) 
#       FROM test 
#       WHERE Product_ID = '6188069' 
#       ORDER BY month(Order_Date) 
#    """)

#    _temp = D.client.execute("""
#select month(Order_Date) as m, SUM(Total_Amount) as sum
#from test
#group by month(Order_Date)
#    """)     
 
#    _temp = D.client.execute("""
#SELECT Order_ID, COUNT (*)
#    FROM test
#GROUP BY Order_ID
#  HAVING COUNT (*) > 1;
#    """)    

#    _temp = D.client.execute("""
#  SELECT Branch_Id, COUNT (*)
#    FROM test e
#         JOIN test d ON (e.Branch_Id = d.Branch_Id)
#    GROUP BY Branch_Id;
#    """) 

#    _temp = D.client.execute("""
#SELECT Branch_Id, COUNT(Branch_Id) FROM test
#     GROUP BY Branch_Id   
#    """) 

#    _temp = D.client.execute("""
# SELECT 
# Branch_Id,
# SUM(Total_Amount)
# FROM test
# GROUP BY Branch_Id
# ORDER BY Branch_Id
#    """) 


     
    #('2020-10-05 23:30:00.000',)
    #Order_Date Date,
 #2020-10-05 22:35:00.000
    print (_temp[:3],_temp[-3:],len(_temp))
    print (np.array(_temp[:10]).shape, len(_temp)) #_temp[0][0] _temp, 



#Модель оттока/
##### Общая статистика
# Сумма проданных продуктов по ID
# Сумма проданных продуктов по Категории
# Cумма покупок

# График продаж продуктов за год
# График продаж продуктов за месяц
# График покупок за год
# График покупок по точкам
# График суммы продаж по точкам
# График 

##### Индивидуальная по продукту


