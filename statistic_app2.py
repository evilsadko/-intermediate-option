import threading
from utils import *
from dbhandler_2 import *




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

def table_category():
    D.delete("category1")
    D.client.execute(f"""
                        CREATE TABLE category1
                        (Category1_ID Int64,
                         sum Int64,
                         floats Array(Float64))
                        ENGINE = MergeTree()
                        ORDER BY Category1_ID
                     """)
    D.show_tables()
    test_file = open("out/category.json", "r").readlines()
    readsss = json.loads(test_file[0])

    print (len(list(readsss.keys())))
    
    for o in readsss:
        #np.array(list(readsss[o].values())
        D.client.execute(f"""
                            INSERT INTO category1 
                              (floats, Category1_ID, sum) 
                            VALUES ({str(list(readsss[o].values()))}, {o}, {str(sum(list(readsss[o].values())))})
                         """)
#        print (f"""
#                            INSERT INTO category1 
#                              (floats, Category1_ID) 
#                            VALUES {str(list(readsss[o].values()))}, {o}
#                         """)
        print (o, str(np.array(list(readsss[o].values()), dtype=np.float64)), list(readsss[o].values()), sum(list(readsss[o].values())))


if __name__ == "__main__":
    D = DataBase()
    #table_category()
    print (D.show_tables())  
#    test_file = open("out/sort_by_point.json", "r").readlines()
#    readsss = json.loads(test_file[0])

#    print (len(list(readsss.keys())))    
#    for o in readsss:
#        print (o, readsss[o])


#    D.delete("category1")
#    D.client.execute(f"""
#                        CREATE TABLE category1
#                        (Category1_ID Int64,
#                         sum Int64,
#                         floats Array(Float64))
#                        ENGINE = MergeTree()
#                        ORDER BY Category1_ID
#                     """)
#    files = open ("out/1_create_file_arr.txt", "r")#.read()
#    for o in files:
#        JS = json.loads(o.split("\n")[0])
    H = D.client.execute(f"""
                            SELECT * FROM category1 
                            order by sum                               
                         """)
    test_data = np.array(H[200][2]) 
    res = test_data.reshape((test_data.shape[0], 1))               
    print (test_data.shape[0], res.shape, res[:,:])              
        #print (len(list(JS.keys())), list(JS.keys())[0], JS[list(JS.keys())[0]])
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


