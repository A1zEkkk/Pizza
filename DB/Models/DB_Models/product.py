from DB.Models import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    categorial: Mapped[str] = mapped_column(String)
    product: Mapped[str] = mapped_column(String, unique=True)
    composition: Mapped[str] = mapped_column(String)
    popularity: Mapped[int] = mapped_column(Integer)
    in_stock: Mapped[bool] = mapped_column(Boolean)

    images: Mapped[list["ProductImage"]] = relationship("ProductImage", back_populates="product", cascade="all, delete")


class ProductImage(Base):
    __tablename__ = 'product_image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    img_url: Mapped[str] = mapped_column(String, unique=True)

    product: Mapped["Product"] = relationship("Product", back_populates="images")