from clickhouse_driver import Client
import threading
from utils import *

class DataBase():
    def __init__(self):
        self.client = Client('localhost')

    def createDB_0(self, x="test"):
        self.client.execute(f'CREATE TABLE {x} (id_prod Int64, info String, date Date DEFAULT today()) ENGINE = MergeTree(date, (id_prod), 8192)')

    def createDB_1(self, x="my_table"):
        self.client.execute(f"""CREATE TABLE {x} 
                                (Order_ID Int64, 
                                 Product_ID Int64, 
                                 Items_Count Float64, 
                                 Total_Amount Float64, 
                                 TotalDiscount Float64, 
                                 Branch_Id Int64, 
                                 Customer_Id Int64,
                                 Order_Date String, 
                                 Category1_Id Int64, 
                                 Category2_Id Int64) 
                            ENGINE = MergeTree() ORDER BY Order_ID""")
                            
    #def add_data(self):

    def delete(self, x):
        self.client.execute(f'DROP TABLE IF EXISTS {x}')

    def show_tables(self):
        print (self.client.execute('SHOW TABLES'))
       
    def show_count_tables(self, x):
        start = time.time()
        LS = self.client.execute(f"SELECT count() FROM {x}")
        print (time.time()-start, LS)
        
    def get_all_data(self, x):
        start = time.time()
        LS = self.client.execute(f"SELECT * FROM {x}")
        print (time.time()-start, len(LS)) 
        return LS
        
    def test(self):
        start = time.time()
        str_temp = f""
        for i in range(100000000):
            #print (i)
            #pass
            str_temp += f"({i},'{i/3}'),"
            if i % 1000 == 0:
                POO = str_temp[:-1]
#                client.execute(f"""INSERT INTO test 
#                                    (id_prod, info) 
#                                    VALUES 
#                                    {POO}
#                                    """)
                str_temp = f""
                
        print (time.time()-start)  
      
#client.execute(f"""INSERT INTO test 
#                        (id_prod, info) 
#                        VALUES 
#                        (2,'3'), (3,'4'), (4,'4')
#                        """) 
       
        
def T(p_arr):
    size = p_arr.shape[0]
    step = int((size/1000)+1)
    D = DataBase()
    for ii in range(0, step):
        end = (ii+1)*step 
        if end>size:
            end = size
        product_arr = p_arr[ii*step:end, :]
        str_temp = f""
        for i in range(product_arr.shape[0]):
            _order = order_arr[ids_order[p_arr[i,0]],:][0]
            try:
                _category = product_name_arr[ids_product_name[product_arr[i,1]],:][0]
            except KeyError:
                print (product_arr[i,1])
                _category = [0,0,0,0,0,0]
            str_temp += f"""({product_arr[i,0]}, {product_arr[i,1]}, {product_arr[i,2]}, {product_arr[i,3]}, {product_arr[i,4]}, 
                         {_order[1]}, {_order[2]}, '{_order[-1]}', {_category[3]}, {_category[5]}),"""
        POO = str_temp[:-1]
        D.client.execute(f"""INSERT INTO my_table 
                        (Order_ID, Product_ID, Items_Count, 
                         Total_Amount, TotalDiscount, Branch_Id, 
                         Customer_Id, Order_Date, Category1_Id, Category2_Id) 
                        VALUES {POO}""")    
                            
        str_temp = f""
        
        
def chunks(lst, count):
    start = 0
    for i in range(count):
          stop = start + len(lst[i::count, :])
          yield lst[start:stop, :]
          start = stop     




def create_file_arr():
    start = time.time()
    ty = chunks(product_arr[:,:],4)
    threads = []
    for f_list in ty:
       my_thread = threading.Thread(target=T, args=(f_list,))
       threads.append(my_thread)
       my_thread.start()
    flag = 1
    while (flag):
        for t in threads:
            if t.isAlive():
                flag = 1
            else:
                flag = 0
                
    print (time.time()-start)     


if __name__ == "__main__":
    D = DataBase()
    #print (D.client.execute('SHOW DATABASES'))
    #D.client.execute("SYSTEM DROP UNCOMPRESSED CACHE")
    
    #D.delete("test")
    #D.delete("my_table")
    
    
    #D.get_all_data("my_table") #"test" / my_table 35 show 100 000 000
    D.show_count_tables("my_table")
    D.show_count_tables("test")
    D.show_count_tables("test2")
    #D.createDB_0()
    
    #D.test()  
    #D.createDB_1()

    D.show_tables()
 
    
#    p_open = PRODUCT() #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount'] 
#    #[188860582.0, 7290001201596.0, 1.0, 10.4, 0.0]
#    product_arr = p_open.to_numpy()
#    print (product_arr.shape[0])
#    #---------------------------------------------->
#    o_open = ORDER() #['Order_Id', 'Branch_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date']  
#    order_arr = o_open.to_numpy()
#    ids_order = func_return(order_arr, 0)

#    #---------------------------------------------->
#    product_name = PRODUCTNAME() #[ ID, Product_Id, LocalName, Category1_Id, Category1_Name, Category2_Id, Category2_Name] 
#    product_name_arr = product_name.to_numpy()
#    ids_product_name = func_return(product_name_arr, 1)
#    
#    
#    create_file_arr()










