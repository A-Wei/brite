from backend import api, movie
from backend.swagger import swagger

from backend.wsgi import remote, messages


class GetIndexRequest(messages.Message):
    limit = messages.IntegerField(1, default=10)
    page = messages.IntegerField(2, default=1)


class MovieIndexResult(messages.Message):
    imdb_id = messages.StringField(1)
    year = messages.StringField(2)
    type = messages.StringField(3)
    title = messages.StringField(4)
    poster = messages.StringField(5)


class GetIndexResponse(messages.Message):
    movies = messages.MessageField(MovieIndexResult, 1, repeated=True)


@api.endpoint(path="healthcheck", title="Health Check")
class HealthCheck(remote.Service):
    @staticmethod
    def get(self):
        return {"message": "ok"}


@api.endpoint(path="movie", title="Movie API")
class Movie(remote.Service):
    @swagger("Get a list of movies")
    @remote.method(GetIndexRequest, GetIndexResponse)
    def get(self, request):
        limit = request.limit
        page = request.page
        movies = movie.Movie.index(limit, page)

        return GetIndexResponse(
            movies=[
                MovieIndexResult(
                    imdb_id=m.imdb_id,
                    year=m.year,
                    type=m.type,
                    title=m.title,
                    poster=m.poster
                ) for m in movies if m is not None
            ]
        )

