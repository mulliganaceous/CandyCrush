import json
import urllib.parse
import urllib.request
import http.cookiejar

WIKI = "https://candycrush.fandom.com"
API = WIKI + "/w/api.php"

USERNAME = "--MULLIGANACEOUS--"
PASSWORD = "Shadowtack666!"

# Cookie jar so we stay logged in
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) fandom-scraper/0.1 (contact: you@example.com)"
}

def http_get(url, params=None):
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    with opener.open(req) as resp:
        return resp.read()

def http_post(url, data_dict):
    data = urllib.parse.urlencode(data_dict).encode("utf-8")
    req = urllib.request.Request(url, headers=HEADERS, data=data, method="POST")
    with opener.open(req) as resp:
        return resp.read()

# 1) Fetch login token
token_raw = http_get(API, {
    "action": "query",
    "meta": "tokens",
    "type": "login",
    "format": "json",
})
token_json = json.loads(token_raw.decode("utf-8"))
login_token = token_json["query"]["tokens"]["logintoken"]

# 2) clientlogin (interactive flow)
login_raw = http_post(API, {
    "action": "clientlogin",
    "format": "json",
    "username": USERNAME,
    "password": PASSWORD,
    "logintoken": login_token,
    "loginreturnurl": WIKI + "/",
})

login_json = json.loads(login_raw.decode("utf-8"))
status = login_json.get("clientlogin", {}).get("status")

if status != "PASS":
    raise RuntimeError(f"Login failed: {login_json}")

print("Logged in.")

# 3) Now call the comments endpoint (example)
comments_url = WIKI + "/wikia.php"
comments_raw = http_get(comments_url, {
    "controller": "ArticleCommentsController",
    "method": "getComments",
    "title": "SomePageTitle",
    "namespace": 0,
    "page": 1,
    "hideDeleted": "false",
    "format": "json",
})
comments_json = json.loads(comments_raw.decode("utf-8"))
print(json.dumps(comments_json, indent=2)[:2000])