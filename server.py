# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.websocket
import cv2
import numpy as np
import os, sys
import base64, json, time

import dbhandler
from temp import heatmap_vis

DB = dbhandler.DataBase()

MONTHS = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December'
]

class ImageWebSocket(tornado.websocket.WebSocketHandler):
    clients = set()
    
    def check_origin(self, origin):
        # Allow access from every origin
        return True

    def open(self):
        ImageWebSocket.clients.add(self)
        print("WebSocket opened from: " + self.request.remote_ip)

    def on_message(self, message):
        print ("Info fro JS", message)
        try:
            message = json.loads(message)
        except:
            pass 
        
        if message["to"] == "show_tables":
            self.write_message(json.dumps({"from":"show_tables", "data":DB.show_tables()}))
        if message["to"] == "show_user":
            _temp = DB.client.execute(f"""   
                                            SELECT
                                              SUM(Items_Count) as sum1, 
                                              SUM(Total_Amount) as sum2,
                                              Customer_Id
                                            FROM test
                                            GROUP BY Customer_Id
                                            ORDER BY sum1
                                            {message["asc_desc"]}
                                          
                                          """)
#                                          LIMIT 20
#                                          OFFSET 10   
                                          #ASC
                                          #DESC
            self.write_message(json.dumps({"from":"show_user", "data":_temp}))
            
            
        if message["to"] == "show_category1":
#                H = DB.client.execute(f"""
#                            SELECT * FROM category1 
#                            order by sum  
#                            DESC
#                            LIMIT 50
#                            OFFSET 0                                                              
#                            """)
#                self.write_message(json.dumps({"from":"show_category1", "data":H}))
                H = DB.client.execute(f"""
                            SELECT * FROM category1 
                            order by sum  
                            DESC
                            LIMIT 50
                            OFFSET 0                                                              
                            """)
                self.write_message(json.dumps({"from":"show_category1", "data":H}))


        if message["to"] == "show_category2":
                H = DB.client.execute(f"""
                            SELECT * FROM category2 
                            order by sum  
                            DESC        
                            LIMIT 50
                            OFFSET 0                      
                            """)
                self.write_message(json.dumps({"from":"show_category1", "data":H}))

                
                
        if message["to"] == "show_script_SQL":
                H = DB.client.execute(f"""{message["data"]}""")
                self.write_message(json.dumps({"from":"script_SQL","data":H}))

        if message["to"] == "show_product":
                H = DB.client.execute(f"""
                            SELECT
                                 count(Product_ID) as SM1,
                                 Product_ID
                            FROM test 
                            GROUP BY Product_ID
                            ORDER BY SM1
                            DESC
                            """)
                self.write_message(json.dumps({"from":"show_product", "data":H}))


        if message["to"] == "sort_category_by_user_id_rt":                
                    H = DB.client.execute(f"""   
                                                    SELECT
                                                      SUM(Items_Count) as sum1, 
                                                      SUM(Total_Amount) as sum2,
                                                      Category1_Id
                                                    FROM test
                                                    WHERE test.Customer_Id = {message["data"]} 
                                                    GROUP BY Category1_Id
                                                    ORDER BY sum1
                                                    DESC

                                                """)
#                                                    LIMIT 20
#                                                    OFFSET 0 
                    self.write_message(json.dumps({"from":"sort_category_by_user_id_rt", "data":H})) 
                    
        if message["to"] == "sort_product_by_user_id_and_category_rt":         
            t = DB.client.execute(f"""
                                    SELECT 
                                        SUM(Items_Count) as sum1, 
                                        SUM(Total_Amount) as sum2,
                                        Product_ID
                                    FROM test
                                    WHERE test.Customer_Id = {message["data"]["id_user"]} 
                                    AND test.Category1_Id = {message["data"]["id_category"]}
                                    GROUP BY Product_ID
                                    ORDER BY sum1
                                    DESC
                                    """)            
            self.write_message(json.dumps({"from":"sort_product_by_user_id_and_category_rt", "data":t}))  
              
        if message["to"] == "sort_product_by_user_id_rt":
                    t = DB.client.execute(f"""   
                                            SELECT
                                            *
                                            FROM test
                                            WHERE test.Customer_Id = {message['data']}
                                            ORDER BY Items_Count
                                            DESC 
                                            LIMIT 20
                                            OFFSET 0 
                                            
                                          """)
                    start = time.time()
                    dict_ = {}
                    for iz in t:
                        count = iz[2]
                        p_id = iz[1]
                        t_sum = iz[3]
                        d_month = iz[7].split(" ")[0].split("-")[1]
                        c_id = iz[6]
                        try:
                            dict_[p_id][d_month][0] += count
                            dict_[p_id][d_month][1] += t_sum
                        except KeyError:
                            dict_[p_id] = {'01':[0,0,0], '02':[0,0,0], '03':[0,0,0], '04':[0,0,0], '05':[0,0,0], '06':[0,0,0], '07':[0,0,0], '08':[0,0,0], '09':[0,0,0], '10':[0,0,0], '11':[0,0,0], '12':[0,0,0]}
                            dict_[p_id][d_month][0] += count
                            dict_[p_id][d_month][1] += t_sum
                    self.write_message(json.dumps({"from":"sort_product_by_user_id_rt", "data":dict_}))     
                                              
        if message["to"] == "sort_category_by_":                                                              
                    ZS = DB.client.execute(f"""   
                                                    SELECT
                                                      SUM(Items_Count) as sum1, 
                                                      SUM(Total_Amount) as sum2,
                                                      Category1_Id
                                                    FROM test
                                                    WHERE test.Customer_Id = {message["id1"]} 
                                                    AND test.Category1_Id = {message["id2"]}
                                                    GROUP BY Category1_Id
                                                """)           
                                                
                                   
        if message["to"] == "sort_product_id_user_id":
                dict_ = DB.client.execute(f"""  
                                    SELECT
                                       SUM(columns.sum1) as s1,
                                       SUM(columns.sum2) as S2,
                                       columns.time
                                    FROM
                                    (SELECT
                                    toMonth(Order_Date) as time,
                                    SUM(Items_Count) as sum1,
                                    SUM(Total_Amount) as sum2
                                    FROM test
                                    WHERE Customer_Id = {message["data"]["id_user"]}
                                    AND Product_ID = {message["data"]["id_product"]}
                                    GROUP BY Order_Date) columns
                                    GROUP BY columns.time
                                    ORDER BY columns.time
                                    ASC
                                            """)#ORDER BY Items_Count   AND Category1_Id = 500
                self.write_message(json.dumps({"from":"sort_product_id_user_id", "data":dict_}))   

        if message["to"] == "show_correlation":
            print (message)
            T = DB.client.execute(f"""
                                    SELECT
                                         Order_ID, 
                                         Product_ID, 
                                         Items_Count, 
                                         Total_Amount, 
                                         Customer_Id,
                                         toMonth(Order_Date) as time
                                    FROM test
                                    WHERE test.Customer_Id = {message["data"]["id_user"]} 
                                    AND test.Product_ID = {message["data"]["id_product"]}
                                    """)    
            G = {}
            t_str = ""
            t_count = 0
            G[message["data"]["id_product"]] = [0,0,0,0,0,0,0,0,0,0,0,0]
            ixz = 0
            LS = []
            for batch_idx, i in enumerate(T):
                if batch_idx % 100 == 0:
                    t_str += f"OR test.Order_ID = {i[0]}\n"
                    t_count += i[2]
                    G[message["data"]["id_product"]][(i[-1])] += i[2]
                    ixz += 1
                    a = DB.client.execute(f"""
                                    SELECT
                                         Order_ID, 
                                         Product_ID, 
                                         Items_Count, 
                                         Total_Amount, 
                                         Customer_Id,
                                         toMonth(Order_Date) as time
                                    FROM test
                                    WHERE test.Customer_Id = {message["data"]["id_user"]}
                                    AND NOT test.Product_ID = {message["data"]["id_product"]}
                                    AND ({t_str[3:]})
                                    
                                    """)
                    LS += a 
            a = LS                                            
            dict_data = {}   
            P1 = t_count   
            for r in a:
                try:
                    dict_data[r[1]][0][(r[-1])] += r[2]  
                    dict_data[r[1]][1] += r[2]
                except KeyError:
                    dict_data[r[1]] = [[0,0,0,0,0,0,0,0,0,0,0,0], 0] 
                    dict_data[r[1]][0][(r[-1])] += r[2]
                    dict_data[r[1]][1] += r[2]  
                #print (r[-1])  

            for r in dict_data:
                P2 = dict_data[r][1]
                P = (P2/P1)*100  
                if P > 5:  
                    G[r] = dict_data[r][0]  
                    
                    
            self.write_message(json.dumps({"from":"show_correlation", "data":G})) 
        if message["to"] == "show_correlation_product":
            T = DB.client.execute(f"""
                                    SELECT
                                        SUM(Items_Count) as IC,
                                        toMonth(Order_Date) as time
                                    FROM test
                                    WHERE test.Product_ID = {message["data"]["id_product"]} 
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
                                    WHERE test.Product_ID = {message["data"]["id_product"]}
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
            ID_s.append(message["data"]["id_product"])
            for k in D:
                #print (np.mean(Z), np.mean(np.array(list(D[k].values()))))
                P = np.mean(np.array(list(D[k].values()))) / np.mean(Z) * 100.
                if P > 10:
                    print (Z, np.array(list(D[k].values())), np.mean(Z), np.mean(np.array(list(D[k].values()))))
                    T_data0.append(np.array(list(D[k].values())))
                    ID_s.append(k)        
            T_data0 = np.array(T_data0)
            corr_0 = np.corrcoef(T_data0)
            corr_0 = tuple(corr_0.tolist())
            #print (corr_0.shape, corr_0.size, ID_s) 
            #heatmap_vis(corr_0, ID_s, f"ic_heatmap_{message['data']['id_product']}.jpg")  
                        
            self.write_message(json.dumps({"from":"show_correlation_product", "data":[corr_0, tuple(ID_s)]}))

        if message["to"] == "sort_product_id":
                T = DB.client.execute(f"""
                        SELECT
                           count(columns.sum1) as s1,
                           columns.time
                        FROM
                        (SELECT
                        toMonth(Order_Date) as time,
                        count(Product_ID) as sum1
                        FROM test
                        WHERE Product_ID = {message["data"]["id_product"]}
                        GROUP BY Order_Date) columns
                        GROUP BY columns.time
                        ORDER BY columns.time
                        ASC    
                                            
                        """)  
                self.write_message(json.dumps({"from":"sort_product_id", "data":T})) 


        if message["to"] == "sort_product_id_month":
                M = message['data']['month']
                T = DB.client.execute(f"""
                                    SELECT
                                       SUM(columns.Items_Count) as s1,
                                       SUM(columns.Total_Amount) as S2,
                                       columns.time_day
                                    FROM
                                    (SELECT
                                        toMonth(Order_Date) as time,
                                        toDayOfMonth(Order_Date) as time_day,
                                        Items_Count,
                                        Total_Amount
                                    FROM test
                                    WHERE Product_ID = {message["data"]["id_product"]}
                                    AND time = {MONTHS.index(M)+1}
                                    ORDER BY time_day) columns
                                    GROUP BY columns.time_day
                                    """)    
                self.write_message(json.dumps({"from":"sort_product_id_month", "data":T}))                                            
        if message["to"] == "sort_product_id_month_day":   
                #print (message)
                M = message['data']['month']
                T = DB.client.execute(f"""
                   SELECT
                       SUM(columns.Items_Count) as s1,
                       SUM(columns.Total_Amount) as S2,
                       columns.time_hour
                   FROM    
                   (SELECT
                        toMonth(Order_Date) as time,
                        toDayOfMonth(Order_Date) as time_day,
                        toHour(Order_Date) as time_hour,
                        Items_Count,
                        Total_Amount
                    FROM test
                    WHERE Product_ID = {message["data"]["id_product"]}
                    AND time = {MONTHS.index(M)+1}
                    AND time_day = {message["data"]["day"]}
                    ORDER BY time_day) columns
                    GROUP BY columns.time_hour
                    """)  
                self.write_message(json.dumps({"from":"sort_product_id_month_day", "data":T}))
                
        if message["to"] == "sort_product_id_user_id_month":                  
                #print (message) 
                M = message['data']['month']
                T = DB.client.execute(f"""
                    SELECT
                       SUM(columns.Items_Count) as s1,
                       SUM(columns.Total_Amount) as S2,
                       columns.time_day
                    FROM    
                    (SELECT
                        toMonth(Order_Date) as time,
                        toDayOfMonth(Order_Date) as time_day,
                        Items_Count,
                        Total_Amount
                    FROM test
                    WHERE Product_ID = {message["data"]["id_product"]}
                    AND Customer_Id = {message["data"]["id_user"]}
                    AND time = {MONTHS.index(M)+1}
                    ORDER BY time) columns
                    GROUP BY columns.time_day
                    """)         
                self.write_message(json.dumps({"from":"sort_product_id_user_id_month", "data":T}))  
        if message["to"] == "sort_product_id_user_id_month_day":                 
                M = message['data']['month']
                T = DB.client.execute(f"""
                   SELECT
                       SUM(columns.Items_Count) as s1,
                       SUM(columns.Total_Amount) as S2,
                       columns.time_hour
                   FROM    
                   (SELECT
                        toMonth(Order_Date) as time,
                        toDayOfMonth(Order_Date) as time_day,
                        toHour(Order_Date) as time_hour,
                        Items_Count,
                        Total_Amount
                    FROM test
                    WHERE Product_ID = {message["data"]["id_product"]}
                    AND Customer_Id = {message["data"]["id_user"]}
                    AND time = {MONTHS.index(M)+1}
                    AND time_day = {message["data"]["day"]}
                    ORDER BY time_day) columns
                    GROUP BY columns.time_hour
                    """)  
                self.write_message(json.dumps({"from":"sort_product_id_user_id_month_day", "data":T}))                 
#                        SELECT
#                           SUM(columns.Items_Count) as s1,
#                           SUM(columns.Total_Amount) as S2,
#                           columns.time_day
#                       FROM    
#                       (SELECT
#                            toMonth(Order_Date) as time,
#                            toDayOfMonth(Order_Date) as time_day,
#                            Items_Count,
#                            Total_Amount
#                        FROM test
#                        WHERE Product_ID = 7290004127329
#                        AND Customer_Id = 0
#                        AND time = 9
#                        ORDER BY time) columns
#                        GROUP BY columns.time_day               
                
                                      
    def on_close(self):
        ImageWebSocket.clients.remove(self)
        print("WebSocket closed from: " + self.request.remote_ip)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index_ex.html", title="Нейронная сеть/Тренировка")

app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/websocket", ImageWebSocket),
        (r"/(chart.min.js)", tornado.web.StaticFileHandler, {'path':'./node_modules/chart.js/dist/'}),
        (r"/(pv_layer_controls.png)", tornado.web.StaticFileHandler, {'path':'./'})
    ])
app.listen(8800)
tornado.ioloop.IOLoop.current().start()

