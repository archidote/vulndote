from pendulum import date
import datetime
import requests
import time 
import schedule
import sqlite3
from controller import *

def last(n) :
    
    if n >= 10 : 
        return "Unable to display more than 10 inputs"
    
    number = n
    i = 0
    url = oldURLApi+"last/"+str(number)

    resp = requests.get(url=url)
    data = resp.json() 
    
    cve = ""
    for i in range(number) : 
        cve+=data[i]["id"]+"\n\n"
        cve+="Published : "+data[i]["Published"]+"\n"
        cve+="Edited : "+data[i]["Modified"]+"\n"
        cve+="CVSS Score : "+str(data[i]["cvss"])+"\n\n"
        cve+="Summary : "+data[i]["summary"]+"\n\n"
        cve+="Vulnerable Product : \n"+data[i]["vulnerable_product"][i]+"\n\n"
        i = i + 1 
    return cve

def lastInRealTime(): 
    
    conn = sqlite3.connect('assets/vulndote.db')
    cursor = conn.cursor()
    
    url = urlAPI+"last/1"
    resp = requests.get(url=url)
    data = resp.json() 
    
    latestCVECode = data[0]["id"]  
    cursor.execute(f"""SELECT cveCode FROM CVE_Stack WHERE cveCode = '{latestCVECode}'""")
    
    row = cursor.fetchall()

    if len(row) != 0:
        x = datetime.datetime.now()
        return x 
    else :
        
        cursor.execute(f"""INSERT OR IGNORE INTO CVE_Stack (cveCode) VALUES ('{latestCVECode}')""")
        conn.commit()
        conn.close()
        
        return cveSearch(latestCVECode) ; 
       
# schedule.every(5).minutes.do(lambda: print(lastInRealTime()))

# while 1:
#     schedule.run_pending()
#     time.sleep(1)