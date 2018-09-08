from Consultas.Lectura.ReviewsDatabase.remove_bot import remove_bot_reviews
from Consultas.Lectura.ReviewsDatabase.remove_tags import remove_tags
from Consultas.Lectura.ReviewsDatabase.review_processing import (check_review,
                                                                 clean_reviews)
import csv


def load_reviews():
    path = "Consultas/Lectura/Database/reviews.csv"
    with open(path, "r", encoding="utf-8") as infile:
        csvfile = csv.DictReader(infile, skipinitialspace=True)
        for review in csvfile:
            yield review


def load_vocabulary():
    path = "Consultas/Lectura/Database/vocabulary.txt"
    with open(path, "r", encoding="utf-8") as infile:
        for word in infile:
            word = word.strip("\n").strip()
            yield word


def load_words():
    with open("Consultas/Lectura/Database/words.csv",
              "r", encoding="utf-8") as infile:
        words = map(lambda word: word.strip("\n").split(","), infile)
        words = filter(lambda word: word[0] != "id", words)
        for word in words:
            word = [data.strip() for data in word]
            yield word


def reviews_database():
    reviews = remove_tags(load_reviews())
    reviews = clean_reviews(reviews)
    reviews = remove_bot_reviews(reviews, list(load_vocabulary()))
    for review in reviews:
        yield review


def review_processing(reviews):
    reviews = clean_reviews(reviews)
    words = list(load_words())
    for review in reviews:
        yield check_review(review, words)
