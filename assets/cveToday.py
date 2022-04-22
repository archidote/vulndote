from datetime import *
from assets.controller import * 
from assets.functions import *
from assets.cveAdditionalInformation import *

def cveTodaySortedByVendor(vendor) :  
    
    response = session.get(OPEN_CVE_API_URL_PARAMS+"vendor="+vendor)
    data = response.json() 

    if "message" in data : 
        return VENDOR_OR_PRODUCT_NOT_FOUND
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
    
    response = session.get(OPEN_CVE_API_URL_PARAMS+"vendor=vendor="+vendor)
    data = response.json() 

    if "message" in data : 
        return VENDOR_OR_PRODUCT_NOT_FOUND
    else : 

        today = now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        
        cve = ""
        for i in range(len(data)):
            if today in formatDate(data[i]["updated_at"]):
                cve += ""+data[i]["id"]+","
        if cve : # IF cve variable is not empty 
            cursor.execute(f"""UPDATE subscriber_vendor_alerts SET api_request = '{cve}' WHERE chat_id = '{chat_id}';""") # à tester en raw 
            cursor.execute(f"""UPDATE subscriber_vendor_alerts SET refresh_date = '{today}' WHERE chat_id = '{chat_id}';""") # à tester en raw 
            dbConnexion.commit()
            
            return cve  
        else : 
            return "No CVE(s) have been registered today for this vendor/product."

def cveTodaySortedByCVSS(cvss) :  
    
    response = session.get(OPEN_CVE_API_URL_PARAMS+'cvss='+cvss)
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
    
    response = session.get(OPEN_CVE_API_URL_PARAMS+'vendor='+vendor+'&cvss='+cvss+'')
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

# print (cveTodaySortedByVendor("microsoft"))
# print (cveTodaySortedByCVSS("critical"))
# print (cveTodaySortedByVendorAndCVSS("Microsoft","Low"))