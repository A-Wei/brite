import httpx
import os
import json
import math

API_KEY = os.environ.get("API_KEY")
OMDB_BASE_URL = f"http://www.omdbapi.com/?apikey={API_KEY}"


class FetchMovies:
    def __init__(self):
        self.url = OMDB_BASE_URL

    def fetch(self, title):
        movies_resp = httpx.get(self.url + f"&s={self.title}")
        movies_json = json.loads(movies_resp.text)

        total_results = movies_json['totalResults']
        movies_list = movies_json['Search']

        total_pages = math.ceil(int(total_results) / len(movies_list))

        for i in range(2, total_pages):
            m = httpx.get(self.url + f"&page={i}")
            movies_list += json.loads(m.text)['Search']
            i += 1

        return movies_list


if __name__ == "__main__":
    if os.path.isfile("../data/movies_data.json"):
        try:
            with open("../data/movies_data.json", "r") as readfile:
                movies = readfile.read()
                if len(movies) < 100:
                    print("data already downloaded but less than 100 movies")
                else:
                    print("data already downloaded")
        except Exception as e:
            print("error:", e)
    else:
        movies = FetchMovies().fetch(title="Avengers")
        with open('../data/movies_data.json', 'w') as outfile:
            outfile.write(json.dumps(movies, indent=4, sort_keys=True))
