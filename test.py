from assets.cvePoCExploits import * 
import httpx
request = httpx.Client(http2=True)
headers = {
'Referer': 'https://sploitus.com/'}

params={"type":"exploits","sort":"default","query":"CVE-2021-4034","title":"true","offset":0}
response = request.post('https://sploitus.com/search', json=params, headers=headers)
print(response)
data = response.json()
print (data)