import threading
from utils import *
from dbhandler_2 import *




# Cопутствующий продукт


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

def table_category(x=""):
    D.delete(f"category{x}")
    D.client.execute(f"""
                        CREATE TABLE category{x}
                        (Category{x}_ID Int64,
                         sum Int64,
                         floats Array(Float64))
                        ENGINE = MergeTree()
                        ORDER BY Category{x}_ID
                     """)

    D.show_tables()
    test_file = open("out/category2.json", "r").readlines()
    readsss = json.loads(test_file[0])

    print (len(list(readsss.keys())))
    
    for o in readsss:
        D.client.execute(f"""
                            INSERT INTO category{x} 
                              (floats, Category{x}_ID, sum) 
                            VALUES ({str(list(readsss[o].values()))}, {o}, {str(sum(list(readsss[o].values())))})
                         """)
        print (o, str(np.array(list(readsss[o].values()), dtype=np.float64)), list(readsss[o].values()), sum(list(readsss[o].values())))


def table_product():
    D.delete("sort_related_products")
    D.client.execute(f"""
                        CREATE TABLE sort_related_products
                        (product_ID Int64,
                         sum Int64,
                         floats1 Array(Float64),
                         floats2 Array(Float64))
                        ENGINE = MergeTree()
                        ORDER BY product_ID
                     """)
    D.show_tables()

    files = open ("out/sort_related_products.json", "r").read() #1_create_file_arr.txt
###    F = open("out/sort_related_products.json", 'r')
###    files = json.load(F)
###    for o in files:
    JS = json.loads(files)
    print (">>>", len(JS))
    Oi = 0
    for o in JS:
        Oi += len(JS[o])
        a = list(JS[o].keys())[:-1] #np.array(list(JS[o].keys())[:-1], dtype=np.float64).reshape((len(JS[o])-1, 1))
        b = list(JS[o].values())[:-1] #np.array(list(JS[o].values())[:-1], dtype=np.float64).reshape((len(JS[o])-1, 1))
        #Z = np.array(list(JS[i].keys())[:-1], dtype=np.float64).reshape((len(JS[i])-1, 1)) + np.array(list(JS[i].values())[:-1], dtype=np.float64).reshape((len(JS[i])-1, 1))
        #Z = np.concatenate((a, b), axis=1)
        
        print (o, len(JS[o]), sum(b), b, a) #
        #Z = Z.tolist()
#        print (f"""
#                            INSERT INTO sort_related_products 
#                              (floats, floats2, product_ID, sum) 
#                            VALUES ({str(Z)}, {o}, {str(b.sum())})
#                         """)
        D.client.execute(f"""
                            INSERT INTO sort_related_products 
                              (floats1, floats2, product_ID, sum) 
                            VALUES ({a}, {b}, {o}, {str(sum(b))})
                         """)   # {str(Z)},      
        
        
    print (Oi)       
        #print (len(list(JS.keys())), list(JS.keys())[0], JS[list(JS.keys())[0]])
        
#--------------------------------------------------------------------------->
#
#

def table_product_data():
    D.delete("sort_related_products")
    D.client.execute(f"""
                        CREATE TABLE sort_related_products
                        (product_ID Int64,
                         sum Int64,
                         floats1 Array(Float64),
                         floats2 Array(Float64))
                        ENGINE = MergeTree()
                        ORDER BY product_ID
                     """)
    D.show_tables()

    files = open ("out/products_date_v1.json", "r").read() #1_create_file_arr.txt
###    F = open("out/sort_related_products.json", 'r')
###    files = json.load(F)
###    for o in files:
    JS = json.loads(files)
    print (">>>", len(JS))
    Oi = 0
    for o in JS:
        Oi += len(JS[o])
        a = list(JS[o].keys())[:-1] #np.array(list(JS[o].keys())[:-1], dtype=np.float64).reshape((len(JS[o])-1, 1))
        b = list(JS[o].values())[:-1] #np.array(list(JS[o].values())[:-1], dtype=np.float64).reshape((len(JS[o])-1, 1))
        #Z = np.array(list(JS[i].keys())[:-1], dtype=np.float64).reshape((len(JS[i])-1, 1)) + np.array(list(JS[i].values())[:-1], dtype=np.float64).reshape((len(JS[i])-1, 1))
        #Z = np.concatenate((a, b), axis=1)
        
        print (o, len(JS[o]), sum(b), b, a) #
        #Z = Z.tolist()
#        print (f"""
#                            INSERT INTO sort_related_products 
#                              (floats, floats2, product_ID, sum) 
#                            VALUES ({str(Z)}, {o}, {str(b.sum())})
#                         """)
        D.client.execute(f"""
                            INSERT INTO sort_related_products 
                              (floats1, floats2, product_ID, sum) 
                            VALUES ({a}, {b}, {o}, {str(sum(b))})
                         """)   # {str(Z)},      
        
        
    print (Oi)  

def products_date_v1():
    D.delete("products_date_v1")
    D.client.execute(f"""
                        CREATE TABLE products_date_v1
                        (product_ID Int64,
                         sum1 Int64,
                         sum2 Int64,
                         sum3 Int64,
                         floats1 Array(Float64),
                         floats2 Array(Float64),
                         floats3 Array(Float64))
                        ENGINE = MergeTree()
                        ORDER BY product_ID
                     """)
    D.show_tables()

    files = open ("out/products_date_v1.json", "r").read() #1_create_file_arr.txt
    JS = json.loads(files)
    print (">>>", len(JS))
    Oi = 0
    for o in JS:
        Oi += len(JS[o])
        a = np.array(list(JS[o].values())).reshape((12, 3))#list(JS[o].keys())[:-1] 
        #sum 
        #b = JS[o]#list(JS[o].values())[:-1] 
        
        print (o, a.shape, sum(a[:, 0]), sum(a[:, 1]), sum(a[:, 2]))
        s1, s2, s3 = a[:, 0].tolist(), a[:, 1].tolist(), a[:, 2].tolist() 
        #a = a.tolist()
#        for i in range(len(a)):
#            a[i]= tuple(a[i])
        #a = tuple(a)    
        
        # 0 'Items_Count'
        # 1 'Total_Amount'
        # 2 'TotalDiscount'
        
        
        print (f"""
                            INSERT INTO products_date_v1
                              (floats1, floats2, floats3, product_ID, sum1, sum2, sum3) 
                            VALUES ({s1}, {s2}, {s3}, {o}, {sum(s1)}, {sum(s2)}, {sum(s3)})
                          """)
        D.client.execute(f"""
                            INSERT INTO products_date_v1
                              (floats1, floats2, floats3, product_ID, sum1, sum2, sum3) 
                            VALUES ({s1}, {s2}, {s3}, {o}, {sum(s1)}, {sum(s2)}, {sum(s3)})
                          """)      
#    print (Oi)  

def test():
    H = D.client.execute(f"""
                            SELECT * FROM sort_related_products 
                            order by sum                               
                         """)
    test_data = np.array(H[200][2]) 
    res = test_data.reshape((test_data.shape[0], 1))               
    print (H[200])#(test_data.shape[0], res.shape, res[:,:])   


def category_by_user():
    D.delete("category_by_user")
    D.client.execute(f"""
                        CREATE TABLE category_by_user
                        (Category1_Id Int64,
                         Customer_Id Int64,
                         
                         sum1 Int64,
                         sum2 Int64,
                         sum3 Int64,
                         floats1 Array(Float64),
                         floats2 Array(Float64),
                         floats3 Array(Float64))
                        ENGINE = MergeTree()
                        ORDER BY Customer_Id
                     """)



    _temp = D.client.execute("""
        SELECT DISTINCT Customer_Id FROM my_table
    """)      
    _temp1 = D.client.execute("""
        SELECT DISTINCT Category1_Id FROM my_table
    """)             
    Str = f""
    print (len(_temp))
    for i in _temp:
      for izz in _temp1:
        ZS = D.client.execute(f"""   
                                        SELECT
                                          SUM(Items_Count) as sum1, 
                                          SUM(Total_Amount) as sum2,
                                          Order_Date
                                        FROM test
                                        WHERE test.Customer_Id = {i[0]} 
                                        AND test.Category1_Id = {izz[0]}
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
        
        print (a.shape, sum(a[:, 0]), sum(a[:, 1]))
        s1, s2 = a[:, 0].tolist(), a[:, 1].tolist()
        print (s1, s2, f"""
                    INSERT INTO category_by_user 
                      (floats1, floats2, Category1_Id, Customer_Id, sum1) 
                    VALUES ({s1}, {s2}, {izz[0]}, {i[0]}, {str(sum(s1))})
                 """)
        D.client.execute(f"""
                    INSERT INTO category_by_user 
                      (floats1, floats2, Category1_Id, Customer_Id, sum1) 
                    VALUES ({s1}, {s2}, {izz[0]}, {i[0]}, {str(sum(s1))})
                 """)   

def chunks(lst, count):
    start = 0
    for i in range(count):
          stop = start + len(lst[i::count])
          yield lst[start:stop]
          start = stop   


#    def T(self, p_arr, t_name):
#        size = p_arr.shape[0]
#        step = int((size/1000)+1)
#        D = DataBase()
#        for ii in range(0, step):
#            end = (ii+1)*step 
#            if end>size:
#                end = size
#            product_arr = p_arr[ii*step:end, :]
#            str_temp = f""
#            for i in range(product_arr.shape[0]):
#                _order = self.order_arr[self.ids_order[p_arr[i,0]],:][0]
#                try:
#                    _category = self.product_name_arr[self.ids_product_name[product_arr[i,1]],:][0]
#                except KeyError:
#                    print (product_arr[i,1])
#                    _category = [0,0,0,0,0,0]
#                #print (_order[-1])   2020-10-05 22:35:00.000
#                #new_arr = [int(product_arr[i,0]), int(product_arr[i,1]), product_arr[i,2], product_arr[i,3], product_arr[i,4], _order[1], _order[2], _order[-1], _category[3], _category[5]]
##                str_temp += f"""({product_arr[i,0]}, {product_arr[i,1]}, {product_arr[i,2]}, {product_arr[i,3]}, {product_arr[i,4]}, 
##                             {_order[1]}, {_order[2]}, '{_order[-1]}', {_category[3]}, {_category[5]}),"""
#                str_temp += f"""({product_arr[i,0]}, {product_arr[i,1]}, {product_arr[i,2]}, {product_arr[i,3]}, {product_arr[i,4]}, 
#                             {_order[1]}, {_order[2]}, '{_order[-1]}', {_category[3]}, {_category[5]}),"""  
#                                                        
#            POO = str_temp[:-1]
#            D.client.execute(f"""INSERT INTO {t_name} 
#                            (Order_ID, Product_ID, Items_Count, 
#                             Total_Amount, TotalDiscount, Branch_Id, 
#                             Customer_Id, Order_Date, Category1_Id, Category2_Id) 
#                            VALUES {POO}""")    
#                                
#            str_temp = f""

def func_insert(x1, x2):
    #step = int((size/1000)+1)
    for i in x1:
        for izz in x2:
            ZS = D.client.execute(f"""   
                                            SELECT
                                              SUM(Items_Count) as sum1, 
                                              SUM(Total_Amount) as sum2,
                                              Order_Date
                                            FROM test
                                            WHERE test.Customer_Id = {i[0]} 
                                            AND test.Product_ID = {izz[0]}
                                            GROUP BY Order_Date
                                        """)   
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
            
            print (a.shape, sum(a[:, 0]), sum(a[:, 1]))
            s1, s2 = a[:, 0].tolist(), a[:, 1].tolist()
            print (s1, s2)
            D.client.execute(f"""
                        INSERT INTO category_by_user 
                          (floats1, floats2, Product_ID, Customer_Id, sum1) 
                        VALUES ({s1}, {s2}, {izz[0]}, {i[0]}, {str(sum(s1))})
                     """)      

def product_correlation():     
    D.delete("product_correlation")
    D.client.execute(f"""
                CREATE TABLE product_correlation
                (Product_ID Int64,
                 floats1 Array(String),
                 floats2 Array(Array(Float64)))
                ENGINE = MergeTree()
                ORDER BY Product_ID
             """)
     
    F = json.load(open("out/correlation_products.json", 'r'))#.readlines()
    for  i in F:
        D.client.execute(f"""
                INSERT INTO product_correlation 
                  (Product_ID, floats1, floats2) 
                VALUES ({i.split("_")[-1]}, {F[i][0]}, {F[i][1]})
             """)    
    
        #print(i, len(F[i]), len(F[i][0]), len(F[i][1]))
    print (len(F))
    print (D.show_tables()) 


def product_by_user():
    D.delete("product_by_user")
    D.client.execute(f"""
                        CREATE TABLE product_by_user
                        (Product_ID Int64,
                         Customer_Id Int64,
                         
                         sum1 Int64,
                         sum2 Int64,
                         sum3 Int64,
                         floats1 Array(Float64),
                         floats2 Array(Float64),
                         floats3 Array(Float64))
                        ENGINE = MergeTree()
                        ORDER BY Customer_Id
                     """)
#--------------------------------->
### WORK !!!
#    t = D.client.execute(f"SELECT * FROM my_table")
#    print (len(t), t[0])
#    #89144855 (188860582, 7290001201596, 1.0, 10.4, 0.0, 21, 0, '2020-01-01 00:04:00.000', 530, 5300)
##    _temp1 = D.client.execute("""
##        SELECT DISTINCT Customer_Id FROM my_table
##    """)      
#    start = time.time()
#    dict_ = {}
#    for iz in t:
#        count = iz[2]
#        t_sum = iz[3]
#        d_month = iz[7].split(" ")[0].split("-")[1]
#        c_id = iz[6]
#        #print (c_id, iz[7], d_month, count, t_sum) 
#        
#        try:
#            dict_[c_id][iz[1]][d_month][0] += count
#            dict_[c_id][iz[1]][d_month][0] += t_sum
#            print (dict_[c_id][iz[1]][d_month])
#        except KeyError:
#            dict_[c_id] = {iz[1]: {'01':[0,0,0], '02':[0,0,0], '03':[0,0,0], '04':[0,0,0], '05':[0,0,0], '06':[0,0,0], '07':[0,0,0], '08':[0,0,0], '09':[0,0,0], '10':[0,0,0], '11':[0,0,0], '12':[0,0,0]}}
#            dict_[c_id][iz[1]][d_month][0] += count
#            dict_[c_id][iz[1]][d_month][0] += t_sum
#------------------------------------------------->
# vers 2
    t = D.client.execute(f"""   
                            SELECT
                            *
                            FROM my_table
                            WHERE my_table.Customer_Id = 3
                            ORDER BY Items_Count
                          """)
    
    print (len(t))
    start = time.time()
    dict_ = {}
    for iz in t:
        count = iz[2]
        p_id = iz[1]
        t_sum = iz[3]
        d_month = iz[7].split(" ")[0].split("-")[1]
        c_id = iz[6]
        print (c_id, iz[7], d_month, count, t_sum, p_id) 
#        try:
#            dict_[c_id].append({'01':[0,0,0], '02':[0,0,0], '03':[0,0,0], '04':[0,0,0], '05':[0,0,0], '06':[0,0,0], '07':[0,0,0], '08':[0,0,0], '09':[0,0,0], '10':[0,0,0], '11':[0,0,0], '12':[0,0,0]})
#        except:
#            dict_[c_id] = [{'01':[0,0,0], '02':[0,0,0], '03':[0,0,0], '04':[0,0,0], '05':[0,0,0], '06':[0,0,0], '07':[0,0,0], '08':[0,0,0], '09':[0,0,0], '10':[0,0,0], '11':[0,0,0], '12':[0,0,0]}]
        
        try:
            dict_[p_id][d_month][0] += count
            dict_[p_id][d_month][1] += t_sum
           # print (dict_[c_id][iz[1]][d_month])
        except KeyError:
            dict_[p_id] = {'01':[0,0,0], '02':[0,0,0], '03':[0,0,0], '04':[0,0,0], '05':[0,0,0], '06':[0,0,0], '07':[0,0,0], '08':[0,0,0], '09':[0,0,0], '10':[0,0,0], '11':[0,0,0], '12':[0,0,0]}
            dict_[p_id][d_month][0] += count
            dict_[p_id][d_month][1] += t_sum
#    print (time.time()-start, len(dict_), 
#    "\n", dict_[list(dict_.keys())[0]], list(dict_.keys())[0],
#    "\n", dict_[list(dict_.keys())[-1]], list(dict_.keys())[-1],
#    "\n", dict_[list(dict_.keys())[-2]], list(dict_.keys())[-2]) #dir(dict_), list(dict_.keys())[0], 
    #a = np.array(list(M.values())).reshape((12, 3))
    for z in dict_:
#        sums = 0
#        for zz in dict_[z]:
#            sums += dict_[z][zz][0]
#            #print ("..................", dict_[z][zz])
#        print (sums, list(dict_[z].values()), "<<<<<<<<<<<<<<<<<<<<<<<<<<END")
        a = np.array(list(dict_[z].values())).reshape((12, 3))
        print (a.shape, a[:,1], a[:,0])
#----------------------------------------------->
            
            #print (dict_[c_id][iz[1]])
            
    #print (len(dict_))
#    for k in dict_:
#        for p in dict_[k] 
#        M = {'01':[0,0,0], '02':[0,0,0], '03':[0,0,0], '04':[0,0,0], '05':[0,0,0], '06':[0,0,0], '07':[0,0,0], '08':[0,0,0], '09':[0,0,0], '10':[0,0,0], '11':[0,0,0], '12':[0,0,0]} 
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
#-----------------------------------?



#    _temp1 = D.client.execute("""
#        SELECT DISTINCT Customer_Id FROM my_table
#    """)      
#    _temp2 = D.client.execute("""
#        SELECT DISTINCT Product_ID FROM my_table
#    """)             
#    Str = f""
#    start = time.time()
#    print (len(_temp1), len(_temp2))
#    list_1 = chunks(_temp1, 5)
#    print (len(list(list_1)))
#    threads = []
#    for f_list in list_1:
#       my_thread = threading.Thread(target=func_insert, args=(f_list, _temp2))
#       threads.append(my_thread)
#       my_thread.start()
#    flag = 1
#    while (flag):
#        for t in threads:
#            if t.isAlive():
#                flag = 1
#            else:
#                flag = 0
#                
#    print (time.time()-start)   

#    for i in _temp:
#      for izz in _temp1:
#        ZS = D.client.execute(f"""   
#                                        SELECT
#                                          SUM(Items_Count) as sum1, 
#                                          SUM(Total_Amount) as sum2,
#                                          Order_Date
#                                        FROM test
#                                        WHERE test.Customer_Id = {i[0]} 
#                                        AND test.Product_ID = {izz[0]}
#                                        GROUP BY Order_Date
#                                    """)   
#                                    #  
##        ZS1 = D.client.execute(f"""   
##                                        SELECT
##                                          SUM(Items_Count) as sum1, 
##                                          SUM(Total_Amount) as sum2,
##                                          Order_Date
##                                        FROM my_table
##                                        WHERE my_table.Customer_Id = {i[0]} 
##                                        AND my_table.Category1_Id = 402
##                                        GROUP BY Order_Date
##                                    """) 
##        ZS = np.array(ZS) 
##        A = func_return(ZS, -1) 
##        for o in range(ZS.shape[0]):
##            print (ZS[o,2:5], ZS[o,2:5]) 
#        #temp_dict = {}
#        M = {'01':[0,0,0], '02':[0,0,0], '03':[0,0,0], '04':[0,0,0], '05':[0,0,0], '06':[0,0,0], '07':[0,0,0], '08':[0,0,0], '09':[0,0,0], '10':[0,0,0], '11':[0,0,0], '12':[0,0,0]} 
#        for op in range(len(ZS)):
#            try:   
#                temp_idx = str(ZS[op][-1]).split(" ")[0].split("-")[1]
#                M[temp_idx][0] += ZS[op][0]
#                M[temp_idx][1] += ZS[op][1]                  
#                #print (len(ZS), M[temp_idx], ZS[op][0], ZS[op][1])#, ZS[-1]) #ZS[10, 1:2]  ZS[:, :] ZS[10]
#            except IndexError:
#                print (ZS)
#        print ("ID=", i[0],"...........................", M)
#        
#        a = np.array(list(M.values())).reshape((12, 3))#list(JS[o].keys())[:-1] 
#        
#        print (a.shape, sum(a[:, 0]), sum(a[:, 1]))
#        s1, s2 = a[:, 0].tolist(), a[:, 1].tolist()
#        print (s1, s2)
#        D.client.execute(f"""
#                    INSERT INTO category_by_user 
#                      (floats1, floats2, Product_ID, Customer_Id, sum1) 
#                    VALUES ({s1}, {s2}, {izz[0]}, {i[0]}, {str(sum(s1))})
#                 """)  


if __name__ == "__main__":
    D = DataBase()
    
    # Создаю бд категории
    #table_category(2)
    
    # Создаю бд продуктов
    #table_product()
    #products_date_v1()
    print (D.show_tables())  
    #test()
    # Категории пользователи
    #category_by_user()  
    # Продукты пользователи
    #product_by_user()
    D.delete("product_correlation")
    D.client.execute(f"""
                CREATE TABLE product_correlation
                (Product_ID Int64,
                 floats1 Array(String),
                 floats2 Array(Array(Float64)))
                ENGINE = MergeTree()
                ORDER BY Product_ID
             """)
     
    F = json.load(open("out/correlation_products.json", 'r'))#.readlines()
    for  i in F:
        print (F[i][0], F[i][1])
#        arr1 = []
#        arr2 = []
#        for ii in range(len(F[i][1])):
#            print (F[i][1][ii])
        D.client.execute(f"""
                INSERT INTO product_correlation 
                  (Product_ID, floats1, floats2) 
                VALUES ({i.split("_")[-1]}, {F[i][0]}, {F[i][1]})
             """)    
    
        #print(i, len(F[i]), len(F[i][0]), len(F[i][1]))
    print (len(F))
    print (D.show_tables()) 
    #print (len(H))
# !!!!!!!!
#        D.client.execute(f"""
#                            INSERT INTO product 
#                              (floats, product_ID, sum) 
#                            VALUES ({str(list(readsss[o].values()))}, {o}, {str(sum(list(readsss[o].values())))})
#                         """)

#------------------------------------------------------>
#................
#        print (f"""
#                            INSERT INTO category1 
#                              (floats, Category1_ID) 
#                            VALUES {str(list(readsss[o].values()))}, {o}
#                         """)
#        print (o, str(np.array(list(readsss[o].values()), dtype=np.float64)), list(readsss[o].values()), sum(list(readsss[o].values())))        
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
# Сортировать покупателей по картам оплаты
# По фотографии продукта определять его прибыльность
# Когда собереться достаточно статистики можно строить модель 
# предсказания
# Цветовые графики

#https://altinity.com/blog/harnessing-the-power-of-clickhouse-arrays-part-1
