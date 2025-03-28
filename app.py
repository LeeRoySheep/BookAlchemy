from datetime import datetime
from flask import Flask, jsonify,render_template, request
from flask_sqlalchemy import SQLAlchemy


from data_models import db, Author, Book

# Create Instance of Flask
app = Flask(__name__)

# Configure Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/library.sqlite"

# Connect Flask to Database
db.init_app(app)

@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    """
    Route to add author with POST or search author/s with GET
    :return:
    """
    if request.method == "GET":
        name = request.args.get("name","")
        if name:
            authors = db.session.query(Author) \
                .filter(Author.name.contains('%'+name+'%')) \
                .all()
            output = []
            # Convert query results to Dictionary to return as JSON
            for author in authors:
                author = dict({'name': author.name, \
                               'birth_date': author.birth_date.strftime('%Y-%m-%d'), \
                               'date_of_death': author.date_of_death.strftime( '%Y-%m-%d') \
                                   if author.date_of_death else None})
                output.append(author)
            return jsonify(output), 200
        else:
            return render_template("add_author.html")
    ### POST ---------------------------------------------------------------
    elif request.method == "POST":
        name = request.form["name"]
        birthdate = datetime.strptime(request.form["birthdate"], "%Y-%m-%d")
        if request.form["date_of_death"]:
            date_of_death = datetime.strptime(request.form["date_of_death"], "%Y-%m-%d")
            author = Author(name=name, birth_date=birthdate, date_of_death=date_of_death)
        else:
            author = Author(name=name, birth_date=birthdate)
        try:
            db.session.add(author)
            db.session.commit()
            return render_template("add_author.html", success=True)
        except Exception as e: # For Debugging and Testing catch all Exceptions
            print(e)
            return render_template("add_author.html", success=False)

# Add Book Route ---------------------------------------------------
@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "GET":
        title = request.args.get("title", "")
        year = request.args.get("year", "")
        isbn = request.args.get("isbn", "")
        if title:
            books = db.session.query(Book) \
                .filter(Book.title.contains('%' + title + '%')) \
                .all()
            output = []
            # Convert query results to Dictionary to return as JSON
            for book in books:
                book = dict({'title': book.title, \
                             'year': book.publication_year})
                output.append(book)
            return jsonify(output), 200
        elif year:
            books = db.session.query(Book) \
                .filter(Book.publication_year.contains('%' + year + '%')) \
                .all()
            output = []
            # Convert query results to Dictionary to return as JSON
            for book in books:
                book = dict({'title': book.title, \
                             'year': book.publication_year})
                output.append(book)
            return jsonify(output), 200
        elif isbn:
            books = db.session.query(Book) \
                .filter(Book.isbn.contains('%' + isbn + '%')) \
                .all()
            output = []
            # Convert query results to Dictionary to return as JSON
            for book in books:
                book = dict({'title': book.title, \
                             'year': book.publication_year})
                output.append(book)
            return jsonify(output), 200
        else:
            return render_template("add_book.html")
    ### POST ---------------------------------------------------------------
    elif request.method == "POST":
        title = request.form["title"]
        year = request.form["year"]
        isbn = request.form["isbn"] if request.form["isbn"] else None
        author = request.form["author"]
        try:
            author_id = db.session.query(Author.id) \
                .filter(Author.name.contains('%' + author + '%')) \
                .one()[0]
            book = Book(title=title, publication_year=year, isbn=isbn, author_id=author_id)
            db.session.add(book)
            db.session.commit()
            return render_template("add_book.html", success=True)
        except Exception as e: # For Debugging and Testing catch all Exceptions
            print(e)
            return render_template("add_book.html", success=False)

app.run(debug=True)

# Only needed to create datatables at the beginning of the project
# with app.app_context():
#   db.create_all()
