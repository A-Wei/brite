from sqlalchemy import Column, Integer, String, Text, Float, Boolean
from .database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    year = Column(String, nullable=False)
    rated = Column(String(25))
    released = Column(String(25))
    run_time = Column(String(25))
    genre = Column(String)
    director = Column(String)
    writer = Column(String)
    actors = Column(String)
    plot = Column(Text)
    language = Column(String)
    country = Column(String)
    awards = Column(String)
    poster = Column(String(100), nullable=False)
    ratings = Column(Text)
    meta_score = Column(String)
    imdb_rating = Column(Float)
    imdb_votes = Column(Integer)
    imdb_id = Column(String, nullable=False, unique=True)
    type = Column(String, nullable=False)
    total_seasons = Column(Integer)
    response = Column(Boolean)
