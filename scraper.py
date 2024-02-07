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
    ascii_art = pyfiglet.figlet_format("Amazon Web Scraper", font="slant")
    print(ascii_art)
    
    URL = input("Enter URL of the product you want data on: ")
    URL = URL.strip()
    
    scraper = Scraper()
    name, price, date = scraper.scrape(URL)
    print(f"Product name: {name}")
    print(f"Product price: {price}")
    print(f"Date registered/viewed: {date}")
    
    
    
    
    