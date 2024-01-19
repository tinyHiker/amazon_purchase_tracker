from bs4 import BeautifulSoup
import requests
import time
import datetime
import csv
import smtplib
import pandas as pd
import sqlite3
from data_classes import *


from typing import Tuple



class WebsiteNotFound(Exception):
    """Custom exception class for when there is no website that matches a passed URL"""

    def __init__(self, message="The URL does not match any website", URL = None):
        super().__init__(message)
        self.faulty_URL = URL


class ProductDoesNotExist(Exception):
    def __init__(self, faulty_code):
        message = f"Product #{faulty_code} does not exist"
        super().__init__(message)
        self.code = faulty_code
        
        

class Scraper:
    """Scraper class for scraping the product information off an Amazon product page"""
    
    def get_content(self, response: requests.Response) -> BeautifulSoup:
        """Parses and returns a beautified version of the given web page's HTML content"""
        soup = BeautifulSoup(response.content, 'html.parser')
        page = BeautifulSoup(soup.prettify(), 'html.parser')
        return page
    
    
    def extract_info(self, content: BeautifulSoup) -> Tuple[str, float, datetime.date]:
        """Extracts the product title and price of the product from the HTML"""
        title = content.find(id="productTitle").get_text().strip()
        whole_price = content.find(class_ = "a-price-whole").get_text()
        whole_price = whole_price.split('.')[0].strip()
        fraction_price = content.find(class_ = "a-price-fraction").get_text().strip()
        final_price = str(whole_price) + '.' + str(fraction_price)
        final_price = float(final_price)
        today = datetime.date.today()
        
        return (title, final_price, today)
    
    
    def scrape(self, URL: str) -> Tuple[str, float, datetime.date]:
        """Takes a URL of the product page and returns information about the product"""
        try:
            page : requests.Response = requests.get(URL)
        except:
            raise WebsiteNotFound()
        
        #Extracting the HTML in a 'prettified' format'
        content : BeautifulSoup = self.get_content(page)
        #Extracting and returning product info from the HTML
        return self.extract_info(content)
        
        

    def already_visited(self, title: str, current_user = None) -> bool:
        """Returns True if the active user has already logged this product"""
        with sqlite3.connect('database.db') as conn:  # This will create a file named 'database.db'
            cursor = conn.cursor()
            query = "SELECT * FROM products WHERE name = ? AND user_id = ?"
            cursor.execute(query, (title, current_user.id))
            results = cursor.fetchall()
        
        return len(results) > 0

    
   


class Modifier:
    """The objects of this class are used to modify the database"""
    
    def __init__(self, active_user: User):
        self.current_user: User = active_user
    
    def new_user(self, username: str):
        """Creates new user with the currrent loggedin user as the master"""
        self.current_user.create_new_user(username)
        
    def create_entry(self, title: str, final_price: float, today: datetime.date(), rating: int):
        product : Product = Product.create_new(title, final_price, today, self.current_user, rating)
            
    
    def new_product(self, URL : str, rating: int):
        scraper = Scraper()
        scraped_data = scraper.scrape(URL)
        self.create_entry(title = scraped_data[0], final_price = scraped_data[1], today = scraped_data[2], rating = rating)
        
        
    def find_product(self, product_code: int) -> Product:
        #takes product code and returns product object
        with sqlite3.connect('database.db') as conn:  # This will create a file named 'database.db'
            cursor = conn.cursor()
            query = "SELECT * FROM products WHERE id = ?"
            cursor.execute(query, (product_code, ))
            results = cursor.fetchall()
            
        if len(results) == 0:
            raise ProductDoesNotExist(product_code)
        else:
            result = results[0]
            return Product(*result)
        
    def delete_product(self, product_code : int):
        ##finds product using find_product() method and then calls delete() method on the returned product object
        product = self.find_product(product_code)
        product.delete()
        
    def change_rating(self, product_code : int, new_rating : int):
        #finds product using find_product() method and the calls new_rating on the returned product object
        product = self.find_product(product_code)
        product.change_rating(new_rating)
        
    def buy(self, product_code: int):
        product = self.find_product(product_code)
        product.buy()
        
        
        
        
        
        
        
        