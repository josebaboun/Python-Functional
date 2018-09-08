import csv


def load_genres():
    path = "Consultas/Lectura/Database/genres.csv"
    with open(path, "r", encoding="utf-8") as infile:
        csvfile = csv.DictReader(infile, skipinitialspace=True)
        for genre in csvfile:
            yield genre
