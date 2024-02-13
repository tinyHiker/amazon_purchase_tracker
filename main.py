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
    """The objects of this class check if certain SQL records exists and if certain user inputs are valid"""
    def __init__(self, active_user: User):
        self.current_user: User = active_user
        

    
    @staticmethod
    def execute_query(query: str, arguments):
        """Executes an SQL query on database.db with specified arguments. Returns results of the query in Tuple Form"""
        with sqlite3.connect('database.db') as conn:  
            cursor = conn.cursor()
            cursor.execute(query, arguments)
            results = cursor.fetchall()
        return results
    
    
    def check_product_not_visited(self, name: str) -> bool:
        """Returns True if the active user has not already logged this product"""
        query = "SELECT * FROM products WHERE name = ? AND user_id = ?" #Query to get all products that have a certain name and user_id. Running this query should only return a list of ONE OR ZERO products
        results = Checker.execute_query("SELECT * FROM products WHERE name = ? AND user_id = ?", (name, self.current_user.id))
    
        if len(results) > 0:
            raise AlreadyBoughtException(results[0][0]) #Passing the id of the already bought product into the exception so that its buy-count can be incremented later on.
        return True
    
    
    @staticmethod    
    def extract_user(user_name):
        """During login, used to check for user existence. Will create and return a new User object if User exists.
        During the creation of a new user, used to check for user existence. If user with the same name already exists, we do not execute the create-new-user command"""
        
        query = "SELECT * FROM users WHERE name = ?" # Query to get all users with a certain. Running this query should only return a list of ONE OR ZERO users
        results = Checker.execute_query(query, (user_name, ))
        
        if len(results) == 0:
            raise UserDoesNotExist(user_name) #Passing the id of the already bought product into the exception so that its buy-count can be incremented later on.
        else:
            return Modifier.create_user_object(results[0][0], results[0][1], results[0][2])
        
    @staticmethod
    def check_rating(rating: int) -> bool:
        """Makes sure rating is an integer and is between appropriate range."""
        return type(rating) == int and rating >= 1 and rating <= 10
        





class Modifier:
    """The objects of this class are used to modify the database according to the user in-session and their entries"""
    def __init__(self, active_user: User):
        self.current_user: User = active_user
        self.create_logger(self.current_user.id, self.current_user.name)
        
        
    def create_logger(self, user_id: int, user_name: str):
        self.logger = logging.getLogger(f"User {user_id} {user_name}")
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        file_handler = logging.FileHandler('activity.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
    
    
    def log_activity(activity_message):
        """This is the decorator that logs every action ever done by any user in the system"""
        def log_activity_inside(func):
            def wrapper(self, *args, **kwargs):
                user_name = self.current_user.name
                user_id = self.current_user.id
                
                result = func(self, *args, **kwargs)
                if result is not None:
                    new_logger_string = f"User #{user_id} ({user_name}) {activity_message} {str(result)}"
                else:
                    new_logger_string = f"User #{user_id} ({user_name}) {activity_message}"
                #old_logger_string = f"User #{user_id} ({user_name}) ran {func.__name__} with args {args} and kwargs {kwargs}: {user_name} {activity_message}"
                
                self.logger.info(new_logger_string)  
                return result
            return wrapper
        return log_activity_inside


    @log_activity("created a new user: ")
    def new_user(self, username: str):
        """Creates new user with the current loggedin user as the master. Returns the User object of the newly created user"""
        
        try:
            Checker.extract_user(username) #Should raise UserDoesNotExist if user with that username does not exist. This is a good thing
            raise UserAlreadyExists(username)
        except UserDoesNotExist:
            new_user: User = self.current_user.create_new_user(username) #Creates a new user. Uses a method from the User class and not the Modifier class becuase of 'master' field in SQL
            return new_user

        
    @staticmethod
    def create_user_object(user_id: int, user_name: str, user_master: Optional[int] = None):
        """Used in Checker classes extract_user() function"""
        user = User(user_id, user_name, user_master)
        return user
        
    
    def enter_SQL_product_record(self, name: str, final_price: float, today: datetime.date, rating: int) -> Product: #WE ARE NOT PASSING IN DATE BECUASE THERE IS NOT DATE FIELD IN OUR SLITE DATABASE AT THE MOMENT
        """Checks is a product is not visited and then adds it to the SQL database. Returns reference to Product if operation completes successfully. Otherwise, raises AlreadyBoughtException"""
        checker = Checker(self.current_user)
        checker.check_product_not_visited(name)
        product: Product = Product.create_new(name, final_price, today, self.current_user, rating)
        return product
    
    
    @log_activity("entered a new product: ")
    def enter_new_product(self, URL : str, rating: int) -> Product:
        """Takes product-page URL, scrapes data, and then registers the visited product under the name of the current user."""
        if not Checker.check_rating(rating):
            raise RatingOutOfBounds(rating)
        scraper = Scraper()
        scraped_data = scraper.scrape(URL)
        product = self.enter_SQL_product_record(name = scraped_data[0], final_price = scraped_data[1], today = scraped_data[2], rating = rating)
        return product
        
        
    @log_activity("found a product: ")
    def find_product(self, product_code: int) -> Product: #If this one does not return product then it raises a ProductDoesNotExist Exception
        """Takes a product code and returns the accociated product object."""
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
        
        
    @log_activity("deleted a product: ")
    def delete_product(self, product_code : int) -> Product:
        """Finds product using find_product() method and then calls delete() method on the returned product object"""
        product: Product = self.find_product(product_code)
        product.delete()
        return product
    
    @log_activity("changed a products rating: ")
    def change_rating(self, product_code : int, new_rating : int) -> Product:
        """Finds product using find_product() method and the calls new_rating() on the returned product object"""
        product: Product = self.find_product(product_code)
        product.change_rating(new_rating)
        return product
    
    @log_activity("bought product: ")
    def buy(self, product_code: int) -> Product:
        """Finds product using find_product() method and then calls buy() method on the returned product object"""
        product: Product = self.find_product(product_code)
        product.buy()
        return product
        
    
    @print_prettified_products_for_user
    def list_products(self, bought: bool = None) -> List[Tuple[int, str, float, int, int, int]]:
        """List the products that are bought (or unbought) by a certain user"""
        product_list = Product.list_products(self.current_user.id, bought)
        return product_list
    
    @log_activity("deleted all bought products from the registry")
    def delete_bought_prods(self) -> bool:
        """Delete all the bought products of a user"""
        #success = Product.delete_bought_products(int(self.current_user.id))
        self.current_user.delete_bought_products()
        
        
    @log_activity("deleted all recorded products")
    def delete_all_prods(self) -> None:
        """Delete all the products of a user"""
        #success = Product.delete_bought_products(int(self.current_user.id))
        self.current_user.delete_all_products()
        

    
            
        
        
            
            
            
        
        
        
        
        
        
        
        