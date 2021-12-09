from imdb_game_api import imdb_game_api
import json

api = imdb_game_api("key.txt")

# movie_query = api.get_movie_by_name('Parasite')
# with open('test_queries/mv.json', 'w') as outfile:
#     outfile.write(movie_query)

# movie_query = api.get_movie_by_id(352699)
# with open('test_queries/mv_id.json', 'w') as outfile:
#     outfile.write(movie_query)

# person_query = api.get_person_by_name('Michael Gambon')
# with open('test_queries/pr.json', 'w') as outfile:
#     outfile.write(person_query)

# person_query = api.get_person_by_id(158)
# with open('test_queries/mp_id.json', 'w') as outfile:
#     outfile.write(person_query)

# autocomplete = api.get_autocomplete('Sar')
# with open('test_queries/autocomplete.json', 'w') as outfile:
#     outfile.write(autocomplete)

# search = api.get_search('Gambon')
# with open('test_queries/search.json', 'w') as outfile:
#     outfile.write(search)

# movies = api.get_movies_by_person(2091)
# with open('test_queries/m_gambon_movies_person.json', 'w') as outfile:
#     outfile.write(movies)

# movies = api.get_movies_by_actor(158)
# with open('test_queries/t_hanks_movies_actor.json', 'w') as outfile:
#     outfile.write(movies)

# people = api.get_actors_by_movie(432283)
# with open('test_queries/fmf_actors.json', 'w') as outfile:
#     outfile.write(people)

# people = api.get_people_by_movie(432283)
# with open('test_queries/fmf_people.json', 'w') as outfile:
#     outfile.write(people)

# api.get_movies_by_actor(114)  # Steve Buscemi
# print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
# api.get_actors_by_movie(198781)  # Monsters Inc.
# print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
# api.get_movies_by_actor(422)  # John Goodman
# print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
# api.get_actors_by_movie(190590) # O Brother, Where Art Thou
# print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
# api.get_movies_by_actor(123) # George Clooney
# print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
# api.get_actors_by_movie(432283) # Fantastic Mr. Fox
# print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
# api.get_person_by_id(5403) # Jason Schwartzman

# game_path = [114, # Steve Buscemi
#              198781, # Monsters Inc.
#              422, # John Goodman
#              190590, # O Brother, Where Art Thou
#              123, # George Clooney
#              432283, # Fantastic Mr. Fox
#              5403] # Jason Schwartzman

api.destructor()