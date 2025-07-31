from sqlalchemy import Delete, Select, Update, Insert
from DB.Models.DB_Models.product import Product, ProductImage
from DB.Models.schemas.product import ProductCreate, ProductUpdate
from DB.engine import ORMDatabase
from DB.init.base_service_product import BaseService

class ProductManager(BaseService):
    async def create_product(self, product: ProductCreate):
        async with self.session_maker() as session:
            stmt = Select(Product).where(Product.product == product.product)
            result = await session.execute(stmt)
            product_db = result.scalar_one_or_none()

            if product_db:
                print("Product in DB")
                return False

            session.add(product)
            await session.commit()
            await session.refresh(product)

            return {"message": "Product created", "product": product}

    async def delete_product(self, product_name: str):
        async with self.session_maker() as session:
            stmt = Select(Product).where(Product.product == product_name)
            result = await session.execute(stmt)
            product = result.scalar_one_or_none()

            if product:
                await session.delete(product)
                await session.commit()
                return product

            return None

    async def update_product(self, product_name: str, val: ProductUpdate):
        async with self.session_maker() as session:
            stmt = Select(Product).where(Product.product == product_name)
            result = await session.execute(stmt)
            product_db = result.scalar_one_or_none()

            if product_db is None:
                print("Product not found")
                return None

            stmt = Update(Product).where(Product.product == product_name).values(**val.model_dump(exclude_unset=True))
            await session.execute(stmt)
            await session.commit()
            print(f"Was updated {product_name}")
            return True

    async def select_product(self, product_name: str):
        async with self.session_maker() as session:
            stmt = Select(Product).where(Product.product == product_name)
            result = await session.execute(stmt)

            if result is None:
                return None

            session.commit()
            return result.scalar_one_or_none()

    async def add_img_url(self, img_url: str, product_name: str):
        async with self.session_maker() as session:
            stmt = Select(Product).where(Product.product == product_name)
            result = await session.execute(stmt)
            row = result.scalar_one_or_none()
            if row:
                id = row.id
                stmt = Insert(ProductImage).values(product_id=id, img_url=img_url)
                await session.execute(stmt)
                await session.commit()
                print(f"добавлено:{id}, {img_url}")
                return True

            return None

    async def delete_img_url(self, img_url: str):
        async with self.session_maker() as session:
            stmt = Delete(ProductImage).where(ProductImage.img_url == img_url)
            result = await session.execute(stmt)

            if result.rowcount > 0:
                await session.commit()
                print(f"{img_url} deleted")
                return True

            return None