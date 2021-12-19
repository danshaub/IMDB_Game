# module defines an API for the IMDB Game Database

from db_operations import db_operations
from helper import helper
import pickle
import random
import json

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

    # given a Person ID, return all movies they contributed to
    def get_movies_by_person(self, id):
        result = self.db_ops.call_proc('get_movies_by_person', (id,))
        result_dicts = [helper.create_movie_dict(i) for i in result[0]]
        result_json = helper.create_json_list([result_dicts], ["Movies"])
        return result_json

    # given a Movie ID, return all people who contributed
    def get_people_by_movie(self, id):
        result = self.db_ops.call_proc('get_people_by_movie', (id,))
        result_dicts = [helper.create_person_dict(i) for i in result[0]]
        result_json = helper.create_json_list([result_dicts], ["People"])
        return result_json

    # given the name of a character, returns the actor and movie associated
    def get_info_by_role(self, characterName):
        # proc info_by_role makes use of a subquery and 
        result = self.db_ops.call_proc('info_by_role', (characterName,))
        result_dicts = [helper.create_role_info_dict(i) for i in result[0]]
        result_json = helper.create_json_list([result_dicts], ["RoleInfo"])
        return result_json

    def get_player_by_id(self, id):
        result = self.db_ops.call_proc('get_player_by_id', (id,))
        result_json = helper.create_player_json(result[0][0])
        return result_json

## Game Functions ##

    # Generates two random endpoints exactly numSteps costars away from
    # one another. Can be given a seed for repeated games
    def get_game_endpoints(self, numSteps=int, gameSeed=0) -> tuple:
        if gameSeed != 0:
            random.seed(gameSeed)
        
        ## get_top_pop_movies uses a View ##
        # Finds random movie within top 1000 most popular
        movies = self.db_ops.call_proc('get_top_pop_movies')
        movies = [helper.create_movie_dict(i) for i in movies[0]]
        movie = movies[random.randint(0, len(movies)-1)]

        # Finds random actor from movie. Set to starting actor
        actors = self.get_actors_by_movie(movie['ID'])
        actors = json.loads(actors)['People']
        actors = [actor['ID'] for actor in actors]
        startActor = actors[random.randint(0, len(actors)-1)]

        # Get ids of all actors numSteps away
        nodes = self.db_ops.get_nodes_at_depth(startActor, numSteps)
        ids = helper.get_ids_from_nodes(nodes)

        # Picks random actor from set of actors numSteps away
        rand_id_index = 0
        if len(ids) > 25:
            rand_id_index = random.randint(0, 24)
        else:
            rand_id_index = random.randint(0, len(ids)-1)

        endActor = ids[rand_id_index]

        return (startActor, endActor)

    # Given two actors, calcuates how far they are away from one another
    def calculate_optimal_score(self, startActor=int, endActor=int):
        return self.db_ops.calculate_optimal_score(startActor, endActor)

    # Given 
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

## Add Records ##
    # add person
    def add_person(self, StageName, Height, Birthday, BirthPlace, Popularity):
        self.db_ops.call_proc(
            'add_person', (StageName, Height, Birthday, BirthPlace, Popularity))
    # add movie
    def add_movie(self, Title, ReleaseYear, Genre, Duration, Country, Rating, Votes):
        self.db_ops.call_proc('add_movie', Title, ReleaseYear,
                            Genre, Duration, Country, Rating, Votes)
    # add player
    def add_player(self, UserName, IsAdmin):
        self.db_ops.call_proc('add_player', UserName, IsAdmin)

    # add cast
    def add_cast(self, movieID, personID, category, characterPlayed):
        self.db_ops.call_proc('add_cast', movieID, None, personID, category, characterPlayed)
    
    # add game
    def add_game(self, player, gamePath=[int]):
        starter = gamePath[0]
        ender = gamePath[-1]
        optimalScore = self.calculate_optimal_score(starter, ender)
        Score = ((len(gamePath) - 1) / 2) - optimalScore
        self.db_ops.call_proc('add_game', (player,
                                starter,
                                ender,
                                optimalScore,
                                Score,
                                pickle.dumps(gamePath)))

## Edit Records ##
    # edit person
    def edit_person(self, ID, StageName, Height, Birthday, BirthPlace, Popularity):
        self.db_ops.call_proc(
            'edit_player', (ID, StageName, Height, Birthday, BirthPlace, Popularity))
    
    # edit movie
    def edit_movie(self, ID, Title, ReleaseYear, Genre, Duration, Country, Rating, Votes):
        self.db_ops.call_proc('edit_movie', (ID, Title, ReleaseYear,
                            Genre, Duration, Country, Rating, Votes))
    # edit player

    def edit_player(self, ID, UserName, IsAdmin):
        self.db_ops.call_proc('edit_player', (ID, UserName, IsAdmin))

    # edit cast
    def edit_cast(self, ID, movieID, personID, category, characterPlayed):
        self.db_ops.call_proc('edit_cast', (ID, movieID, None,
                            personID, category, characterPlayed))

## Delete Records ##
    # delete person
    def delete_person(self, ID):
        self.db_ops.call_proc(
            'delete_person', (ID,))

    # delete movie
    def delete_movie(self, ID):
        self.db_ops.call_proc('delete_movie', (ID,))
    
    # delete player
    def delete_player(self, ID):
        self.db_ops.call_proc('delete_player', (ID,))

    # delete cast
    def delete_cast(self, ID):
        self.db_ops.call_proc('delete_cast', (ID,))