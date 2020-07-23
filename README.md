## Test task: Scraping citrus.ua and API with Django Rest Framework
Main web-scraping file scraper.py.

Information saves in database PostgraseSQL using peeve and Django ORM.

#### Implement:
  1. used Django Rest Framework
  2. models: ProductItem
  3. scraping with HTMLSession, BeautifulSoup
  4. use Celery and Redis for run scraping in the background
  5. testing models, views, urls
  6. filtering by 'type', 'price', 'cashbak' using ```django-filter```
  
  
#### Urls:
1. main page with one button  ```/```
2. list of all scraping items ```items/```
![](templates/api_page.jpg)
3. list of iPhones ```items/phone``` or notebooks ```items/phone```

```
    {
        "id": 1,
        "name": "Apple iPhone 11 Pro Max 64Gb Midnight Green (MWHH2)",
        "type": "iPhone",
        "link": "https://www.citrus.ua//smartfony/iphone-11-pro-max-64gb-midnight-green-apple-653246.html",
        "image_link": "https://i.citrus.ua/imgcache/size_180/uploads/shop/1/3/1354916085a1a1199f81e7cd5a69686e.jpg",
        "price": 39999,
        "cashback": 699,
        "specifications": "Материалы корпуса: Металл, Стекло; Влагозащита: IP68; Влагозащита: IP68; К....",
        "product_html": "<div class="product-card__name"><a class="" href="/smartfony/....>"
    },
```

### Running project

To get this project up and running you should start by having Python installed on your computer. It's advised you create a virtual environment to store your projects dependencies separately. You can install virtualenv with

```
pip install virtualenv
```

Clone or download this repository and open it in your editor of choice. In a terminal (mac/linux) or windows terminal, run the following command in the base directory of this project

```
virtualenv env
```

That will create a new folder `env` in your project directory. Next activate it with this command on mac/linux:

```
source env/bin/active
```
 or 
 ```
 env\Scripts\activate
```

Then install the project dependencies with

```
pip install -r requirements.txt
```

Migrate for creating all tables 

```
python manage.py migrate
```

Run Redis in one terminal 

```
redis-server
```

Run Celery in another terminal 

```
celery -A Test_scraping_django worker  -l info
```

Now you can run the project with this command in third terminal

```
python manage.py runserver
```

