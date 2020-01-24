import requests
params={"q":"pizza"}
r=requests.get("http://google.com/search",params=params)
print("status: ", r.status_code)
print(r.url)
file=open("./page.html","w+")
file.write(r.text)