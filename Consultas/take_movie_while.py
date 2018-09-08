from typing import Generator
from Consultas.Lectura.movies_database import _imdb, _rt, _mc, _box
from Consultas.decorators import param_checker, column_checker
from Consultas.customexceptions import MovieError
import types


@param_checker('take_movie_while', ['movies', types.GeneratorType],
               ['column', str], ['symbol', str], ['value', int])
def take_movie_while(movies: Generator, column: str,
                     symbol: str, value: int) -> Generator:
    movies = check_na(column, movies)
    if column == "RT" or column == "Rotten Tomatoes":
        movies = tmw_rt(movies, symbol, value)
    elif column == "IMDb" or column == "Internet Movie Database":
        movies = tmw_imbd(movies, symbol, value)
    elif column == "Metacritic" or column == "MC":
        movies = tmw_mc(movies, symbol, value)
    elif column == "date":
        movies = tmw_date(movies, symbol, value)
    elif column == "box_office":
        movies = tmw_box(movies, symbol, value)
    for movie in movies:
        yield movie


def check_na(column, movies):
    if column == "RT" or column == "Rotten Tomatoes":
        movies = column_checker('take_movie_while', movies, 'rating_rt')
    elif column == "IMDb" or column == "Internet Movie Database":
        movies = column_checker('take_movie_while', movies, 'rating_imdb')
    elif column == "Metacritic" or column == "MC":
        movies = column_checker('take_movie_while', movies,
                                'rating_metacritic')
    elif column == "date":
        movies = column_checker('take_movie_while', movies, 'date')
    elif column == "box_office":
        movies = column_checker('take_movie_while', movies, 'box_office')
    return movies


def tmw_rt(movies: Generator, symbol: str, value: int) -> Generator:
    for movie in movies:
        if break_cond(_rt(movie['rating_rt']), value, symbol):
            break
        yield movie


def tmw_imbd(movies: Generator, symbol: str, value: int) -> Generator:
    for movie in movies:
        if not break_cond(_imdb(movie['rating_imdb']), value, symbol):
            break
        yield movie


def tmw_mc(movies: Generator, symbol: str, value: int) -> Generator:
    for movie in movies:
        if not break_cond(_mc(movie['rating_metacritic']), value, symbol):
            break
        yield movie


def tmw_date(movies: Generator, symbol: str, value: int) -> Generator:
    for movie in movies:
        if not break_cond(int(movie['date']), value, symbol):
            break
        yield movie


def tmw_box(movies: Generator, symbol: str, value: int) -> Generator:
    for movie in movies:
        if not break_cond(_box(movie), value, symbol):
            break
        yield movie


def break_cond(value1: int, value2: int, symbol: str) -> bool:
    if symbol == ">":
        return value1 > value2
    if symbol == "<":
        return value1 < value2
    if symbol == "!=":
        return value1 != value2
    if symbol == "==":
        return value1 == value2
