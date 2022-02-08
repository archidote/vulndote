import requests
from sympy import N
from controller import *
import json 

def last(n) :
    
    number = n
    i = 0
    url = urlAPI+"last/"+str(number)

    resp = requests.get(url=url)
    data = resp.json() 
    
    a = ""
    for i in range(number) : 
        a+=data[i]["id"]+"\n"
        a+=data[i]["summary"]+"\n"
        i = i + 1 
        # print (i)
    return a 
print(last(3))