from assets.controller import * 
from assets.cveAdditionalInformation import * 
from assets.send_message import * 

def check_for_new_cve():
    
    try: 
        logging.info("Execution of check_for_new_cve() "+todayHS)
        cursor.execute(f"""SELECT * FROM subscriber_vendor_alerts """)
        rows = cursor.fetchall()
            
        try : 
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
                            logging.info("New CVE"+data[i]["id"]+"has been fetched for"+vendor+" - user id :"+str(chat_id))
                            CVEs += data[i]["id"]+","
                            newCVEs += cveSearch(data[i]["id"],1)
                            newCVEs = summaryRegex(newCVEs) # Escape other chars than common HTML special chars like &amp;
                            send_message(TELEGRAM_BOT_TOKEN,chat_id,newCVEs)
                        else : 
                            logging.info("CVE"+data[i]["id"]+"has been ALREADY fetched for"+vendor+" - user id :"+str(chat_id))
                            CVEs += data[i]["id"]+","
                        cursor.execute(f"""UPDATE subscriber_vendor_alerts SET api_request = '{CVEs}', refresh_date = '{today}' WHERE chat_id = {chat_id};""")
                    else : 
                        logging.info("No new CVE for :"+vendor+" today - user id :"+str(chat_id))
            
        except Exception as e : 
            logging.error("Fatal Error : "+str(e))
            
        dbConnection.commit() 
        
    except Exception as e : 
        logging.error("Fatal Error (db error): "+str(e))
        


    
