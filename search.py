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
        cve+="CVSS Score : "+str(data["cvss"])+"\n"
        cve+="Summary : "+data["summary"]+"\n"
        cve+="Vulnerable Product : \n"+data["vulnerable_product"][0]+"\n"

    return cve

print (cveSearch("CVE-2021-4034"))