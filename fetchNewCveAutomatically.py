import schedule 
import time as t
from assets.cveToday import * 
from assets.functions import * 

def sendAlertAutoVendor() : 
    
    print ("Execution of sendAlertAutoVendor()")
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
                    print ("New CVE"+data[i]["id"]+"has been fetched for"+vendor+" - user id :"+str(chat_id))
                    CVEs += data[i]["id"]+","
                    newCVEs += cveSearch(data[i]["id"],1)
                    newCVEs = summaryRegex(newCVEs) # Escape other chars than common HTML special chars like &amp;
                    send_text = 'https://api.telegram.org/bot' + TELEGRAM_BOT_TOKEN + '/sendMessage?chat_id=' + str(chat_id)+ '&parse_mode=HTML&text=' + newCVEs + ''
                    response = requests.get(send_text)
                else : 
                    print ("CVE"+data[i]["id"]+"has been ALREADY fetched for"+vendor+" - user id :"+str(chat_id))
                    CVEs += data[i]["id"]+","
                
                cursor.execute(f"""UPDATE subscriber_vendor_alerts SET api_request = '{CVEs}', refresh_date = '{today}' WHERE chat_id = {chat_id};""")

    dbConnexion.commit() 

schedule.every(20).minutes.do(lambda: sendAlertAutoVendor())

while True:
    schedule.run_pending()
    t.sleep(1)