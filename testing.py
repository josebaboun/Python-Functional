import unittest
import csv
from Consultas.actors_filter import *
from Consultas.movies_filter import (filter_by_date, popular_movies,
                                     filter_by_date_test)
from Consultas.reviews_filter import best_comments
from Consultas.take_movie_while import take_movie_while
from Consultas.popular_genre import popular_genre
from Consultas.actors_filter import (popular_actors, highest_paid_actors,
                                     successful_actors)
from Consultas.customexceptions import BadQuerry, WrongInput, MovieError
from consultas import consultas


class Testing(unittest.TestCase):

    def setUp(self):
        path1 = "Consultas/Lectura/Testing/movies.csv"
        path2 = "Consultas/Lectura/Testing/movies2.csv"
        path3 = "Consultas/Lectura/Testing/movies3.csv"
        self.movies1 = self.load_movies(path1)
        self.movies2 = self.load_movies(path2)
        self.movies3 = self.load_movies(path3)

    def load_movies(self, path):
        with open(path, "r", encoding="utf-8") as infile:
            csvfile = csv.DictReader(infile, skipinitialspace=True)
            for movie in csvfile:
                yield(movie)

    def load_output(self, path):
        with open(path, "r", encoding="utf-8") as infile:
            csvfile = csv.DictReader(infile, skipinitialspace=True)
            for movie in csvfile:
                yield(movie)

    def load_output2(self, path):
        with open(path, "r", encoding="utf-8") as infile:
            for line in infile:
                yield line

    def test_filter_by_date(self):
        output = filter_by_date(self.movies2, 2000, False)
        path = "Consultas/Lectura/Testing/outputs/filter_by_date.csv"
        expected_output = self.load_output(path)
        self.assertEqual(list(output), list(expected_output))

    def test_popular_movies(self):
        output = popular_movies(self.movies1, 40, 60)
        path = "Consultas/Lectura/Testing/outputs/popular_movies.csv"
        expected_output = self.load_output(path)
        self.assertEqual(list(output), list(expected_output))

    def test_best_comments(self):
        output = best_comments(self.movies1, 4)
        path = "Consultas/Lectura/Testing/outputs/best_comments.csv"
        expected_output = self.load_output(path)
        self.assertEqual(list(output), list(expected_output))

    def test_take_movie_while1(self):
        output = take_movie_while(self.movies1, 'IMDb', '>', 50)
        path = "Consultas/Lectura/Testing/outputs/take_movie_while_1.csv"
        expected_output = self.load_output(path)
        self.assertEqual(list(output), list(expected_output))

    def test_take_movie_while2(self):
        output = take_movie_while(self.movies1, 'box_office', '>', 200000000)
        path = "Consultas/Lectura/Testing/outputs/take_movie_while_2.csv"
        expected_output = self.load_output(path)
        self.assertEqual(list(output), list(expected_output))

    def test_popular_genre(self):
        expected_output = ['Thiller', 'Comedia', 'Musical', 'Acción']
        output = popular_genre(self.movies1, 'Rotten Tomatoes')
        self.assertEqual(output, expected_output)

    def test_popular_actors(self):
        output = popular_actors(self.movies1, 2, 10, 'Internet Movie Database')
        expected_output = ['Ricardo Schilling', 'Diego Quezada']
        self.assertEqual(output, expected_output)

    def test_highest_paid_actors(self):
        path = "Consultas/Lectura/Database/movies.csv"
        output = highest_paid_actors(self.movies1)
        expected_output = [("['Tomás Rivera', 423079989,"
                            " ['El exorcista', 'Pulp fiction']]")]
        self.assertEqual(output, expected_output)

    def test_successfull_actors(self):
        path = "Consultas/Lectura/Testing/outputs/successful_actors.csv"
        output = successful_actors(self.movies1)
        expected_output = list(self.load_output2(path))
        self.assertEqual(len(output), len(expected_output))

    def test_MovieError(self):
        self.assertRaises(MovieError, filter_by_date, self.movies1, 2000,
                          False)

    def test_BadQuerry(self):
        self.assertRaises(BadQuerry, consultas, "not a querry")

    def test_WrongInput(self):
        self.assertRaises(WrongInput, filter_by_date, self.movies1, "2000",
                          False)


suite = unittest.TestLoader().loadTestsFromTestCase(Testing)
unittest.TextTestRunner().run(suite)
