from bs4 import BeautifulSoup as BS
import requests

search = input("enter search terms:")
params = {"q": search}
url = "https://www.bing.com/search?"
r = requests.get(url, params=params)

soup = BS(r.text, "html.parser")
print(soup.prettify())

result = soup.find("ol", {"id": "b_results"})
links = result.findAll("li", {"class": "b_algo"})

for item in links:
    item_text = item.find("a").text
    item_href = item.find("a").attrs["href"]

    if item_text and item_href:
        print(item_text)
        print(item_href)
        print("resumé: ", item.find("a").parent.parent.find("p").text)
        children = item.children

        for child in children:
            print("child: ", child)
