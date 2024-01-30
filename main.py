#External imports
from bs4 import BeautifulSoup
import requests
import time
import datetime
import csv
import smtplib
import pandas as pd
import sqlite3

#Internal imports
from data_classes import *
from exceptions import *  #Notice how main.py imports from data_classes but not the other way around to prevent circular imports.
from scraper import *


#Typing imports
from typing import List, Tuple, Optional


def print_SQL_records(func):
    """A decorator that print all the return records from a function"""
    def wrapper(self, *args, **kwargs):
        records_list = func(self, *args, **kwargs)
        for record in records_list:
            str_tuple = tuple(map(str, record))
            print_string = " ".join(str_tuple)
            print(print_string)
    return wrapper
        
     

class Checker:
    """The objects of this class check if certain SQL records exists"""
    def __init__(self, active_user: User):
        self.current_user: User = active_user
        
    def check_product_already_visited(self, name: str) -> bool:
        """Returns True if the active user has already logged this product"""
        with sqlite3.connect('database.db') as conn:  
            cursor = conn.cursor()
            query = "SELECT * FROM products WHERE name = ? AND user_id = ?" #Query to get all products that have a certain name and user_id. Running this query should only return a list of ONE OR ZERO products
            cursor.execute(query, (name, self.current_user.id))
            results = cursor.fetchall()
        if len(results) > 0:
            raise AlreadyBought(results[0][0]) #Passing the id of the already bought product into the exception so that its buy-count can be incremented later on.
        return True
    
    @staticmethod    
    def extract_user(user_name):
        """During login, used to check for user existence and create and return a new User object is User exists.
        During the creation of a new user, used to check for user existence. If user with the same name already exists, we do not execute the create-new-user command"""
        with sqlite3.connect('database.db') as conn:  
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE name = ?" #Query to get all users with a certain. Running this query should only return a list of ONE OR ZERO users
            cursor.execute(query, (user_name))
            results = cursor.fetchall()
        if len(results) == 0:
            raise UserDoesNotExist(user_name) #Passing the id of the already bought product into the exception so that its buy-count can be incremented later on.
        else:
            return Modifier.create_user_object(*results[0])
        

class Modifier:
    """The objects of this class are used to modify the database according to the user in-session and their entries"""
    
    def __init__(self, active_user: User):
        self.current_user: User = active_user
    
    def new_user(self, username: str):
        """Creates new user with the current loggedin user as the master"""
        try:
            Checker.extract_user(username) #Should raise UserDoesNotExist
            print('A user with this username already exists')
        except UserDoesNotExist:
            self.current_user.create_new_user(username) #Creates a new user with the new username if a user with that username does not already exist
            #Uses a method from the User class and not the Modifier class becuase of 'master' field in SQL

        
    @staticmethod
    def create_user_object(*user_data):
        """Used in Checker classes extract_user() function"""
        user = User(user_data[0], user_data[1], user_data[2])
        return User
        
    
    def enter_SQL_product(self, name: str, final_price: float, today: datetime.date(), rating: int) -> bool: #WE ARE NOT PASSING IN DATE BECUASE THERE IS NOT DATE FIELD IN OUR SLITE DATABASE AT THE MOMENT
        product: Product = Product.create_new(name, final_price, today, self.current_user, rating)
        return True
        #NEED TO ADD check_product_already_visited() from checker class functionality    
    
    def enter_new_product(self, URL : str, rating: int) -> bool:
        scraper = Scraper()
        scraped_data = scraper.scrape(URL)
        self.enter_SQL_product(name = scraped_data[0], final_price = scraped_data[1], today = scraped_data[2], rating = rating)
        return True
        
        
    def find_product(self, product_code: int) -> Product: #If this one does not return product then it raises a ProductDoesNotExist Exception
        """Takes a product code and returns a product object"""
        query = "SELECT * FROM products WHERE id = ?"
        
        with sqlite3.connect('database.db') as conn:  # This will create a file named 'database.db'
            cursor = conn.cursor()
            cursor.execute(query, (product_code, ))
            results = cursor.fetchall()
            
        if len(results) == 0:
            raise ProductDoesNotExist(product_code)
        else:
            result = results[0]
            return Product(*result)
        
    def delete_product(self, product_code : int) -> bool:
        """Finds product using find_product() method and then calls delete() method on the returned product object"""
        product: Product = self.find_product(product_code)
        product.delete()
        return True
        
    def change_rating(self, product_code : int, new_rating : int) -> bool:
        """Finds product using find_product() method and the calls new_rating() on the returned product object"""
        product: Product = self.find_product(product_code)
        product.change_rating(new_rating)
        return True
        
    def buy(self, product_code: int) -> bool:
        """Finds product using find_product() method and then calls buy() method on the returned product object"""
        product: Product = self.find_product(product_code)
        product.buy()
        return True
        
    @print_SQL_records
    def list_products(self, bought: bool = None) -> List[Tuple[int, str, float, int, int, int]]:
        """List the products that are bought (or unbought) by a certain user"""
        product_list = Product.list_products(self.current_user.id, bought)
        return product_list

    
            
        
        
            
            
            
        
        
        
        
        
        
        
        