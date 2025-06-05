from fastapi import APIRouter
from core.game import Game
from core.game.models.game import GameRepoModel, GameInDB
from core.game.models.genre import GenreRepo
from core.game.models.review import ReviewRepo
from ..schemas.game import GameCreateSchema, EditGameSchema, UserReviewCreateSchema, ReviewInAdminPanel

admin_games_router = APIRouter()


@admin_games_router.get("/games/{id}")
async def get_game_by_id(id: int):
    return await GameRepoModel.get_game_by(game_id=id, as_dto=True)


@admin_games_router.get("/games")
async def get_games(page: int = 1):
    page -= 1
    page = 0 if page < 0 else page
    per_page = 12
    return await GameRepoModel.get_games(only_visible=False, as_dto=True)


@admin_games_router.post("/games")
async def create_game(game: GameCreateSchema):
    await Game.create(
        name=game.name,
        description=game.description,
        system_requirements=game.system_requirements,
        current_price=game.current_price,
        images=game.images,
        old_price=game.old_price,
        genre_id_list=game.genre_id_list
    )
    return 'OK'


@admin_games_router.put("/games/{id}")
async def edit_game_by_id(id: int, edited_game: EditGameSchema):
    updates = edited_game.dict(exclude_unset=True)
    game = await Game.get_by(game_id=id)
    await game.update(**updates)
    return updates


@admin_games_router.delete("/games/{id}")
async def delete_game_by_id(id: int):
    game = await Game.get_by(game_id=id)
    await game.delete()
    return 'OK'


@admin_games_router.get("/games/{id}/reviews")
async def get_game_reviews(id: int):
    return await ReviewRepo.get_reviews_by_game_id(id, as_dto=True)


@admin_games_router.post("/games/{id}/reviews", response_model=ReviewInAdminPanel)
async def create_game_review(id: int, review: UserReviewCreateSchema):
    review_instance = await ReviewRepo.create(**{'game_id': id, **review.dict()})
    return ReviewInAdminPanel(
        id=review_instance.id,
        game_id=review_instance.game_id,
        text=review_instance.text,
        customer_name=review_instance.customer_name,
        rating=review_instance.rating,
        date=review_instance.date
    )


@admin_games_router.delete("/games/reviews/{id}")
async def delete_game_review(id: int):
    review = await ReviewRepo.get_review_by_id(review_id=id)
    await review.delete()
    return 'OK'


@admin_games_router.get("/game-genres")
async def get_all_genres():
    return await GenreRepo.get_all()
