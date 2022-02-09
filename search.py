import requests
from controller import *

def cveSearch(cveCode) :
    url = urlAPI+"/cve/"+cveCode

    resp = requests.get(url=url)
    data = resp.json() 
    
    if data == None:
        cve="No CVE is attached to this CVE code."
    else : 
        cve="Details : "+cveCode+"\n\n"
        cve+="Published : "+data["Published"]+"\n"
        cve+="Edited : "+data["Modified"]+"\n"
        cve+="CVSS Score : "+str(data["cvss"])+"\n\n"
        cve+="Summary : "+data["summary"]+"\n\n"
        cve+="References :\n"
        for line in range(len(data['references'])):
            cve += data['references'][line]+"\n"
        
    return cve

def ConfigurationAffectedByTheVuln(cveCode) :
    
    url = urlAPI+"/cve/"+cveCode

    resp = requests.get(url=url)
    data = resp.json() 
    
    if data == None:
        cve="No CVE is attached to this CVE code."
    else : 
        cve="Details : "+cveCode+"\n\n"
        cve +="Product(s)/Configuration(s) Affected by "+cveCode+"\n\n"
        
        for line in range(len(data['vulnerable_product'])):
            cve += data['vulnerable_product'][line]+"\n"
        return cve 
    
def terminology() : 
    terms = """
    CVE
    CVSS
    CVSS-Vector
    CWE
    
    """
    
    return terms

print (cveSearch("CVE-2021-4034"))
print (ConfigurationAffectedByTheVuln("CVE-2021-4034"))