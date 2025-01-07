import requests
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--enable-logging")
options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
driver = webdriver.Chrome(options=options)

url="https://mora.jp/package/43000002/ANTCD-61742_F/?fmid=TOPRNKA" #change this

driver.get(url)
logs = driver.get_log("performance")
for item in logs:
    log = json.loads(item["message"])["message"]
    if "Network.requestWillBeSentExtraInfo" in log["method"]:
        if "packageMeta.jsonp" in log["params"]["headers"][":path"]:
            meta = log["params"]["headers"][":path"]
            break

res_music = requests.get('https://cf.mora.jp'+str(meta))
a=re.search(r'moraCallback\((.*)\);', res_music.text, re.DOTALL).group(1)
data = json.loads(a)
trackl=data['trackList']
for i in trackl:
    print(i['title'])

