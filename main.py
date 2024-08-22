
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from BOOKS.models import Book, Author
from BOOKS.database import engine, SessionLocal
from BOOKS import models
from BOOKS import schemas

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

# Books CRUD Operations
@app.get('/books', status_code=status.HTTP_200_OK, tags=['Books'])
def getting_all_books(db: Session = Depends(get_db)):
    get_all_book = db.query(models.Book).all()
    return get_all_book


@app.get('/books/{id}', status_code=status.HTTP_200_OK, tags=['Books'])
def get_books_info_by_id(id: int, db: Session = Depends(get_db)):
    get_book_byid = db.query(models.Book).filter(models.Book.id == id).first()
    if not get_book_byid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {id} not found")

    book_data = {
        "language_medium": get_book_byid.language_medium,
        "id": get_book_byid.id,
        "name": get_book_byid.name,
        "standard": get_book_byid.standard,
        "author_id": get_book_byid.author_id
        # Exclude author here
    }

    return {
        "book": book_data,
        "author": get_book_byid.author  # Author is separate
    }


@app.post('/books', status_code=status.HTTP_201_CREATED, tags=['Books'])
def creating_book(request: schemas.Book, db: Session = Depends(get_db)):
    try:
        new_book_creation = Book.create_book(
            db=db,
            author_id=request.author_id,
            name=request.name,
            standard=request.standard,
            language_medium=request.language_medium
        )
        return new_book_creation
    except HTTPException as e:
        raise e

@app.put('/books/{id}', status_code=status.HTTP_200_OK, tags=['Books'])
def updating_the_books(id: int, request: schemas.Book, db: Session = Depends(get_db)):
    book_id_updation = db.query(models.Book).filter(models.Book.id == id).first()
    if not book_id_updation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {id} not found")

    book_id_updation.name = request.name
    book_id_updation.standard = request.standard
    book_id_updation.language_medium = request.language_medium

    db.commit()
    db.refresh(book_id_updation)
    return book_id_updation

@app.delete('/books/{id}', tags=['Books'])
def deleting_book(id: int, db: Session = Depends(get_db)):
    book_to_delete = db.query(models.Book).filter(models.Book.id == id).first()
    if book_to_delete:
        db.delete(book_to_delete)
        db.commit()
        return {'detail': f"Book with id {id} deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {id} not found")

# Authors CRUD Operations
@app.get('/authors', tags=['Authors'])
def getting_all_authors(db: Session = Depends(get_db)):
    get_all_authors = db.query(models.Author).all()
    return get_all_authors

@app.post('/authors', tags=['Authors'])
def creating_authors(request: schemas.Author, db: Session = Depends(get_db)):
    creating_authors_fields = models.Author(
        name=request.name,
        email=request.email,
        password=request.password
    )
    db.add(creating_authors_fields)
    db.commit()
    db.refresh(creating_authors_fields)
    return creating_authors_fields

@app.put('/authors/{id}', tags=['Authors'])
def updating_author_info(id: int, request: schemas.Author, db: Session = Depends(get_db)):
    update_author = db.query(models.Author).filter(models.Author.id == id).first()
    if not update_author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Author with id {id} not found")
    update_author.name = request.name
    update_author.email = request.email
    update_author.password = request.password
    db.commit()
    db.refresh(update_author)

    return update_author

@app.delete('/authors/{id}', tags=['Authors'])
def deleting_author(id: int, db: Session = Depends(get_db)):
    author_to_delete = db.query(models.Author).filter(models.Author.id == id).first()
    if not author_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Author with id {id} not found")
    db.delete(author_to_delete)
    db.commit()
    return {'detail': f"Author with id {id} deleted successfully"}






















# from fastapi import FastAPI, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from urllib3 import request
#
# from BOOKS.models import Book, Author
# from BOOKS.database import engine, SessionLocal
# from BOOKS import models
# from BOOKS import schemas
#
# models.Base.metadata.create_all(bind=engine)
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
# app = FastAPI()
#
# # Books CRUD Operations
# @app.get('/books', status_code=status.HTTP_200_OK, tags=['Books'])
# def getting_all_books(db: Session = Depends(get_db)):
#     get_all_book = db.query(models.Book).all()
#     return get_all_book
#
# @app.get('/books/{id}', status_code=status.HTTP_200_OK, tags=['Books'])
# def get_books_info_by_id(id: int, db: Session = Depends(get_db)):
#     get_book_byid = db.query(models.Book).filter(models.Book.id == id).first()
#     if not get_book_byid:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {id} not found")
#     return get_book_byid
#
# @app.post('/books', status_code=status.HTTP_200_OK, tags=['Books'])
# def creating_book(request: schemas.Book, db: Session = Depends(get_db)):
#     new_book_creation = models.Book(
#         name=request.name,
#         standard=request.standard,
#         language_medium=request.language_medium,
#         author_id=request.author_id
#     )
#     db.add(new_book_creation)
#     db.commit()
#     db.refresh(new_book_creation)
#     return new_book_creation
#
# @app.delete('/books/{id}', tags=['Books'])
# def deleting_book(id: int, db: Session = Depends(get_db)):
#     book_to_delete = db.query(models.Book).filter(models.Book.id == id).first()
#     if book_to_delete:
#         db.delete(book_to_delete)
#         db.commit()
#         return {'detail': f"Book with id {id} deleted successfully"}
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {id} not found")
#
# @app.put('/books/{id}', status_code=status.HTTP_200_OK, tags=['Books'])
# def updating_the_books(id: int, request: schemas.Book, db: Session = Depends(get_db)):
#     book_id_updation = db.query(models.Book).filter(models.Book.id == id).first()
#     if not book_id_updation:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {id} not found")
#
#     book_id_updation.name = request.name
#     book_id_updation.standard = request.standard
#     book_id_updation.language_medium = request.language_medium
#
#     db.commit()
#     db.refresh(book_id_updation)
#     return book_id_updation
#
# # Authors CRUD Operations
# @app.get('/authors', tags=['Authors'])
# def getting_all_authors(db: Session = Depends(get_db)):
#     get_all_authors = db.query(models.Author).all()
#     return get_all_authors
#
# @app.post('/authors', tags=['Authors'])
# def creating_authors(request: schemas.Author, db: Session = Depends(get_db)):
#     creating_authors_fields = models.Author(
#         name=request.name,
#         email=request.email,
#         password=request.password
#     )
#     db.add(creating_authors_fields)
#     db.commit()
#     db.refresh(creating_authors_fields)
#     return creating_authors_fields
#
#
# @app.put('/authors/{id}', tags=['Authors'])
# def updating_author_info(id: int, request: schemas.Author, db: Session = Depends(get_db)):
#     update_author = db.query(models.Author).filter(models.Author.id == id).first()
#     if not update_author:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Author with id {id} not found")
#     update_author.name = request.name
#     update_author.email = request.email
#     update_author.password = request.password
#     db.commit()
#     db.refresh(update_author)
#
#     return update_author
#
#
# @app.delete('/authors/{id}', tags=['Authors'])
# def deleting_author(id:int, db:Session = Depends(get_db)):
#     author_to_delete = db.query(models.Author).filter(models.Author.id == id).first()
#     if not author_to_delete:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=
#         f"Author with id {id} not found")
#     return author_to_delete



























































#
# from fastapi import FastAPI, Depends
# from BOOKS.models import Book
# from BOOKS.database import engine, SessionLocal
# from BOOKS import models
# from requests import Session
# from fastapi import status, HTTPException
# from .schemas import Book, Author
#
# models.Base.metadata.create_all(bind=engine)
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
# app = FastAPI()
#
# @app.get('/blog', status_code=status.HTTP_200_OK)
# def getting_all_books(db: Session = Depends(get_db)):
#     get_all_book = db.query(models.Book).all()
#     return get_all_book
#
# @app.get('/blog/{id}', status_code=status.HTTP_200_OK)
# def get_books_info_by_id(id: int, db: Session = Depends(get_db)):
#     get_book_byid = db.query(models.Book).filter(models.Book.id == id).first()
#     if Book:
#         return
#     return get_book_byid
#
#
# @app.post('/blog', status_code=status.HTTP_200_OK)
# def creating_book(request : Book, db : Session = Depends(get_db)):
#     new_book_creation = models.Book(name=request.name, standard=request.standard
#                                     , language_medium=request.language_medium)
#     db.add(new_book_creation)
#     db.commit()
#     db.refresh(new_book_cron)
#     return request
#
# @app.delete('/blog/{id}')
# def deleting_book(id: int, db: Session = Depends(get_db)):
#     book_to_delete = db.query(models.Book).filter(models.Book.id == id).first()
#     if book_to_delete:
#         db.delete(book_to_delete)  # Delete the book object
#         db.commit()
#         return {'detail': f"Book with id {id} deleted successfully"}
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {id} not found")
#
#
# @app.put('/blog/{id}', status_code=status.HTTP_200_OK)
# def updating_the_books( id, request: schemas.Book,db: Session = Depends(get_db)):
#     book_id_updation =db.query(models.Book).filter(models.Book.id == id)
#     if not book_id_updation:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the id{id} want "
#                                                                           f"to update"
#                                                                           f"not created in db")
#     return book_id_updation













# @app.get('/')
# def reading_book(request:Book):
#
#     return request

# @app.put('/blog/{id}')
# def updating_book(request:Book, id:int):
#     return request, id











# @app.get('/')
# def reading_book(request:Book):
#
#     return request

# @app.put('/blog/{id}')
# def updating_book(request:Book, id:int):
#     return request, id
