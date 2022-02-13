import requests
from bs4 import BeautifulSoup
import pandas as pd

header = {"User-Agent":'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0'}

def requestWeb(url):
    page = requests.get(url, headers=header)
    soupe = BeautifulSoup(page.text, 'html.parser')
    return soupe

def search(name,website):
    if(website == "Ebay"):
        url = 'https://www.ebay.ca/sch/i.html?_from=R40&_nkw='+name+'&_sacat=0&rt=nc&_pgn=1'
    elif(website == "Stockx"):
        url = 'https://stockx.com/search?s='+name
    elif(website == "Kijiji"):
        url = 'https://www.kijiji.ca/b-ville-de-montreal/'+name+'/k0l1700281?rb=true&dc=true'
    soupe = requestWeb(url)
    return soupe

def scraper (name,website):
    soupe = search(name,website)
    products = []
    if(website == "Ebay"):
        results1 = soupe.find_all('div',{'class':'s-item__info clearfix'})
        for item in results1:
            if(item.find('h3',{'class':'s-item__title'}).text != "Shop on eBay"):

                product1 = {
                    'title': item.find('h3',{'class':'s-item__title'}).text,
                    'price': item.find('span',{'class' : 's-item__price'}).text,
                    'link': item.find('a',{'class': 's-item__link'})['href'],
                }
                products.append(product1)

    elif(website == "Stockx"):
        results2 = soupe.find_all("div",{"class":"css-1ibvugw-GridProductTileContainer"})
        for item in results2:
            product2 = {
                'title': item.find('p', {'class': 'chakra-text css-3lpefb'}).text,
                'price': item.find('p', {'class': 'chakra-text css-9ryi0c'}).text,
                # 'bids':
                'link': "https://stockx.com"+item.find('a')['href'],
            }
            products.append(product2)
    elif(website == 'Kijiji'):
        results3 = soupe.find_all("div",{"class":"info"})
        for item in results3:
            product3 = {
                'title': item.find('div', {'class':"title"}).text.replace("\n","").replace(" ",""),
                'price': item.find('div', {'class':"price"}).text.replace("\n","").replace("\xa0","").replace(" ",""),
                'link':  "https://www.kijiji.ca"+item.find('a',  {'class':"title"})['href'],
            }
            products.append(product3)

    productspd = pd.DataFrame(products)
    productspd.to_csv(name +' '+website+' '+'output.csv', index=False)
    print('CSV generated !')
    return

productslist = scraper("iphone 13","Ebay")