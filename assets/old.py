# Sploitus bypass cloudflare WAF PoC

import httpx
request = httpx.Client(http2=True)
headers = {
'Host': 'sploitus.com',
'Accept': 'application/json',
'Content-Type': 'application/json',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
'Origin': 'https://sploitus.com',
'Sec-Fetch-Site': 'same-origin',
'Referer': 'https://sploitus.com/'} # Only Referrer is required

params={"type":"exploits","sort":"default","query":"CVE-2021-4034","title":"true","offset":0}
response = request.post('https://sploitus.com/search', json=params, headers=headers)
print(response)
data = response.json()
print (data)