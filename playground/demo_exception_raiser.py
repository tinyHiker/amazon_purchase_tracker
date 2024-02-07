
class RatingOutOfBounds(Exception):
    def __init__(self, rating: int):
        message = f"Entry '{rating}' out of bounds.\nThe rating must be an integer between 1 and 10 inclusive"
        super().__init__(message)
        self.wrong_rating = rating
        
def example_function():
    raise RatingOutOfBounds(5)
