# same requeste but changing user agent
from bs4 import BeautifulSoup as bs
import requests


def http_request():
    url = "https://httpbin.org/anything"
    params = {"msg": "welcomeuser", "isadmin": 1}
    headers = {"User-Agent": "Chrome"}
    r = requests.post(url=url, headers=headers, params=params)
    soup = bs(r.text, "html.parser")
    print(soup.prettify())


http_request()
