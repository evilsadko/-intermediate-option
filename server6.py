# -*- coding: utf-8 -*-
##import ctypes
import tornado.ioloop
import tornado.web
import tornado.websocket

import cv2
import numpy as np

import os, sys
import base64, json, time

import dbhandler_2




DB = dbhandler_2.DataBase()
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
            print (DB.show_tables())
            #self.write_message("from python")#, binary=True
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
            print (_temp, len(_temp), message["offset"], message["limit"])
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
                            SELECT * FROM category1 
                            order by sum                               
                            """)
                test_data = np.array(H[200][2]) 
                res = test_data.reshape((test_data.shape[0], 1))               
                print (test_data.shape[0], res.shape, res[:,:])  
                self.write_message(json.dumps({"from":"show_category1", "data":H}))


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
                    print (H)
                    self.write_message(json.dumps({"from":"sort_category_by_user_id_rt", "data":H})) 
                    
        if message["to"] == "sort_product_by_user_id_and_category_rt":         
#            t = DB.client.execute(f"""   
#                                                    SELECT *
#                                                    FROM my_table
#                                                    WHERE my_table.Customer_Id = {message["data"]["id_user"]} 
#                                                    AND my_table.Category1_Id = {message["data"]["id_category"]}
#                                                    ORDER BY Items_Count
#                                                """)   
#            #print (len(t)) 
#            dict_ = {}
#            for iz in t:
#                count = iz[2]
#                p_id = iz[1]
#                t_sum = iz[3]
#                d_month = iz[7].split(" ")[0].split("-")[1]
#                c_id = iz[6]
#                #print (c_id, iz[7], d_month, count, t_sum, p_id) 
#                try:
#                    dict_[p_id][d_month][0] += count
#                    dict_[p_id][d_month][1] += t_sum
#                except KeyError:
#                    dict_[p_id] = {'01':[0,0,0], '02':[0,0,0], '03':[0,0,0], '04':[0,0,0], '05':[0,0,0], '06':[0,0,0], '07':[0,0,0], '08':[0,0,0], '09':[0,0,0], '10':[0,0,0], '11':[0,0,0], '12':[0,0,0]}
#                    dict_[p_id][d_month][0] += count
#                    dict_[p_id][d_month][1] += t_sum
#            print (len(dict_))
#            self.write_message(json.dumps({"from":"sort_product_by_user_id_and_category_rt", "data":dict_}))    

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
            print (t)
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

                    #print ("sort_product_by_user_id_rt",len(t))
                    start = time.time()
                    dict_ = {}
                    for iz in t:
                        count = iz[2]
                        p_id = iz[1]
                        t_sum = iz[3]
                        d_month = iz[7].split(" ")[0].split("-")[1]
                        c_id = iz[6]
                        #print (c_id, iz[7], d_month, count, t_sum, p_id) 
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
                                                
         #                                          
        if message["to"] == "sort_related_products":
                H = DB.client.execute(f"""
                            SELECT * FROM sort_related_products 
                            order by sum                               
                            """)
                test_data = np.array(H[200][2]) 
                res = test_data.reshape((test_data.shape[0], 1))               
                print (test_data.shape[0], res.shape, res[:,:])  
                self.write_message(json.dumps({"from":"sort_related_products", "data":H}))                         
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
                print (dict_)                             
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
#            print (ixz)
                   
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
#                    LS.append(a[:])
                    LS += a 
                    
            a = LS                                            
            print ("!@#>>>>>>>>>>>>>>>",LS, len(LS))
            dict_data = {}   
            #print (a)  
            #A = {}
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
                    #print (dict_data[r], P, P1, P2)    
            #print (G)
            
                            
            self.write_message(json.dumps({"from":"show_correlation", "data":G})) 

    def on_close(self):
        ImageWebSocket.clients.remove(self)
        print("WebSocket closed from: " + self.request.remote_ip)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index_4.html", title="Нейронная сеть/Тренировка")

app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/websocket", ImageWebSocket),
        (r"/(chart.min.js)", tornado.web.StaticFileHandler, {'path':'./node_modules/chart.js/dist/'}),
    ])
app.listen(8800)

print("Starting server: http://xxx.xx.xx.xxx:8800/") # IP

tornado.ioloop.IOLoop.current().start()

##https://tobiasahlin.com/blog/chartjs-charts-to-get-you-started/

#import dbhandler_2
#DB = dbhandler_2.DataBase()
#t = DB.client.execute(f"""  
#                            SELECT
#                               columns.time,
#                               SUM(columns.sum1) as s1,
#                               SUM(columns.sum2) as S2
#                            FROM
#                            (SELECT
#                            toMonth(Order_Date) as time,
#                            SUM(Items_Count) as sum1,
#                            SUM(Total_Amount) as sum2
#                            FROM test
#                            WHERE Customer_Id = 0 
#                            AND Product_ID = 72940761.0
#                            AND Category1_Id = 500
#                            GROUP BY Order_Date) columns
#                            GROUP BY columns.time
#                            ORDER BY columns.time
#                            """)#ORDER BY Items_Count
#                                                
#print (t[0], t[-1], len(t))#AND test.Category1_Id = 500

#('2020-01-01 00:04:00.000', 10.0, 29.4) 
#('2020-10-06 10:28:00.000', 4.0, 12.399999999999999)
