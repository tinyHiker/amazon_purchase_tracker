# Import the necessary modules from rich
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from rich.markdown import Markdown
# Create a console object

import pyfiglet
from termcolor import colored

import tkinter
import customtkinter 

console = Console()



def login():
    console.print("Rafa: Amazon Purchase Tracker", style="bold gold1")
    username = ""
    while username != "Taha":
        username = Prompt.ask("[gold1]Please enter your username[/gold1]")

    # Create a welcome message
    welcome_message = Text(f"Welcome back, {username}.", style="bold blue")
    console.print(welcome_message)
    
def markdown_test():
    MARKDOWN = """# Amazon Purchase Tracker made by Taha Iqbal"""
    
    md = Markdown(MARKDOWN)
    console.print(md)
    
    
def pyfiglet_test():
    figlet_text = pyfiglet.figlet_format("RAFA Amazon Purchase Tracker", font='georgia11')
    colored_text = colored(figlet_text, 'yellow')  # Change 'green' to your desired color
    print(colored_text, end = "")
    #font list: broadway, greek, varsity, georgia11 is really good, georgi16 is even better
    
    
def GUI():
    app = customtkinter.CTk()
    app.geometry("720x480")
    app.title("Youtube Downloader")
    #app.iconbitmap(r'images\youtube_logo.ico')
    #Adding UI elements
    title = customtkinter.CTkLabel(app, text= "Insert youtube link ", font=("Segoe UI", 12))
    title.pack(padx = 10, pady=10)
    url_var = tkinter.StringVar()
    link = customtkinter.CTkEntry(app, width = 350, height = 40, textvariable = url_var, font=("Segoe UI", 12))
    link.pack()
    finishLabel = customtkinter.CTkLabel(app, text = "", font=("Segoe UI", 12))
    finishLabel.pack(padx=10, pady= 10)
    #Progress Percentage
    pPercentage = customtkinter.CTkLabel( app, text = '0%', font=("Segoe UI", 30), text_color="red")
    pPercentage.pack()
    download = customtkinter.CTkButton(app, text = "Download", font=("Segoe UI", 12), command = startDownload, fg_color=("red", "red"), text_color=("white", "white"), hover_color=("red", "red"))
    download.pack(padx= 10, pady = 10)
    # Run app
    app.mainloop()
    
    
    

if __name__ == "__main__":
    pyfiglet_test()
    login()
    GUI()
    #print(pyfiglet.FigletFont.getFonts())
    
