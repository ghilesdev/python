from bs4 import BeautifulSoup as BS
import requests
from PIL import Image
from io import BytesIO

search = input("search for: ")
params = {"q": search}
url = "http://www.google.com/images/search"
r = requests.get(url, params=params)

soup = BS(r.text, "html.parser")
links = soup.findAll("a", {"class": "rg_l"})

for item in links:
    img_obj = requests.get(item.attrs["href"])
    # -1 means last item in the list
    title = item.attrs["href"].split("/")[-1]
    img = Image.open(BytesIO(img_obj.content))
    img.save("./images/" + title, img.format)

    item_text = item.find("a").text
    item_href = item.find("a").attrs["href"]

    if item_text and item_href:
        print(item_text)
        print(item_href)
