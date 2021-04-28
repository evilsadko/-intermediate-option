import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import base64
import cv2
import os, sys
import numpy
import time



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        #data_json = json.loads(self.request)
        print (self.request)
        print (int(self.request.arguments['a'][0]))
        self.write(json.dumps({"get":"ok"})) 
        
        
    def post(self):
        self.write(json.dumps({"get":"ok"}))  



app = tornado.web.Application([
        (r"/", MainHandler),
    ])
app.listen(8800)


tornado.ioloop.IOLoop.current().start()

#https://www.tornadoweb.org/en/stable/web.html
