import csv
from functools import reduce
from typing import Generator, List


def _box(movie):
    return int("".join(chr for chr in movie['box_office'] if chr.isdigit()))


def movie_pay(movie):
    """Dada una pelicula, retorna cuanto le paga a cada actor"""
    actors = filter(lambda actor: actor['id'] == movie['id'], load_actors())
    return _box(movie)//len(list(actors))


def actor_movies(actor: str, movies: List) -> List:
    actor_movies = filter(lambda actor2: actor2['actor'] == actor,
                          load_actors())
    movies_id = list(map(lambda movie: movie['id'], actor_movies))
    movies = [movie for movie in movies if movie['id'] in movies_id]
    return movies


def top_movies(actor: str, movies: List) -> List[str]:
    """Dado un actor, retorna las 3 peliculas que mas le pagaron"""
    actor_movies = filter(lambda actor2: actor2['actor'] == actor,
                          load_actors())
    movies_id = list(map(lambda movie: movie['id'], actor_movies))
    movies = [movie for movie in movies if movie['id'] in movies_id]
    pays = list(map(lambda movie: [movie['title'], movie_pay(movie)], movies))
    pays.sort(key=lambda x: x[1], reverse=True)
    pays = [pay[0] for pay in pays]
    return pays[:3]


def load_actors():
    path = "Consultas/Lectura/Database/actors.csv"
    with open(path, "r", encoding="utf-8") as infile:
        csvfile = csv.DictReader(infile, skipinitialspace=True)
        for actor in csvfile:
            yield actor


def actors_count(movies_id: List) -> List[str]:
    """Dada una cantidad de ids de peliculas, retorna una
    lista con los actores ordernados por cantidad de peliculas"""
    actors = list(load_actors())
    actors_in_movies = (movie_actors(id, actors) for id in movies_id)
    total_actors = reduce(lambda x, y: x + y, actors_in_movies)
    total_actors = list(filter(lambda actor: actor != "N/A", total_actors))
    actors = list(set(total_actors.copy()))
    actors = [_actors_count(actor, total_actors) for actor in actors]
    actors.sort(key=lambda x: x[1], reverse=True)
    actors = [actor[0] for actor in actors]
    return actors


def movie_actors(movie_id: int, actors: List) -> List[str]:
    """Dado el id de una pelicula y una lista de actores, retorna una lista con los
    actores que aparecen en ella"""
    actors = [actor['actor'] for actor in actors if actor['id'] == movie_id]
    return actors


def _actors_count(actor: str, total_actors: List) -> List:
    """Dado un actor, retorna cuantas veces se repite en la lista de
    actores totales"""
    return [actor, total_actors.count(actor)]


def actor_earnings(actor: str, movies: List) -> int:
    actor_movies = filter(lambda actor2: actor2['actor'] == actor,
                          load_actors())
    actor_movies_ids = [actor['id'] for actor in actor_movies]
    actor_movies = filter(lambda movie: movie['id'] in actor_movies_ids and
                          movie['box_office'] != "N/A", movies)
    actor_movies_earnings = list(map(lambda movie: movie_pay(movie),
                                     actor_movies))
    if not actor_movies_earnings:
        earnings = 0
    elif len(actor_movies_earnings) > 1:
        earnings = reduce(lambda x, y: x + y, actor_movies_earnings)
    else:
        earnings = actor_movies_earnings[0]
    return [earnings, actor]
