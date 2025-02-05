import httpx, json, base64, random
from time import sleep, time
import websocket
import undetected_chromedriver as uc
from urllib import parse
from json import dumps
from os import _exit
from os.path import dirname
from inspect import getsourcefile

# Discord invite link
# Just replace with None if you don't want to join a server upon creation
#invite = "xxxxxx" # Only the string after /
invite = None

# Delay to wait after creating an account
delay = 120

# Enable email verification
# This also needs an extra captchakey for verification part
# Provider 1: 10minutemail.com, Provider 2: 10minemail.com, Provider 3: noopmail.org, Provider 4: praisegang.com, Provier 5: throwaway.io
emailver = True
provider = 2

# Rotating proxy or does it use a list of proxies
rotating = False
rotatingproxy = ""

# Debug mode, gives all information about what the gen is doing
debug = True

# Phone verify (only if email is verified as well)
phonever = False
# Mode 1: 5sim.net, Mode 2: sms-activate.ru
mode = 2
# 5sim.net api key
simapikey = 'x.x.x--x-x-x-x-x-x-x-x-x-x'
# sms-activate.ru api key
smsapikey = 'x'

# Join a hypesquad (only if email is verified as well)
hypesquad = True
# House of Bravery (id = 1), House of Brilliance (id = 2), House of Balance (id = 3)
#house_id = 1
# For randomization
house_id = random.randint(1,3)

# Download and upload a random profile picture
pfp = True

# Turn off tracking and censorship
privacy = True

# Multithreading mode
# 1: threading module [less ram heavy but slower], 2: multiprocessing module [more ram heavy but faster]
mode = 2

# Webhook to post account details
webhook = "https://discord.com/api/webhooks/x/x-x-x"

# Tries from a single IP before discarding it (hcaptcha)
tries = 3

# Random usernames from a text file
usernames = []
path = dirname(getsourcefile(lambda:0))
with open(f'{path}/discord_usernames.txt', 'r', encoding='UTF-8') as discordnames:
    for x in discordnames:
        usernames.append(x)

# Handling captcha
sitekey = "f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34"
host = "discord.com"
discordratelimit = []

# Random Stuff
data = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&'()*+,-./;<=>?@[\]^_`{|}~'''
dataE = '''abcdefghijklmnopqrstuvwxyz0123456789'''

# 5sim.net
headersPHONE = {
    'Authorization': 'Bearer ' + simapikey,
    'Accept': 'application/json',
}

if mode == 1:
    from threading import Thread, active_count
    def active_threads():
        return active_count()-1
    genned = [0.0]
elif mode == 2:
    from multiprocessing import Process as Thread
    from multiprocessing import active_children, Value
    def active_threads():
        return len(active_children())
    genned = Value('d', 0.0)

if rotating == False:
    # Used.txt (HCaptcha logic)
    try:
        # Check if hcaptcha used proxies are past 24 hour discordratelimit

        with open(f'{path}/used.txt', 'r') as hp_file:
            # Reads the entire file into a list
            hcaptcharatelimit = hp_file.readlines()

        # We can not delete lines from the array as we try to scan through
        # it with a for statement so I make a copy to work with.
        copy_of_lines = hcaptcharatelimit.copy()
        for line in copy_of_lines:
            try:
                if time()-float(line.split(",")[1]) >= 86400: #86400 seconds or 1440 minutes or 24 hours
                    hcaptcharatelimit.remove(line)      # to remove this line
            except:
                hcaptcharatelimit.remove(line) # error so remove the line
        hcaptcharatelimit[-1] = hcaptcharatelimit[-1].replace("\n","") # avoid blank line at the end
        with open(f'{path}/used.txt', 'w') as hp_file:  # Open in mode "w" removes all the data from the file.
            hp_file.writelines(hcaptcharatelimit)    # Writes the entire list into the file

        for i in range(len(hcaptcharatelimit)): # I only need the proxies not their timestamp
            hcaptcharatelimit[i] = hcaptcharatelimit[i][0:hcaptcharatelimit[i].rfind(",")]
    except:
        hcaptcharatelimit = []
        pass
    proxieshcaptcha = []
    for line in open(f'{path}/proxieshcaptcha.txt'):
        proxieshcaptcha.append(line.replace('\n', ''))

uc.TARGET_VERSION = 93
options = uc.ChromeOptions()
options.headless=True
driver = uc.Chrome(options=options)
driver.execute_script("null")
hsj = open(f"{path}/hsj.js", "r").read()
def getcaptchakey(numbert, proxy):
    headersCONFIG = {
        "Host": "hcaptcha.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json; charset=utf-8",
        "Cache-Control": "no-cache",
        "Origin": "https://newassets.hcaptcha.com",
        "Connection": "keep-alive",
        "Referer": "https://newassets.hcaptcha.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "TE": "trailers"
    }
    try:
        config = httpx.get("https://hcaptcha.com/checksiteconfig?host=discord.com&sitekey=f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34&sc=1&swa=1", headers=headersCONFIG, timeout=None)
        c = config.json()
        c["c"]["type"] = "hsj"
        c = dumps(c["c"])
        req = config.json()["c"]["req"]
    except:
        return False
    n = driver.execute_script(hsj + f"return hsj('{req}');")
    json = {
        "v": "7b183e4",
        "sitekey": "f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34",
        "host": "discord.com",
        "hl": "en",
        "motionData": '{"v":1,"topLevel":{"st":1632506059500,"sc":{"availWidth":1366,"availHeight":734,"width":1366,"height":768,"colorDepth":24,"pixelDepth":24,"top":0,"left":0,"availTop":0,"availLeft":0,"mozOrientation":"landscape-primary","onmozorientationchange":null},"nv":{"permissions":{},"doNotTrack":"unspecified","maxTouchPoints":0,"mediaCapabilities":{},"oscpu":"Linux x86_64","vendor":"","vendorSub":"","productSub":"20100101","cookieEnabled":true,"buildID":"20181001000000","mediaDevices":{},"credentials":{},"clipboard":{},"mediaSession":{},"webdriver":false,"hardwareConcurrency":4,"geolocation":{},"appCodeName":"Mozilla","appName":"Netscape","appVersion":"5.0 (X11)","platform":"Linux x86_64","userAgent":"Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0","product":"Gecko","language":"en-US","languages":["en-US","en"],"onLine":true,"storage":{},"plugins":[]},"dr":"","inv":false,"exec":false,"wn":[[1354,590,1,1632506059651]],"wn-mp":0,"xy":[[0,0,1,1632506059652]],"xy-mp":0,"mm":[[540,474,1632506059653],[541,473,1632506059702]],"mm-mp":49},"session":[],"widgetList":["075smy0yd1tm"],"widgetId":"075smy0yd1tm","href":"https://discord.com/","prev":{"escaped":false,"passed":false,"expiredChallenge":false,"expiredResponse":false}}',
        "n": n,
        "c": c
    }
    data = parse.urlencode(json)
    headersCAPTCHA = {
        "Host": "hcaptcha.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-type": "application/x-www-form-urlencoded",
        "Content-Length": str(len(data)),
        "Origin": "https://newassets.hcaptcha.com",
        "Connection": "keep-alive",
        "Referer": "https://newassets.hcaptcha.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "TE": "trailers"
    }
    try:
        cookies = {"hc_accessibility": "0A/jgkF8hJmTiHAKKtEDHfrxCwOBEhfwSzM9u8A87vRY2UOuHu7Xm/iR71bappwF+VhBZe2W8FaVzpioleqz9hOQlFbmKvSg1xAFsmh3VcWyJu4OjxJ6j39Qd0czB+e3b329f9iKVsgvaIfVTKp8sUdWy3Uqf9X7oR60+JtFYsZ3Kqtz9/UHS0S1l2cMBVMOUu2paokIWfsRRNPU++wJ12w1sfPohySN14OQ/3EDIc2Su9LS9UF/EVrlriRx3IMeb64fzHsEXKV5qBZsuTi6WvTfqamrhu+b8SDnFD0iMLxYl4QV+Zst5lXn+OTNkselStdfj2eGeELazDMkNUFgh7EnrAI5X+baMqhcbPDTvXA9MjXqAjaLYmuOBLpinHili0baKmUrW31wgq6rChpX7bDbIiUXx35JRkAyEA==rM0T7f/v8SQEfUiM"}
        captcha = httpx.post("https://hcaptcha.com/getcaptcha?s=f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34", cookies=cookies, headers=headersCAPTCHA, data=data, proxies=proxy, timeout=None)
        return captcha.json()["generated_pass_UUID"]
    except:
        return False

def ensurecaptchakey(numbert, proxy=None):
    dprint(numbert, "Getting captcha key...")
    while True:
        if rotating == False:
            for x in hcaptcharatelimit:
                try:
                    proxieshcaptcha.remove(x)
                except:
                    pass
            if proxieshcaptcha == []:
                print("All proxies for hcaptcha are ratelimited...")
                _exit(1)
            origproxy = random.choice(proxieshcaptcha)
            if origproxy == "None":
                proxy = None
            else:
                proxy = "http://"+origproxy
            for i in range(tries):
                captchakey = getcaptchakey(numbert, proxy)
                if i == (tries-1) and captchakey == False:
                    hcaptcharatelimit.append(origproxy)
                    with open(f'{path}/used.txt','a+') as hp:
                        hp.write(f"\n{origproxy},{time()}")
                    dprint(numbert, "Discarded "+origproxy+" proxy for hcaptcha")
                if captchakey != False:
                    break
        else:
            captchakey = getcaptchakey(numbert, proxy)
        if captchakey != False:
            break
    return(captchakey)

def dprint(numbert, string):
    if debug == True:
        print(f"Thread {str(numbert)}: {string}")

def book(proxy):
    if rotating == False:
        temporary = proxy+",9999999999"
        discordratelimit.append(temporary) # No one uses this proxy once it's being used

def release(proxy, time, retry=delay):
    if rotating == False:
        temporary = proxy+",9999999999"
        discordratelimit.remove(temporary)
        discordratelimit.append(f"{proxy},{time},{retry}")

def accountgen(proxydiscord, numbert, genned):
    # Handling proxy
    
    origproxydiscord = proxydiscord
    book(origproxydiscord)
    username = random.choice(usernames)
    if proxydiscord == "None":
        proxydiscord = None
    else:
        proxydiscord = "http://"+proxydiscord
    
    captchakey = ensurecaptchakey(numbert, proxydiscord)
    
    try:
        with httpx.Client(timeout=None) as client:

            #Getting of email
            emailwork = False
            phonework = False
            if emailver == True:
                password = "".join(random.sample(data,8))
                if provider == 1:
                    try:
                        # Get email
                        dprint(numbert, "Getting the email...")
                        email = client.get("https://10minutemail.com/session/address").json()
                        email = email["address"]
                        emailwork=True
                    except:
                        dprint(numbert, "Failed to get email for 10minutemail")
                elif provider == 2:
                    try:
                        dprint(numbert, "Getting the email...")
                        getmail = client.post("https://web2.10minemail.com/mailbox").json()
                        email = getmail["mailbox"]
                        authorize = getmail["token"]
                        emailwork=True
                    except:
                        dprint(numbert, "Failed to get email for 10minemail")
                elif provider == 3:
                    try:
                        domains = client.get("https://www.noopmail.org/api/d").json()
                        # Remove .xyz domains
                        for x in domains:
                            if ".xyz" in x:
                                domains.remove(x)
                        domain = random.choice(domains)
                        e = "".join(random.sample(dataE,15))
                        email = e+"@"+domain
                        emailwork=True
                    except:
                        dprint(numbert, "Failed to get email for noopmail")
                elif provider == 4:
                    try:
                        email = client.get("https://privtempmail.praisegang.com/api/email/thisfunction/DJ9XH1b0z2P8fcKhiuFy").text
                        name = email.split("@")[0]
                        emailwork = True
                    except:
                        dprint(numbert, "Failed to get email for praisegang.com")
                elif provider == 5:
                    try:
                        http = client.get("https://www.throwaway.io/").text
                        http = http[http.find('<input type="hidden" name="_token"'):http.find('<input type="submit" action="Create" value="Create">')].split('\n')
                        t = http[0]
                        t = t[t.find('value')+7:t.find('">')]
                        domains = []
                        for x in http:
                            if '"domain-selector' in x:
                                domains.append(x[x.find('"#">')+4:x.find('</a>')])
                        try:
                            domains.remove("@throwaway.io")
                        except:
                            pass
                        e = "".join(random.sample(dataE,15))
                        domain = random.choice(domains)
                        email = e+domain
                        json = {"_token":t,"email":e,"domain":domain}
                        if client.post("https://www.throwaway.io/mailbox/create/custom", json=json).status_code == 200:
                            client.get(f"https://www.throwaway.io/mailbox/{email}")
                            emailwork = True
                    except:
                        dprint(numbert, "Failed to get email for throwaway.io")

            if emailwork == True:
                dprint(numbert, "Email: "+email+" Password: "+password)

        	# Get __dcfduid and __sdcfduid cookies

            headersCOOKIE = {
            	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            	"Accept-Encoding": "gzip, deflate, br",
            	"Accept-Language": "en-US,en;q=0.5",
            	"Connection": "keep-alive",
            	"Host": "discord.com",
            	"Sec-Fetch-Dest": "document",
            	"Sec-Fetch-Mode": "navigate",
            	"Sec-Fetch-Site": "none",
            	"Sec-Fetch-User": "?1",
            	"Upgrade-Insecure-Requests": "1",
            	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
            }
            dprint(numbert, "Getting the __dcfduid and __sdcfduid cookies...")
            cookies = client.get("https://discord.com/register", headers=headersCOOKIE).cookies
            dcfduid = cookies["__dcfduid"]
            sdcfduid = cookies["__sdcfduid"]
            '''
            #Convert __sdcfduid to __dcfduid (Shouldn't use unless needed)
            dcfduid = sdcfduid[:7]+"0"+sdcfduid[8:32]
            '''

            # Get the fingerprint

            headersMAIN = {
            	"Host": "discord.com",
            	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
            	"Accept": "*/*",
            	"Accept-Language": "en-US",
            	"Accept-Encoding": "gzip, deflate, br",
            	"X-Super-Properties": "eyJvcyI6IkxpbnV4IiwiYnJvd3NlciI6IkZpcmVmb3giLCJkZXZpY2UiOiIiLCJzeXN0ZW1fbG9jYWxlIjoiZW4tVVMiLCJicm93c2VyX3VzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoWDExOyBMaW51eCB4ODZfNjQ7IHJ2OjkxLjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvOTEuMCIsImJyb3dzZXJfdmVyc2lvbiI6IjkxLjAiLCJvc192ZXJzaW9uIjoiIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjk3MDk3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==",
            	"X-Context-Properties": "eyJsb2NhdGlvbiI6IkFjY2VwdCBJbnZpdGUgUGFnZSJ9",
            	"Authorization": "undefined",
            	"X-Debug-Options": "bugReporterEnabled",
            	"Connection": "keep-alive",
            	"Referer": "https://discord.com/register",
            	"Sec-Fetch-Dest": "empty",
            	"Sec-Fetch-Mode": "cors",
            	"Sec-Fetch-Site": "same-origin",
            	"TE": "trailers"
            }
            dprint(numbert, "Getting the fingerprint...")
            fingerprint = client.get("https://discord.com/api/v9/experiments", headers=headersMAIN).json()["fingerprint"]
            headersMAIN.pop("X-Context-Properties")
            headersMAIN["X-Fingerprint"] = fingerprint

            # Register JSON
            if emailwork == True:
                register = {"fingerprint":fingerprint,"email":email,"password":password,"username":username,"invite":invite,"consent":True,"gift_code_sku_id":None,"captcha_key":captchakey}
            else:
                register = {"fingerprint":fingerprint,"username":username,"invite":invite,"consent":True,"gift_code_sku_id":None,"captcha_key":captchakey}
            # Registration headers

            headersREGISTER = {
            	"Host": "discord.com",
            	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
            	"Accept": "*/*",
            	"Accept-Language": "en-US",
            	"Accept-Encoding": "gzip, deflate, br",
            	"Content-Type": "application/json",
            	"Authorization": "undefined",
            	"X-Super-Properties": "eyJvcyI6IkxpbnV4IiwiYnJvd3NlciI6IkZpcmVmb3giLCJkZXZpY2UiOiIiLCJzeXN0ZW1fbG9jYWxlIjoiZW4tVVMiLCJicm93c2VyX3VzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoWDExOyBMaW51eCB4ODZfNjQ7IHJ2OjkxLjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvOTEuMCIsImJyb3dzZXJfdmVyc2lvbiI6IjkxLjAiLCJvc192ZXJzaW9uIjoiIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjk3MDk3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==",
            	"X-Fingerprint": fingerprint,
                "Cookie": f"__dcfduid={dcfduid}; __sdcfduid={sdcfduid}",
            	"X-Debug-Options": "bugReporterEnabled",
            	"Origin": "https://discord.com",
            	"Connection": "keep-alive",
            	"Referer": "https://discord.com/register",
            	"Sec-Fetch-Dest": "empty",
            	"Sec-Fetch-Mode": "cors",
            	"Sec-Fetch-Site": "same-origin",
                "TE": "trailers"
            }

            # Register an account
            dprint(numbert, "Registering account...")
            registration = httpx.post("https://discord.com/api/v9/auth/register", headers=headersREGISTER, json=register, proxies=proxydiscord, timeout=None)
            registrationjson = registration.json()
            try:
                token = registrationjson["token"]
                dprint(numbert, "Registration successful Token: "+token)
                ws = websocket.WebSocket()
                ws.connect("wss://gateway.discord.gg/?encoding=json&v=9&compress=zlib-stream")
                
                auth = {
                    "op":2,
                    "d": {
                    "token": token,
                    "capabilities": 61,
                    "properties": {"os":"Windows","browser":"Chrome","device":"","system_locale":"en-GB","browser_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36","browser_version":"90.0.4430.212","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":"85108","client_event_source":"null"}, 
                    "presence": {
                        "status":"online",
                        "since":0,
                        "activities":[],
                        "afk":False
                    },
                    "compress":False,
                    "client_state":{
                        "guild_hashes":{},
                        "highest_last_message_id":"0",
                        "read_state_version":0,
                        "user_guild_settings_version":-1
                    }
                    }
                }

                ws.send(dumps(auth))
                ws.recv()
                ws.close()
            except:
                dprint(numbert, "Registration unsuccessful. Error:")
                print("RESPONSE CODE:", str(registration.status_code)+"\nRESPONSE CONTENT: ",registration.content.decode('utf-8'))
                try:
                    retry = registrationjson["retry_after"]
                    release(origproxydiscord, time(), retry)
                except:
                    #registrationjson["errors"]["username"]["_errors"][0]["code"]
                    release(origproxydiscord,"0")
                    pass
                exit()

            headersMAIN["Authorization"] = token
            headersMAIN["Content-Type"] = "application/json"
            headersMAIN["Origin"] = "https://discord.com"

            # Email verification
            if emailwork == True:
                try:
                    # Headers
                    headersVERIFY = {
                        "Host": "discord.com",
                        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
                        "Accept": "*/*",
                        "Accept-Language": "en-US",
                        "Accept-Encoding": "gzip, deflate, br",
                        "X-Super-Properties": "eyJvcyI6IkxpbnV4IiwiYnJvd3NlciI6IkZpcmVmb3giLCJkZXZpY2UiOiIiLCJzeXN0ZW1fbG9jYWxlIjoiZW4tVVMiLCJicm93c2VyX3VzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoWDExOyBMaW51eCB4ODZfNjQ7IHJ2OjkxLjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvOTEuMCIsImJyb3dzZXJfdmVyc2lvbiI6IjkxLjAiLCJvc192ZXJzaW9uIjoiIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjk4NjQzLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==",
                        "X-Fingerprint": fingerprint,
                        "Authorization": "undefined",
                        "Origin": "https://discord.com",
                        "Content-Type": "application/json",
                        "X-Debug-Options": "bugReporterEnabled",
                        "Connection": "keep-alive",
                        "Referer": "https://discord.com/verify",
                        "Sec-Fetch-Dest": "empty",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Site": "same-origin",
                        "TE": "trailers"
                    }
                    # Waiting and extraction of verification link
                    dprint(numbert, "Waiting for email verification link...")
                    if provider == 1:
                        while True:
                            try:
                                link = client.get("https://10minutemail.com/messages/messagesAfter/0").json()[0]["bodyPlainText"]
                                link = link[link.rfind("Verify Email: ")+14:-4]
                                break
                            except:
                                pass
                    elif provider == 2:
                        headersMINEMAIL = {
                            "Host": "web2.10minemail.com",
                            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
                            "Accept": "application/json",
                            "Accept-Language": "en-US,en;q=0.5",
                            "Accept-Encoding": "gzip, deflate, br",
                            "Authorization": "Bearer "+authorize,
                            "Origin": "https://10minemail.com",
                            "DNT": "1",
                            "Connection": "keep-alive",
                            "Referer": "https://10minemail.com/",
                            "Sec-Fetch-Dest": "empty",
                            "Sec-Fetch-Mode": "cors",
                            "Sec-Fetch-Site": "same-site",
                            "TE": "trailers"
                        }
                        while True:
                            try:
                                identi = client.get("https://web2.10minemail.com/messages", headers=headersMINEMAIL).json()["messages"][0]["_id"]
                                break
                            except:
                                pass
                        link = client.get("https://web2.10minemail.com/messages/"+identi, headers=headersMINEMAIL).json()["bodyHtml"]
                        link = link[link.rfind('><a href="')+10:link.rfind('" style="t')]
                    elif provider == 3:
                        while True:
                            try:
                                identi = client.post("https://www.noopmail.org/api/c", json={"e":e,"d":domain}).json()[0]["id"]
                                break
                            except:
                                pass
                        link = client.get("https://www.noopmail.org/api/i/"+identi).json()["text"]
                        link = link[link.rfind("Verify Email: ")+14:-2]
                    elif provider == 4:
                        while True:
                            try:
                                link = client.get(f"https://privtempmail.praisegang.com/api/messages/{name}/DJ9XH1b0z2P8fcKhiuFy").json()[0]["content"]
                                link = link[link.rfind('><a target="blank" href="')+25:link.rfind('" style="t')]
                                break
                            except:
                                sleep(5)
                                pass
                    elif provider == 5:
                        while True:
                            etc = client.get("https://www.throwaway.io/mail/fetch?new=true").json()
                            if len(etc) > 1:
                                del etc["length"]
                                for x in etc:
                                    link = etc[x]["text"]
                                    link = link[link.rfind("Verify Email: ")+14:-10]
                                break
                    # Verification after getting the link
                    dprint(numbert, "Getting the email verification token...")
                    tokenv = httpx.get(link, allow_redirects=False).headers["location"][33:]
                    dprint(numbert, "Received successfully, starting verification...")
                    everify = client.post("https://discord.com/api/v9/auth/verify", headers=headersVERIFY, json={"token":tokenv,"captcha_key":None})
                    if everify.status_code == 400:
                        dprint(numbert, "Captcha required for email verification...")
                        everify = client.post("https://discord.com/api/v9/auth/verify", headers=headersVERIFY, json={"token":tokenv,"captcha_key":ensurecaptchakey(numbert, proxydiscord)})
                    token=everify.json()["token"]
                    dprint(numbert, "New token after verification: "+token)
                    headersMAIN["Authorization"] = token
                except Exception as e:
                    print(e)
                    print(f"Failed to verify {token}")
                    release(origproxydiscord,"0")
                    exit()

            if emailwork == True and hypesquad == True:
                dprint(numbert, "Setting the hypesquad...")
                client.post("https://discord.com/api/v9/hypesquad/online", headers=headersMAIN, json={"house_id":house_id})

            if emailwork == True and phonever == True:
                dprint(numbert, "Buying an activation phone number...")
                if mode == 1:
                    try:
                        buy = client.get('https://5sim.net/v1/user/buy/activation/england/lycamobile/discord', headers=headersPHONE)
                        buy = buy.json()
                        idi = buy["id"]
                        number = buy["phone"]
                        phonework = True
                    except:
                        print(buy.text)
                        phonework = False
                        pass
                elif mode == 2:
                    try:
                        buy = client.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key={smsapikey}&action=getNumber&service=ds&country=16').text
                        buys = buy.split(":")
                        idi = buys[1]
                        number = "+"+buys[2]
                        phonework = True
                    except:
                        print(buy)
                        phonework = False


            if phonework == True:
                try:
                    dprint(numbert, "Sending phone to discord...")
                    if client.post("https://discord.com/api/v9/users/@me/phone", headers=headersMAIN, json={"phone":number}).status_code == 204:
                        dprint(numbert, "Waiting for verification code...")
                        if mode == 1:
                            while True:
                                try:
                                    codereq = client.get('https://5sim.net/v1/user/check/' + str(idi), headers=headersPHONE)
                                    code = codereq.json()["sms"][0]["code"]
                                    break
                                except:
                                    if codereq.text == "order not found":
                                        break
                                    sleep(2)
                        elif mode == 2:
                            while True:
                                codereq = client.get(f"https://sms-activate.ru/stubs/handler_api.php?api_key={smsapikey}&action=getStatus&id={idi}", timeout=None).text
                                if "STATUS_OK" in codereq:
                                    code = codereq[10:]
                                    break
                                elif codereq != "STATUS_WAIT_CODE":
                                    print(codereq)
                                    break
                                else:
                                    sleep(2)
                        dprint(numbert, "Getting phone verification token...")
                        phonevertoken = client.post("https://discord.com/api/v9/phone-verifications/verify", headers=headersMAIN, json={"phone":number, "code":code}).json()["token"]
                        dprint(numbert, "Sending the phone verification token...")
                        if client.post("https://discord.com/api/v9/users/@me/phone", headers=headersMAIN, json={"phone_token":phonevertoken,"password":password}).status_code != 204:
                            phonework = False
                    else:
                        phonework = False
                except:
                    phonework = False
                
            headersMAIN.pop("X-Fingerprint")

            # Set date of birth and in the process get the discriminator :)
            dprint(numbert, "Submitting the date of birth...")
            info = client.patch("https://discord.com/api/v9/users/@me", headers=headersMAIN, json={"date_of_birth":"1900-01-01"}).json()
            #print("RESPONSE CODE:", str(info.status_code)+"\nRESPONSE CONTENT: ",info.content.decode('utf-8'))
            accountid = info["id"]
            username = info["username"]
            discriminator = info["discriminator"]
            headersMAIN["X-Fingerprint"] = fingerprint

            if pfp == True:
                # Set a random picture because why not
                dprint(numbert, "Downloading a random picture...")
                pic = str(base64.b64encode(client.get("https://picsum.photos/128/128").content),'UTF-8')
                dprint(numbert, "Uploading the picture as profile picture...")
                client.patch("https://discord.com/api/v9/users/@me", data='{"avatar":"data:image/png;base64,'+pic+'"}', headers=headersMAIN)

            if privacy == True:
                # Turn off some data tracking and censorship
                try:
                    dprint(numbert, 'Turning off "explicit filter" and turning on "view nsfw guild on iOS"...')
                    client.patch("https://discord.com/api/v9/users/@me/settings", headers=headersMAIN, json={"explicit_content_filter":0,"view_nsfw_guilds":True})
                    dprint(numbert, "Denying discord the access to usage statistics and personalization...")
                    client.post("https://discord.com/api/v9/users/@me/consent", headers=headersMAIN, json={"grant":[],"revoke":["usage_statistics", "personalization"]})
                    headersMAIN.pop("Content-Type")
                    dprint(numbert, "Skipping all the tips and tutorials...")
                    client.post("https://discord.com/api/v9/tutorial/indicators/suppress", headers=headersMAIN)
                except Exception as e:
                    print(e)
                    pass
        
            if phonework == True:
                output = f"{token} // ID: {accountid} Name: {username}#{discriminator} Details: {email}:{password} Phone: {number}"
                kind = "phone"
            elif emailwork == True:
                output = f"{token} // ID: {accountid} Name: {username}#{discriminator} Details: {email}:{password}"
                kind = "email"
            else:
                output = f"{token} // ID: {accountid} Name: {username}#{discriminator}"
                kind = "unverified"

            try:
                dprint(numbert, "Sending account details to webhook...")
                client.post(webhook, json={"username":username,"content":f"```{output}```"})
            except:
                pass
        
        # Print and save the details
        print(output)
        with open(f"{path}/tokens_{kind}.txt","a+") as f:
            f.write(f"\n{output}")
        if mode == 1:
            genned[0] += 1
        elif mode == 2:
            genned.value += 1
    except Exception as e:
        dprint(numbert, "An exception occured due to non working proxy or wrong code. Exception:")
        print(e)
        pass

# Parsing proxies
proxiesdiscord = []
for line in open(f'{path}/proxiesdiscord.txt'):
    proxiesdiscord.append(line.replace('\n', ''))

numbert = 0

try:
    threads = int(input("Number of threads to use: "))
    origthreads = threads
    accounts = int(input("Amount of accounts to generate (0 for unlimited): "))
except:
    print("Please input a valid number")
    exit()

if accounts < threads and accounts != 0:
    print("Threads must be lower than or equal to the accounts to be generated.")
    exit()

while True:
    if accounts != 0:
        # Limit number of accounts generated if requested
        if mode == 1:
            generated = int(genned[0])
        elif mode == 2:
            generated = int(genned.value)
        if generated >= accounts:
            print(generated, "accounts generated.")
            _exit(1)
        while True:
            if generated + threads >= accounts + 1:
                threads -= 1
                origthreads = threads
            else:
                break
    if rotating == False:
        # discordRatelimit checks for proxies
        for x in discordratelimit:
            y = x.split(",")
            try:
                proxiesdiscord.remove(y[0])
            except:
                pass
            try: 
                wait = round(float(y[2]))
            except:
                wait = delay
            if (time()-float(y[1])) >= wait:
                proxiesdiscord.append(y[0])
                discordratelimit.remove(x)
        # Decrease/Increase threads if proxies are discordratelimited
        while True:
            if len(proxiesdiscord) < threads:
                threads -= 1
            elif len(proxiesdiscord) > threads and threads < origthreads:
                threads += 1
            else:
                break
        try:
            proxysdiscord = random.sample(proxiesdiscord, threads)
            for i in range(threads-active_threads()):
                numbert += 1
                Thread(target=accountgen, args=(proxysdiscord[i],numbert,genned,)).start()
        except:
            pass
    else:
        for i in range(threads-active_threads()):
            numbert += 1
            Thread(target=accountgen, args=(rotatingproxy,numbert,genned,)).start()
