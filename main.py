import requests
from bs4 import BeautifulSoup
from time import sleep # Set sleep time between requests to avoid being blocked by the website

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0 (Edition Yx GX)'}

def download_image(url):
    response = requests.get(url, stream=True) # stream - потоковая передача
    r = open('C:\\Users\\admin\\Desktop\\python\\parcing\\image' + url.split('/')[-1], 'wb')
    for value in response.iter_content(1024*1024): # Download 1KB at a time
        r.write(value)
    r.close()




def fetch_product_data(): # fetch data from card page    fetch - выборка
    page_list = ['https://nikifilini.com/product-category/new-ru/']
        # for i in range(2,10):
        #     url = f'https://nikifilini.com/product-category/new-ru/page/{i}'
        #     page_list.append(url)         
    for url in page_list:
        sleep(3) # Wait 3 seconds for new requests
        response = requests.get(url, headers = headers) # Send a GET request to the URL/ get the HTML code
        soup = BeautifulSoup(response.text, 'lxml') # lxml nedd to parse HTML code and find needed elements. 2 atribute - 'lxml' and 'html.parser'
        #find elements in the soup
        # find - takes first element  find_all - takes all elements and return list
        data = soup.find_all('li', class_='product')
        for item in data:
            card_url = item.find('a', class_='woocommerce-LoopProduct-link').get('href') # get src attribute
            yield card_url  # генератор. сначала заполняем одну карточку, потом следующую. Оптимизация.

def product_arr():
    for card_url in fetch_product_data():
        sleep(1)
        response = requests.get(card_url, headers = headers)
        soup = BeautifulSoup(response.text, 'lxml')
        data = soup.find('div', class_='summary entry-summary')
    
        name = data.find('h1', class_='product_title entry-title').text
        price = data.find('p', class_='price').text
        sizes = data.find('ul')
        if sizes:
            sizes = data.find('ul').get('data-attribute_values')  # .get (name HTML atribute)
        description = data.find('div', class_ = 'product-short-description-content').text

        data_img = soup.find('div', class_='woocommerce-product-gallery__image')
        img = data_img.find('img').get('src')
        download_image(img)
        yield name, price, sizes, description, img
