import customtkinter 
import tkinter 

def startDownload():
    pass
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
    
    
GUI()