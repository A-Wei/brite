from fastapi import FastAPI
from backend.database import database, Base, engine
from backend.movie import Movie as MovieSchema
from backend.utils import create_data
from typing import List, Dict
from backend.handlers.movie_handler import MovieHandler


app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.on_event("startup")
async def startup():
    await database.connect()
    query = """SELECT * FROM movies"""
    result = await database.fetch_all(query)
    if not result:
        await create_data(database)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def health_check():
    return {"message": "ok"}


@app.get("/movies/")
async def read_movie(limit: int = 10, page_num: int = 1) -> List[MovieSchema]:
    movies = await MovieHandler.index(db=database, limit=limit, page_num=page_num)

    response = {
        "data": movies,
        "count": len(movies)
    }

    return response


@app.get("/movies/search/")
async def read_movie(title: str) -> MovieSchema:
    movie = await MovieHandler.search(db=database, title=title)

    response = {
        "data": movie,
        "count": len(movie)
    }

    return response


@app.post("/movies/")
async def add_movie(title: str) -> MovieSchema:
    response = await MovieHandler.fetch_movie(db=database, title=title)

    return response


@app.delete("/movies/{m_id}")
async def delete_movie(m_id: int) -> Dict:
    response = await MovieHandler.delete(db=database, m_id=m_id)

    return response
