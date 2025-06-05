from sqlalchemy import select, func
from sqlalchemy.orm import column_property, relationship
from ... import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey


class SteamKeySqlModel(BaseModel):
    __tablename__ = 'keys'

    id = Column(Integer, primary_key=True)
    value = Column(String(64), unique=True)
    category_id = Column(Integer, ForeignKey('key_categories.id'))
    order_item_id = Column(Integer, ForeignKey('order_items.id'), nullable=True, default=None)
    # order = relationship("OrderSqlModel")


class KeyCategorySqlModel(BaseModel):
    __tablename__ = 'key_categories'

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(255), unique=True)

    count_keys = column_property(
        select(func.count(SteamKeySqlModel.id))
        .where(
            SteamKeySqlModel.category_id == id,
            SteamKeySqlModel.order_item_id == None
        )
        .correlate_except(SteamKeySqlModel)
        .scalar_subquery()
    )
