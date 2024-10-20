from bs4 import BeautifulSoup
import requests
from PIL import Image
import json
import urllib.request, urllib.error, urllib.parse
import os

def get_soup(url, header):
    url = url.replace(" ", "+")
    url = url.replace("♀", "+male")
    url = url.replace("♂", "+female")
    return BeautifulSoup(urllib.request.urlopen(
        urllib.request.Request(url, headers=header)),
        'html.parser')

query = ["+pokemon+wallpaper", "+pokemon+card", "+pokemon+art"]

header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

def find_image(name, orname):
    url = "http://www.bing.com/images/search?q=" + name + "&FORM=HDRSC2"
    soup = get_soup(url, header)
    found_imgs = []
    for a in soup.find_all("a", {"class": "iusc"}):
        try:
            m = json.loads(a["m"])
            murl = m["murl"]
            turl = m["turl"]
            image_name = urllib.parse.urlsplit(murl).path.split("/")[-1]
            if orname in image_name.lower():
                found_imgs.append((turl, image_name.split(".")[-1]))
        except:
            pass
    return found_imgs

with open("temp1.json") as file:
    dex = json.load(file)
    for key in dex:
        name = dex[key]["name"]
        print()
        count = 2
        for suffix in query:
            print(name + suffix, key)
            c = 1
            found_imgs = find_image(name + suffix, name.lower())
            for link in found_imgs:
                try:
                    img = Image.open(requests.get(link[0], stream=True).raw)
                    img = img.resize((224, 224))
                    directory = f"E:/DataSet/{key}_{name}"
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    img.save(f"{directory}/{count}.{link[1]}")
                    count += 1
                    c += 1
                except Exception as e:
                    pass
                if c == 20:
                    break
        print()