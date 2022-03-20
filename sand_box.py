from assets.todayCVE import * 
from assets.controller import * 
import schedule
import time
import sqlite3

def sendAlertAuto() : 
    
    conn = sqlite3.connect('assets/vulndote.db')
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM subscriber_vendor_alerts""")
    
    rows = cur.fetchall()

    for row in rows:
        updateOrNot = cveTodaySortedByVendor(row[1])
        if row[2] != updateOrNot : 
            if updateOrNot == "No CVE" : 
                print("pas de cve contrairement à hier")
            else : 
                chatId = row[0]
                print ("New CVE for :"+row[1]+"")
                cur.execute(f"""UPDATE subscriber_vendor_alerts SET api_request = '{updateOrNot}' WHERE chat_id = '{chatId}';""") # à tester en raw 
        else : 
            print ("No CVE / No CVE")

    conn.commit() # Valide la request dans le cadre de plusieurs ".execute"
    conn.close()

# faire une fonction pour uniquement la criticité toutes cve confondu 

sendAlertAuto()

schedule.every(5).minutes.do(lambda : sendAlertAuto())

while 1:
    schedule.run_pending()
    time.sleep(1)