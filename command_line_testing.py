#In order to perform these tests, you have to clear the database 

#Internal imports 
from main import *
import exceptions

#External imports
import sqlite3


def print_all_records():
    """Accesses the database and prints all its records"""
    conn = sqlite3.connect('database.db')  
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()  
    print("Users:")
    for user in users:
        print(user)  
    
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()  
    print("\nProducts:")
    for product in products:
        print(product)  

    conn.commit()
    conn.close()





#TEST #1: Testing login, seeing if a user is returned properly and if I can properly access its attributes
print("TEST #1: LOGIN", end ="\n\n\n")
user = login("Taha")
print(user)
print(user.id)
print(user.name)
print(user.master)  # WILL EVENTUALLY NEED TO UPDATE THIS
print("\n")
print("--------------------------------------------------------------------------------------------------------")





#TEST #2: Testing the creating of modifier
print("TEST #2: CREATION OF A MODIFIER", end ="\n\n\n")
modifier = Modifier(user)
print(f"Testing to see if modifier object has the right user: {modifier.current_user.name}") #Checking if the User object is actually in the modifier
print("\n")
print("--------------------------------------------------------------------------------------------------------")





#TEST #3: Testing creation of a new user
print("TEST #3: TESTING CREATION OF A NEW USER", end ="\n\n\n")
new_user = modifier.new_user("Joe") 
print(new_user)
print(new_user.name)
print_all_records()  #Finding Joe in the database

try:
    new_user = modifier.new_user("Joe") 
except UserAlreadyExists as uae:  #This should be caught
    print(uae)
    
print("\n")
print("--------------------------------------------------------------------------------------------------------")
    
    
    
    
    
#TEST #4: Testing entry and scraping of a new product
print("TEST #3: TESTING ENTRY OF A NEW PRODUCT", end ="\n\n\n")
sucess = modifier.enter_new_product('https://www.amazon.com/Funny-Data-Systems-Business-Analyst/dp/B07FNW9FGJ', 3)
print_all_records()

#Checking if
try:
    success = modifier.enter_new_product('', 11)
except exceptions.RatingOutOfBounds as rob:  
    print("Caught RatingOutOfBoundsException") #RatingOutOfBounds should be raised immediately by the enter_new_product function
    print(rob)
    
    
try:
    success = modifier.enter_new_product('https://www.amazon.com/Funny-Data-Systems-Business-Analyst/dp/B07FNW9FGJ', 7)
    print(success)
except exceptions.AlreadyBoughtException as ab: #AlreadyBoughtException should be raised by Checker classes check_product_not_visited()
    print("Caught AlreadyBoughtException") 
    print(ab)
    
print("\n")
print("--------------------------------------------------------------------------------------------------------")





#TEST 5: TESTING THE FINDING OF THE PRODUCT
print("TEST #5: TESTING THE FINDING OF A PRODDUCT", end ="\n\n\n")
found_product = modifier.find_product(3)
print(found_product)
print(found_product.id)
print(type(found_product.id))
print(found_product.name)
print(type(found_product.name))

print("\n")
print("--------------------------------------------------------------------------------------------------------")






#TEST 6: Testing the deletion of a product
print("TEST #6: TESTING THE DELETION OF PRODUCTS", end ="\n\n\n")
modifier.delete_product(product_code=3)
print_all_records()


try:
    found_product = modifier.delete_product(3)
except ProductDoesNotExist as pdn:
    print("Caught ProductDoesNotExist for delete operation")
    print(pdn)
    
    
try:
    found_product = modifier.find_product(3)
except ProductDoesNotExist as pde:
    print("Caught ProductDoesNotExist Exception")
    
print("\n")
print("--------------------------------------------------------------------------------------------------------")
    



#TEST 7: Testing the change_rating functionality
print("TEST #7: TESTING THE CHANGE RATING FUNCTIONALITY", end ="\n\n\n")
print("\nBEFORE:", end="\n")
print_all_records()
modifier.change_rating(1, 2) #Should change "Widget" rating from 9 to 2
print("\n\nAFTER ['WIDGET' RATING SHOULD NOW BE 2]:", end="\n")
print_all_records()
print("\n")
print("--------------------------------------------------------------------------------------------------------")
 
 
 
 
 
 
#TEST 8: Testing the list products functionality
# I NEED TO FIX THE DISPLAY
print("TEST #8: TESTING THE LIST PRODUCTS FUNCTIONALITY", end ="\n\n\n")

print("\nVIEWING ALL PRODUCTS:", end="\n") 
#Should show both "Widget" and "Gadget"
modifier.list_products()

print("\n\nVIEWING ALL UNBOUGHT PRODUCTS:", end="\n")
#Should show only "Widget"
modifier.list_products(0)


print("\n\nVIEWING ALL BOUGHT PRODUCTS:", end="\n")
#Should show only "Gadget"
modifier.list_products(1)
print("\n")
print("--------------------------------------------------------------------------------------------------------")
 



#TEST 9: Deleting all the bought products
#
print("TEST #9: DELETING ALL THE BOUGHT PRODUCTS", end ="\n\n\n")

print("\n\nVIEWING ALL BOUGHT PRODUCTS BEFORE:", end="\n")
#Should show only "Gadget"
modifier.list_products(1)
print("\n")

modifier.delete_bought_prods()

print("\n\nVIEWING ALL BOUGHT PRODUCTS AFTER:", end="\n")
#Should show only "Gadget"
modifier.list_products(1)
print("\n")

print("\n\nTRYING TO DELETE ALL BOUGHT PRODUCTS WHEN THERE ARE NONE:", end="\n")
try:
    modifier.delete_bought_prods()
except NoProductsDeleted:
    print("Caught NoProductsDeletedException")


print("--------------------------------------------------------------------------------------------------------")


#TEST 10: Delete all products for the user that's logged in functionality. Must check 


 








