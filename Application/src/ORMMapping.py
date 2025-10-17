from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, func
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine("mysql+pymysql://root:Ponzano05@localhost/pizza_ordering", echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class Pizza(Base):
    __tablename__ = "Pizza"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    ingredients = relationship("PizzaIngredient", back_populates="pizza")


class Ingredient(Base):
    __tablename__ = "Ingredient"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    cost = Column(Float, nullable=False)
    is_vegetarian = Column(Boolean, default=False)
    is_vegan = Column(Boolean, default=False)

    pizzas = relationship("PizzaIngredient", back_populates="ingredient")


class PizzaIngredient(Base):
    __tablename__ = "PizzaIngredient"
    pizza_id = Column(Integer, ForeignKey("Pizza.id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("Ingredient.id"), primary_key=True)

    pizza = relationship("Pizza", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="pizzas")

class Drink(Base):
    __tablename__ = "Drink"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    cost = Column(Float, nullable=False)
    is_alcoholic = Column(Boolean, default=False)

class Dessert(Base):
    __tablename__ = "Dessert"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    cost = Column(Float, nullable=False)

class Order(Base):
    __tablename__ = "Orders"
    id = Column(Integer, primary_key=True)
    item_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)

