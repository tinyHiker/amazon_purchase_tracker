import pyfiglet
ascii_art = pyfiglet.figlet_format("Amazon Purchase Tracker", font="slant")
print(ascii_art)
logged_in = False

while True:
    if not logged_in:
        input("Username: ")

        
    command = input("> ")
    
    