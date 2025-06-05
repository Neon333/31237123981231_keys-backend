from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from ... import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Date, SmallInteger, Boolean, func

GameGenrePivotTable = Table(  # Жанры
    "game_genre",
    BaseModel.metadata,
    Column("game_id", Integer, ForeignKey("games.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True),
)


class ReviewSqlModel(BaseModel):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)

    customer_name = Column(String(128))
    text = Column(String(1024))
    rating = Column(SmallInteger, default=5)
    date = Column(Date)

    game_id = Column(Integer, ForeignKey('games.id'))
    game = relationship("GameSqlModel", back_populates="reviews")


class PreviewImageSqlModel(BaseModel):
    __tablename__ = "preview_images"

    id = Column(Integer, primary_key=True)
    path = Column(String(255))
    filename = Column(String(255))

    game_id = Column(Integer, ForeignKey('games.id'))
    game = relationship("GameSqlModel", back_populates="images")


class GenreSqlModel(BaseModel):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    games = relationship(
        "GameSqlModel",
        secondary=GameGenrePivotTable,
        back_populates="genres"
    )


class GameSqlModel(BaseModel):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    alias = Column(String(255))
    description = Column(String(8192))
    visible = Column(Boolean, default=True)
    system_requirements = Column(String(1024))
    current_price = Column(Integer)
    old_price = Column(Integer)
    key_category_id = Column(Integer, ForeignKey('key_categories.id'), nullable=True)
    key_category = relationship("KeyCategorySqlModel")
    genres = relationship(
        "GenreSqlModel",
        secondary=GameGenrePivotTable,
        back_populates="games"
    )
    images = relationship("PreviewImageSqlModel", back_populates="game")
    reviews = relationship("ReviewSqlModel", back_populates="game")

    # rating: int = 5
