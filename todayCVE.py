from numpy import empty
from controller import * 
from datetime import datetime
from datetime import timezone

def cveTodaySortedByVendor(vendor) :  
    
    response = session.get('https://www.opencve.io/api/cve?vendor='+vendor)
    
    data = response.json() 

    today = now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    
    cve = ""
    for i in range(len(data)):
        if today in formatDate(data[i]["updated_at"]):
            cve += "CVE ID : "+data[i]["id"]+"\n"
            cve += "Summary : "+data[i]["summary"]+"\n"
            cve += "Published/Updated : "+data[i]["updated_at"]+"\n\n"
    if cve : # IF cve variable is not empty 
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
        if today == formatDate(data[i]["updated_at"]):
            cve += "CVE ID : "+data[i]["id"]+"\n"
            cve += "Summary : "+data[i]["summary"]+"\n"
            cve += "Published/Updated :"+data[i]["updated_at"]+"\n\n"
    return cve  

def cveTodaySortedByVendorAndCVSS(vendor,cvss) :  
    
    response = session.get('https://www.opencve.io/api/cve?vendor='+vendor+'&cvss='+cvss+'')
    
    data = response.json() 

    today = now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    
    cve = ""
    for i in range(len(data)):
        if today == formatDate(data[i]["updated_at"]):
            cve += "CVE ID : "+data[i]["id"]+"\n"
            cve += "Summary : "+data[i]["summary"]+"\n"
            cve += "Published/Updated :"+data[i]["updated_at"]+"\n\n"
    return cve  

def cveTodayNotSorted() :  
    
    response = session.get('https://www.opencve.io/api/cve')
    
    data = response.json() 

    today = now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    
    cve = ""
    for i in range(len(data)):
        if today == formatDate(data[i]["updated_at"]):
            cve += "CVE ID : "+data[i]["id"]+"\n"
            cve += "Summary : "+data[i]["summary"]+"\n"
            cve += "Published/Updated : "+data[i]["updated_at"]+"\n\n"
    return cve  

def formatDate(rawDate) :
    
    res = rawDate.split("T")[0]
    return res


# print (cveTodaySortedByVendor("microsoft"))
# print (cveTodaySortedByCVSS("critical"))
# print (cveTodayNotSorted())
# print (cveTodaySortedByVendorAndCVSS("Linux","Low"))