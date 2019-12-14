import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38?Tpk=graphics%20cards'

# open connection and grabbing page
uClient = uReq(my_url)
page_html = uClient.read()

# close connection
uClient.close()

# html parsing
page_soup = soup(page_html, "html.parser")

# grabs each product
containers = page_soup.findAll("div", {"class": "item-container"})

filename = "products.csv"
f = open(filename, "w")

headers = "prouctName, brand, features, shipping\n"

f.write(headers)

# grab the current products item-info
for container in containers:
    infoDiv = container.find("div", "item-info")
    brand = infoDiv.div.a.img["title"]
    productName = infoDiv.find("a", "item-title").text
    shipping = infoDiv.find(
        "div", "item-action").find("li", "price-ship").text.strip()

    f.write(productName.replace(",", " | ") + " , " + brand + " , ")

    # get item features and store in a list
    # Using two lists because first list stores all the text including the \n escapechars that need to be replaced which is done in the second loop and appended to the first
    features = infoDiv.find("ul", "item-features").findAll("li")
    tempFeatures = []
    featureTextList = []
    for feature in features:
        tempFeatures.append(feature.text)

    for feature in tempFeatures:
        tempText = feature.replace('\n', ' | ')
        featureTextList.append(tempText)
        f.write(tempText + " | ")

    print(f"Product Name: {productName}")
    print(f"Brand: {brand}")
    print(f"Feature list: {featureTextList}")
    print(f"Shipping: {shipping}")
    print("\n")

    f.write(" , " + shipping + "\n")

f.close()
