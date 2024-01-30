#External imports
from bs4 import BeautifulSoup
import requests
import time
import datetime
import smtplib

#UI External Imports
import pyfiglet

#Internal imports
from exceptions import * 

#Typing imports
from typing import Tuple


def print_SQL_records(func):
    """A decorator that print all the return records from a function"""
    def wrapper(self, *args, **kwargs):
        records_list = func(self, *args, **kwargs)
        for record in records_list:
            str_tuple = tuple(map(str, record))
            print_string = " ".join(str_tuple)
            print(print_string)
    return wrapper
        

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
        
        content : BeautifulSoup = self.get_content(page) #Extracting the HTML in a 'prettified' format
        
        return self.extract_info(content)  #Extracting and returning product info from the HTML
        
      
if __name__ == "__main__":
    ascii_art = pyfiglet.figlet_format("Amazon Purchase Tracker", font="slant")
    print(ascii_art)