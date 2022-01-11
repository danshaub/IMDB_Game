from functools import partial
import tkinter as tk
import startPage

#Initial script

#window
tkWindow = tk.Tk()  
tkWindow.geometry('300x150')  
tkWindow.configure(background="black")
tkWindow.attributes('-fullscreen',True)
tkWindow.title('IMDB Game Start Screen')

#instruction
titleLabel = tk.Label(tkWindow,text="Welcome! Please select user to display options.")

#button(selection type)->load login from startPage
def button(type):
    if type=='a':
        startPage.loadScreen("a")
        tkWindow.destroy()
    else: 
        startPage.loadScreen("r")
        tkWindow.destroy()
    

#admin/reg button
adminButton = tk.Button(tkWindow, text="ADMIN")
adminButton.config(command=partial(button,'a'))
regButton = tk.Button(tkWindow, text="GUEST")
regButton.config(command=partial(button,'r'))

def exitCommand():
    exit()

exitButton = tk.Button(tkWindow,text="EXIT",command=exitCommand)

titleLabel.pack()
regButton.pack()
adminButton.pack()
exitButton.pack()

tkWindow.mainloop()