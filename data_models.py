from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    birth_date = db.Column(db.Date)
    date_of_death = db.Column(db.Date)


    def __str__(self):
        output = f'Name: {self.name}, Birth Date: {self.birth_date}'
        return output


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(13))
    title = db.Column(db.String(100))
    publication_year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)

    def __str__(self):
        output = f'Title: {self.title}, Year: {self.year}'
        return output
