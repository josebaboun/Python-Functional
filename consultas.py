from Consultas.Lectura.movies_database import load_movies
from Consultas.movies_filter import filter_by_date, popular_movies
from Consultas.reviews_filter import best_comments
from Consultas.take_movie_while import take_movie_while
from Consultas.popular_genre import popular_genre
from Consultas.actors_filter import (popular_actors, highest_paid_actors,
                                     successful_actors)
from Consultas.customexceptions import BadQuerry, WrongInput, MovieError


def unpack(queries):
    if len(queries) == 1:
        return consultas(queries[0])
    else:
        return consultas(queries[0], unpack(queries[1]), *queries[2:])


def consultas(name, *args):
    if name == "load_database":
        return load_movies()
    if name == "filter_by_date":
        return filter_by_date(*args)
    if name == "popular_movie":
        return popular_movies(*args)
    if name == "best_comments":
        return best_comments(*args)
    if name == "take_movie_while":
        return take_movie_while(*args)
    if name == "popular_genre":
        return popular_genre(*args)
    if name == "popular_actors":
        return popular_actors(*args)
    if name == "highest_paid_actors":
        return highest_paid_actors(*args)
    if name == "successful_actors":
        return successful_actors(*args)
    else:
        raise BadQuerry(name)
