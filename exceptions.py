class AlreadyBought(Exception):
    def __init__(self):
        message = f"You have already bought this product"
        super().__init__(message)
       
        
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