import requests
from bs4 import BeautifulSoup
from time import sleep # Set sleep time between requests to avoid being blocked by the website


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0 (Edition Yx GX)'}
list_cards = []

def fetch_card_data(url):   # fetch - выборка
    sleep(3)  # Wait 3 seconds for new requests
    response = requests.get(url, headers = headers)  # Send a GET request to the URL/ get the HTML code
    # print(response.text)  # Print the response text (HTML code)
    # lxml nedd to parse HTML code and find needed elements. 2 atribute - 'lxml' and 'html.parser'
    soup = BeautifulSoup(response.text, 'lxml')
    #find elements in the soup
    # find - takes first element  find_all - takes all elements and return list
    data = soup.find_all('li', class_='product')
    for item in data:
        name = item.find('span', class_='woocommerce-loop-product__title').text
        price = item.find('span', class_='price').text
        url_img = item.find('img').get('src') # get src attribute of img...
        print(f'Name: {name}, Price: {price}, URL_img: {url_img}')

def fetch_product_data(url): # fetch data from card page
    global list_cards
    sleep(3)
    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.text, 'lxml')
    data = soup.find_all('li', class_='product')
    for item in data:
        card_url = item.find('a', class_='woocommerce-LoopProduct-link').get('href')
        list_cards.append(card_url)
    return list_cards

first_page = fetch_product_data('https://nikifilini.com/product-category/new-ru/')
print(len(list_cards))
#for i in range(2,10):
#    fetch_product_data(f'https://nikifilini.com/product-category/new-ru/page/{i}')

for card_url in list_cards:
    #print('Card URL:', card_url)
    sleep(1)
    response = requests.get(card_url, headers = headers)

    # Check if the response was successful
    if response.status_code != 200:
        print(f"Failed to fetch {card_url}. Status code: {response.status_code}")
        continue
    
    soup = BeautifulSoup(response.text, 'lxml')
    data = soup.find('div', class_='summary entry-summary')
    if data:
        name = data.find('h1', class_='product_title entry-title').text
        price = data.find('p', class_='price').text
        sizes = data.find('ul').get('data-attribute_values')  # .get (name HTML atribute)
        description = data.find('div', class_ = 'product-short-description-content').text

        print(f'Name: {name}, Price: {price}, Size: {sizes}, Description: {description}')
    else:
        print("No data found")