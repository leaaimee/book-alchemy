from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Integer

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    birth_date = Column(Date)
    date_of_death = Column(Date, nullable=True)

    books = relationship('Book', back_populates='author')

    def __repr__(self):
        return f"Author(name: {self.name})"

class Book(db.Model):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    isbn = Column(String(17))
    title = Column(String(100))
    publication_year = Column(Integer)
    author_id = Column(Integer, ForeignKey('authors.id'))

    author = relationship('Author', back_populates='books')
    rating = Column(Integer, nullable=True, default=None)

    def __repr__(self):
        return f"Book(book: {self.title} by {self.author.name})"

    def __str__(self):
        return f"'{self.title}' ({self.publication_year}) by {self.author.name}"

