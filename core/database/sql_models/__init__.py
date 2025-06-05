from .game import GameSqlModel, ReviewSqlModel, GenreSqlModel, PreviewImageSqlModel
from .key import KeyCategorySqlModel, SteamKeySqlModel
from .user import UserSqlModel, AuthTokenSqlModel
from .order import OrderSqlModel, OrderItemSqlModel


MODEL_REGISTRY = [
    GameSqlModel,
    ReviewSqlModel,
    GenreSqlModel,
    PreviewImageSqlModel,
    KeyCategorySqlModel,
    SteamKeySqlModel,
    UserSqlModel,
    AuthTokenSqlModel,
    OrderSqlModel,
    OrderItemSqlModel,
]
