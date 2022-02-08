import requests
from controller import *

def currentweather() :
    url = urlAPI+"/last/10"

    resp = requests.get(url=url)
    data = resp.json() 

    return data

print (currentweather())