import urllib.request
import base64
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch_b64(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            b64 = base64.b64encode(response.read()).decode('utf-8')
            return f"data:image/png;base64,{b64}"
    except Exception as e:
        return str(e)

bkash = fetch_b64("https://freelogopng.com/images/all_img/1656234745bkash-app-logo-png.png")

nagad_urls = [
    "https://freelogopng.com/images/all_img/1679746592nagad-logo-png.png",
    "https://seeklogo.com/images/N/nagad-logo-7A70CCFEE0-seeklogo.com.png",
    "https://upload.wikimedia.org/wikipedia/commons/7/76/Nagad_Logo_2019.svg"
]

nagad = "Not found"
for url in nagad_urls:
    res = fetch_b64(url)
    if "data:image" in res:
        if "svg" in url:
            res = res.replace("image/png", "image/svg+xml")
        nagad = res
        break

with open("logos.txt", "w") as f:
    f.write(bkash + "\n\n")
    f.write(nagad + "\n")
