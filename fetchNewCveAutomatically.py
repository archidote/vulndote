from psycopg2 import connect
import schedule
import sqlite3
import time as t
from assets.cveToday import * 
from assets.functions import * 

def sendAlertAutoVendor() : 
    
    cursor.execute(f"""SELECT * FROM subscriber_vendor_alerts """)
    rows = cursor.fetchall()
            
    for row in rows:
        
        chat_id = row[0]
        vendor = row[1]
        
        response = session.get('https://www.opencve.io/api/cve?vendor='+row[1])
        data = response.json() 
        
        CVEs = ""
        
        for i in range(len(data)):
            if today in formatDate(data[i]["updated_at"]):
                newCVEs = "📍 New CVE for :"+vendor+"\n\n"
                if data[i]["id"] not in row[2]:
                    CVEs += data[i]["id"]+","
                    newCVEs += cveSearch(data[i]["id"],1)
                    newCVEs = summaryRegex(newCVEs) # Escape other chars than common HTML special chars like &amp;
                    send_text = 'https://api.telegram.org/bot' + TELEGRAM_BOT_TOKEN + '/sendMessage?chat_id=' + str(chat_id)+ '&parse_mode=HTML&text=' + newCVEs + ''
                    response = requests.get(send_text)
                else : 
                    CVEs += data[i]["id"]+","
                
                cursor.execute(f"""UPDATE subscriber_vendor_alerts SET api_request = '{CVEs}', refresh_date = '{today}' WHERE chat_id = {chat_id};""")

    dbConnexion.commit() 
    
    
sendAlertAutoVendor()

# schedule.every(2).minutes.do(lambda: sendAlertAutoVendor())

# while True:
#     schedule.run_pending()
#     t.sleep(1)