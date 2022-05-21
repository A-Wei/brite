import os

from backend.database import database
from backend.movie import Movie as MovieSchema

from typing import List

import httpx
import json
import os

from backend.utils import convert_keys

API_KEY = os.environ.get("API_KEY", "")


class MovieHandler:
    @classmethod
    async def index(cls, db: database, limit: int, page_num: int) -> List[MovieSchema]:
        query = """
                SELECT 
                    * 
                FROM movies
                ORDER BY title
            """
        movies = await db.fetch_all(query)

        start = (page_num - 1) * limit
        end = start + limit

        return movies[start:end]

    @classmethod
    async def search(cls, db: database, title: str) -> MovieSchema:
        query = """
            SELECT 
                * 
            FROM movies
            WHERE title LIKE :title
            ORDER BY title
        """

        values = {"title": "%" + title + "%"}
        movies = await database.fetch_all(query=query, values=values)

        return movies

    @classmethod
    async def post(cls, db: database, title: str) -> MovieSchema:
        if not title:
            return {"message": "Missing title"}

    @classmethod
    async def show(cls, db: database, m_id: int) -> MovieSchema:
        query = """
            SELECT * FROM movies WHERE id = :id
        """

        movie = await db.fetch_all(query=query, values={"id": m_id})

        return movie

    @classmethod
    async def delete(cls, db: database, m_id: int):
        query = """
            DELETE FROM movies WHERE id = :id
        """

        row = await db.execute(query=query, values={"id": m_id})

        if row:
            return {
                "success": True,
                "message": "Movie is deleted"
            }
        else:
            return {
                "success": False,
                "message": f"Can't find movie with id {m_id}"
            }

    @classmethod
    async def fetch_movie(cls, db: database, title: str):
        search_movie = httpx.get(f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}")

        movie_json = json.loads(search_movie.text)

        if movie_json['Response'] == 'True':
            m = convert_keys(movie_json)

            query = """
                    INSERT OR IGNORE INTO movies (
                        imdb_id, year, type, title, poster, rated, released, run_time, genre, director, writer,
                        actors, plot, language, country, awards, poster, ratings, meta_score, imdb_rating,
                        imdb_votes, response
                    )
                    VALUES (
                        :imdb_id, :year, :type, :title, :poster, :rated, :released, :run_time, :genre, :director, :writer,
                        :actors, :plot, :language, :country, :awards, :poster, :ratings, :meta_score, :imdb_rating,
                        :imdb_votes, :response
                    )
                """
            if m['ratings']:
                m['ratings'] = str(m['ratings'])

            row = await database.execute(query=query, values=m)

            if row:
                return {
                    "success": True,
                    "message": f"{title} added",
                    "data": await MovieHandler.show(db, row)
                }
            else:
                return {
                    "success": False,
                    "message": f"{title} add failed, try search it first",
                    "data": await MovieHandler.search(db, title)
                }
        else:
            return {"message": f"Did not find {title} in omdbapi."}
