import html
from datetime import *
from assets.controller import * 
from assets.functions import *
from assets.cveAdditionalInformation import *

def cveTodaySortedByVendor(vendor) :  
    
    response = session.get('https://www.opencve.io/api/cve?vendor='+vendor)
    data = response.json() 

    if "message" in data : 
        return "Vendor/Product hasn't been found."
    else : 

        today = now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        
        cve = ""
        for i in range(len(data)):
            if today in formatDate(data[i]["updated_at"]):
                cve += cveCommonInfo(data[i])
        if cve : # IF cve variable is not empty 
            cve += "<b><i>Sort CVE by</i> : </b> "
            return cve  
        else : 
            return "No CVE(s) have been registered today for this vendor/product."

def collectCVE_ID_TodaySortedByVendor(vendor,chat_id) :  
    
    response = session.get('https://www.opencve.io/api/cve?vendor='+vendor)
    data = response.json() 

    if "message" in data : 
        return "Vendor/Product hasn't been found."
    else : 

        today = now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        
        cve = ""
        for i in range(len(data)):
            if today in formatDate(data[i]["updated_at"]):
                cve += ""+data[i]["id"]+","
        if cve : # IF cve variable is not empty 
            conn = sqlite3.connect('assets/vulndote.db')
            cur = conn.cursor()
            cur.execute(f"""UPDATE subscriber_vendor_alerts SET api_request = '{cve}' WHERE chat_id = '{chat_id}';""") # à tester en raw 
            cur.execute(f"""UPDATE subscriber_vendor_alerts SET refresh_date = '{today}' WHERE chat_id = '{chat_id}';""") # à tester en raw 
            conn.commit()
            conn.close()
            return cve  
        else : 
            return "No CVE(s) have been registered today for this vendor/product."

def cveTodaySortedByCVSS(cvss) :  
    
    response = session.get('https://www.opencve.io/api/cve?cvss='+cvss)
    data = response.json() 

    today = now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    
    cve = ""
    for i in range(len(data)):
        if today in formatDate(data[i]["updated_at"]):
            cve += cveCommonInfo(data[i])
    if cve : # IF cve variable is not empty 
        return cve  
    else : 
        return "No CVE(s) have been registered today yet with this level of threat : <b>"+cvss+"</b>"

def cveTodaySortedByVendorAndCVSS(vendor,cvss) :  # Ok 
    
    response = session.get('https://www.opencve.io/api/cve?vendor='+vendor+'&cvss='+cvss+'')
    data = response.json() 
    
    if "message" in data : 
        return "Vendor/Product has'nt been found."
    else : 
        today = now = datetime.now()
        today = now.strftime("%Y-%m-%d")

        cve = ""
        for i in range(len(data)):
            if today in formatDate(data[i]["updated_at"]):
                cve += cveCommonInfo(data[i])
        if cve : # IF cve variable is not empty 
            cve += "<b><i>Sort CVE by</i> : </b> "
            return cve  
        else : 
            return "No CVE(s) have been registered Today for <b>"+vendor+"</b> with this level of threat : <b>"+cvss+"</b>"

def cveTodayNotSorted() :  
    
    response = session.get('https://www.opencve.io/api/cve')
    data = response.json() 

    today = now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    
    cve = ""
    for i in range(len(data)):
        if today == formatDate(data[i]["updated_at"]):
            cve += cveCommonInfo(data[i])
    return cve  

# print (cveTodaySortedByVendor("microsoft"))
# print (cveTodaySortedByCVSS("critical"))
# print (cveTodayNotSorted())
# print (cveTodaySortedByVendorAndCVSS("Microsoft","Low"))