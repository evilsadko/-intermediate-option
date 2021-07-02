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



                        
                          
            
    def on_close(self):
        ImageWebSocket.clients.remove(self)
        print("WebSocket closed from: " + self.request.remote_ip)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index_t.html", title="Нейронная сеть/Тренировка")

app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/websocket", ImageWebSocket),
        (r"/(chart.min.js)", tornado.web.StaticFileHandler, {'path':'./node_modules/chart.js/dist/'})
    ])
app.listen(8800)
tornado.ioloop.IOLoop.current().start()

