from fastapi import APIRouter

from api.schemas.key_category import CreateKeyCategorySchema, KeyCategorySchema, AppendKeysSchema
from core.game.key_category import KeyCategory

admin_keys_router = APIRouter()


@admin_keys_router.get("/key-categories")
async def get_key_categories():
    return [
        KeyCategorySchema(
            id=c.id,
            name=c.name,
            count_keys=c.count_keys
        )
        for c in await KeyCategory.get_all()
    ]


@admin_keys_router.post("/key-categories", response_model=KeyCategorySchema)
async def create_key_category(category: CreateKeyCategorySchema):
    new_category = await KeyCategory.create(category.name)
    return KeyCategorySchema(id=new_category.id, name=new_category.name, count_keys=new_category.count_keys)


@admin_keys_router.put("/key-categories/{id}/keys")
async def append_keys(id: int, new_keys: AppendKeysSchema):
    category = await KeyCategory.get_by_id(id)
    await category.append_keys(new_keys.keys)
    return "OK"
