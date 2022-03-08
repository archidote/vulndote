import html
from datetime import *
from assets.controller import * 
from assets.functions import *

def cveTodaySortedByVendor(vendor) :  
    
    response = session.get('https://www.opencve.io/api/cve?vendor='+vendor)
    data = response.json() 

    if "message" in data : 
        return "Vendor/Product has'nt been found."
    else : 

        today = now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        
        cve = ""
        for i in range(len(data)):
            if today in formatDate(data[i]["updated_at"]):
                cve += "<b>CVE ID</b> : "+data[i]["id"]+"\n"
                cve += "<b>CVSS</b> : "+cvssScale((data[i]["id"]))+"\n"
                cve += "<b>Summary</b> : "+html.escape(data[i]["summary"],quote=True)+"\n"
                cve += "<b>Published/Updated</b> : "+data[i]["updated_at"]+"\n\n"
                cveIdFormated=data[i]["id"].replace("-", "_")
                cve += "More Info ? : /Cve@"+cveIdFormated+"\n"
        if cve : # IF cve variable is not empty 
            cve += "<b><i>Sort CVE by</i> : </b> "
            return cve  
        else : 
            return "No CVE"

def cveTodaySortedByCVSS(cvss) :  
    
    response = session.get('https://www.opencve.io/api/cve?cvss='+cvss)
    data = response.json() 

    today = now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    
    cve = ""
    for i in range(len(data)):
        if today in formatDate(data[i]["updated_at"]):
                cve += "<b>CVE ID</b> : "+data[i]["id"]+"\n"
                cve += "<b>CVSS</b> : "+cvssScale((data[i]["id"]))+"\n"
                cve += "<b>Summary</b> : "+html.escape(data[i]["summary"],quote=True)+"\n"
                cve += "<b>Published/Updated</b> : "+data[i]["updated_at"]+"\n\n"
                cveIdFormated=data[i]["id"].replace("-", "_")
                cve += "More Info ? : /Cve@"+cveIdFormated+"\n"
    if cve : # IF cve variable is not empty 
        return cve  
    else : 
        return "No CVE(s) have been registered today yet with this level of threat : *"+cvss+"*"

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
                cve += "<b>CVE ID</b> : "+data[i]["id"]+"\n"
                cve += "<b>CVSS</b> : "+cvssScale((data[i]["id"]))+"\n"
                cve += "<b>Summary</b> : "+html.escape(data[i]["summary"],quote=True)+"\n"
                cve += "<b>Published/Updated</b> : "+data[i]["updated_at"]+"\n\n"
                cveIdFormated=data[i]["id"].replace("-", "_")
                cve += "More Info ? : /Cve@"+cveIdFormated+"\n"
        if cve : # IF cve variable is not empty 
            cve += "<b><i>Sort CVE by</i> : </b> "
            return cve  
        else : 
            return "No CVE(s) have been registered Today for *"+vendor+"* with this level of threat : *"+cvss+"*"

def cveTodayNotSorted() :  
    
    response = session.get('https://www.opencve.io/api/cve')
    data = response.json() 

    today = now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    
    cve = ""
    for i in range(len(data)):
        if today == formatDate(data[i]["updated_at"]):
                cve += "<b>CVE ID</b> : "+data[i]["id"]+"\n"
                cve += "<b>CVSS</b> : "+cvssScale((data[i]["id"]))+"\n"
                cve += "<b>Summary</b> : "+html.escape(data[i]["summary"],quote=True)+"\n"
                cve += "<b>Published/Updated</b> : "+data[i]["updated_at"]+"\n\n"
    return cve  

def formatDate(rawDate) :
    
    res = rawDate.split("T")[0]
    return res


# print (cveTodaySortedByVendor("microsoft"))
# print (cveTodaySortedByCVSS("critical"))
# print (cveTodayNotSorted())
# print (cveTodaySortedByVendorAndCVSS("Microsoft","Low"))