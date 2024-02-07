class AlreadyBoughtException(Exception):
    def __init__(self, product_id):
        message = f"You have already bought this product (Product #{product_id})"
        super().__init__(message)
       
        
class WebsiteNotFound(Exception):
    """Custom exception class for when there is no website that matches a passed URL"""

    def __init__(self, message="The URL does not match any website", URL = None):
        super().__init__(message)
        self.faulty_URL = URL


class ProductDoesNotExist(Exception):
    def __init__(self, faulty_code: int ):
        message = f"Product #{faulty_code} does not exist"
        super().__init__(message)
        self.code = faulty_code
        
class UserDoesNotExist(Exception):
    def __init__(self, wrong_name: str):
        message = f"User '{wrong_name}' does not exist"
        super().__init__(message)
        self.wrong_name = wrong_name
        
class UserAlreadyExists(Exception):
    def __init__(self, user_name: str):
        message = f"User '{user_name}' already exists"
        super().__init__(message)
        self.user_name = user_name
        
class RatingOutOfBounds(Exception):
    def __init__(self, rating: int):
        message = f"Entry '{rating}' out of bounds.\nThe rating must be an integer between 1 and 10 inclusive"
        super().__init__(message)
        self.wrong_rating = rating
        
class NoProductsDeleted(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        