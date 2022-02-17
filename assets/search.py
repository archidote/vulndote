import requests

urlAPI = "https://cve.circl.lu/api/"

def cveSearch(cveCode) :
    
    url = urlAPI+"cve/"+cveCode
    
    print (url)

    resp = requests.get(url=url)
    data = resp.json() 
    
    print (data)
    
    if data == None:
        cve="No CVE is attached to this CVE code."
    else : 
        cve="Details : "+cveCode+"\n\n"
        cve+="Published : "+data["Published"]+"\n"
        cve+="Edited : "+data["Modified"]+"\n"
        cve+="CVSS Score : "+str(data["cvss"])+"\n"
        cve+="CWE : "+str(data["cwe"])+"\n\n"
        cve+="Summary : "+data["summary"]+"\n\n"
        
    return cve

def impact(cvecode) :

    url = urlAPI+"cve/"+cvecode
    resp = requests.get(url=url)
    data = resp.json() 
    
    cve =""
    cve+="Impact : \n"
    cve += "  Availability : "+data["impact"]["availability"]+"\n"
    cve += "  Confidentiality : "+data["impact"]["confidentiality"]+"\n"
    cve += "  Integrity : "+data["impact"]["integrity"]+"\n"
    
    return cve

def access(cveCode) : 
    
    url = urlAPI+"cve/"+cveCode
    resp = requests.get(url=url)
    data = resp.json() 
    
    cve =""
    cve+="Access : \n"
    cve += "  Availability : "+data["access"]["authentication"]+"\n"
    cve += "  Confidentiality : "+data["access"]["complexity"]+"\n"
    cve += "  Integrity : "+data["access"]["vector"]+"\n"
    
    return cve 

def reference(cveCode) : 
    
    url = urlAPI+"cve/"+cveCode
    resp = requests.get(url=url)
    data = resp.json() 
    
    cve =""
    cve+="\nReferences :\n"
    for line in range(len(data['references'])):
        cve += data['references'][line]+"\n"

    
    return cve 

def ConfigurationAffectedByTheVuln(cveCode) :
    
    url = urlAPI+"cve/"+cveCode

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
TERMINOLOGY : 

CVE : Common Vulnerabilities and Exposures
CVSS : Common Vulnerability Scoring System (0->10)
CVSS-Vector : AV:N/AC:L/Au:N/C:N/I:N/A:P
    More info cvss-vector (v2): https://www.first.org/cvss/v2/guide 
    More info cvss-vector (v3): https://www.first.org/cvss/calculator/3.0
CWE : Common Weakness Enumeration
    More Info : https://fr.wikipedia.org/wiki/Common_Weakness_Enumeration
CPE : Common Platform Enumeration
    More info : https://en.wikipedia.org/wiki/Common_Platform_Enumeration
    
    """
    return terms

# print (cveSearch("CVE-2021-39994"))
# print (impact("CVE-2021-4034"))
# print (access("CVE-2021-4034"))
# print (reference("CVE-2021-4034"))
# print (ConfigurationAffectedByTheVuln("CVE-2021-4034"))
# print (terminology())