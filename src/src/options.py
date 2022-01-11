from json import loads
import game,stats,browse,adminEdit
import tkinter as tk
from functools import partial

#Options Menu

class Options():
    user = ""
    #guesScreen(user)->load user menu
    def guestScreen(self,user):
        self.user = user
        optionsWindow = tk.Tk()
        optionsWindow.configure(background="black")
        optionsWindow.attributes('-fullscreen',True)
        optionsWindow.title = "Options Menu"
        text = "Welcome "+tk.StringVar.get(self.user)+"! Please select from the following options:"
        optionsLabel = tk.Label(optionsWindow, text = text)

        #Load selected screen
        def loadNext(screen):
            if screen=="g":
                gm = game.Game()
                gm.startGame(self.user)
            elif screen=="b":
                br = browse.Browse()
                br.browseOptions()
            elif screen=="s":
                stats.showStats()
            optionsWindow.destroy()
            return

        browseButton = tk.Button(optionsWindow, text="BROWSE", command=partial(loadNext,"b"))
        statsButton = tk.Button(optionsWindow, text="STATS", command=partial(loadNext,"s"))
        gameButton = tk.Button(optionsWindow, text="GAME", command=partial(loadNext,"g"))

        def exitCommand():
            exit()

        exitButton = tk.Button(optionsWindow,text="EXIT",command=exitCommand)

        optionsLabel.pack()
        browseButton.pack()
        statsButton.pack()
        gameButton.pack()
        exitButton.pack()
        
    #adminScreen()-> load admin menu
    def adminScreen(self):
        self.user="admin"
        optionsWindow = tk.Tk()
        optionsWindow.configure(background="black")
        optionsWindow.attributes('-fullscreen',True)
        optionsWindow.title = "Options Menu"
        optionsLabel = tk.Label(optionsWindow, text = "Welcome, admin! Please select from the following options:")
        
        #Load selected screen
        def loadNext(screen):
            if screen=="g":
                gm = game.Game()
                gm.startGame(self.user)
            elif screen=="b":
                br = browse.Browse()
                br.browseOptions()
            elif screen=="s":
                stats.showStats()
            elif screen=="e":
                ed = adminEdit.Edit()
                ed.editOptions()
            optionsWindow.destroy()
            return
        
        browseButton = tk.Button(optionsWindow, text="BROWSE", command=partial(loadNext,"b"))
        statsButton = tk.Button(optionsWindow, text="STATS", command=partial(loadNext,"s"))
        gameButton = tk.Button(optionsWindow, text="GAME", command=partial(loadNext,"g"))
        editButton = tk.Button(optionsWindow, text="EDIT", command=partial(loadNext,"e"))

        def exitCommand():
            exit()

        exitButton = tk.Button(optionsWindow,text="EXIT",command=exitCommand)

        optionsLabel.pack()
        browseButton.pack()
        statsButton.pack()
        gameButton.pack()
        editButton.pack()
        exitButton.pack()