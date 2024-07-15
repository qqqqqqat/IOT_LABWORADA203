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
    is_published = Column(Boolean, index=True)

class Info(Base):
    __tablename__ = 'Informations'

    firstname = Column(String, index=True)
    surname = Column(String, index=True)
    id = Column(String, primary_key=True, index=True)
    dateofbirth = Column(String, index=True)
    gender = Column(String, index=True)

