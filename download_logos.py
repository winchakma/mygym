import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req1 = urllib.request.Request("https://upload.wikimedia.org/wikipedia/commons/e/e0/Bkash_Logo.svg", headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req1, context=ctx) as response, open("frontend/img/bkash.svg", 'wb') as out_file:
    out_file.write(response.read())

req2 = urllib.request.Request("https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Nagad_Logo_2019.svg/512px-Nagad_Logo_2019.svg.png", headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req2, context=ctx) as response, open("frontend/img/nagad.png", 'wb') as out_file:
    out_file.write(response.read())

print("Downloaded bkash.svg and nagad.png successfully.")
