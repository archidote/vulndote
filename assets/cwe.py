import requests
from bs4 import BeautifulSoup


response = requests.get("https://cwe.mitre.org/top25/archive/2021/2021_cwe_top25.html")
soup = BeautifulSoup(response.text, 'html.parser')
arrays = soup.findAll('table', attrs={"id":"Detail","style":"margin-left:auto; margin-right:auto;"})
i = 0
for _array in arrays:
    rows = _array.findAll('tr')
    i = i + 1
    if i == 2 : 
        break
    for row in rows :
        rs = row.findAll('td')
        j = 1
        output = ""
        tupleToStr = ""
        for r in rs :
            if j == 1 : 
                tupleToStr = "".join(r.text)
                output += "Rank : "+tupleToStr+"\n"
            if j == 2 : 
                tupleToStr = "".join(r.text)
                output += "ID : "+tupleToStr+"\n"
            if j == 3 : 
                tupleToStr = "".join(r.text)+"\n"
                output += "Name : "+tupleToStr
            if j == 4 : 
                tupleToStr = "".join(r.text)+"\n"
                output += "Score : "+tupleToStr
            if j == 5 : 
                tupleToStr = "".join(r.text)+"\n"
                output += "2020 Rank Change : "+tupleToStr
            j = j + 1
        print(output)