from clickhouse_driver import Client
from utils import *
client = Client('localhost')
#client.execute('CREATE TABLE test (id_prod Int64, info String, date Date DEFAULT today()) ENGINE = MergeTree(date, (id_prod), 8192)')

#client.execute("""CREATE TABLE my_table 
#                    (Order_ID Int64, 
#                     Product_ID Int64, 
#                     Items_Count Float64, 
#                     Total_Amount Float64, 
#                     TotalDiscount Float64, 
#                     Branch_Id Int64, 
#                     Customer_Id Int64,
#                     Order_Date String, 
#                     Category1_Id Int64, 
#                     Category2_Id Int64) 
#                 ENGINE = MergeTree() ORDER BY Order_ID""")

#client.execute('DROP TABLE IF EXISTS test')
print (client.execute('SHOW TABLES'))
#client.execute(f"""INSERT INTO test 
#                        (id_prod, info) 
#                        VALUES 
#                        (2,'3'), (3,'4'), (4,'4')
#                        """)

##LS = client.execute("SELECT * FROM my_table")
LS = client.execute("SELECT * FROM test")
print (len(LS))

#start = time.time()
#str_temp = f""
#for i in range(100000000):
#    #print (i)
#    #pass
#    str_temp += f"({i},'{i/3}'),"
#    if i % 1000 == 0:
#        POO = str_temp[:-1]
##        print (i, f"""INSERT INTO test 
##                            (id_prod, info) 
##                            VALUES 
##                            {POO}
##                            """, "\n")
#        
#        client.execute(f"""INSERT INTO test 
#                            (id_prod, info) 
#                            VALUES 
#                            {POO}
#                            """)
#        str_temp = f""
#        
#print (time.time()-start)
