import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import json
import utils as TG
import time

file_arr_temp = open("out/file_arr_temp_v2.txt", "r")  
def get_batch():
    L = []
    for i in file_arr_temp:
            res = json.loads(i.split("\n")[0])
            Z = np.zeros((12, num_ids))
            L1 = list(res.values())[0][0]
            L2 = list(res.values())[0][1]
            for i in range(len(L1)):
                 Z[L1[i],L2[i]] += 1  
            L.append(Z)
            if len(L) == 32:
                yield np.array(L)
                L = []       

def plot_user():
    start = time.time()
    file_arr_temp = open("out/file_arr_temp_v3.txt", "r") 
    ix = 0 
    for i in file_arr_temp:
        res = json.loads(i.split("\n")[0])
        Z = np.zeros((12, 48603))
        L1 = list(res.values())[0][0]
        L2 = list(res.values())[0][1]
        for i in range(len(L1)):
             Z[L1[i],L2[i]] += 1    
        ix += 1 
        
        fig, ax = plt.subplots(figsize=(10,10), clear=True)
        A = []
        B = []
        for o in range(Z.shape[0]):
            A.append(o)
            B.append(sum(Z[o,:]))
        plt.plot(A, B, label = f"{o}")    
        fig.savefig(f"temp/{i}.jpg")  # cat/cat2
        fig.clear(True)
        plt.close(fig) 
        
    print (time.time()-start, ix) 

def imgs_v(x):
      cv2.imshow('Rotat', np.array(x))
      cv2.waitKey(0)
      cv2.destroyAllWindows()


def similarity(vector1, vector2):
        return np.dot(vector1, vector2.T) / np.dot(np.linalg.norm(vector1, axis=1, keepdims=True), np.linalg.norm(vector2.T, axis=0, keepdims=True))

def crt(i):
        res = json.loads(i.split("\n")[0])
        Z = np.zeros((12, 48603))
        L1 = list(res.values())[0][0]
        L2 = list(res.values())[0][1]
        for i in range(len(L1)):
             Z[L1[i],L2[i]] += 1  
               
        Y = []
        for o in range(Z.shape[0]):
            if sum(Z[o,:]) > 0:
                Y.append(1) 
            if sum(Z[o,:]) == 0:
                Y.append(0)      
        return np.reshape(np.array(Y), (1,12)), list(res.keys())[0]


def func_rec(ID):
    print (len(file_arr_temp))
    for ix, i in enumerate(file_arr_temp):
        Z0 = crt(i)
        try:
            G[ID].append(Z0[1])
        except KeyError:
            G[ID] = [Z0[1]]   
        del file_arr_temp[ix]
        for ix2, ii in enumerate(file_arr_temp):
            Z1 = crt(ii)
            KEF = similarity(Z0[0], Z1[0])
            if KEF[0]>tresh:
                G[ID].append(Z1[1])
                del file_arr_temp[ix2]
        ID += 1


def chunks(lst, count):
    start = 0
    for i in range(count):
          stop = start + len(lst[i::count])
          yield lst[start:stop]
          start = stop     


if __name__ == "__main__":
    tresh = .68
    G = {}
    
    
    start = time.time()
    file_arr_temp = open("out/file_arr_temp_v3.txt", "r").readlines()[:1000]


    ty = chunks(file_arr_temp, 10)
    threads = []
    for f_list in ty:
        print (len(f_list))
        my_thread = threading.Thread(target=func_rec, args=([0]))
        threads.append(my_thread)
        my_thread.start()
    flag = 1
    while (flag):
        for t in threads:
            if t.isAlive():
                flag = 1
            else:
                flag = 0    
    with open(f"out/test_claster_2.json", 'w') as js_file:
        json.dump(G, js_file)      
