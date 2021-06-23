# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.websocket
import cv2
import numpy as np
import os, sys
import base64, json, time

import dbhandler

DB = dbhandler.DataBase()

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
                                            FROM my_table
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
                                                    FROM my_table
                                                    WHERE my_table.Customer_Id = {message["data"]} 
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
                                    FROM my_table
                                    WHERE my_table.Customer_Id = {message["data"]["id_user"]} 
                                    AND my_table.Category1_Id = {message["data"]["id_category"]}
                                    GROUP BY Product_ID
                                    ORDER BY sum1
                                    DESC
                                    """)            
            self.write_message(json.dumps({"from":"sort_product_by_user_id_and_category_rt", "data":t}))  
              
        if message["to"] == "sort_product_by_user_id_rt":
                    t = DB.client.execute(f"""   
                                            SELECT
                                            *
                                            FROM my_table
                                            WHERE my_table.Customer_Id = {message['data']}
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
                                                    FROM my_table
                                                    WHERE my_table.Customer_Id = {message["id1"]} 
                                                    AND my_table.Category1_Id = {message["id2"]}
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

                        
                          
            
    def on_close(self):
        ImageWebSocket.clients.remove(self)
        print("WebSocket closed from: " + self.request.remote_ip)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", title="Нейронная сеть/Тренировка")

app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/websocket", ImageWebSocket),
        (r"/(chart.min.js)", tornado.web.StaticFileHandler, {'path':'./node_modules/chart.js/dist/'}),
    ])
app.listen(8800)
tornado.ioloop.IOLoop.current().start()

