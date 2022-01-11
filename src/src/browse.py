import tkinter as tk
from functools import partial
import json
from tkinter.constants import END, LEFT
from imdb_game_api import imdb_game_api

#Browse

#Connect to database
api = imdb_game_api("key.txt")
  
class Browse:

    #Global variables
    searchtype=""

    #browseOptions(self) -> displays browse options
    def browseOptions(self):

        #Window
        optionsWindow = tk.Tk()
        optionsWindow.geometry('300x150')  
        optionsWindow.title("Browse")
        optionsWindow.configure(background="black")
        optionsWindow.attributes('-fullscreen',True)

        text = "Please select from the following browsing options:"
        optionsLabel = tk.Label(optionsWindow, text = text)

        #Search for actor
        searchPersonLabel = tk.Label(optionsWindow, text="Search People")
        searchPersonString = tk.StringVar(optionsWindow)
        searchPersonEntry = tk.Entry(optionsWindow,textvariable=searchPersonString)
        searchPersonButton = tk.Button(optionsWindow,text="SEARCH",command=partial(self.search,'p',searchPersonString,optionsWindow))

        #Search for movie
        searchMovieLabel = tk.Label(optionsWindow, text="Search Movies")
        searchMovieString = tk.StringVar(optionsWindow)
        searchMovieEntry = tk.Entry(optionsWindow,textvariable=searchMovieString)
        searchMovieButton = tk.Button(optionsWindow,text="SEARCH",command=partial(self.search,'m',searchMovieString,optionsWindow))

        #Search for role
        searchRoleLabel = tk.Label(optionsWindow, text="Search Roles")
        searchRoleString = tk.StringVar(optionsWindow)
        searchRoleEntry = tk.Entry(optionsWindow,textvariable=searchRoleString)
        searchRoleButton = tk.Button(optionsWindow,text="SEARCH",command=partial(self.search,'r',searchRoleString,optionsWindow))

        def exitCommand():
            exit()

        exitButton = tk.Button(optionsWindow,text="EXIT",command=exitCommand)

        optionsLabel.pack()

        searchPersonLabel.pack()
        searchPersonEntry.pack()
        searchPersonButton.pack()

        searchMovieLabel.pack()
        searchMovieEntry.pack()
        searchMovieButton.pack()

        searchRoleLabel.pack()
        searchRoleEntry.pack()
        searchRoleButton.pack()

        exitButton.pack()
        
        return 

    #search(search type, search string, window) -> display search results 
    def search(self,type,searchString,window):
        self.type = type
        search = tk.StringVar.get(searchString)

        if type!="r":
            output=json.loads(api.get_search(search))
            if type=="p":
                options=[]
                for i in range(0,len(output["People"])):
                    options.append(output["People"][i]["ID"])
            elif type=="m":
                options=[]
                for i in range(0,len(output["Movies"])):
                    options.append(output["Movies"][i]["ID"])
            listbox = tk.Listbox(
                window,
                selectmode='single'
                )
            listbox.insert(END,*options)
            listbox.pack()

        else:
            output=json.loads(api.get_info_by_role(search))
        
        #viewInfo()-> display info on selected search result
        def viewInfo():

            show = tk.Label(window)

            if self.type!="r":
                if listbox.curselection():
                    selection = listbox.get(listbox.curselection())
                listbox.destroy()
                viewInfoButton.destroy()

                if self.type=="p":
                    objectInfo = json.loads(api.get_person_by_name(selection))
                    person = objectInfo["People"][0]
                    show.config(text="\nName: "+person["StageName"]+
                    "\nHeight: "+str(person["Height"])+
                    "\nBirthday: "+str(person["Birthday"])+
                    "\nBirthplace: "+person["BirthPlace"]
                    )
                elif self.type=="m":
                    objectInfo = json.loads(api.get_movie_by_name(selection))
                    movie = objectInfo["Movies"][0]
                    show.config(text="Title: "+movie["Title"]+
                    "\nRelease Year: "+str(movie["ReleaseYear"]))
            else:
                viewInfoButton.destroy()
                text1="\nMovie: "+output["RoleInfo"][0]["Movie"]+"\nActor: "+output["RoleInfo"][0]["Actor"]
                text2="\nMovie: "+output["RoleInfo"][2]["Movie"]+"\nActor: "+output["RoleInfo"][3]["Actor"]
                text3="\nMovie: "+output["RoleInfo"][3]["Movie"]+"\nActor: "+output["RoleInfo"][3]["Actor"]   
                show.config(text=text1+text2+text3)        
            
            show.pack()
        

        viewInfoButton = tk.Button(window,text="VIEW INFO",command=viewInfo)

        
        viewInfoButton.pack()