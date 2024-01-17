from bs4 import BeautifulSoup
import requests
import time
import datetime
import csv
import smtplib
import pandas as pd



class WebsiteNotFound(Exception):
    """Custom exception class for when there is no website that matches a passed URL"""

    def __init__(self, message="The URL does not match any website", URL = None):
        self.message = message
        super().__init__(self.message)
        self.faulty_URL = URL



class Scraper:
    """Scraper class for scraping the product information off an Amazon product page"""
    
    
    def get_content(self, page):
        soup = BeautifulSoup(page.content, 'html.parser')
        page = BeautifulSoup(soup.prettify(), 'html.parser')
        return page
    
    def extract_info()
    
    
    def scrape(self, URL):
        
        #Getting a response from the page
        try:
            page = requests.get(URL)
        except:
            raise WebsiteNotFound()
        
        #Extracting the HTML in a 'prettified' format'
        content = self.get_content(page)
        
        #Getting the name and price of the product from the page.
        title = content.find(id="productTitle").get_text().strip()
        whole_price = content.find(class_ = "a-price-whole").get_text()
        whole_price = whole_price.split('.')[0].strip()
        fraction_price = content.find(class_ = "a-price-fraction").get_text().strip()
        final_price = str(whole_price) + '.' + str(fraction_price)
    
        #Getting today's date
        today = datetime.date.today()
        
        return (title, final_price, today)
        
        

    def already_visited(self, title):
        df = pd.read_csv(r'visited_products.csv')
        value_exists = df['Title'].isin([title]).any()
        return value_exists
        
        

    def newEntry(self, URL):
        
        #Obtaining the name, price and date_viewed of the product
        title, final_price, today = self.scrape(URL)
        data = [title, final_price, today]
        
        if not self.already_visited(title):
            #Adding it to the list of viewed products
            with open('visited_products.csv', 'a+', newline='\n', encoding = 'UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(data)
            
        df = pd.read_csv(r'visited_products.csv')
        print(df)
        
        
new_scraper = Scraper()
Scraper.newEntry()




