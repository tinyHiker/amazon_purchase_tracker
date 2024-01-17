class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        
        
        
class Product:
    def __init__(self, *args):
        self.args = args
        self.id = args[1]
        self.name = args[2]
        self.price = args[3]
        self.bought = args[4]
        self.user_id = args[5]
        self.rating = args[6]
        
    