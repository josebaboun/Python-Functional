from typing import Generator, List
from functools import reduce
from Consultas.Lectura.genres_database import load_genres
from Consultas.Lectura.movies_database import _rating, _imdb, _rt, _mc
from Consultas.decorators import param_checker, rating_columns_checker
import itertools
import types


@param_checker('popular_genre', ['movies', types.GeneratorType],
               ['r_type', str])
def popular_genre(movies: Generator, r_type: str="All") -> List[str]:
    """se quitan los generos N/A, de lo contrario no se podria ejecutar la
    funcion nunca en caso de existir uno, y en el caso de no existir
    no pasaria nada"""
    movies = rating_columns_checker('popular_genre', movies)
    movies = list(movies)
    genres = list({line['genre'] for line in load_genres() if
                   line['genre'] != 'N/A'})
    genre_rating = [map_ratings(genre, r_type, movies) for genre in genres]
    genre_rating.sort(key=lambda x: x[1], reverse=True)
    genres = (genre[0] for genre in genre_rating)
    return list(genres)[:4]


def map_ratings(genre: str, r_type: str, movies: Generator) -> List[int]:
    movies = filter_genre(genre, movies)
    if r_type == 'All':
        movies = map(lambda movie: _rating(movie['rating_imdb'],
                     movie['rating_rt'], movie['rating_metacritic']),
                     movies)
    if r_type == 'Rotten Tomatoes' or r_type == 'RT':
        movies = map(lambda movie: _rt(movie['rating_rt']), movies)
    if r_type == "Internet Movie Database" or r_type == "IMDb":
        movies = map(lambda movie: _imdb(movie['rating_imdb']), movies)
    if r_type == "Metacritic" or r_type == "MC":
        movies = map(lambda movie: _mc(movie['rating_metacritic']), movies)
    lenght, movies = itertools.tee(movies, 2)
    movies = map(lambda movie: int(movie//1), movies)
    rating_avg = (reduce(lambda x, y: x + y, movies))//len(list(lenght))
    return [genre, rating_avg]


def filter_genre(genre: str, movies: Generator) -> Generator:
    """Retorna un generador con las peliculas de un genero"""
    genres = load_genres()
    genres = filter(lambda genre2: genre2['genre'] == genre, genres)
    movies_id = [genre['id'] for genre in genres]
    movies = filter(lambda movie: movie['id'] in movies_id, movies)
    for movie in movies:
        yield movie
