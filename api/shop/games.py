from fastapi import APIRouter

from api.schemas.shop.game import GameOnSale
from core.game.dto import Genre
from core.game.models.game import GameRepoModel
from core.game.models.genre import GenreRepo, GenreModel
from core.game.models.review import ReviewRepo

shop_router = APIRouter(prefix="")


@shop_router.get("/games/total")
async def get_games_total(genre_id: int = None):
    return {'total': await GameRepoModel.get_games_total(genre_id)}


@shop_router.get("/games/{id}")
async def get_game_by_id(id: int):
    game = await GameRepoModel.get_game_by(game_id=id, as_dto=True)
    return game.dict(exclude={"key_category_id"})


@shop_router.get("/games")
async def get_games(page: int = 1, name: str = None, genre_id: int = None):
    page -= 1
    page = 0 if page < 0 else page
    per_page = 12
    games = await GameRepoModel.get_games(per_page, offset=page * per_page, name=name, genre_id=genre_id, as_dto=True)
    return [
        GameOnSale(
            id=game.id,
            name=game.name,
            description=game.description,
            system_requirements=game.system_requirements,
            rating=game.rating,
            current_price=game.current_price,
            images=game.images,
            old_price=game.old_price,
            genres=[Genre(id=g.id, name=g.name) for g in game.genres]
        )
        for game in games
    ]


@shop_router.get("/bestsellers")
async def get_bestsellers():
    games = await GameRepoModel.get_games(count=10, min_rating=5, as_dto=True)
    return [
        GameOnSale(
            id=game.id,
            name=game.name,
            description=game.description,
            system_requirements=game.system_requirements,
            rating=game.rating,
            current_price=game.current_price,
            images=game.images,
            old_price=game.old_price,
            genres=[Genre(id=g.id, name=g.name) for g in game.genres]
        )
        for game in games
    ]


@shop_router.get("/games/{id}/reviews")
async def get_game_reviews(id: int):
    return await ReviewRepo.get_reviews_by_game_id(id, as_dto=True)


@shop_router.get("/genres")
async def get_all_genres():
    return await GenreRepo.get_all()
