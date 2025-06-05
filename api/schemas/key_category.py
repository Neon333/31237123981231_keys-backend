from pydantic import BaseModel


class CreateKeyCategorySchema(BaseModel):
    name: str


class KeyCategorySchema(CreateKeyCategorySchema):
    id: int
    count_keys: int


class AppendKeysSchema(BaseModel):
    keys: list[str]
