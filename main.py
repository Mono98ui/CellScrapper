import requests
from bs4 import BeautifulSoup
import pandas as pd #csv file

url = 'https://www.ebay.ca/sch/i.html?_from=R40&_trksid=p2380057.m570.l1311&_nkw=samsung+galaxy+s10&_sacat=0';

#User-Agent :
#Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0

def get_data(url):
    # try:
    #     r = requests.get(url, headers = header)
    #     r.raise_for_status()
    #     print(r.request.headers)
    #
    #     return r.text
    # except:
    #     print("scrap failed")
    #     return " "
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse (soup):
    products = []
    results = soup.find_all('div',{'class':'s-item__info clearfix'})
    for item in results:
        product= {
            'title': item.find('h3',{'class':'s-item__title'}).text,
            'price': item.find('span',{'class' : 's-item__price'}).text,
            # 'bids':
            # 'link':
        }
        products.append(product)
    return products

def output (products):
    productsdf = pd.DataFrame(products)
    productsdf.to_csv('output.csv',index = False)
    print('save to CSV')
    return

header = {'user-agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0'}
soup = get_data(url)
productslist = parse(soup)
output(productslist)
