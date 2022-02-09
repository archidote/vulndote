import requests
from controller import *

def last(n) :
    
    if n >= 10 : 
        return "Unable to display more than 10 inputs"
    
    number = n
    i = 0
    url = urlAPI+"last/"+str(number)

    resp = requests.get(url=url)
    data = resp.json() 
    
    cve = ""
    for i in range(number) : 
        cve+=data[i]["id"]+"\n\n"
        cve+="Published : "+data[i]["Published"]+"\n"
        cve+="Edited : "+data[i]["Modified"]+"\n"
        cve+="CVSS Score : "+str(data[i]["cvss"])+"\n\n"
        cve+="Summary : "+data[i]["summary"]+"\n\n"
        cve+="Vulnerable Product : \n"+data[i]["vulnerable_product"][i]+"\n\n"
        i = i + 1 
    return cve

def lastInRealTime(): 
    return ""

print(last(3))