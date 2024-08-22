
from pydantic import BaseModel

class Book(BaseModel):
    name: str
    standard: str
    language_medium: str
    author_id : int = 2
    class Config:
        from_attributes = True


class Author(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        from_attributes = True
