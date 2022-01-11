from functools import partial
import tkinter as tk
from tkinter.constants import END
from typing import Text
from imdb_game_api import imdb_game_api
import json

class Game:
    api = imdb_game_api("key.txt")
    user = ""
    gameDiff = 0
    gamePath = []

    startPoint=""
    currPoint=""
    endPoint=""

    currSelection=""
    
    def startGame(self,user):
        #Set global variables
        api=self.api
        self.user = user

        #Graphics
        optionsWindow = tk.Tk()
        optionsWindow.geometry('300x150')  
        optionsWindow.title("Game")
        optionsWindow.configure(background="black")
        optionsWindow.attributes('-fullscreen',True)
        
        def diffButton():
            index = listbox.curselection()
            if index:
                selection = str(listbox.get(index))
                listbox.destroy()
                button.destroy() 
                difflabel.config(text="Difficulty level: "+selection)

            self.gameDiff = int(selection)

            playText = "Let's play! Try to connect the following actors:"
            playLabel = tk.Label(optionsWindow, text = playText)

            #Use API to get game endpoints
            endpoints = api.get_game_endpoints(self.gameDiff)

            #Use API to fetch names by endpoint ids
            self.startPoint = json.loads(api.get_person_by_id(endpoints[0]))["StageName"]
            self.endPoint = json.loads(api.get_person_by_id(endpoints[1]))["StageName"]

            playLabel.pack()

            self.displayOptions(optionsWindow,0)

        diffText = "Difficulty level:"
        difflabel = tk.Label(optionsWindow,text=diffText)
        diffList = [1,2,3,4,5,6]
        listbox = tk.Listbox(optionsWindow)
        listbox.insert(END,*diffList)
        
        
        button = tk.Button(optionsWindow,text="SELECT")
        button.config(command=diffButton)

        def exitCommand():
            exit()

        exitButton = tk.Button(optionsWindow,text="EXIT",command=exitCommand)

        difflabel.pack()
        listbox.pack()
        button.pack()
        exitButton.pack()
            
        return 

    def displayOptions(self,window,movie):

        starttext = "Start: "+self.startPoint
        if self.currPoint=="":self.currPoint=self.startPoint
        currtext = "Current: "+self.currPoint
        endtext = "End: "+self.endPoint

        startLabel = tk.Label(window, text=starttext)
        currLabel = tk.Label(window, text=currtext)
        listbox = tk.Listbox(window)
        gameOverLabel = tk.Label(window)

        if not movie:
            if self.currSelection!="":
                self.gamePath.append(json.loads(self.api.get_person_by_name(self.currSelection))["People"][0]["ID"])
            options = self.calculateMovies(self.currPoint)
        elif movie:
            if self.currSelection!="":
                self.gamePath.append(json.loads(self.api.get_movie_by_name(self.currSelection))["Movies"][0]["ID"])
            options = self.calculateActors(self.currPoint)
        listbox.insert(END,*options)

        def button():
            self.gameDiff-=1
            index = listbox.curselection()
            startLabel.destroy()
            currLabel.destroy()
            endLabel.destroy()
            selectButton.destroy()
            if index:
                self.currSelection = str(listbox.get(index))
                if self.currSelection==self.endPoint:
                    displaySuccess()
                elif self.gameDiff==0:
                    displayLoss()
                else:
                    self.currPoint=self.currSelection
                    self.startPoint+=", "+self.currSelection
                    listbox.destroy()
                    self.displayOptions(window,not movie)
            return
        
        def displayLoss():
            listbox.destroy()
            #self.api.add_game(self.user,self.gamePath)
            lossWindow = tk.Toplevel(window)
            lossText = "Unfortunately, your 6 degrees are up! \nYour score: 0"
            gameOverLabel = tk.Label(lossWindow,text=lossText)
            gameOverLabel.pack()


        def displaySuccess():
            listbox.destroy()
            successWindow = tk.Toplevel(window)
            print(self.gamePath)
            successtext = "Congratulations, "+self.user+"! \nYour score: "
            gameOverLabel = tk.Label(successWindow,text=successtext)
            gameOverLabel.pack()

        selectButton = tk.Button(window,text="SELECT")
        selectButton.config(command=button)
        
        endLabel = tk.Label(window, text=endtext)

        startLabel.pack()
        currLabel.pack()
        listbox.pack()
        selectButton.pack()
        endLabel.pack()

    def calculateMovies(self,actor):
        api = self.api

        actorID = json.loads(api.get_person_by_name(actor))["People"][0]["ID"]
        
        options=[]
        moviesJson = json.loads(api.get_movies_by_actor(actorID))
        for movie in moviesJson["Movies"]:
            options.append(movie["Title"])
        
        return options[0:10]

    def calculateActors(self,movie):
        api = self.api
        
        movieID = json.loads(api.get_movie_by_name(movie))["Movies"][0]["ID"]

        options=[]
        actorsJson = json.loads(api.get_actors_by_movie(movieID))
        for actor in actorsJson["People"]:
            options.append(actor["StageName"])
        
        return options[0:10]