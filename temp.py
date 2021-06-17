import threading
from utils import *
from dbhandler_2 import *


if __name__ == "__main__":
    D = DataBase()
    
    
#        self.client.execute(f"""CREATE TABLE {x} 
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
#                            ENGINE = MergeTree() 
#                            
#                            ORDER BY Order_Date""")  
    #print (D.show_tables())  
#    T = D.client.execute(f"""   
#                                            SELECT
#                                              SUM(Items_Count) as sum1, 
#                                              SUM(Total_Amount) as sum2,
#                                              Customer_Id
#                                            FROM test
#                                            GROUP BY Customer_Id
#                                            ORDER BY sum1
#                          """)


#dict_ = DB.client.execute(f"""  
#                    SELECT
#                       SUM(columns.sum1) as s1,
#                       SUM(columns.sum2) as S2,
#                       columns.time
#                    FROM
#                    (SELECT
#                    toMonth(Order_Date) as time,
#                    SUM(Items_Count) as sum1,
#                    SUM(Total_Amount) as sum2
#                    FROM test
#                    WHERE Customer_Id = {message["data"]["id_user"]}
#                    AND Product_ID = {message["data"]["id_product"]}
#                    GROUP BY Order_Date) columns
#                    GROUP BY columns.time
#                    ORDER BY columns.time
#                    ASC
#                            """)#OR


#    vals_prod  = D.client.execute(f"""
#                        SELECT 
#                        count() 
#                        FROM 
#                            (SELECT DISTINCT 
#                             Product_ID
#                             FROM test)
#                            """)[0][0]
    #Z = np.zeros((vals_prod))
#    print (Z.shape)
#    T = D.client.execute(f"""
#                            SELECT
#                                  *
#                            FROM test
#                            WHERE test.Customer_Id = 5123650 
#                            AND test.Product_ID = 7290011017873
#                            """)
#    G = {}
#    izs = 0
#    for i in T:
#    
#        a = D.client.execute(f"""
#                        SELECT
#                            *
#                        FROM test
#                        WHERE test.Customer_Id = 5123650 
#                        AND test.Order_ID = {i[0]}
#                        """)
#        izs += len(a)
#        for k in a:
#            if k[1] != 7290011017873:
#                print (k)                
#        G[i[0]] = len(a)
        #new_dict[j] = Z.tolist()                
        #print (a[0], len(a), i[0])
#    print (G, izs)#(T[0], T[-1], len(T), len(G))
    
    
#------------------------------------------>
    # Работает для небольших запросов      
    T = D.client.execute(f"""
                            SELECT
                                 Order_ID, 
                                 Product_ID, 
                                 Items_Count, 
                                 Total_Amount, 
                                 Customer_Id,
                                 toMonth(Order_Date) as time
                            FROM test
                            WHERE test.Customer_Id = 5123650 
                            AND test.Product_ID = 7290011017873
                            """)    
    G = {}
    t_str = ""
    t_count = 0
    G[7290011017873] = [0,0,0,0,0,0,0,0,0,0,0,0]
    for i in T:
        t_str += f"OR test.Order_ID = {i[0]}\n"
        t_count += i[2]
        G[7290011017873][(i[-1]-1)] += i[2]
           
    a = D.client.execute(f"""
                    SELECT
                         Order_ID, 
                         Product_ID, 
                         Items_Count, 
                         Total_Amount, 
                         Customer_Id,
                         toMonth(Order_Date) as time
                    FROM test
                    WHERE test.Customer_Id = 5123650
                    AND NOT test.Product_ID = 7290011017873
                    AND ({t_str[3:]})
                    
                    """)
    dict_data = {}   
    print (a)  
    
    P1 = t_count   
    for r in a:
        try:
            dict_data[r[1]][0][(r[-1]-1)] += r[2]  
            dict_data[r[1]][1] += r[2]
        except KeyError:
            dict_data[r[1]] = [[0,0,0,0,0,0,0,0,0,0,0,0], 0] 
            dict_data[r[1]][0][(r[-1])] += r[2]
            dict_data[r[1]][1] += r[2]  
        print (r[-1])  
    
    for r in dict_data:
        P2 = dict_data[r][1]
        P = (P2/P1)*100  
        if P > 5:  
            G[r] = dict_data[r]   
            print (dict_data[r], P, P1, P2)    
    print (G)    
    #print (t_count, dict_data)#(dict_data, len(T), len(a), t_count, G)    
#    for x in a:
#        print (x)
    
    
    """
    Сопутствующие товары для пользователя
    
    получаю все данные с ид товара, ид пользователя

    извлекаю все покупки из этих данных 
    
    смотрю какие товары продовались   
    """
    # Кореляция
    
    
    #P 7290011017873 CATeG-350  USER
#f"SELECT count() FROM {x}"

#    def related_products(self):
#        product_dict = self.func_return(self.product_arr, 0) #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount'] 
#        product_open = self.product_open.sort_values(['Items_Count']) # Сортировка
#        vals_prod = self.product_open.drop_duplicates("Product_ID") # Убрать дубликаты
#        vals_prod = vals_prod["Product_ID"] 
#        print (len(vals_prod)) # Узнать кол во ID продуктов
#        #----------------------->
#        # Декодирование кодирование в словарь
#        dict_to_coding = {}
#        dict_to_encoding = {}
#        for ix, ij in enumerate(vals_prod):
#            dict_to_coding[ij] = ix 
#            dict_to_encoding[ix] = ij
#        
#        #------------------------------------->
#        # Обработка файлов
#        start = time.time()
#        new_dict = {}
#        _product_dict = self.func_return(self.product_arr, 1)  #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount'] 
#        for j in vals_prod[:]:
#            #print (len(_product_dict[j])) # Кол во покупок с этим товаром
#            Z = np.zeros((len(vals_prod)))
#            for k in _product_dict[j]:
#                _id_o = self.product_arr[k,0]    #получаю ИД oredr и продукта
#                for u in product_dict[_id_o]:
#                     ix_z = int(self.product_arr[u,1])
#                     if int(j) != int(ix_z): 
#                        ix_z = dict_to_coding[ix_z]
#                        Z[ix_z] += self.product_arr[u,2]

#            new_dict[j] = Z.tolist()
#        print ("END", time.time()-start, len(new_dict))

#        data = new_dict
#        for i in data:
#            P1 = sum(data[i])
#            t_d = {}
#            for ix, o in enumerate(data[i]):
#                    try:
#                        if o > 0:
#                            P = o / int(P1) * 100
#                            if P > 0.5:
#                                #t_d[ix] = o
#                                t_d[dict_to_encoding[str(ix)]] = o
#                                P1 = P1 - o
#                    except:
#                           print (o, P1, i)   
#                    
#            if P1 > 0:
#                t_d["остальные"] = P1
#                _dict[i] = t_d  
