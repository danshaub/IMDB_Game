import tkinter as tk
from functools import partial
import options

#Start Page

#loadScreen(user)->load admin/user login page
def loadScreen(user):

    newWindow = tk.Tk()
    newWindow.geometry('300x150')  
    newWindow.configure(background="black")
    newWindow.attributes('-fullscreen',True)

    def exitCommand():
            exit()

    exitButton = tk.Button(newWindow,text="EXIT",command=exitCommand)
    
    if user=='a':
        title = 'Admin Login'
        label = "Please enter admin password."
        text = "Password:"
        password = tk.StringVar(newWindow)
    else:
        title = "Guest Login"
        label = "Please enter username."
        text = "Username:"
        username = tk.StringVar(newWindow)
    
    newWindow.title(title)

    #instruction
    titleLabel = tk.Label(newWindow,text=label)

    #password label and password entry box
    passwordLabel = tk.Label(newWindow,text=text)

    #button(login type)-> validate login
    def button(type):
        if type=='a':
            adminPw = "pw"
            pw = tk.StringVar.get(password)
            if pw==adminPw:
                opt=options.Options()
                opt.adminScreen()
                newWindow.destroy()
            else:
                errorWindow = tk.Toplevel(newWindow)
                errorLabel = tk.Label(errorWindow, text = "Wrong password, please try again.")
                errorLabel.pack()
        else: 
            opt=options.Options()
            opt.guestScreen(username)
            newWindow.destroy()
    
    if user=='a':
        entry = tk.Entry(newWindow, textvariable=password, show='*')
        loginButton = tk.Button(newWindow, text="LOGIN", command=partial(button,'a'))
    else:
        entry = tk.Entry(newWindow, textvariable=username)
        opt=options.Options()
        loginButton = tk.Button(newWindow, text="LOGIN", command=partial(button,'r'))

    titleLabel.pack()
    passwordLabel.pack()
    entry.pack()
    loginButton.pack()
    exitButton.pack()

