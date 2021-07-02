import threading
from utils import *
import dbhandler
import matplotlib.pyplot as plt
import matplotlib.dates as dates

DB = dbhandler.DataBase()

def heatmap_vis(x, y, name):
    fig, ax = plt.subplots()
    im = ax.imshow(x)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(y)))
    ax.set_yticks(np.arange(len(y)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(y)
    ax.set_yticklabels(y)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(x.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(x.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    # Loop over data dimensions and create text annotations.
    for z in range(len(y)):
        for j in range(len(y)):
            text = ax.text(j, z, round(x[z, j], 1), ha="center", va="center", color="w")

    ax.set_title("Зависемость продуктов")
    fig.tight_layout()
    #plt.show()
    fig.savefig(name)    
    fig.clear(True)
    plt.close(fig)
if __name__ == "__main__":
    
#    P = PRODUCT()
#    A = P.loc[P['Product_ID'] == 554815] #554815 #313528
#    O = ORDER()
#    
#    #554815
#    #print (A)
#    A = A.to_numpy()
#    cats = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
#    M = {'01':0, '02':0, '03':0, '04':0, '05':0, '06':0, '07':0, '08':0, '09':0, '10':0, '11':0, '12':0}
#    for i in A:
#        OID = i[0]
#        
#        O_t = O.loc[O['Order_Id'] == OID]
#        data = O_t.to_numpy()[0][-1]
#        s_mon = data.split(" ")[0].split("-")[1]
#        M[s_mon] += 1 #i[3]
#        print (i[1], OID, data, s_mon)
#        #print (OID,list(i), len(cats))
#    print (M)   

#    T = DB.client.execute(f"""
#            SELECT
#               count(columns.sum1) as s1,
#               columns.time
#            FROM
#            (SELECT
#            toMonth(Order_Date) as time,
#            count(Product_ID) as sum1
#            FROM my_table
#            WHERE Product_ID = 554815
#            GROUP BY Order_Date) columns
#            GROUP BY columns.time
#            ORDER BY columns.time
#            ASC    
#            """)  # test


#    T = DB.client.execute(f"""
#            SELECT
#                toMonth(Order_Date) as time
#            FROM test
#            WHERE Product_ID = 554815
#            """) #554815 #313528
#    #print (T)
#    #M = {'01':0, '02':0, '03':0, '04':0, '05':0, '06':0, '07':0, '08':0, '09':0, '10':0, '11':0, '12':0}
#    M = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}
#    for i in T:
#        #data = i[-3]
#        #s_mon = data.split(" ")[0].split("-")[1]
#        #print (data, s_mon)
#        s_mon = i[0]
#        M[s_mon] += 1#i[2]
#--------------------------------->
#    T = DB.client.execute(f"""
#            SELECT
#               count(columns.sum1) as s1,
#               columns.time
#            FROM
#            (SELECT
#            toMonth(Order_Date) as time,
#            count(Product_ID) as sum1
#            FROM test
#            WHERE Product_ID = 554815
#            GROUP BY Order_Date) columns
#            GROUP BY columns.time
#            ORDER BY columns.time
#            ASC    
#                                
#            """)      
#                                             SUM(Items_Count) as IC, 
#                                 SUM(Total_Amount) as TA, 
#                                 toMonth(Order_Date) as time






#    T = DB.client.execute(f"""
#             SELECT 
#                Items_Count,
#                Product_ID,
#                Order_ID,
#                toMonth(Order_Date) as time
#               FROM test
#               WHERE Items_Count > (
#                 SELECT AVG(Items_Count)
#                   FROM test
#                   WHERE Order_ID = Order_ID);
#                            """) 

    #Получить сопутствующий продукты
#    T = DB.client.execute(f"""
#                            SELECT
#                                 Order_ID, 
#                                 Product_ID, 
#                                 Items_Count, 
#                                 Total_Amount, 
#                                 Customer_Id,
#                                 toMonth(Order_Date) as time
#                            FROM test
#                            WHERE test.Product_ID = 554815
#                            """)   
    T = DB.client.execute(f"""
                            SELECT
                                SUM(Items_Count) as IC,
                                toMonth(Order_Date) as time
                            FROM test
                            WHERE test.Product_ID = 554815 
                            GROUP BY time
                            """) 
    Z = np.array(T)[:,0]
    print (np.array(T)[:,0])
                             
    T = DB.client.execute(f"""
             SELECT 
                Items_Count,
                Product_ID,
                Order_ID,
                toMonth(Order_Date) as time
               FROM test              
               WHERE Order_ID IN (                        
                            SELECT
                                 Order_ID
                            FROM test
                            WHERE test.Product_ID = 554815
                           )
                            """)    
    D = {}  
    #print (T)                       
    for k in T:
        try:
            D[k[1]][k[-1]] += k[0]
            #print (k[1], D[k[1]])
        except KeyError:
            D[k[1]] = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}
            D[k[1]][k[-1]] += k[0]
    #print (len(D), D)
    T_data0 = []
    ID_s = []
    
    T_data0.append(Z)
    ID_s.append(554815)
    for k in D:
        #print (np.mean(Z), np.mean(np.array(list(D[k].values()))))
        P = np.mean(np.array(list(D[k].values()))) / np.mean(Z) * 100.
        if P > 10:
            print (Z, np.array(list(D[k].values())), np.mean(Z), np.mean(np.array(list(D[k].values()))))
            T_data0.append(np.array(list(D[k].values())))
            ID_s.append(k)        
    T_data0 = np.array(T_data0)
    corr_0 = np.corrcoef(T_data0) 
    #heatmap_vis(corr_0, ID_s, f"ic_heatmap_554815.jpg")   
    print (corr_0.shape, len(ID_s))
                           
#    T = DB.client.execute(f"""
#            SELECT
#               count(columns.sum1) as s1,
#               columns.time
#            FROM
#            (SELECT
#            toMonth(Order_Date) as time,
#            count(Product_ID) as sum1
#            FROM my_table
#            WHERE Product_ID = 554815
#            GROUP BY Order_Date) columns
#            GROUP BY columns.time
#            ORDER BY columns.time
#            ASC    
#            """)  # test     

                       
#    WHERE Product_ID = 554815


#    G = {}
#    t_str = ""
#    t_count = 0
#    G[554815] = [0,0,0,0,0,0,0,0,0,0,0,0]
#    ixz = 0
#    LS = []
#    for batch_idx, i in enumerate(T):
#        if batch_idx % 100 == 0:
#            t_str += f"OR test.Order_ID = {i[0]}\n"
#            t_count += i[2]
#            G[554815][(i[-1])] += i[2]
#            ixz += 1
#            a = DB.client.execute(f"""
#                            SELECT
#                                 Order_ID, 
#                                 Product_ID, 
#                                 Items_Count, 
#                                 Total_Amount, 
#                                 Customer_Id,
#                                 toMonth(Order_Date) as time
#                            FROM test
#                            WHERE NOT test.Product_ID = 554815
#                            AND ({t_str[3:]})
#                            
#                            """)
#            LS += a 
#    a = LS                                            
#    dict_data = {}   
#    P1 = t_count   
#    for r in a:
#        try:
#            dict_data[r[1]][0][(r[-1])] += r[2]  
#            dict_data[r[1]][1] += r[2]
#        except KeyError:
#            dict_data[r[1]] = [[0,0,0,0,0,0,0,0,0,0,0,0], 0] 
#            dict_data[r[1]][0][(r[-1])] += r[2]
#            dict_data[r[1]][1] += r[2]  
#        #print (r[-1])  

#    for r in dict_data:
#        P2 = dict_data[r][1]
#        P = (P2/P1)*100  
#        if P > 5:  
#            G[r] = dict_data[r][0]  
            
             
    print (len(T))
#    


#https://www.sqlservertutorial.net/sql-server-basics/sql-server-correlated-subquery/
#https://coderoad.ru/1555051/SQL-%D0%BA%D0%BE%D1%80%D1%80%D0%B5%D0%BB%D1%8F%D1%86%D0%B8%D1%8F
#https://coderoad.ru/23415492/%D0%9A%D0%BE%D1%8D%D1%84%D1%84%D0%B8%D1%86%D0%B8%D0%B5%D0%BD%D1%82-%D0%9A%D0%BE%D1%80%D1%80%D0%B5%D0%BB%D1%8F%D1%86%D0%B8%D0%B8-%D0%9F%D0%B8%D1%80%D1%81%D0%BE%D0%BD%D0%B0-SQL-Server
#https://habr.com/ru/post/512304/
#https://github.com/linyue515/ClickHouse-1/blob/master/docs/en/query_language/agg_functions/reference.md


#https://github.com/ClickHouse/ClickHouse/issues/1777



#https://academy-of-capital.ru/blog/soputstvuyushchie-tovary/
#https://habr.com/ru/company/datawiz/blog/241738/
#https://habr.com/ru/company/retailrocket/blog/441366/

#https://github.com/mourner/simpleheat/blob/gh-pages/simpleheat.js
