import json
import os
from backend.movie import Movie


def populate_data():
    db_data = Movie.query().count()

    if db_data < 100:
        file_path = os.path.realpath("backend/data/movies_data.json")
        with open(file_path, "r") as readfile:
            movies_list = readfile.read()

        movies_json = json.loads(movies_list)
        for m in movies_json:
            Movie.create(m)
