from Consultas.Lectura.reviews_database import (review_processing,
                                                reviews_database)
from typing import Generator, List
from Consultas.decorators import param_checker
import types


@param_checker('best_comments', ['movies', types.GeneratorType], ['n', int])
def best_comments(movies: Generator, n: int) -> Generator:
    movies = map(lambda movie: _best_comments(movie), movies)
    movies = list(movies)
    if n < 0:
        movies.sort(key=lambda x: x[1])
    else:
        movies.sort(key=lambda x: x[1], reverse=True)
    for i in range(abs(n)):
        yield movies[i][0]


def _best_comments(movie: List) -> List:
    """Dado una pelicula, retorna la pelicula y la cantidad de
    comentarios positivos"""
    reviews = list(reviews_database())
    reviews = filter(lambda review: review['id'] == movie['id'], reviews)
    return [movie, count_comments(review_processing(reviews), "positive")]


def count_comments(reviews: Generator, key: str) -> int:
    """Count the ammount of reviews of the type key
    (positive, negative, neutral)"""
    reviews = filter(lambda review: review == key, reviews)
    return len(list(reviews))
