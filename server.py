# -*- coding: utf-8 -*-
#import ctypes
import tornado.ioloop
import tornado.web
import tornado.websocket

import cv2
import numpy as np

import os, sys
import base64, json, time

import dbhandler_2


#lib = ctypes.cdll.LoadLibrary('./lib.so')
#lib.bar()
#W = lib.getW()
#H = lib.getH()
#def imgbite():
#           res = np.zeros(dtype=np.uint8, shape=(H, W, 4))
#           lib.fdata(res.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte)))
#           _, img_str = cv2.imencode('.jpg', res)
#           BS = img_str.tobytes()
#           return BS



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
#            DB.client.execute(f"""   
#                                        FROM test GROUP BY Customer_Id ORDER BY Customer_Id
#                                      """)
            _temp = DB.client.execute("""
                                        SELECT Customer_Id, SUM(Items_Count) AS ass_sum FROM test GROUP BY Customer_Id ORDER BY ass_sum DESC
                                      """)    #GROUP BY Customer_Id ORDER BY ass_sum   
            print (len(_temp), _temp[0], _temp[100], _temp[-1])      
            arr = np.array(_temp)
            print(arr.shape, arr[0,1])
            self.write_message(json.dumps({"from":"show_user", "data":_temp}))
            
            
#        if message["to"] == "show_user_id":
#            print ("id", message["data"])
#            print (DB.client.execute(f"""   
#                                        SELECT
#                                          my_table.Customer_Id
#                                        FROM my_table
#                                        WHERE my_table.Customer_Id = {i[0]}
#                                      """))    
#            temp_dict = {"to":"<<<<<DSD","data":"OKOI"}
#            self.write_message(json.dumps(temp_dict))
            
#        if message["to"] == "show_user":
        
        if message["to"] == "show_category1":
                H = DB.client.execute(f"""
                            SELECT * FROM category1 
                            order by sum                               
                            """)
                test_data = np.array(H[200][2]) 
                res = test_data.reshape((test_data.shape[0], 1))               
                print (test_data.shape[0], res.shape, res[:,:])  
                self.write_message(json.dumps({"from":"show_category1", "data":H}))
                
                
        if message["to"] == "show_script_SQL":
                H = DB.client.execute(f"""{message["data"]}""")
                #test_data = np.array(H[200][2]) 
                #res = test_data.reshape((test_data.shape[0], 1))               
                #print (test_data.shape[0], res.shape, res[:,:])  
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

        if message["to"] == "sort_related_products":
                H = DB.client.execute(f"""
                            SELECT * FROM sort_related_products 
                            order by sum                               
                            """)
                test_data = np.array(H[200][2]) 
                res = test_data.reshape((test_data.shape[0], 1))               
                print (test_data.shape[0], res.shape, res[:,:])  
                self.write_message(json.dumps({"from":"sort_related_products", "data":H}))                

        if message["to"] == "sort_category_by_user_id":                
                    H = D.client.execute(f"""   
                                                    SELECT
                                                      SUM(Items_Count) as sum1, 
                                                      SUM(Total_Amount) as sum2,
                                                      Category1_Id
                                                    FROM my_table
                                                    WHERE my_table.Customer_Id = {message["id1"]} GROUP BY Category1_Id
                                                    ORDER BY sum2
                                                """)
                    self.write_message(json.dumps({"from":"sort_category_by_user_id", "data":H}))   
        if message["to"] == "sort_category_by_":                                                              
                    ZS = D.client.execute(f"""   
                                                    SELECT
                                                      SUM(Items_Count) as sum1, 
                                                      SUM(Total_Amount) as sum2,
                                                      Category1_Id
                                                    FROM my_table
                                                    WHERE my_table.Customer_Id = {message["id1"]} 
                                                    AND my_table.Category1_Id = {message["id2"]}
                                                    GROUP BY Category1_Id
                                                """)              
                


    def on_close(self):
        ImageWebSocket.clients.remove(self)
        print("WebSocket closed from: " + self.request.remote_ip)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", title="Нейронная сеть/Тренировка")

app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/websocket", ImageWebSocket),
    ])
app.listen(8800)

print("Starting server: http://xxx.xx.xx.xxx:8800/") # IP

tornado.ioloop.IOLoop.current().start()










#class MainHandler(tornado.web.RequestHandler):
#    def get(self):
#        #data_json = json.loads(self.request)
#        print (self.request)
#        print (int(self.request.arguments['a'][0]))
#        self.write(json.dumps({"get":"ok"})) 
#        
#        
#    def post(self):
#        self.write(json.dumps({"get":"ok"}))  



#app = tornado.web.Application([
#        (r"/", MainHandler),
#    ])
#app.listen(8800)


#tornado.ioloop.IOLoop.current().start()

#https://www.tornadoweb.org/en/stable/web.html
