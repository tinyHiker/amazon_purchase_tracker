
def my_decorator(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        print("Testing Decorator Functionality")
    return wrapper

@my_decorator
def scooby(*args):
    print(args[0])
    
    
scooby(*(1,2,3,4,5,6))