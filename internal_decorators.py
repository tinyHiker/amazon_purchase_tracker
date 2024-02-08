from prettytable import PrettyTable

def print_SQL_records(func):
    """A decorator that prints all the return records from a function"""
    def wrapper(self, *args, **kwargs):
        records_list = func(self, *args, **kwargs)
        for record in records_list:
            str_tuple = tuple(map(str, record))
            print_string = " ".join(str_tuple)
            print(print_string)
    return wrapper


def print_prettified_products_for_user(func):
    """A decorator that prints all the returned product_records in a prettified format"""
    def wrapper(self, *args, **kwargs):
        products_list: List[Tuple[int, str, float, int, int, int]] = func(self, *args, **kwargs)  #product_list variable is a list of tuples (product_id, name, price, bought, user_id, rating)
        
        table = PrettyTable()
        table.field_names = ["PRODUCT ID", "PRODUCT NAME", "PRICE ($CAD)", "BOUGHT-STATUS", "RATING (/10)"]
        
        for product in products_list:
            product = list(product)
            product[2] = f"${product[2]:.2f}" #converting the price from a float to a string with a dollar sign in front of it.
            
            if product[3] == 1:   #converting the integer version of the 'bought' field to a string. It is more user-friendly
                product[3] = 'Bought'
            else:
                product[3] = 'Unbought'
                
            modified_list = list(map(str, product))
            m_list_sliced = list(modified_list[:4] + [modified_list[-1]])
            table.add_row(m_list_sliced)
            
        print(table)
        return products_list
    
    return wrapper
    
     