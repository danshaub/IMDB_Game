# module defines an API for the IMDB Game Database

import json
from db_operations import db_operations
from helper import helper

class imdb_game_api:
    def __init__(self, key_path) -> None:
        self.db_ops = db_operations(key_path)
    
    def destructor(self):
        self.db_ops.destructor()

    ### DQL ###

    # given a string, search people and movies
    # returns list of people sorted by popularity with the schema
    #   (ID, ScreenName, MostPopularMovieTitle, ReleaseYear, RoleInMovie)
    # and a list of movies sorted by popularity with the schema
    #   (ID, Title, ReleaseYear)
    # Results returned in JSON format
    def get_search(self, search):
        result_sw = self.db_ops.call_proc('starts_with', (search,))
        result_ct = self.db_ops.call_proc('contained', (search,))

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
        # result = self.db_ops.call_proc('get_person_by_name', (name,))
        result = self.db_ops.call_proc('get_actor', (name,))
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

    # given a player, return list of games they played
    # given a player, return stats from games they played
    # retrun a start and end actor
    # given an actor, return all movies they acted in
    # given a movie, return all actors who played in it

    ### DML ###

    # add player
    # add actor
    # add movie
    # add game

    # edit movie details
    # edit actor details
    # edit player details
        # add games to list of games

    # add actors to movies

