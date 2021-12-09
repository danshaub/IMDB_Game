# module defines an API for the IMDB Game Database

import json
from db_operations import db_operations
from helper import helper
import pickle
import random

class imdb_game_api:
    def __init__(self, key_path) -> None:
        self.db_ops = db_operations(key_path)
    
    def destructor(self):
        self.db_ops.destructor()

    ### DQL ###

    ## Browsing ##

    # given a string, search people and movies
    # returns list of people sorted by popularity with the schema
    #   (ID, ScreenName, MostPopularMovieTitle, ReleaseYear, RoleInMovie)
    # and a list of movies sorted by popularity with the schema
    #   (ID, Title, ReleaseYear)
    # Results returned in JSON format
    def get_search(self, search):
        result_sw = self.db_ops.call_proc('starts_with', (search,))
        result_ct = self.db_ops.call_proc('contains_String', (search,))

        results_mv = [helper.create_mv_search_dict(i) for i in (result_sw[0] + result_ct[0])]
        results_pr = [helper.create_pr_search_dict(i) for i in (result_sw[1] + result_ct[1])]

        result_json = helper.create_json_list([results_pr, results_mv], ["People", "Movies"])

        return result_json

    # given a string, autocomplete actors and movies
    def get_autocomplete(self, search):
        result = self.db_ops.call_proc('starts_with', (search,))

        results_mv = [helper.create_mv_search_dict(i) for i in result[0]]
        results_pr = [helper.create_pr_search_dict(i) for i in result[1]]

        result_json = helper.create_json_list([results_pr, results_mv], ["People", "Movies"])

        return result_json

    # given a StageName, return all details of all Movie People
    # whose name matches StageName in JSON Format (sorted by popularity)
    def get_person_by_name(self, name):
        result = self.db_ops.call_proc('get_person_by_name', (name,))
        result_dicts = [helper.create_person_dict(i) for i in result[0]]
        result_json = helper.create_json_list([result_dicts], ["People"])
        return result_json

    # given a MoviePerson ID, return all details in JSON Format
    def get_person_by_id(self, id):
        result = self.db_ops.call_proc('get_person_by_id', (id,))
        result_json = helper.create_person_json(result[0][0])
        return result_json

    # given a movie Title, return all details of all Movies
    # whose name matches Title in JSON Format (sorted by popularity)

    def get_movie_by_name(self, name):
        result = self.db_ops.call_proc('get_movie_by_name', (name,))
        result_dicts = [helper.create_movie_dict(i) for i in result[0]]
        result_json = helper.create_json_list([result_dicts], ["Movies"])
        return result_json

    # given a Movie ID, return all details in JSON Format
    def get_movie_by_id(self, id):
        result = self.db_ops.call_proc('get_movie_by_id', (id,))
        result_json = helper.create_movie_json(result[0][0])
        return result_json

    

    def get_movies_by_person(self, id):
        result = self.db_ops.call_proc('get_movies_by_person', (id,))
        result_dicts = [helper.create_movie_dict(i) for i in result[0]]
        result_json = helper.create_json_list([result_dicts], ["Movies"])
        return result_json

    def get_people_by_movie(self, id):
        result = self.db_ops.call_proc('get_people_by_movie', (id,))
        result_dicts = [helper.create_person_dict(i) for i in result[0]]
        result_json = helper.create_json_list([result_dicts], ["People"])
        return result_json

    ## Game Functions ##

    def get_game_endpoints(self, gameSeed=int, numSteps=int, minStartPopularity=int) -> tuple:
        temp_games = [(114,5403), # S. Buscemi -> J. Schwartzman
                      (102, 6819854), # K. Bacon -> Justice Smith 
                      (375, 185819)]  # R. Downey Jr. -> D. Craig

        return temp_games[random.randint(0,2)]

    def get_movies_by_actor(self, id):
        result = self.db_ops.call_proc('get_movies_by_actor', (id,))
        result_dicts = [helper.create_movie_dict(i) for i in result[0]]
        result_json = helper.create_json_list([result_dicts], ["Movies"])
        return result_json

    def get_actors_by_movie(self, id):
        result = self.db_ops.call_proc('get_actors_by_movie', (id,))
        result_dicts = [helper.create_person_dict(i) for i in result[0]]
        result_json = helper.create_json_list([result_dicts], ["People"])
        return result_json

    ## Player Stats ##

    # given a player, return list of games they played
    def get_games_by_player(self, playerID):
        result = self.db_ops.call_proc('get_games', (playerID,))
        result_dicts = [helper.create_game_dict(i) for i in result[0]]
        result_json = helper.create_json_list([result_dicts], ["Games"])
        return result_json

    def get_game_by_id(self, id):
        result = self.db_ops.call_proc('get_game_by_id', (id,))
        result_json = helper.create_game_json(result[0][0])
        return result_json


    ### DML ###

    # Commits current transaction
    def commit_action(self):
        self.db_ops.commit_transation()

    # Rollsback current transaction
    def rollback_action(self):
        self.db_ops.rollback_transaction()

    # add player
    # add actor
    # add movie
    # add game

    # edit movie details
    # edit actor details
    # edit player details
        # add games to list of games

    def insert_game(self, PlayerID, GamePath=[int]):
        StarterPersonID = GamePath[0]
        EnderPersonID = GamePath[-1]
        OptimalScore = 0 # TODO: implement finding optimal score
        Score = ((len(GamePath) - 1) / 2) - OptimalScore
        self.db_ops.insert_game((PlayerID,
                                 StarterPersonID,
                                 EnderPersonID,
                                 OptimalScore,
                                 Score,
                                 pickle.dumps(GamePath)))

    # add actors to movies

