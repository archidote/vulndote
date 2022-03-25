from assets.todayCVE import * 
from assets.controller import * 
from assets.functions import * 
import schedule
import time
import sqlite3

def sendAlertAutoVendor() : 
    
    conn = sqlite3.connect('assets/vulndote.db')
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM subscriber_vendor_alerts""")
    
    rows = cur.fetchall()
    
    for row in rows:
        chatId = str(row[0])
        updateOrNot = cveTodaySortedByVendor(row[1])
        if updateOrNot == "No CVE":
            cur.execute(f"""UPDATE subscriber_vendor_alerts SET api_request = '{updateOrNot}' WHERE chat_id = '{chatId}';""") # à tester en raw 
        elif row[2] == updateOrNot : 
            cur.execute(f"""UPDATE subscriber_vendor_alerts SET api_request = '{updateOrNot}' WHERE chat_id = '{chatId}';""") # à tester en raw 
            conn.commit() # Valide la request dans le cadre de plusieurs ".execute"
            print ("No update since the last fetch. (vendor)")
        else : 
            print ("New CVE for :"+row[1]+"")
            cve = "New CVE for :"+row[1]+"\n\n"
            cve += updateOrNot
            
            cur.execute(f"""UPDATE subscriber_vendor_alerts SET api_request = '{updateOrNot}' WHERE chat_id = '{chatId}';""") # à tester en raw 
            conn.commit() # Valide la request dans le cadre de plusieurs ".execute"
            # Send the notif 
            
            markup="""{"inline_keyboard":[[{"text":"Unsubscribe","callback_data":"unsubscribe_vendor_alerts"}],[{"text":"🔄 Refresh","callback_data":"refresh_vendor_request_from_alert"}]]}"""
            send_text = 'https://api.telegram.org/bot' + TELEGRAM_BOT_TOKEN + '/sendMessage?chat_id=' + chatId + '&text=' + cve + '&reply_markup=' + markup
            response = requests.get(send_text)
            return response.json()
        
    conn.close()

def sendAlertAutoCVSS() : 
    
    conn = sqlite3.connect('assets/vulndote.db')
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM subscriber_cvss_alerts""")
    
    rows = cur.fetchall()

    for row in rows:
        chatId = str(row[0])
        updateOrNot = cveTodaySortedByCVSS(row[1])
        if updateOrNot == "No CVE":
            cur.execute(f"""UPDATE subscriber_cvss_alerts SET api_request = '{updateOrNot}' WHERE chat_id = '{chatId}';""") # à tester en raw 
        elif row[2] == updateOrNot : 
            cur.execute(f"""UPDATE subscriber_cvss_alerts SET api_request = '{updateOrNot}' WHERE chat_id = '{chatId}';""") # à tester en raw 
            conn.commit() # Valide la request dans le cadre de plusieurs ".execute"
            print ("No update since the last fetch. (cvss)")
        else : 
            print ("New CVE for :"+row[1]+"")
            cve = "New CVE for :"+row[1]+"\n\n"
            cve += updateOrNot
            
            cur.execute(f"""UPDATE subscriber_cvss_alerts SET api_request = '{updateOrNot}' WHERE chat_id = '{chatId}';""") # à tester en raw 
            conn.commit() # Valide la request dans le cadre de plusieurs ".execute"
            # Send the notif 
            
            markup="""{"inline_keyboard":[[{"text":"Unsubscribe","callback_data":"unsubscribe_cvss_alerts"}],[{"text":"🔄 Refresh","callback_data":"refresh_cvss_request_from_alert"}]]}"""
            send_text = 'https://api.telegram.org/bot' + TELEGRAM_BOT_TOKEN + '/sendMessage?chat_id=' + chatId + '&text=' + cve + '&reply_markup=' + markup
            response = requests.get(send_text)
            return response.json()
        
    conn.close()

def sendAlertAutoVendorV2(chat_id,vendor) : 
    
    conn = sqlite3.connect('assets/vulndote.db')
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM subscriber_vendor_alerts WHERE chat_id = {chat_id} """)
    
    rows = cur.fetchall()
    
    response = session.get('https://www.opencve.io/api/cve?vendor='+vendor)
    data = response.json() 

    if "message" in data : 
        return "Vendor/Product hasn't been found."
    else : 
        
        today = now = datetime.now()
        today = now.strftime("%Y-%m-%d")
    
        for row in rows:
            for i in range(len(data)):
                if today in formatDate(data[i]["updated_at"]):
                    if data[i]["id"] in row[2]: 
                        print (data[i]["id"])
                        # CVE déjà présente dans la table 
                    else : 
                        print ("NEW CVE \n"+data[i]["id"])
                        #cur.execute(f"""UPDATE subscriber_vendor_alerts SET api_request = '{cve}' WHERE chat_id = '{chat_id}';""") # à tester en raw 
                    
        
print(sendAlertAutoVendorV2(653258620,"Linux"))
# print (collectCVE_ID_TodaySortedByVendor("Linux",653258620))