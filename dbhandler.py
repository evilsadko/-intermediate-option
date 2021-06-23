from clickhouse_driver import Client
import threading
from utils import *

class DataBase():
    def __init__(self):
        self.client = Client('localhost')

#    def createDB_0(self, x="test"):
#        self.client.execute(f'CREATE TABLE {x} (id_prod Int64, info String, date Date DEFAULT today()) ENGINE = MergeTree(date, (id_prod), 8192)')

    def createDB(self, x="my_table"):
#        self.client.execute(f"""CREATE TABLE {x} 
#                                (Order_ID Int64, 
#                                 Product_ID Int64, 
#                                 Items_Count Float64, 
#                                 Total_Amount Float64, 
#                                 TotalDiscount Float64, 
#                                 Branch_Id Int64, 
#                                 Customer_Id Int64,
#                                 Order_Date String, 
#                                 Category1_Id Int64, 
#                                 Category2_Id Int64) 
#                            ENGINE = MergeTree() ORDER BY Order_ID""")
        self.client.execute(f"""CREATE TABLE {x} 
                                (Order_ID Int64, 
                                 Product_ID Int64, 
                                 Items_Count Float64, 
                                 Total_Amount Float64, 
                                 TotalDiscount Float64, 
                                 Branch_Id Int64, 
                                 Customer_Id Int64,
                                 Order_Date DateTime64,
                                 Category1_Id Int64, 
                                 Category2_Id Int64) 
                            ENGINE = MergeTree() 
                            
                            ORDER BY Order_Date""")                            
                            #PARTITION BY toYYYYMM(Order_Date)
                            #DateTime64, 
    #def add_data(self):

    def delete(self, x):
        self.client.execute(f'DROP TABLE IF EXISTS {x}')

    def show_tables(self):
        return self.client.execute('SHOW TABLES')
       
    def show_count_tables(self, x):
        start = time.time()
        LS = self.client.execute(f"SELECT count() FROM {x}")
        print (time.time()-start, LS)
        return LS
        
        
    def get_all_data(self, x):
        start = time.time()
        LS = self.client.execute(f"SELECT * FROM {x}")
        print (time.time()-start, len(LS)) 
        return LS
        
    def info_1(self):
        print (self.client.execute("""
        select parts.*,
               columns.compressed_size,
               columns.uncompressed_size,
               columns.ratio
        from (
                 select table,
                        formatReadableSize(sum(data_uncompressed_bytes))          AS uncompressed_size,
                        formatReadableSize(sum(data_compressed_bytes))            AS compressed_size,
                        sum(data_compressed_bytes) / sum(data_uncompressed_bytes) AS ratio
                 from system.columns
                 where database = currentDatabase()
                 group by table
                 ) columns
                 right join (
            select table,
                   sum(rows)                                            as rows,
                   max(modification_time)                               as latest_modification,
                   formatReadableSize(sum(bytes))                       as disk_size,
                   formatReadableSize(sum(primary_key_bytes_in_memory)) as primary_keys_size,
                   any(engine)                                          as engine,
                   sum(bytes)                                           as bytes_size
            from system.parts
            where active and database = currentDatabase()
            group by database, table
            ) parts on columns.table = parts.table
        order by parts.bytes_size desc;
            """))

    def info_2(self):
        print (self.client.execute("""
        select concat(database, '.', table)                         as table,
               formatReadableSize(sum(bytes))                       as size,
               sum(rows)                                            as rows,
               max(modification_time)                               as latest_modification,
               sum(bytes)                                           as bytes_size,
               any(engine)                                          as engine,
               formatReadableSize(sum(primary_key_bytes_in_memory)) as primary_keys_size
        from system.parts
        where active
        group by database, table
        order by bytes_size desc;
            """))       

        
    def T(self, p_arr, t_name):
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
                _order = self.order_arr[self.ids_order[p_arr[i,0]],:][0]
                try:
                    _category = self.product_name_arr[self.ids_product_name[product_arr[i,1]],:][0]
                except KeyError:
                    print (product_arr[i,1])
                    _category = [0,0,0,0,0,0]
                #print (_order[-1])   2020-10-05 22:35:00.000
                #new_arr = [int(product_arr[i,0]), int(product_arr[i,1]), product_arr[i,2], product_arr[i,3], product_arr[i,4], _order[1], _order[2], _order[-1], _category[3], _category[5]]
#                str_temp += f"""({product_arr[i,0]}, {product_arr[i,1]}, {product_arr[i,2]}, {product_arr[i,3]}, {product_arr[i,4]}, 
#                             {_order[1]}, {_order[2]}, '{_order[-1]}', {_category[3]}, {_category[5]}),"""
                str_temp += f"""({product_arr[i,0]}, {product_arr[i,1]}, {product_arr[i,2]}, {product_arr[i,3]}, {product_arr[i,4]}, 
                             {_order[1]}, {_order[2]}, '{_order[-1]}', {_category[3]}, {_category[5]}),"""  
                                                        
            POO = str_temp[:-1]
            D.client.execute(f"""INSERT INTO {t_name} 
                            (Order_ID, Product_ID, Items_Count, 
                             Total_Amount, TotalDiscount, Branch_Id, 
                             Customer_Id, Order_Date, Category1_Id, Category2_Id) 
                            VALUES {POO}""")    
                                
            str_temp = f""
            
            
    def chunks(self, lst, count):
        start = 0
        for i in range(count):
              stop = start + len(lst[i::count, :])
              yield lst[start:stop, :]
              start = stop     




    def create_file_arr(self, t_name):
        p_open = PRODUCT() #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount'] 
        #[188860582.0, 7290001201596.0, 1.0, 10.4, 0.0]
        product_arr = p_open.to_numpy()
        print (product_arr.shape[0])
        #---------------------------------------------->
        o_open = ORDER() #['Order_Id', 'Branch_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date']  
        self.order_arr = o_open.to_numpy()
        self.ids_order = func_return(self.order_arr, 0)

        #---------------------------------------------->
        product_name = PRODUCTNAME() #[ ID, Product_Id, LocalName, Category1_Id, Category1_Name, Category2_Id, Category2_Name] 
        self.product_name_arr = product_name.to_numpy()
        self.ids_product_name = func_return(self.product_name_arr, 1)   
        start = time.time()
        
        ty = self.chunks(product_arr[:,:],4)
        threads = []
        for f_list in ty:
           my_thread = threading.Thread(target=self.T, args=(f_list, t_name))
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

def clean(x):
    D.delete(x)
    D.createDB(x)
    D.show_tables()
    D.create_file_arr(x)

if __name__ == "__main__":
    D = DataBase()
    #print (D.client.execute('SHOW DATABASES'))
    #D.client.execute("SYSTEM DROP UNCOMPRESSED CACHE")
    #------------------------>
    #clean("test")
    
    #D.delete("my_table")
    
    
    #D.get_all_data("my_table") #"test" / my_table 35 show 100 000 000
    #D.show_count_tables("test") #"my_table"
    
    #D.createDB_0("test")
# 
#    D.info_1()
#    D.info_2()
        

#    
#    
#    D.create_file_arr("test")










