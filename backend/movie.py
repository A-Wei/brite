import re
import httpx
import json

from google.cloud import ndb
from enum import Enum

from backend import error


class NotFound(error.Error):
    pass


class KeyNameEnum(str, Enum):
    DVD = "dvd"
    imdbID = "imdb_id"


class Ratings(ndb.Model):
    source = ndb.TextProperty(indexed=False)
    value = ndb.TextProperty(indexed=False)


class Movie(ndb.Model):
    imdb_id = ndb.StringProperty(required=True)
    year = ndb.TextProperty(required=True)
    type = ndb.TextProperty(required=True)
    title = ndb.StringProperty(required=True)
    poster = ndb.TextProperty(required=True)
    rated = ndb.TextProperty()
    released = ndb.TextProperty()
    runtime = ndb.TextProperty()
    genre = ndb.TextProperty()
    director = ndb.TextProperty()
    writer = ndb.TextProperty()
    actors = ndb.TextProperty()
    plot = ndb.TextProperty()
    language = ndb.TextProperty()
    country = ndb.TextProperty()
    awards = ndb.TextProperty()
    poster = ndb.TextProperty()
    ratings = ndb.StructuredProperty(Ratings, repeated=True)
    metascore = ndb.TextProperty()
    imdb_rating = ndb.TextProperty()
    imdb_votes = ndb.TextProperty()
    total_seasons = ndb.TextProperty()
    dvd = ndb.TextProperty()
    box_office = ndb.TextProperty()
    production = ndb.TextProperty()
    website = ndb.TextProperty()
    response = ndb.BooleanProperty()


    @classmethod
    def create(cls, attr={}):
        attr_snake = cls.convert_keys(attr)
        imdb_id = attr_snake["imdb_id"]
        movie = cls.get_by_imdb_id(imdb_id)

        if movie:
            return movie
        else:
            entity = cls(**attr_snake)
            entity.put()
            return entity

    @classmethod
    def index(cls, limit, page):
        query = cls.query().order(cls.title)

        movies = query.fetch(limit=limit, offset=limit*(page-1))

        return movies

    @classmethod
    def get(cls, id):
        entity = ndb.Key(urlsafe=id).get()

        if entity is None or not isinstance(entity, cls):
            raise NotFound("No movie found with id: %s" % id)

        return entity

    @classmethod
    def delete(cls, id):
        entity = ndb.Key(urlsafe=id).get()

        if entity is None or not isinstance(entity, cls):
            raise NotFound("No movie found with id: %s" % id)
        else:
            entity.key.delete()

        return {
            "message": "Movie is deleted"
        }

    @classmethod
    def get_by_imdb_id(cls, imdb_id):
        query = cls.query().filter(cls.imdb_id == imdb_id)

        return query.fetch()

    @classmethod
    def post(cls, title):
        movie = cls.search_in_omdbapi(title)

        return movie

    @classmethod
    def search_in_omdbapi(cls, title):

        resp = httpx.get(f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}")

        movie_json = json.loads(resp.text)

        if movie_json['Response'] == 'True':
            movie = cls.create(movie_json)

        return movie

    @classmethod
    def search(cls, title):
        query = cls.query()
        if title is not None:
            query = query.filter(cls.title == title)

        return query.fetch(limit=1)

    @classmethod
    def convert_keys(cls, dict_data):
        new_dict = {}
        pattern = re.compile(r'(?<!^)(?=[A-Z])')

        for k, v in dict_data.items():
            if k in [e.name for e in KeyNameEnum]:
                new_dict[KeyNameEnum[k].value] = v
            elif k == "Ratings":
                ratings_list = []
                for i in v:
                    ratings_dict = {}
                    for k2, v2 in i.items():
                        ratings_dict[pattern.sub('_', k2).lower()] = v2
                    ratings_list.append(ratings_dict)
                new_dict[pattern.sub('_', k).lower()] = ratings_list
            elif k == "Response":
                new_dict[pattern.sub('_', k).lower()] = bool(v)
            else:
                new_dict[pattern.sub('_', k).lower()] = v

        return new_dict

    @property
    def id(self):
        return self.key.urlsafe().decode("utf-8")

