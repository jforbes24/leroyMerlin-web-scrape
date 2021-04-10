import requests
import bs4
import lxml
import random
import numpy as np
import pandas as pd
import re
import time
import os

# assign user-agent
user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 6.0.1; RedMi Note 5 Build/RB3N5C; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36'
    ]

catLinks = []
subCatLinks = []
brickLinks = []
productLinks = []
nestedLinks = []
productData = []

# pick a random user agent
for i in range(1,6):
    user_agent = random.choice(user_agent_list)
    # set the headers
    headers = {'User-Agent' : user_agent}

# create IP address pool for IP rotation - https://www.codementor.io/@scrapingdog/10-tips-to-avoid-getting-blocked-while-scraping-websites-16papipe62
 
#get the list of free proxies

try:

    import requests
    from bs4 import BeautifulSoup
    import random

except:
    print(" Library Not Found !")


class Random_Proxy(object):

    def __init__(self):
        self.__url = 'https://www.sslproxies.org/'
        self.__headers = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'http://www.wikipedia.org/',
            'Connection': 'keep-alive',
            }
        self.random_ip = []
        self.random_port = []

    def __random_proxy(self):

        """
        This is Private Function Client Should not have accesss
        :return: Dictionary object of Random proxy and port number
        """

        r = requests.get(url=self.__url, headers=self.__headers)
        soup = BeautifulSoup(r.text, 'html.parser')

        # Get the Random IP Address
        for x in soup.findAll('td')[::8]:
            self.random_ip.append(x.get_text())

        # Get Their Port
        for y in soup.findAll('td')[1::8]:
            self.random_port.append(y.get_text())

        # Zip together
        z = list(zip(self.random_ip, self.random_port))

        # This will Fetch Random IP Address and corresponding PORT Number
        number = random.randint(0, len(z)-50)
        ip_random = z[number]

        # convert Tuple into String and formart IP and PORT Address
        ip_random_string = "{}:{}".format(ip_random[0],ip_random[1])

        # Create a Proxy
        proxy = {'https':ip_random_string}

        # return Proxy
        return proxy

    def Proxy_Request(self,request_type='get',url='',**kwargs):
        """

        :param request_type: GET, POST, PUT
        :param url: URL from which you want to do webscrapping
        :param kwargs: any other parameter you pass
        :return: Return Response
        """
        while True:
            try:
                proxy = self.__random_proxy()
                print("Using Proxy {}".format(proxy))
                r = requests.request(request_type,url,proxies=proxy,headers=self.__headers ,timeout=8, **kwargs)
                return r
                break
            except:
                pass

# Create a class
proxy = Random_Proxy()

url = 'https://www.leroymerlin.fr/produits'
request_type = "get"

r = proxy.Proxy_Request(url=url, request_type=request_type, cookies={'region': 'eyJpdiI6IlN1SUhieDhmUGtxbDVzcHIyZVgrSUE9PSIsInZhbHVlIjoiZHhycHE0MGRlVWNkNHk0U2NDSCtCZz09IiwibWFjIjoiMmFiMjVhZTFjMjFhNWU4NzkyZmFiNTUxOGM5MWYzMmIzYmJiYzNkMDk4NDJjYWFiYTdkNDVjNjMzYzVjNWNhMCJ9'})
print(r)



# get category pages
baseurl = 'https://www.leroymerlin.fr/produits/'
urlConcat = 'https://www.leroymerlin.fr'



# result = requests.get(baseurl, headers=headers)
soup = bs4.BeautifulSoup(r.content, 'lxml')
catGrid = soup.find('ul', class_='col-container l-childrencategories l-childrencategories--wide')




# get category links
try:
    for cat in catGrid.find_all('a', class_='l-childrencategories-item-designation__link l-childrencategories-item-designation__link--wide'):
        catLinks.append(urlConcat + cat['href'])
        time.sleep(1)
    print(catLinks)
except Exception as ex:
    print('Error in Category: ', ex)



# get sub-category links
try:
    for subCatGrid in catLinks:
        r = proxy.Proxy_Request(url=subCatGrid, request_type=request_type, cookies={'region': 'eyJpdiI6IlN1SUhieDhmUGtxbDVzcHIyZVgrSUE9PSIsInZhbHVlIjoiZHhycHE0MGRlVWNkNHk0U2NDSCtCZz09IiwibWFjIjoiMmFiMjVhZTFjMjFhNWU4NzkyZmFiNTUxOGM5MWYzMmIzYmJiYzNkMDk4NDJjYWFiYTdkNDVjNjMzYzVjNWNhMCJ9'})
        broth = bs4.BeautifulSoup(r.content, 'lxml')
        for subCat in broth.find_all('a', class_='l-childrencategories-item-designation__link l-childrencategories-item-designation__link--grid'):
            if urlConcat + subCat['href'] in subCatLinks:
                continue
            else:
                subCatLinks.append(urlConcat + subCat['href'])
                print(len(subCatLinks))
                print(urlConcat + subCat['href'])
                time.sleep(1)
except Exception as ex:
    print('Error in Sub-Category: ', ex)

    
# get brick links
try:
    for brickGrid in subCatLinks:
        r = proxy.Proxy_Request(url=brickGrid, request_type=request_type, cookies={'region': 'eyJpdiI6IlN1SUhieDhmUGtxbDVzcHIyZVgrSUE9PSIsInZhbHVlIjoiZHhycHE0MGRlVWNkNHk0U2NDSCtCZz09IiwibWFjIjoiMmFiMjVhZTFjMjFhNWU4NzkyZmFiNTUxOGM5MWYzMmIzYmJiYzNkMDk4NDJjYWFiYTdkNDVjNjMzYzVjNWNhMCJ9'})
        stew = bs4.BeautifulSoup(r.content, 'lxml')
        for brick in stew.find_all('a', class_='l-childrencategories-item-designation__link l-childrencategories-item-designation__link--grid'):
            if urlConcat + brick['href'] in brickLinks:
                continue
            else:
                brickLinks.append(urlConcat + brick['href'])
                print(len(brickLinks))
                print(urlConcat + brick['href'])
                time.sleep(1)
except Exception as ex:
    print('Error in Bricks: ', ex)



# get nested links

try:
    for nextPage in brickLinks:
        r = proxy.Proxy_Request(url=nextPage, request_type=request_type, cookies={'region': 'eyJpdiI6IlN1SUhieDhmUGtxbDVzcHIyZVgrSUE9PSIsInZhbHVlIjoiZHhycHE0MGRlVWNkNHk0U2NDSCtCZz09IiwibWFjIjoiMmFiMjVhZTFjMjFhNWU4NzkyZmFiNTUxOGM5MWYzMmIzYmJiYzNkMDk4NDJjYWFiYTdkNDVjNjMzYzVjNWNhMCJ9'})
        broth = bs4.BeautifulSoup(r.content, 'lxml')
        print(result.status_code)
        # get nested page links
        try:
            for urlLink in broth.find_all('div', class_='mc-pagination__button   js-next'):
                nestedLink = urlLink.find_all('a', href=True)
                if urlConcat + nestedLink[1]['href'] in brickLinks:
                    continue
                else:
                    brickLinks.append(urlConcat + nestedLink[1]['href'])
                    print(urlConcat + nestedLink[1]['href'])
                    time.sleep(1)
              
        except Exception as ex:
            print('Error in Nested Page Link: ', ex)
except Exception as ex:
    print('Error in Next Page: ', ex)


# get products

try:
    for product in brickLinks:
        r = proxy.Proxy_Request(url=product, request_type=request_type, cookies={'region': 'eyJpdiI6IlN1SUhieDhmUGtxbDVzcHIyZVgrSUE9PSIsInZhbHVlIjoiZHhycHE0MGRlVWNkNHk0U2NDSCtCZz09IiwibWFjIjoiMmFiMjVhZTFjMjFhNWU4NzkyZmFiNTUxOGM5MWYzMmIzYmJiYzNkMDk4NDJjYWFiYTdkNDVjNjMzYzVjNWNhMCJ9'})
        soup = bs4.BeautifulSoup(r.content, 'lxml')
        products = soup.find_all('article', class_='kl-tile kl-tile--h-to-v')

        # get product links
        for item in products:
            for link in item.find_all('a', href=True):
                if baseurl + link['href'] not in productLinks:
                    productLinks.append(baseurl + link['href'])
                else:
                    continue
                print(len(productLinks))
                time.sleep(1)
except Exception as ex:
    print('Error: ', ex)



try:
    for link in productLinks:
        # get product attributes
        r = proxy.Proxy_Request(url=link, request_type=request_type, cookies={'region': 'eyJpdiI6IlN1SUhieDhmUGtxbDVzcHIyZVgrSUE9PSIsInZhbHVlIjoiZHhycHE0MGRlVWNkNHk0U2NDSCtCZz09IiwibWFjIjoiMmFiMjVhZTFjMjFhNWU4NzkyZmFiNTUxOGM5MWYzMmIzYmJiYzNkMDk4NDJjYWFiYTdkNDVjNjMzYzVjNWNhMCJ9'})
        soup = bs4.BeautifulSoup(r.content, 'lxml')
        products = soup.find('div', id_='corps')

        # productData = []

        # get SKU
        try:
            sku = str(soup.find_all('span', class_='a-reflm')[0].text.strip().lstrip('Réf '))
        except:
            sku = 'na'

        # get name
        try:
            name = soup.find_all('h1')[0].text.strip().replace('\n', '')
        except:
            name = 'na'

        # get brand
        try:
            all_tr = soup.find_all('tr', class_='m-product-attr-row')
            for row in all_tr:
                all_th = row.find_all('th', recursive=False)
                brand = row.find('scope', row='Marque du produit').text.strip()
                print(brand)
                for i in all_th:
                    print(i)
            # brand = soup.find('div', class_='o-product-detail-description__images col-s-12 col-m-10 col-start-m-2 col-l-8 col-start-l-3').text.strip()
        except:
            brand = 'na'
 
        # get category
        try:
            category = soup.select('#component-breadcrumb')[0].find_all('li')[2].text.strip()
        except:
            category = 'na'

        # get subCategory
        try:
            subCat = soup.select('#component-breadcrumb')[0].find_all('li')[3].text.strip()
        except:
            subCat = 'na'

        # get subSubCategory
        try:
            subSubCat = soup.select('#component-breadcrumb')[0].find_all('li')[4].text.strip()
        except:
            subSubCat = 'na'

        # get subSubCategory
        try:
            brickCat = soup.select('#component-breadcrumb')[0].find_all('li')[5].text.strip()
        except:
            brickCat = 'na'

        # get rating
        try:
            rating = float(soup.find('span', class_='mc-stars-result__text').text.strip('Global score: ').rstrip('/5').replace(',','.'))
        except:
            rating = 'na'

        # totalReviews
        try:
            totalReviews = int(soup.find('span', class_='o-reviews__label').text.strip(' avis'))
        except:
            totalReviews = 'na'

        # reviews
        try:
            reviews = soup.find_all('p', class_='m-review__title')[0].text.strip()
        except:
            reviews = 'na'

        # recommendation
        try:
            recommend = soup.find('div', class_='m-review__rating-text').find_all('span')[0].text.strip()
        except:
            recommend = 'na'

        # get price
        try:
            price = float(soup.find_all('p', class_='km-main-price')[0].text.strip().rstrip(' €'))
        except:
            price = 'na'

        # get availability
        try:
            availability = soup.find('h1').find_all('span')[1].text.strip()
        except:
            availability = 'na'
        
        # get delivery charge
        try:
            deliveryCharge = soup.find('span', class_='mu-ml-050 ku-fw-bold').text.strip()
        except:
            deliveryCharge = 'na'

        # get lead time
        try:
            leadTime = soup.find('span', class_='km-delivery-product__type').text.strip()
        except:
            leadTime = "na"

        # get images
        try:
            container = soup.find('ul', class_='m-nav-thumbnails__container')
            images = 0
            for image in container.find_all('li'):
                image.get('alt')
                images = images + 1
            else:
                pass
        except:
            images = 'na'

        # add to cart
        try:
            add2Cart = soup.find('button', class_='mc-button a-add-to-cart js-cart-add a-add-to-cart mc-button--l mc-button--full').text.strip()
        except:
            add2Cart = 'na'

        # create sku dictionary
        try:
            sku = {'sku' : sku,
                   'description' : name,
                   'price' : price,
                   #'brand' : brand,
                   'category' : category,
                   'subCat' : subCat,
                   'subSubCat' : subSubCat,
                   'brickCat' : brickCat,
                   'rating' : rating,
                   'totalReviews' : totalReviews,
                   'reviews' : reviews,
                   'recommend' : recommend,
                   'availability' : availability,
                   'deliveryCharge' : deliveryCharge,
                   'leadTime' : leadTime,
                   'images' : images,
                   'add2Cart' : add2Cart,
                   'link' : link
                   }
            if sku in productData:
                continue
            else:
                productData.append(sku)
        except Exception as ex:
            print('Error: ', ex)

        time.sleep(2)

        print(len(productData))
              
except Exception as ex:
    print('Error: ', ex)


# create dataframe
df = pd.DataFrame(productData)

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.width', 1000)

# save to excel
df.to_excel(r'C:\\Users\\jforbes84\\PycharmProjects\\bs4leroyMerlin.xlsx')

print(df)

