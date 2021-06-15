import threading
from utils import *
from dbhandler_2 import *


if __name__ == "__main__":
    D = DataBase()
    
    #print (D.show_tables())  
    T = D.client.execute(f"""   
                                            SELECT
                                              SUM(Items_Count) as sum1, 
                                              SUM(Total_Amount) as sum2,
                                              Customer_Id
                                            FROM my_table
                                            GROUP BY Customer_Id
                                            ORDER BY sum1
                          """)
    print (T, len(T))
#f"SELECT count() FROM {x}"
