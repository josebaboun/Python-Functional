from typing import Generator, List
import types
from Consultas.decorators import (param_checker, column_checker,
                                  rating_columns_checker)
from Consultas.Lectura.movies_database import (rating_average, rating_filter,
                                               _rating, _mc, _rt, _imdb)


@param_checker('filer_by_date', ['movies', types.GeneratorType],
               ['date', int], ['lower', bool])
def filter_by_date(movies: Generator,
                   date: int, lower: bool = True) -> Generator:
    movies = column_checker('filter_by_date', movies, 'date')
    if lower:
        movies = filter(lambda movie: int(movie['date']) < date, movies)
    else:
        movies = filter(lambda movie: int(movie['date']) > date, movies)
    for movie in movies:
        yield movie


@param_checker('popular_movies', ['movies', types.GeneratorType],
               ['r_min', int], ['r_max', int], ['r_type', str])
def popular_movies(movies: Generator, r_min: int, r_max: int,
                   r_type: str = "All") -> Generator:
    if r_type == "All":
        movies = rating_columns_checker('popular_movies', movies)
        movies = map(lambda movie: rating_average(movie), movies)
        movies = filter(lambda movie: movie[1] > r_min and movie[1] < r_max,
                        movies)
        movies = (movie[0] for movie in movies)
    else:
        movies = rating_filter(movies, r_min, r_max, r_type)
    for movie in movies:
        yield movie


def most_popular_movies(movies: Generator, n_movies: int,
                        r_type: str = 'All') -> List[int]:
    """Retorna una lista con ids de las n peliculas mas
    populares según el tipo de rating"""
    movies_rating = list(_movies_rating(movies, r_type))
    movies_rating.sort(key=lambda x: x[1], reverse=True)
    movies = [movie[0] for movie in movies_rating]
    return movies[:n_movies]


def _movies_rating(movies: Generator, r_type: str) -> Generator:
    if r_type == "All":
        movies = rating_columns_checker('popular_actors', movies)
        movies = map(lambda movie: [movie['id'], _rating(movie['rating_imdb'],
                     movie['rating_rt'], movie['rating_metacritic'])], movies)
    if r_type == "Rotten Tomatoes" or r_type == "RT":
        movies = column_checker('popular_actors', movies, 'rating_rt')
        movies = map(lambda movie: [movie['id'], _rt(movie['rating_rt'])],
                     movies)
    if r_type == "Internet Movie Database" or r_type == "IMDb":
        movies = column_checker('popular_actors', movies, 'rating_imdb')
        movies = map(lambda movie: [movie['id'], _imdb(movie['rating_imdb'])],
                     movies)
    if r_type == "Metacritic" or r_type == "MC":
        movies = column_checker('popular_actors', movies, 'rating_metacritic')
        movies = map(lambda movie: [movie['id'],
                     _mc(movie['rating_metacritic'])], movies)
    for movie in movies:
        yield movie


def succesful_movies(movies: List):
    for movie in movies:
        cond1 = _rt(movie['rating_rt']) < 50
        cond2 = _imdb(movie['rating_imdb']) < 50
        cond3 = _mc(movie['rating_metacritic']) < 50
        if cond1 or cond2 or cond3:
            return False
    return True


# Se usa en testing, ya que solo chequeaba el decorador de la funcion cuando
# se trata de levantar un error
def filter_by_date_test(movies: Generator,
                        date: int, lower: bool = True) -> Generator:
    movies = column_checker('filter_by_date', movies, 'date')
    movies = filter(lambda movie: movie['date'] != "N/A", movies)
    if lower:
        movies = filter(lambda movie: int(movie['date']) < date, movies)
    else:
        movies = filter(lambda movie: int(movie['date']) > date, movies)
    for movie in movies:
        yield movie
