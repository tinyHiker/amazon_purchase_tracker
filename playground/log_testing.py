import logging

class Log:
    # A decorator defined inside a class
    
    def __init__(self):
        self.logger = logging.getLogger(f"Username")
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)s:%(message)s')
        file_handler = logging.FileHandler('test_activity.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
    
    def log_activity(func):
        def wrapper(self, *args, **kwargs):
            self.logger.info("User ran func")
            result = func(self, *args, **kwargs)
            return result
        return wrapper

    # Applying the decorator to an instance method
    @log_activity
    def say_hello(self, name):
        print(f"Hello, {name}!")

# Usage
my_instance = Log()
my_instance.say_hello("World")