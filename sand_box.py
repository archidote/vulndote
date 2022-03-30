import schedule
import sqlite3
import time as t
from assets.cveToday import * 
from assets.functions import * 

def sendAlertAutoVendorV2() : 
    
    conn = sqlite3.connect('assets/vulndote.db')
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM subscriber_vendor_alerts """)
    rows = cur.fetchall()
            
    for row in rows:
        
        chat_id = row[0]
        vendor = row[1]
        
        response = session.get('https://www.opencve.io/api/cve?vendor='+row[1])
        data = response.json() 
        
        CVEs = ""
        
        for i in range(len(data)):
            if today in formatDate(data[i]["updated_at"]):
                newCVEs = "New CVE for :"+vendor+"\n\n"
                if data[i]["id"] not in row[2]:
                    CVEs += data[i]["id"]+","
                    newCVEs += data[i]["id"]+"\n More info : /Cve@"+data[i]["id"].replace("-", "_")+""
        if len(CVEs) > 0 : 
            cur.execute(f"""UPDATE subscriber_vendor_alerts SET api_request = '{CVEs}', refresh_date = '{today}' WHERE chat_id = {chat_id};""") 
            markup="""{"inline_keyboard":[[{"text":"Unsubscribe","callback_data":"unsubscribe_cvss_alerts"}],[{"text":"🔄 Refresh","callback_data":"refresh_cvss_request_from_alert"}]]}"""
            send_text = 'https://api.telegram.org/bot' + TELEGRAM_BOT_TOKEN + '/sendMessage?chat_id=' + str(chat_id)+ '&text=' + newCVEs + '&reply_markup=' + markup
            response = requests.get(send_text)

    conn.commit() # Valide la request dans le cadre de plusieurs ".execute"
    conn.close()
    
schedule.every(20).seconds.do(lambda: sendAlertAutoVendorV2())
  
while True:
    schedule.run_pending()
    t.sleep(1)