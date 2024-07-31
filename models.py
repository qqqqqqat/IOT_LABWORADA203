from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship

from database import Base

class Book(Base):
    # ชื่อฐานข้อมูล
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    year = Column(Integer, index=True)
    describe = Column(String, index=True)
    summary = Column(String, index=True)
    category = Column(String, index=True)
    is_published = Column(Boolean, index=True)
    imgurl = Column(String, index=True)

class Info(Base):
    __tablename__ = 'Informations'

    firstname = Column(String, index=True)
    surname = Column(String, index=True)
    id = Column(String, primary_key=True, index=True)
    dateofbirth = Column(String, index=True)
    gender = Column(String, index=True)


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True, index=True)
    menuname = Column(String, index=True)
    price = Column(Integer, index=True)
    imgurl = Column(String, index=True)
    is_published = Column(Boolean, index=True)

class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, index=True)
    total = Column(Integer, index=True)
    detail = Column(String, index=True)
    getmenuname = Column(String, index=True)

