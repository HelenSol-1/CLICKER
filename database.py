from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, Session

# Создаем базу данных SQLite
engine = create_engine('sqlite:///bot.db', echo=False)
Base = declarative_base()

# Таблица для связи продуктов и типов питания (многие ко многим)
product_diet = Table('product_diet', Base.metadata,
    Column('product_id', Integer, ForeignKey('products.product_id')),
    Column('diet_id', Integer, ForeignKey('diet_types.diet_id'))
)

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    gender = Column(String)
    age = Column(Integer)
    weight = Column(Float)
    height = Column(Float)
    activity_level = Column(String)
    goal = Column(String)
    calories = Column(Float)
    protein = Column(Float)
    fat = Column(Float)
    carbs = Column(Float)
    stars = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    diet_type_id = Column(Integer, ForeignKey('diet_types.diet_id'))
    diet_type = relationship('DietType', back_populates='users')

class DietType(Base):
    __tablename__ = 'diet_types'

    diet_id = Column(Integer, primary_key=True)
    name = Column(String)
    protein_percent = Column(Float)
    fat_percent = Column(Float)
    carbs_percent = Column(Float)
    products = relationship('Product', secondary=product_diet, back_populates='diets')
    users = relationship('User', back_populates='diet_type')

class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    name = Column(String)
    protein = Column(Float)
    fat = Column(Float)
    carbs = Column(Float)
    calories = Column(Float)
    category = Column(String)
    diets = relationship('DietType', secondary=product_diet, back_populates='products')

# Создаем таблицы
Base.metadata.create_all(engine)
