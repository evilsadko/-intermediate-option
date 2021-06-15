from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from pynput.mouse import Button, Controller
from selenium.webdriver.common.keys import Keys

import numpy as np
import cv2
import time
import random
import os
import io
import base64
import scipy.interpolate as si
import pickle
import dbhandler_2



DB = dbhandler_2.DataBase()

# get a new selenium webdriver with tor as the proxy
def my_proxy(PROXY_HOST,PROXY_PORT):
    fp = webdriver.FirefoxProfile()
    fp.set_preference("network.proxy.type", 1)
    fp.set_preference("network.proxy.socks",PROXY_HOST)
    fp.set_preference("network.proxy.socks_port",int(PROXY_PORT))
    fp.set_preference("http.response.timeout", 1000)

    fp.update_preferences()
    options = Options()
    options.add_argument("-devtools")
    #options.headless = True
    #return webdriver.Firefox(executable_path="geckodriver/geckodriver", options=options, firefox_profile=fp)
    return webdriver.Firefox(options=options, firefox_profile=fp)
    
def imgs(x):
      cv2.imshow('google image', np.array(x))
      cv2.waitKey(0)
      cv2.destroyAllWindows()

#image_product
#51.15.197.24
#https://api.ipify.org/
if __name__ == "__main__":
        t_data = DB.client.execute(f"SELECT Product_ID, SUM(Items_Count) as sum FROM my_table GROUP BY Product_ID")
        #proxy = my_proxy("127.0.0.1", 9050)
        #proxy = my_proxy("91.233.61.210", "8000")
        #proxy.get("http://gexperiments.ru/")
        for k in t_data:
            #print (int(k[0]), 319455)
            if int(k[0]) == 1934987:
                print (int(k[0]) == 1934987)
        print (len(t_data))
#            proxy.get(f"https://www.tivtaam.co.il/?catalogProduct={k[0]}") #?catalogProduct=151115
##        proxy.get("https://www.tivtaam.co.il/?catalogProduct=151115")
##        #1934987
##        #2066074
##        #2338365
##        #319455
##        #18718
##        ##------------------------------------>
#            img_prod = proxy.find_elements_by_xpath('//img[@class="image"]')[0]
###        print (img_prod.get_attribute("src"))
#            time.sleep(1)
#            answ = proxy.execute_script(''' 
#                    var img = new Image();
#                    var cnv = document.createElement('canvas');
#                    cnv.id = 'tutorial';
#                        img.onload = function(){
#                          cnv.height = img.height;
#                          cnv.width = img.width;
#                          console.log(cnv.width, cnv.height, img.width, img.height);
#                          cnv.getContext('2d').drawImage(img, 0, 0);
#                        }
#                            var request = new XMLHttpRequest();
#                            request.open('GET', arguments[0].src);
#                            request.responseType = 'blob';
#                            request.onload = function() {
#                                var reader = new FileReader();
#                                reader.readAsDataURL(request.response);
#                                reader.onload =  function(e){
#                                    img.src = e.target.result;
#                                };
#                            };
#                            request.send();
#                    var child = document.body.appendChild(cnv);
#                    ''', img_prod)
#            time.sleep(1)
#            answ = proxy.execute_script(''' 
#                    cnv = document.getElementById('tutorial');
#                    return cnv.toDataURL('image/jpeg').substring(22);
#            ''')
#            print (answ)
#            nparr = np.asarray(bytearray(io.BytesIO(base64.b64decode(answ)).read()), dtype=np.uint8)
#            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#            print (img_np.shape)
#            imgs(img_np)
        #proxy.get("https://www.tivtaam.co.il/?catalogProduct=2066074")
#https://www.tivtaam.co.il/categories/92052/products?catalogProduct=1934987
