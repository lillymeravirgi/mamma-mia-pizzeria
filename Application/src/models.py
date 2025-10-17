from typing import Optional
import datetime
import decimal

from sqlalchemy import BigInteger, CheckConstraint, Column, DECIMAL, Date, Enum, ForeignKeyConstraint, Index, Integer, String, TIMESTAMP, Table, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = 'customer'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[str] = mapped_column(Enum('male', 'female', 'other'), nullable=False)
    birthdate: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    postcode: Mapped[str] = mapped_column(String(20), nullable=False)
    pizzas_ordered_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("'0'"))
    city: Mapped[Optional[str]] = mapped_column(String(50))
    country: Mapped[Optional[str]] = mapped_column(String(50))

    order: Mapped[list['Order']] = relationship('Order', back_populates='customer')


class Dessert(Base):
    __tablename__ = 'dessert'
    __table_args__ = (
        CheckConstraint('(`cost` > 0)', name='dessert_chk_1'),
        Index('name', 'name', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    cost: Mapped[decimal.Decimal] = mapped_column(DECIMAL(5, 2), nullable=False)


class DiscountCode(Base):
    __tablename__ = 'discountcode'
    __table_args__ = (
        Index('code', 'code', unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    is_valid: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text("'1'"))
    expiry_date: Mapped[Optional[datetime.date]] = mapped_column(Date)

    orders: Mapped[list["OrderDiscount"]] = relationship("OrderDiscount", back_populates="discount")


class Drink(Base):
    __tablename__ = 'drink'
    __table_args__ = (
        CheckConstraint('(`cost` > 0)', name='drink_chk_1'),
        Index('name', 'name', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    cost: Mapped[decimal.Decimal] = mapped_column(DECIMAL(5, 2), nullable=False)
    is_alcoholic: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text("'0'"))


class Ingredient(Base):
    __tablename__ = 'ingredient'
    __table_args__ = (
        CheckConstraint('(`cost` > 0)', name='ingredient_chk_1'),
        Index('name', 'name', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    cost: Mapped[decimal.Decimal] = mapped_column(DECIMAL(5, 2), nullable=False)
    is_vegan: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    is_vegetarian: Mapped[int] = mapped_column(TINYINT(1), nullable=False)

    pizzas: Mapped[list['PizzaIngredient']] = relationship('PizzaIngredient', back_populates='ingredient')



class Pizza(Base):
    __tablename__ = 'pizza'
    __table_args__ = (
        Index('name', 'name', unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    
    ingredients: Mapped[list['PizzaIngredient']] = relationship('PizzaIngredient', back_populates='pizza')


t_pizzamenu = Table(
    'pizzamenu', Base.metadata,
    Column('pizza_id', Integer, server_default=text("'0'")),
    Column('pizza_name', String(50)),
    Column('price', DECIMAL(31, 2)),
    Column('is_vegan', BigInteger),
    Column('is_vegetarian', BigInteger)
)


class Staff(Base):
    __tablename__ = 'staff'
    __table_args__ = (
        CheckConstraint('(`salary` >= 0)', name='staff_chk_1'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[str] = mapped_column(Enum('male', 'female', 'other'), nullable=False)
    role: Mapped[str] = mapped_column(Enum('chef', 'driver', 'cashier', 'manager'), nullable=False)
    salary: Mapped[decimal.Decimal] = mapped_column(DECIMAL(8, 2), nullable=False)
    birthdate: Mapped[datetime.date] = mapped_column(Date, nullable=False)


class DeliveryPerson(Staff):
    __tablename__ = 'deliveryperson'
    __table_args__ = (
        ForeignKeyConstraint(['id'], ['staff.id'], ondelete='CASCADE', onupdate='CASCADE', name='deliveryperson_ibfk_1'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    postcode: Mapped[str] = mapped_column(String(20), nullable=False)
    available: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text("'1'"))

    order: Mapped[list['Order']] = relationship('Order', back_populates='delivery')


class PizzaIngredient(Base):
    __tablename__ = 'pizzaingredient'
    __table_args__ = (
        ForeignKeyConstraint(['pizza_id'], ['pizza.id'], ondelete='CASCADE', onupdate='CASCADE'),
        ForeignKeyConstraint(['ingredient_id'], ['ingredient.id'], ondelete='CASCADE', onupdate='CASCADE'),
        Index('ingredient_id', 'ingredient_id')
    )
    
    pizza_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    pizza: Mapped["Pizza"] = relationship("Pizza", back_populates="ingredients")
    ingredient: Mapped["Ingredient"] = relationship("Ingredient", back_populates="pizzas")

class Order(Base):
    __tablename__ = 'order'
    __table_args__ = (
        ForeignKeyConstraint(['customer_id'], ['customer.id'], ondelete='CASCADE', onupdate='CASCADE', name='order_ibfk_1'),
        ForeignKeyConstraint(['delivery_id'], ['deliveryperson.id'], ondelete='SET NULL', onupdate='CASCADE', name='order_ibfk_2'),
        Index('customer_id', 'customer_id'),
        Index('delivery_id', 'delivery_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(Enum('pending', 'in preparation', 'prepared', 'in delivery', 'delivered', 'cancelled'), nullable=False, server_default=text("'pending'"))
    delivery_id: Mapped[Optional[int]] = mapped_column(Integer)
    order_time: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    total: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(8, 2))

    discounts: Mapped[list["OrderDiscount"]] = relationship("OrderDiscount", back_populates="order")
    customer: Mapped['Customer'] = relationship('Customer', back_populates='order')
    delivery: Mapped[Optional['DeliveryPerson']] = relationship('DeliveryPerson', back_populates='order')
    orderitem: Mapped[list['OrderItem']] = relationship('OrderItem', back_populates='order')


class OrderDiscount(Base):
    __tablename__ = 'orderdiscount'
    __table_args__ = (
        ForeignKeyConstraint(['order_id'], ['order.id'], ondelete='CASCADE', onupdate='CASCADE', name='orderdiscount_ibfk_1'),
        ForeignKeyConstraint(['discount_id'], ['discountcode.id'], ondelete='CASCADE', onupdate='CASCADE', name='orderdiscount_ibfk_2'),
        Index('discount_id', 'discount_id')
    )

    order_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    discount_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    order: Mapped["Order"] = relationship("Order", back_populates="discounts")
    discount: Mapped["DiscountCode"] = relationship("DiscountCode", back_populates="orders")


class OrderItem(Base):
    __tablename__ = 'orderitem'
    __table_args__ = (
        CheckConstraint('(`quantity` > 0)', name='orderitem_chk_1'),
        ForeignKeyConstraint(['order_id'], ['order.id'], ondelete='CASCADE', onupdate='CASCADE', name='orderitem_ibfk_1')
    )

    order_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_type: Mapped[str] = mapped_column(Enum('pizza', 'drink', 'dessert'), primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    order: Mapped['Order'] = relationship('Order', back_populates='orderitem')
