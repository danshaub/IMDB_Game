import json
from imdb_game_api import imdb_game_api
from json import loads

#Edit

class Edit():

    #Connect to database
    api = imdb_game_api("key.txt") 

    #editOptions()-> handles dml logic
    def editOptions(self):
        api = self.api
        exit=0
        #main loop for main edit options
        while not exit:
            #Display main edit options
            choice = input("\nPlease select from the following options:\n(1)Add\n(2)Delete\n(3)Edit\n(4)Save\n(5)Undo\n(6)Exit\n")

            #ADD
            if choice=="1":
                choice = input("\nPlease select from the following insertion options:\n(1)Player\n")
                #PLAYER
                if choice=="1":
                    user = input("\nPlease input the username: ")
                    isAdmin = input("\nAdmin? (Y/N): ")
                    if isAdmin=="Y":isAdmin=1
                    else: isAdmin=0
                    api.add_player(user,isAdmin)
                    print(user+" successfully added.")
            
            #EDELETE
            if choice=="2":
                choice = input("\nPlease select from the following deletion options:\n(1)Delete Movie\n(2)Delete Player\n(3)Delete Person\n(4)Exit\n")
                #MOVIE
                if choice=="1":
                    movieName = input("\nPlease input the name of the movie whose record you would like to delete: ")
                    api.delete_movie(json.loads(api.get_movie_by_name(movieName))["Movies"][0]["ID"])
                    print(movieName+" has been successfully deleted.")
                #PLAYER
                elif choice=="2":
                    userID = input("\nPlease input the ID of the player whose record you would like to delete: ")
                    api.delete_player(userID)
                    print(userID+" has been successfully deleted.")
                #PERSON
                elif choice=="3":
                    personName = input("\nPlease input the name of the person whose record you would like to delete: ")
                    api.delete_person(json.loads(api.get_person_by_name(personName))["People"][0]["ID"])
                    print(personName+" has been successfully deleted.")

            #EDIT
            elif choice=="3":
                choice = input("\nPlease select from the following editing options:\n(1)Edit Movie\n(2)Edit Player\n(3)Edit Person\n(4)Exit\n")
                #MOVIE
                if choice=="1":
                    movieName = input("\nPlease input the name of the movie whose record you would like to edit: ")
                    movieInfo = json.loads(api.get_movie_by_name(movieName))["Movies"][0]
                    movieID = movieInfo["ID"]
                    print("\nHere is the current info for "+movieName+" : ")
                    print(movieInfo)
                    print("Please select from the following attributes to edit: ")

                    newTitle = movieInfo["Title"]
                    newYear = movieInfo["ReleaseYear"]
                    newGenre = movieInfo["Genre"]
                    newDuration = movieInfo["Duration"]
                    newCountry = movieInfo["Country"]
                    newRating = movieInfo["Rating"]
                    newVotes = movieInfo["Votes"]

                    emovieExit = 0
                    #movie edit loop
                    while not emovieExit:
                        choice = input("\n(1)Title\n(2)Release Year\n(3)Genre\n(4)Duration\n(5)Country\n(6)Rating\n(7)Votes\n(8)I'm Done Editing\n")
                        if choice=="1":
                            newTitle = input("\nPlease input the updated movie title: ")
                        elif choice=="2":
                            newYear = input("\nPlease input the updated movie release year: ")
                        elif choice=="3":
                            newGenre = input("\nPlease input the updated movie genre: ")
                        elif choice=="4":
                            newDuration = input("\nPlease input the updated movie duration: ")
                        elif choice=="5":
                            newCountry = input("\nPlease input the updated movie country: ")
                        elif choice=="6":
                            newRating = input("\nPlease input the updated movie rating: ")
                        elif choice=="7":
                            newVotes = input("\nPlease input the updated movie votes: ")
                        elif choice=="8":
                            emovieExit=1
                    
                    api.edit_movie(movieID,newTitle,newYear,newGenre,newDuration,newCountry,newRating,newVotes)
                    print(newTitle+" has been successfully updated")
                #PLAYER
                elif choice=="2":
                    userID = input("\nPlease input the ID of the player whose record you would like to edit: ")
                    userInfo = json.loads(api.get_player_by_id(userID))
                    print(userInfo)
                #PERSON
                elif choice=="3":
                    personName = input("\nPlease input the name of the person whose record you would like to edit: ")
                    personInfo = json.loads(api.get_person_by_name(personName))["People"][0]
                    personID = personInfo["ID"]
                    print("\nHere is the current info for "+personName+" : ")
                    print(personInfo)
                    print("Please select from the following attributes to edit: ")

                    newName = personInfo["StageName"]
                    newHeight = personInfo["Height"]
                    newBday = personInfo["Birthday"]
                    newBplace = personInfo["BirthPlace"]
                    newPopularity = personInfo["Popularity"]

                    epersonExit = 0
                    #person edit loop
                    while not epersonExit:
                        choice = input("\n(1)Stage Name\n(2)Height\n(3)Birthday\n(4)Birthplace\n(5)Popularity\n(6)I'm Done Editing\n")
                        if choice=="1":
                            newName = input("\nPlease input the updated person name: ")
                        elif choice=="2":
                            newHeight = input("\nPlease input the updated person height: ")
                        elif choice=="3":
                            newBday = input("\nPlease input the updated person birthday: ")
                        elif choice=="4":
                            newBplace = input("\nPlease input the updated person birthplace: ")
                        elif choice=="5":
                            newPopularity = input("\nPlease input the updated person popularity: ")
                        elif choice=="6":
                            epersonExit=1
                    
                    api.edit_person(personID,newName,newHeight,newBday,newBplace,newPopularity)
                    print(newName+" has been successfully updated")
        
            #SAVE
            elif choice=="4":
                api.commit_action()
                print("Actions successfully committed.")

            #UNDO
            elif choice=="5":
                api.rollback_action()
                print("Actions successfully rolledback.")

            #EXIT
            elif choice=="6":
                exit=1