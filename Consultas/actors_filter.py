from typing import Generator, List
from Consultas.movies_filter import most_popular_movies, succesful_movies
from Consultas.Lectura.actors_database import (load_actors, actors_count,
                                               movie_actors, actor_earnings,
                                               top_movies, actor_movies)
from functools import reduce
from Consultas.decorators import (param_checker, column_checker,
                                  rating_columns_checker)
import types


@param_checker('popular_actors', ['movies', types.GeneratorType],
               ['k_actors', int], ['n_movies', int], ['r_type', str])
def popular_actors(movies: Generator, k_actors: int, n_movies: int,
                   r_type: str = 'All') -> List[str]:
    movies_id = most_popular_movies(movies, n_movies, r_type)
    actors = actors_count(movies_id)
    return actors[:k_actors]


@param_checker('highest_paid_actors', ['movies', types.GeneratorType],
               ['k_actors', int])
def highest_paid_actors(movies: Generator, k_actors: int = 1) -> List[str]:
    movies = column_checker('highest_paid_actors', movies, 'box_office')
    movies = list(movies)
    actors = map(lambda actor: actor['actor'], load_actors())
    actors = list(set(actors))
    actors_earnings = list(map(lambda actor: actor_earnings(actor, movies),
                               actors))
    actors_earnings.sort(key=lambda x: x[1], reverse=True)
    actors = actors_earnings[:k_actors]
    actors = [str([actor[1], actor[0], top_movies(actor[1], movies)])
              for actor in actors]
    return actors


@param_checker('successful_actors', ['movies', types.GeneratorType])
def successful_actors(movies: Generator) -> List[str]:
    movies = rating_columns_checker('successful_actors', movies)
    actors = map(lambda actor: actor['actor'], load_actors())
    actors = list(set(actors))
    actor_movie = [[actor, actor_movies(actor, movies)] for actor in actors]
    actors = filter(lambda actor: succesful_movies(actor[1]), actor_movie)
    actors = [actor[0] for actor in actors]
    return actors
