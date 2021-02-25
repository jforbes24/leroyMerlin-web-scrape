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
    'Mozilla/5.0 (Linux; Android 10; LM-X420) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36', #blocked
    'Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36', #open
    'Mozilla/5.0 (X11; Linux i686; rv:85.0) Gecko/20100101 Firefox/85.0', #open
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'
    ]

catLinks = []
subCatLinks = []
brickLinks = []
productLinks = []
nestedLinks = []

# pick a random user agent
for i in range(1,6):
    user_agent = random.choice(user_agent_list)
    # set the headers
    headers = {'User-Agent' : user_agent}


# get category pages
baseurl = 'https://www.leroymerlin.fr/produits/'
urlConcat = 'https://www.leroymerlin.fr'

"""

result = requests.get(baseurl, headers=headers)
soup = bs4.BeautifulSoup(result.content, 'lxml')
catGrid = soup.find('ul', class_='col-container l-taxonomy l-taxonomy--wide')
print(result.status_code)



# get category links
try:
    for cat in catGrid.find_all('a', class_='l-taxonomy-item-designation__link'):
        catLinks.append(urlConcat + cat['href'])
        time.sleep(0.5)
    print(len(catLinks))
except Exception as ex:
    print('Error in Category: ', ex)

# get sub-category links
try:
    for subCatGrid in catLinks:
        result = requests.get(subCatGrid, headers=headers)
        broth = bs4.BeautifulSoup(result.content, 'lxml')
        for subCat in broth.find_all('a', class_='l-taxonomy-item-designation__link'):
            if urlConcat + subCat['href'] in subCatLinks:
                continue
            else:
                subCatLinks.append(urlConcat + subCat['href'])
                print(len(subCatLinks))
                time.sleep(0.5)
except Exception as ex:
    print('Error in Sub-Category: ', ex)

# get brick links
try:
    for brickGrid in subCatLinks:
        result = requests.get(brickGrid, headers=headers)
        stew = bs4.BeautifulSoup(result.content, 'lxml')
        for brick in stew.find_all('a', class_='l-taxonomy-item-designation__link'):
            if urlConcat + brick['href'] in brickLinks:
                continue
            else:
                brickLinks.append(urlConcat + brick['href'])
                print(urlConcat + brick['href'])
                time.sleep(0.5)
except Exception as ex:
    print('Error in Bricks: ', ex)



# get nested links

try:
    for nextPage in range(1): # brickLinks
        test = 'https://www.leroymerlin.fr/produits/electricite-domotique/alarme-camera-de-surveillance-et-detecteur-de-fumee/camera-de-surveillance/'
        result = requests.get(test, headers=headers)
        broth = bs4.BeautifulSoup(result.content, 'lxml')
        print(result.status_code)
        # get nested page links
        try:
            for urlLink in broth.find_all('div', class_='mc-pagination js-pagination m-list-pagination'):
                nestedLink = urlLink.find_all('a', href=True)
                if urlConcat + nestedLink[1]['href'] in brickLinks:
                    continue
                else:
                    brickLinks.append(urlConcat + nestedLink[1]['href'])
                    print(urlConcat + nestedLink[1]['href'])
                    time.sleep(0.5)
              
        except Exception as ex:
            print('Error in Nested Page Link: ', ex)
except Exception as ex:
    print('Error in Next Page: ', ex)


# get products

try:
    for product in brickLinks:
        result = requests.get(product, headers=headers)
        soup = bs4.BeautifulSoup(result.content, 'lxml')
        products = soup.find_all('article', class_='kl-tile kl-tile--h-to-v')

        # get product links
        for item in products:
            for link in item.find_all('a', href=True):
                if baseurl + link['href'] not in productLinks:
                    productLinks.append(baseurl + link['href'])
                else:
                    continue
                print(len(productLinks))
                time.sleep(0.5)
except Exception as ex:
    print('Error: ', ex)
"""

test = 'https://www.leroymerlin.fr/produits/electricite-domotique/alarme-camera-de-surveillance-et-detecteur-de-fumee/alarme-maison/accessoires-pour-alarme-de-maison/support-mural-pour-camera-somfy-79355052.html'
try:
    for link in range(1,2): #productLinks
        # get product attributes
        result = requests.get(test, headers=headers)
        soup = bs4.BeautifulSoup(result.content, 'lxml')
        products = soup.find('div', id_='corps')

        productData = []

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
            add2Cart = soup.find('span', class_='mc-button__label').text.strip()
        except:
            add2Cart = 'na'

        # create sku dictionary
        try:
            sku = {'sku' : sku,
                   'description' : name,
                   'price' : price,
                   'brand' : brand,
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
                   'add2Cart' : add2Cart
                   }
            if sku in productData:
                continue
            else:
                productData.append(sku)
        except Exception as ex:
            print('Error: ', ex)

        time.sleep(0.5)

        print(len(productData))
              
except Exception as ex:
    print('Error: ', ex)


print(result.status_code)
# create dataframe
df = pd.DataFrame(productData)

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.width', 1000)

# save to excel
df.to_excel(r'C:\\Users\\forbej06\\OneDrive - Kingfisher PLC\\dev\\Range\\Leroy Merlin\\bs4leroyMerlin.xlsx')

print(df)

