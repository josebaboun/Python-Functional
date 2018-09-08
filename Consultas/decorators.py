from Consultas.customexceptions import WrongInput, MovieError
from functools import wraps
from itertools import tee


def param_checker(name, *params):
    """la funcion recibe una lista con el nombre de la variable y su tipo y
    checkea que sea instancia del tipo"""
    def _param_checker(f):
        def param_wrapper(*args, **kwargs):
            for i in range(len(args)):
                if not isinstance(args[i], params[i][1]):
                    raise WrongInput(name, args[i], params[i][0])
            return f(*args, **kwargs)
        return param_wrapper
    return _param_checker


def column_checker(name, movies, column):
    """No es decorador, pero tiene un funcionamiento parecido. por eso va en
    este archivo"""
    movies, check = tee(movies)
    for movie in check:
        if movie[column] == "N/A":
            title = movie['title']
            raise MovieError(str(name), str(title), str(column))
    return movies


def rating_columns_checker(name, movies):
    movies = column_checker(name, movies, 'rating_rt')
    movies = column_checker(name, movies, 'rating_imdb')
    movies = column_checker(name, movies, 'rating_metacritic')
    return movies
