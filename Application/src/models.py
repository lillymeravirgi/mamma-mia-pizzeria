from typing import Optional
import datetime
import decimal

from sqlalchemy import BigInteger, CheckConstraint, Column, DECIMAL, Date, Enum, ForeignKeyConstraint, Index, Integer, String, Table, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = 'Customer'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[str] = mapped_column(Enum('male', 'female', 'other'), nullable=False)
    birthdate: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    postcode: Mapped[str] = mapped_column(String(20), nullable=False)
    pizzas_ordered_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("'0'"))
    city: Mapped[Optional[str]] = mapped_column(String(50))
    country: Mapped[Optional[str]] = mapped_column(String(50))


class Dessert(Base):
    __tablename__ = 'Dessert'
    __table_args__ = (
        CheckConstraint('(`cost` > 0)', name='dessert_chk_1'),
        Index('name', 'name', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    cost: Mapped[decimal.Decimal] = mapped_column(DECIMAL(5, 2), nullable=False)


class DiscountCode(Base):
    __tablename__ = 'DiscountCode'
    __table_args__ = (
        Index('code', 'code', unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    is_valid: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text("'1'"))
    expiry_date: Mapped[Optional[datetime.date]] = mapped_column(Date)


class Drink(Base):
    __tablename__ = 'Drink'
    __table_args__ = (
        CheckConstraint('(`cost` > 0)', name='drink_chk_1'),
        Index('name', 'name', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    cost: Mapped[decimal.Decimal] = mapped_column(DECIMAL(5, 2), nullable=False)
    is_alcoholic: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text("'0'"))


class Ingredient(Base):
    __tablename__ = 'Ingredient'
    __table_args__ = (
        CheckConstraint('(`cost` > 0)', name='ingredient_chk_1'),
        Index('name', 'name', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    cost: Mapped[decimal.Decimal] = mapped_column(DECIMAL(5, 2), nullable=False)
    is_vegan: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    is_vegetarian: Mapped[int] = mapped_column(TINYINT(1), nullable=False)

    pizza: Mapped[list['Pizza']] = relationship('Pizza', secondary='PizzaIngredient', back_populates='ingredient')


class Pizza(Base):
    __tablename__ = 'Pizza'
    __table_args__ = (
        Index('name', 'name', unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    ingredient: Mapped[list['Ingredient']] = relationship('Ingredient', secondary='PizzaIngredient', back_populates='pizza')


class Staff(Base):
    __tablename__ = 'Staff'
    __table_args__ = (
        CheckConstraint('(`salary` >= 0)', name='staff_chk_1'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[str] = mapped_column(Enum('male', 'female', 'other'), nullable=False)
    role: Mapped[str] = mapped_column(Enum('chef', 'driver', 'cashier', 'manager'), nullable=False)
    salary: Mapped[decimal.Decimal] = mapped_column(DECIMAL(8, 2), nullable=False)


t_pizzamenu = Table(
    'pizzamenu', Base.metadata,
    Column('pizza_id', Integer, server_default=text("'0'")),
    Column('pizza_name', String(50)),
    Column('price', DECIMAL(30, 2)),
    Column('is_vegan', BigInteger),
    Column('is_vegetarian', BigInteger)
)


class DeliveryPerson(Staff):
    __tablename__ = 'DeliveryPerson'
    __table_args__ = (
        ForeignKeyConstraint(['id'], ['Staff.id'], ondelete='CASCADE', onupdate='CASCADE', name='deliveryperson_ibfk_1'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    postcode: Mapped[str] = mapped_column(String(20), nullable=False)
    available: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text("'1'"))


t_PizzaIngredient = Table(
    'PizzaIngredient', Base.metadata,
    Column('pizza_id', Integer, primary_key=True),
    Column('ingredient_id', Integer, primary_key=True),
    ForeignKeyConstraint(['ingredient_id'], ['Ingredient.id'], ondelete='CASCADE', onupdate='CASCADE', name='pizzaingredient_ibfk_2'),
    ForeignKeyConstraint(['pizza_id'], ['Pizza.id'], ondelete='CASCADE', onupdate='CASCADE', name='pizzaingredient_ibfk_1'),
    Index('ingredient_id', 'ingredient_id')
)
