
from click import FloatRange
from requests import Session
from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError
from http.client import HTTPException
from starlette import status


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    books = relationship("Book", back_populates="author", cascade="all, delete")


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    standard = Column(String)
    language_medium = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))

    author = relationship("Author", back_populates="books")

    @staticmethod
    def create_book(db: Session, author_id: int, **kwargs):
        # Check if the author has already written 5 books
        author = db.query(Author).filter(Author.id == author_id).first()
        if len(author.books) >= 5:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Author can only write up to 5 books")

        new_book = Book(author_id=author_id, **kwargs)
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return new_book










# from .database import Base
# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
#
#
# class Author(Base):
#     __tablename__ = 'authors'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     email = Column(String)
#     password = Column(String)
#     books = relationship("Book", back_populates="author")
#
#
# class Book(Base):
#     __tablename__ = 'books'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     standard = Column(String)
#     language_medium = Column(String)
#     author_id = Column(Integer, ForeignKey('authors.id'))
#
#     author = relationship("Author", back_populates="books")
#















#
# from .database import Base
# from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
# from sqlalchemy.orm import relationship
#
#
# class Book(Base):
#     __tablename__ = 'books'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     standard = Column(String)
#     language_medium = Column(String)
#     created_by_author= relationship("Author", back_populates="books")
#
# class Author(Base):
#     __tablename__ = 'authors'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     email = Column(String)
#     password = Column(String)
#
#
