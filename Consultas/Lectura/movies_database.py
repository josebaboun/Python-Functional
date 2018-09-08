import csv
from functools import namedtuple
from Consultas.Lectura.actors_database import load_actors
from Consultas.decorators import column_checker


def load_movies():
    path = "Consultas/Lectura/Database/movies.csv"
    with open(path, "r", encoding="utf-8") as infile:
        csvfile = csv.DictReader(infile, skipinitialspace=True)
        for movie in csvfile:
            yield(movie)


def rating_average(movie):
    return [movie, _rating(movie['rating_imdb'], movie['rating_rt'],
                           movie['rating_metacritic'])]


def _rating(imbd, rt, mc):
    return (_imdb(imbd) + _rt(rt) + _mc(mc))//3


def _imdb(rating):
    return int(float(rating.split("/")[0]) * 10)


def _rt(rating):
    return int(rating.strip("%"))


def _mc(rating):
    return int(rating.split("/")[0])


def _box(movie):
    return int("".join(chr for chr in movie['box_office'] if chr.isdigit()))


def rating_filter(movies, r_min, r_max, r_type):
    if r_type == "Internet Movie Database" or r_type == "IMBd":
        movies = column_checker('popular_movies', movies, 'rating_imdb')
        movies = filter(lambda movie: _imdb(movie['rating_imdb']) > r_min
                        and _imdb(movie['rating_imbd']) < r_max, movies)
    elif r_type == "Rotten Tomatoes" or r_type == "RT":
        movies = column_checker('popular_movies', movies, 'rating_rt')
        movies = filter(lambda movie: _rt(movie['rating_rt']) > r_min
                        and _rt(movie['rating_rt']) < r_max, movies)
    elif r_type == "Metacritic" or r_type == "MC":
        movies = column_checker('popular_movies', movies, 'rating_metacritic')
        movies = filter(lambda movie: _mc(movie['rating_metacritic']) > r_min
                        and _mc(movie['rating_metacritic']) < r_max, movies)
    for movie in movies:
        yield movie


def movie_pay(movie):
    """Dada una pelicula, retorna cuanto le paga a cada actor"""
    actors = filter(lambda actor: actor['id'] == movie['id'], load_actors())
    return _box(movie['box_office'])//len(list(actors))
