from imdb_game_api import imdb_game_api
import json

api = imdb_game_api("key.txt")

# movie_query = api.get_movie_by_name('Parasite')
# with open('test_queries/mv.json', 'w') as outfile:
#     outfile.write(movie_query)

# movie_query = api.get_movie_by_id('Forrest Gump')
# with open('test_queries/mv_id.json', 'w') as outfile:
#     outfile.write(movie_query)

person_query = api.get_person_by_name('Michelle Williams')
with open('test_queries/pr.json', 'w') as outfile:
    outfile.write(person_query)

# person_query = api.get_person_by_id('Tom Hanks')
# with open('test_queries/mp_id.json', 'w') as outfile:
#     outfile.write(person_query)


autocomplete = api.get_autocomplete('Sar')
with open('test_queries/autocomplete.json', 'w') as outfile:
    outfile.write(autocomplete)
# print("\n\n ############## \n\n")
# search = api.get_search('Sar')
# with open('test_queries/search.json', 'w') as outfile:
#     outfile.write(search)

api.destructor()