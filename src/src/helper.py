import json
import pickle

class helper():
    __pr_schema = ["ID","StageName","Height","Birthday","BirthPlace", "Popularity", "Category", "Role"]
    __mv_schema = ["ID", "Title", "ReleaseYear", "Genre", "Duration", "Country", "Rating", "Votes", "Category", "Role"]
    __ct_schema = ["ID", "Movie", "Importance", "MoviePeople", "Category", "CharacterPlayed"]
    __gm_schema = ["ID", "Player", "Starter", "Ender", "OptimalScore", "Score", "GamePath"]
    __pl_shcema = ["ID", "UserName", "IsAdmin"]
    __pr_search_schema = ["ID", "ScreenName", "MovieTitle", "ReleaseYear", "RoleInMovie"]
    __mv_search_schema = ["ID", "Title", "ReleaseYear"]
    __role_schema = ["Movie", "Actor"]

    # Given Lists of dictionaries and names of those lists
    # returns a json string with all lists included and named as separate attributes
    @staticmethod
    def create_json_list(lsts=[[]], names=[str]):
        json_dict = {}
        for indx, ls in enumerate(lsts):
            json_dict[names[indx]] = ls
        return json.dumps(json_dict, indent=2)

    # Given data, type of data, and a schema, return a dictionary of info
    @staticmethod
    def __create_dict_from_schema(data=(), data_type=str, schema=[str]) -> dict:
        return_dict = {"Type": data_type}
        for indx, value in enumerate(data):
            return_dict[schema[indx]] = value

        return return_dict

    # Given data, type of data, and a schema, return a json string
    @staticmethod
    def __create_json_from_schema(data=(), data_type=str, schema=[str]) -> str:
        return json.dumps(helper.__create_dict_from_schema(data, data_type, schema), indent=2)

    ## Following functions turn SQL query results into dictionaries and JSON strings ##

    @staticmethod
    def create_person_dict(mp=()) -> dict:
        return helper.__create_dict_from_schema(mp, "Person", helper.__pr_schema)

    @staticmethod
    def create_person_json(mp=()) -> str:
       return helper.__create_json_from_schema(mp, "Person", helper.__pr_schema)
    
    @staticmethod
    def create_movie_dict(mv=()) -> dict:
        return helper.__create_dict_from_schema(mv, "Movie", helper.__mv_schema)

    @staticmethod
    def create_movie_json(mv=()) -> str:
        return helper.__create_json_from_schema(mv, "Movie", helper.__mv_schema)

    @staticmethod
    def create_cast_dict(ct=()) -> dict:
        return helper.__create_dict_from_schema(ct, "Cast Member", helper.__ct_schema)
    
    @staticmethod
    def create_movie_json(mv=()) -> str:
        return helper.__create_json_from_schema(mv, "Movie", helper.__mv_schema)

    @staticmethod
    def create_cast_dict(ct=()) -> dict:
        return helper.__create_dict_from_schema(ct, "Cast Member", helper.__ct_schema)

    @staticmethod
    def create_cast_json(ct=()) -> str:
        return helper.__create_json_from_schema(ct, "Cast Member", helper.__ct_schema)

    @staticmethod
    def create_pr_search_dict(pr=()) -> dict:
        return helper.__create_dict_from_schema(pr, "Search Result Person", helper.__pr_search_schema)

    @staticmethod
    def create_pr_search_json(pr=()) -> str:
        return helper.__create_json_from_schema(pr, "Search Result Person", helper.__pr_search_schema)

    @staticmethod
    def create_mv_search_dict(mv=()) -> dict:
        return helper.__create_dict_from_schema(mv, "Search Result Movie", helper.__mv_search_schema)

    @staticmethod
    def create_mv_search_json(mv=()) -> str:
        return helper.__create_json_from_schema(mv, "Search Result Movie", helper.__mv_search_schema)

    @staticmethod
    def create_role_info_dict(mp=()) -> dict:
        return helper.__create_dict_from_schema(mp, "Role", helper.__role_schema)

    @staticmethod
    def create_role_info_json(mp=()) -> str:
       return helper.__create_json_from_schema(mp, "Role", helper.__role_schema)

    @staticmethod
    def create_player_dict(mp=()) -> dict:
        return helper.__create_dict_from_schema(mp, "Player", helper.__pl_shcema)

    @staticmethod
    def create_player_json(mp=()) -> str:
       return helper.__create_json_from_schema(mp, "Player", helper.__pl_shcema)

    @staticmethod
    def create_game_dict(gm=()) -> dict:
        gm = helper.unpickle_game_data(gm)
        return helper.__create_dict_from_schema(gm, "Game", helper.__gm_schema)

    @staticmethod
    def create_game_json(gm=()) -> str:
        gm = helper.unpickle_game_data(gm)
        return helper.__create_json_from_schema(gm, "Game", helper.__gm_schema)

    # Serializes a game integer array
    @staticmethod
    def unpickle_game_data(gm=()) -> tuple:
        lst = list(gm[0:-1]) + [pickle.loads(gm[-1])]
        return tuple(lst)

    # Returns a list of ids from Neo4j nodes
    @staticmethod
    def get_ids_from_nodes(nodes=[]) -> list:
        ids = [node._properties['id'] for node in nodes]
        return ids