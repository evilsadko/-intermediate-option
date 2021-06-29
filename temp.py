import threading
from utils import *
import dbhandler
DB = dbhandler.DataBase()

if __name__ == "__main__":
    
    P = PRODUCT()
    A = P.loc[P['Product_ID'] == 554815] #554815 #313528
    O = ORDER()
    
    #554815
    #print (A)
    A = A.to_numpy()
    cats = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    M = {'01':0, '02':0, '03':0, '04':0, '05':0, '06':0, '07':0, '08':0, '09':0, '10':0, '11':0, '12':0}
    for i in A:
        OID = i[0]
        
        O_t = O.loc[O['Order_Id'] == OID]
        data = O_t.to_numpy()[0][-1]
        s_mon = data.split(" ")[0].split("-")[1]
        M[s_mon] += 1 #i[3]
        print (i[1], OID, data, s_mon)
        #print (OID,list(i), len(cats))
    print (M)   
#{1: 401, 2: 82, 3: 1074, 4: 1332, 5: 1136, 6: 91, 7: 572, 8: 688, 9: 719, 10: 1044, 11: 1709, 12: 2303}

#{'01': 131963.43000000008, '02': 118786.96999999978, '03': 165455.81000000046, '04': 203461.25000000093, '05': 227038.53000000026, '06': 152014.69000000015, '07': 162823.32000000105, '08': 150667.54000000024, '09': 155146.86000000016, '10': 177031.57999999897, '11': 141911.0500000001, '12': 161564.06999999966}

    
    
#    {'01': 101639.75999999631, '02': 82335.62000000032, '03': 73239.76000000202, '04': 67848.46000000316, '05': 81354.9100000005, '06': 63359.62000000348, '07': 69590.65000000274, '08': 76650.01000000129, '09': 86164.85999999921, '10': 99933.39999999681, '11': 80033.54000000052, '12': 87513.42999999908}

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


    T = DB.client.execute(f"""
            SELECT
                toMonth(Order_Date) as time
            FROM test
            WHERE Product_ID = 554815
            """) #554815 #313528
    #print (T)
    #M = {'01':0, '02':0, '03':0, '04':0, '05':0, '06':0, '07':0, '08':0, '09':0, '10':0, '11':0, '12':0}
    M = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}
    for i in T:
        #data = i[-3]
        #s_mon = data.split(" ")[0].split("-")[1]
        #print (data, s_mon)
        s_mon = i[0]
        M[s_mon] += 1#i[2]
        
    print (M)
#    
    
    
    
    
    
    
    
    
    
#    if __name__ == "__main__":
#    o_open = ORDER()  #['Order_Id', 'Customer_Id', ', 'price_before_discount', 'Amount_Charged', 'Order_Date']
#    o_open = o_open.sort_values(by=['Order_Date']) #, inplace=True, ascending=False
#    o_open = o_open.to_numpy()
#    #cats = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun', 'Jul', 'Aug','Sep', 'Oct', 'Nov', 'Dec']
#    
#    dicts = {}
#    dicts2 = {}
#    M = "11"
#    for i in range(o_open.shape[0]):
#        t = o_open[i,:].tolist()
#        o_id = t[0]
#        cust_id = t[1]
#        items_count = t[2]
#        date = t[-1]
#        s_mon = date.split(" ")[0].split("-")[1]
#        s_day = date.split(" ")[0].split("-")[-1]
#        if s_mon == M:
#            try:
#                dicts[s_day] += 1
#            except KeyError:
#                dicts[s_day] = 1       
#            try:
#                dicts2[s_day] += int(items_count)
#            except KeyError:
#                dicts2[s_day] = int(items_count) 
#        #print (o_id, items_count, date.split(" ")[0].split("-")[1])#, IDX[0], len(IDX[0].tolist()))   
#    #print (list(dicts.keys()), list(dicts.values()))
##----------------------------->
#    plt.plot(list(dicts.keys()), list(dicts.values()))
#    plt.plot(list(dicts2.keys()), list(dicts2.values()))
#    plt.show()
