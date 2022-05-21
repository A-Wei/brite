from backend import test, movie
from unittest.mock import patch


class TestUser(test.TestCase):

    def test_create(self):
        attr = {
            "imdbID": "tt1234567",
            "Year": "2000-2001",
            "Type": "movie",
            "Title": "A great movie",
            "Poster": "https://m.media-amazon.com/images/M/MV",
            "Ratings": [
                {
                    "Source": "s1",
                    "Value": "v1"
                },
                {
                    "Source": "s2",
                    "Value": "v2"
                }
            ]
        }
        obj = movie.Movie.create(attr=attr)
        ratings = [
            movie.Ratings(
                source=attr["Ratings"][0]["Source"],
                value=attr["Ratings"][0]["Value"]
            ),
            movie.Ratings(
                source=attr["Ratings"][1]["Source"],
                value=attr["Ratings"][1]["Value"]
            )
        ]

        self.assertEqual(obj, movie.Movie.get(obj.id))
        self.assertTrue(obj.imdb_id == "tt1234567")
        self.assertTrue(obj.year == "2000-2001")
        self.assertTrue(obj.type == "movie")
        self.assertTrue(obj.ratings == ratings)

    def test_search(self):
        attr = {
            "imdbID": "tt1234567",
            "Year": "2000-2001",
            "Type": "movie",
            "Title": "A great movie",
            "Poster": "https://m.media-amazon.com/images/M/MV"
        }
        obj = movie.Movie.create(attr=attr)
        searched_obj = movie.Movie.search(title="A great movie")[0]
        self.assertEqual(obj, searched_obj)

    def test_index(self):
        attr1 = {
            "imdbID": "tt1234567",
            "Year": "2000-2001",
            "Type": "movie",
            "Title": "B movie",
            "Poster": "https://m.media-amazon.com/images/M/MV"
        }
        attr2 = {
            "imdbID": "tt7654321",
            "Year": "2000-2001",
            "Type": "movie",
            "Title": "A movie",
            "Poster": "https://m.media-amazon.com/images/M/MV"
        }
        movie.Movie.create(attr=attr1)
        movie.Movie.create(attr=attr2)

        obj = movie.Movie.index(limit=1, page=2)

        self.assertEqual(len(obj), 1)
        self.assertTrue(obj[0].title == "B movie")

        # Test for index sort on "title"
        obj = movie.Movie.index()
        self.assertTrue(len(obj), 2)
        self.assertTrue(obj[0].title == attr2["Title"])
        self.assertTrue(obj[1].title == attr1["Title"])

    @patch("backend.movie.httpx.get")
    def test_post(self, mocked_get):
        movie_title = "Superman"
        mocked_get.return_value.text = '{"Title":"Superman","Year":"1978","Rated":"PG","Released":"15 Dec 1978","Runtime":"143 min","Genre":"Action, Adventure, Sci-Fi","Director":"Richard Donner","Writer":"Jerry Siegel, Joe Shuster, Mario Puzo","Actors":"Christopher Reeve, Margot Kidder, Gene Hackman","Plot":"An alien orphan is sent from his dying planet to Earth, where he grows up to become his adoptive home\'s first and greatest superhero.","Language":"English","Country":"United States, United Kingdom, Canada","Awards":"Nominated for 3 Oscars. 17 wins & 23 nominations total","Poster":"https://m.media-amazon.com/images/M/MV5BMzA0YWMwMTUtMTVhNC00NjRkLWE2ZTgtOWEzNjJhYzNiMTlkXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie Database","Value":"7.4/10"},{"Source":"Rotten Tomatoes","Value":"94%"},{"Source":"Metacritic","Value":"81/100"}],"Metascore":"81","imdbRating":"7.4","imdbVotes":"171,767","imdbID":"tt0078346","Type":"movie","DVD":"01 May 2001","BoxOffice":"$134,478,449","Production":"N/A","Website":"N/A","Response":"True"}'

        movie.Movie.post(title=movie_title)

        obj = movie.Movie.search(title=movie_title)

        self.assertEqual(1, len(obj))

    def test_delete(self):
        attr = {
            "imdbID": "tt1234567",
            "Year": "2000-2001",
            "Type": "movie",
            "Title": "C movie",
            "Poster": "https://m.media-amazon.com/images/M/MV"
        }
        obj = movie.Movie.create(attr=attr)
        resp = movie.Movie.delete(obj.id)

        expected_response = {
            "message": "Movie is deleted"
        }

        self.assertEqual(resp, expected_response)
