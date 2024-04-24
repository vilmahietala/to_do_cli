from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()
engine = create_engine("sqlite:///todo.db", echo = False, future = True)



# items
class Item(Base):
    __tablename__ = "items"
    item_id = Column(Integer, primary_key= True, autoincrement= True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    time = Column(DateTime, default=datetime.datetime.now)
    users = relationship("User", secondary="user_items", back_populates="items", single_parent=True)



# users
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key= True, autoincrement= True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    items = relationship("Item", secondary="user_items", back_populates="users", single_parent=True)



# associative entity table
class User_Item(Base):
    __tablename__ = "user_items"
    item_id = Column(Integer, ForeignKey("items.item_id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)



Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)