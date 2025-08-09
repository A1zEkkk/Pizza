from .base import BaseRepository, InstrumentedAttribute
from DB.Models.DB_models.product import Product, ProductImage

class ProductRepository(BaseRepository[Product]):
    def get_pk_column(self) ->InstrumentedAttribute:
        return self.model.id

class ProductIMGRepository(BaseRepository[ProductImage]):
    def get_pk_column(self) ->InstrumentedAttribute:
        return self.model.product_id