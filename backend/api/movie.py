from backend import api, movie
from backend.swagger import swagger

from backend.wsgi import remote, messages, message_types
from backend.oauth2 import oauth2


class MovieIndexResult(messages.Message):
    imdb_id = messages.StringField(1)
    year = messages.StringField(2)
    type = messages.StringField(3)
    title = messages.StringField(4)
    poster = messages.StringField(5)


class GetIndexRequest(messages.Message):
    limit = messages.IntegerField(1, default=10)
    page = messages.IntegerField(2, default=1)


class GetIndexResponse(messages.Message):
    movies = messages.MessageField(MovieIndexResult, 1, repeated=True)


class GetByTitleRequest(messages.Message):
    title = messages.StringField(1)


class RemoveMovieRequest(messages.Message):
    id = messages.IntegerField(1)


class AddMovieRequest(messages.Message):
    title = messages.StringField(1)
    add_movie = messages.BooleanField(2)


class MovieResponse(messages.Message):
    imdb_id = messages.StringField(1)
    year = messages.StringField(2)
    type = messages.StringField(3)
    title = messages.StringField(4)
    poster = messages.StringField(5)


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

    @swagger("Get a movie by title")
    @remote.method(GetByTitleRequest, MovieResponse)
    def search(self, request):
        m = movie.Movie.search(request.title)

        return MovieResponse(
            imdb_id=m.imdb_id,
            year=m.year,
            type=m.type,
            title=m.title,
            poster=m.poster
        )

    @swagger("Add a movie by title")
    @remote.method(AddMovieRequest, MovieResponse)
    def add(self, request):
        if request.add_movie:
            m = movie.Movie.search_in_omdbapi(request.title)

            if m:
                movie.Movie.create(m)

                return MovieResponse(
                    imdb_id=m.imdb_id,
                    year=m.year,
                    type=m.type,
                    title=m.title,
                    poster=m.poster
                )

    @swagger("Remove a movie by id")
    @oauth2.required()
    @remote.method(RemoveMovieRequest, message_types.VoidMessage)
    def remove(self, request):
        movie.Movie.delete(id=request.id)

        return message_types.VoidMessage
