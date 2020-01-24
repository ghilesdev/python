from  bs4 import  BeautifulSoup as bs
import  requests


def http_request():
    url='https://httpbin.org/anything'
    params={"msg":"welcomeuser","isadmin":1}
    r=requests.post(url=url,params=params)
    soup=bs(r.text,"html.parser")
    print(soup.prettify())

