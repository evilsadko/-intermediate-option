from clickhouse_driver import Client
from utils import *
client = Client('localhost')
#client.execute('CREATE TABLE my_table (date Date DEFAULT today(), s String) ENGINE = MergeTree(date, (date), 8192)')

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

#client.execute('DROP TABLE IF EXISTS my_table')
print (client.execute('SHOW TABLES'))
#[188877189, 8437646, 1.0, 0.09, 0.01, 52, 2276053, '2020-01-01 19:38:00.000', 160, 1605]
#[188877190, 7777777, 1.0, 0.0, 0.0, 52, 5032865, '2020-01-01 19:37:00.000', 139, 1380]
#[188877190, 8697431460217, 1.0, 11.9, 5.0, 52, 5032865, '2020-01-01 19:37:00.000', 125, 3301]

#client.execute(f"INSERT INTO my_table VALUES (21, 12, 1, 1, 1, 3, 4, 45, 32, 100)")
#client.execute("INSERT INTO my_table (s) VALUES ('1 foo')")
##client.execute("ALTER TABLE my_table ADD COLUMN f Float64")
#client.execute("INSERT INTO my_table (s) VALUES ('2. bar')")

#LS = client.execute("SELECT * FROM my_table")
#print (len(LS), LS)

#C = CUSTOMER() # Покупатели
#P = PRODUCT() # Продукты
#PN = PRODUCTNAME() # Категории
#O = ORDER() # Покупки
#see_stat(PN)

def create_file_arr():
    p_open = PRODUCT() #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount'] 
    #[188860582.0, 7290001201596.0, 1.0, 10.4, 0.0]
    product_arr = p_open.to_numpy()


    o_open = ORDER() #['Order_Id', 'Branch_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged', 'Order_Date']  
    order_arr = o_open.to_numpy()
    ids_order = func_return(order_arr, 0)

#---------------------------------------------->
    product_name = PRODUCTNAME() #[ ID, Product_Id, LocalName, Category1_Id, Category1_Name, Category2_Id, Category2_Name] 
    product_name_arr = product_name.to_numpy()
    ids_product_name = func_return(product_name_arr, 1)
    
    start = time.time()
    for i in range(product_arr.shape[0]):
        #_order_id = product_arr[i,0]
        _order = order_arr[ids_order[product_arr[i,0]],:][0]
        try:
            _category = product_name_arr[ids_product_name[product_arr[i,1]],:][0]
        except KeyError:
            print (product_arr[i,1])
            _category = [0,0,0,0,0,0]
            
        new_arr = [int(product_arr[i,0]), int(product_arr[i,1]), product_arr[i,2], product_arr[i,3], product_arr[i,4], _order[1], _order[2], _order[-1], _category[3], _category[5]]
        #print (new_arr)
        client.execute(f"""INSERT INTO my_table 
                        (Order_ID, Product_ID, Items_Count, Total_Amount, TotalDiscount, Branch_Id, Customer_Id, Order_Date, Category1_Id, Category2_Id) 
                        VALUES 
                        ({product_arr[i,0]}, {product_arr[i,1]}, {product_arr[i,2]}, {product_arr[i,3]}, {product_arr[i,4]}, 
                         {_order[1]}, {_order[2]}, '{_order[-1]}', {_category[3]}, {_category[5]})
                        """)
    print (time.time()-start)                        
#                        {int(product_arr[i,0])} {int(product_arr[i,1])} {float(product_arr[i,2])} {float(product_arr[i,3])} {float(product_arr[i,4])} {int(_order[1])} {int(_order[2])} {str(_order[-1])} {int(_category[3])} {int(_category[5])}
#        print (product_arr[i,:].tolist(),
#               "\n",
#               _order.tolist(),
#               "\n",
#               _category,
#               "\n",
#               "\n......................"
#               )

create_file_arr()


# product ['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount', 'Branch_Id', 'Customer_Id', 'Order_Date', 'Category1_Id', 'Category2_Id']


"""
Нужно искать в таблицах общий ID
https://clickhouse.tech/docs/ru/sql-reference/statements/create/view/ - События
https://cloud.yandex.ru/docs/managed-clickhouse/operations/insert
https://habr.com/ru/post/539538/
https://habr.com/ru/post/509540/
https://habr.com/ru/company/oleg-bunin/blog/551572/
https://readthedocs.org/projects/clickhouse-driver/downloads/pdf/latest/
https://gist.github.com/hatarist/5e7653808e59349c34d4589b2fc69b14
Мне нужно запихнуть все данные в одну строку для создания колоночной бд
CREATE DATABASE yourdbname;
CREATE USER youruser WITH ENCRYPTED PASSWORD 'yourpass';
CREATE USER newuser WITH LOGIN ENCRYPTED PASSWORD '1234';
GRANT ALL PRIVILEGES ON DATABASE yourdbname TO youruser;
DROP DATABASE [IF EXISTS] database_name;
https://www.postgresqltutorial.com/postgresql-list-users/
DROP USER [USERNAME];
\du
\l+
https://tableplus.com/blog/2018/04/postgresql-how-to-grant-access-to-users.html
https://stackoverflow.com/questions/22483555/postgresql-give-all-permissions-to-a-user-on-a-postgresql-database
https://gist.github.com/pierrejoubert73/85b3ce8b52e7f6dbce69e2636f68383f
https://chartio.com/resources/tutorials/how-to-change-a-user-to-superuser-in-postgresql/
https://stackoverflow.com/questions/2732474/restore-a-postgres-backup-file-using-the-command-line

git add .
git commit -m 'update'
git push --set-upstream origin v0.2

CREATE ROLE name;
ALTER USER name CREATEDB REPLICATION CREATEROLE BYPASSRLS LOGIN;
ALTER USER name CREATEDB;
ALTER USER name REPLICATION;
ALTER USER name CREATEROLE;
ALTER USER name BYPASSRLS;
ALTER USER name LOGIN;
ALTER USER name WITH SUPERUSER;

pg_restore -d b24online b24online.com-2021-04-26.psql - перед этим создаю бд и роль с именем совпадающим в бд
pg_restore b24online.com-2021-04-26.psql - старая версия, создаю роль в бд с именем супер пользователя, назначаю привелегии, из консоли автоматически создается

\c name_db
\dt смотрю все таблици

"""
