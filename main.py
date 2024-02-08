#External imports
from bs4 import BeautifulSoup
import requests
import time
import datetime
import csv
import smtplib
import pandas as pd
import sqlite3
from prettytable import PrettyTable
import logging

#Internal imports
from data_classes import *
from exceptions import *  #Notice how main.py imports from data_classes but not the other way around to prevent circular imports.
from scraper import *
from internal_decorators import *


#Typing imports
from typing import List, Tuple, Optional


def login(user_name):
    return Checker.extract_user(user_name)
    
    
    
class Checker:
    """The objects of this class check if certain SQL records exists"""
    def __init__(self, active_user: User):
        self.current_user: User = active_user
        
    def check_product_not_visited(self, name: str) -> bool:
        """Returns True if the active user has already logged this product"""
        with sqlite3.connect('database.db') as conn:  
            cursor = conn.cursor()
            query = "SELECT * FROM products WHERE name = ? AND user_id = ?" #Query to get all products that have a certain name and user_id. Running this query should only return a list of ONE OR ZERO products
            cursor.execute(query, (name, self.current_user.id))
            results = cursor.fetchall()
        if len(results) > 0:
            raise AlreadyBoughtException(results[0][0]) #Passing the id of the already bought product into the exception so that its buy-count can be incremented later on.
        return True
    
    @staticmethod    
    def extract_user(user_name):
        """During login, used to check for user existence and create and return a new User object is User exists.
        During the creation of a new user, used to check for user existence. If user with the same name already exists, we do not execute the create-new-user command"""
        with sqlite3.connect('database.db') as conn:  
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE name = ?" #Query to get all users with a certain. Running this query should only return a list of ONE OR ZERO users
            cursor.execute(query, (user_name, ))
            results = cursor.fetchall()
        if len(results) == 0:
            raise UserDoesNotExist(user_name) #Passing the id of the already bought product into the exception so that its buy-count can be incremented later on.
        else:
            return Modifier.create_user_object(results[0][0], results[0][1], results[0][2])
        
    @staticmethod
    def check_rating(rating: int) -> bool:
        return rating >= 1 and rating <= 10
        





class Modifier:
    """The objects of this class are used to modify the database according to the user in-session and their entries"""
    
    def __init__(self, active_user: User):
        self.current_user: User = active_user
        
        self.logger = logging.getLogger(f"User {self.current_user.id} {self.current_user.name}")
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)s: %(message)s')
        file_handler = logging.FileHandler('activity.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    
    def log_activity(activity_message):
        def log_activity_inside(func):
            def wrapper(self, *args, **kwargs):
                self.logger.info(f"Ran {func.__name__} with args {args} and kwargs {kwargs}: {activity_message}")
                result = func(self, *args, **kwargs)
                return result
            return wrapper
        return log_activity_inside

    @log_activity("You created a new user")
    def new_user(self, username: str):
        """Creates new user with the current loggedin user as the master"""
        try:
            Checker.extract_user(username) #Should raise UserDoesNotExist
            raise UserAlreadyExists(username)
        except UserDoesNotExist:
            new_user: User = self.current_user.create_new_user(username) #Creates a new user with the new username if a user with that username does not already exist
            #Uses a method from the User class and not the Modifier class becuase of 'master' field in SQL
            return new_user

        
    @staticmethod
    def create_user_object(user_id: int, user_name: str, user_master: Optional[int] = None):
        """Used in Checker classes extract_user() function"""
        user = User(user_id, user_name, user_master)
        return user
        
    
    def enter_SQL_product(self, name: str, final_price: float, today: datetime.date, rating: int) -> bool: #WE ARE NOT PASSING IN DATE BECUASE THERE IS NOT DATE FIELD IN OUR SLITE DATABASE AT THE MOMENT
        checker = Checker(self.current_user)
        checker.check_product_not_visited(name)
        product: Product = Product.create_new(name, final_price, today, self.current_user, rating)
        return True
    
    @log_activity("You entered a new product")
    def enter_new_product(self, URL : str, rating: int) -> bool:
        if not Checker.check_rating(rating):
            raise RatingOutOfBounds(rating)
        scraper = Scraper()
        scraped_data = scraper.scrape(URL)
        self.enter_SQL_product(name = scraped_data[0], final_price = scraped_data[1], today = scraped_data[2], rating = rating)
        return True
        
    @log_activity("You found a product")
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
        
        
    @log_activity("You deleted a product")
    def delete_product(self, product_code : int) -> bool:
        """Finds product using find_product() method and then calls delete() method on the returned product object"""
        product: Product = self.find_product(product_code)
        product.delete()
        return True
    
    @log_activity("You changed a product rating")
    def change_rating(self, product_code : int, new_rating : int) -> bool:
        """Finds product using find_product() method and the calls new_rating() on the returned product object"""
        product: Product = self.find_product(product_code)
        product.change_rating(new_rating)
        return True
    
    @log_activity("You bought a product")
    def buy(self, product_code: int) -> bool:
        """Finds product using find_product() method and then calls buy() method on the returned product object"""
        product: Product = self.find_product(product_code)
        product.buy()
        return True
        
    @print_prettified_products_for_user
    def list_products(self, bought: bool = None) -> List[Tuple[int, str, float, int, int, int]]:
        """List the products that are bought (or unbought) by a certain user"""
        product_list = Product.list_products(self.current_user.id, bought)
        return product_list
    
    @log_activity("You cleansed the palet")
    def delete_bought_prods(self) -> bool:
        """Delete all the bought products of a user"""
        success = Product.delete_bought_products(int(self.current_user.id))
        return success
        
        

    
            
        
        
            
            
            
        
        
        
        
        
        
        
        