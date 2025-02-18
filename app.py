from flask import Flask, render_template, request, redirect, url_for
import os
from data_models import db, Author, Book
from datetime import datetime
from flask import flash
import openai
from dotenv import load_dotenv


load_dotenv()  # Load API key from .env file
openai.api_key = os.getenv("OPENAI_API_KEY")


print("✅ Starting Flask App...")
app = Flask(__name__)


print("✅ Flask App Created!")
db_path = os.path.join(os.getcwd(), "data", "library.sqlite")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
db.init_app(app)


# with app.app_context():
#     chucks = Author.query.filter_by(name="Chuck Palahniuk").all()
#     if len(chucks) > 1:
#         for twin in chucks[1:]:
#             db.session.delete(twin)  # Absorbed into the void
#         db.session.commit()
#         print("🔥 The weaker Chucks have been erased. Only one remains.")
#     else:
#         print("✅ Balance is restored. Only one Chuck exists.")


@app.route('/')
@app.route('/home')
def home():
    """ Render the home page with a list of books. Supports sorting and keyword search """
    books = Book.query  # Keep books as a query object

    # Search part
    search_query = request.args.get('search', '').strip()
    if search_query:
        books = books.filter(Book.title.ilike(f"%{search_query}%"))

    # Sorting part
    sort_by = request.args.get('sort', 'title')
    if sort_by == "author":
        books = books.join(Author).order_by(Author.name)
    else:
        books = books.order_by(Book.title)

    books = books.all()  # ✅ Only now, execute the query and turn it into a list

    return render_template('home.html', books=books, sort_by=sort_by)



@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """ Add a new author to the database via a form submission """
    if request.method == 'POST':
        name = request.form['name']
        birthdate_str = request.form.get('birthdate')
        date_of_death_str = request.form.get('date_of_death', None)

        birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d").date()

        date_of_death = None
        if date_of_death_str:
            date_of_death = datetime.strptime(date_of_death_str, "%Y-%m-%d").date()

        new_author = Author(name=name, birth_date=birthdate, date_of_death=date_of_death)

        db.session.add(new_author)
        db.session.commit()

        return render_template('add_author.html', success=True)

    return render_template('add_author.html', success=False)


@app.route('/add_book', methods=['POST', 'GET'])
def add_book():
    """ Add a new book to the database and associate it with an existing author """
    authors = Author.query.all()

    if request.method == 'POST':
        title = request.form['title']
        isbn = request.form['isbn']
        publication_year = request.form['publication_year']
        author_name = request.form['author']
        rating = request.form.get('rating', None)

        author = Author.query.filter_by(name=author_name).first()
        if not author:
            return "<h3 style='color: red;'>Error: Author not found! Please add the author first.</h3>"

        new_book = Book(title=title, isbn=isbn, publication_year=publication_year, author_id=author.id, rating=rating)

        db.session.add(new_book)
        db.session.commit()

        return render_template('add_book.html', success=True, authors=authors)

    return render_template('add_book.html', success=False, authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """ Delete a book from the database. If no other books remain by the author, consider deleting the author """
    book = Book.query.get_or_404(book_id)

    # author = book.author

    db.session.delete(book)
    db.session.commit()

    flash(f"🔥 {book.title} has been purged!", "success")


    # If the author has no more books, this could be an option to delete them
    # if not Book.query.filter_by(author_id=author.id).first():
    #     db.session.delete(author)
    #     db.session.commit()

    return redirect(url_for('home'))


@app.route('/book/<int:book_id>')
def book_detail(book_id):
    """ Display details for a specific book, including author info and rating """
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)


load_dotenv()  # Load API key from .env file
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route('/recommend')
def recommend():
    """ Generate a book recommendation based on the current library collection """
    """ AI-Powered Book Recommendations """
    books = Book.query.all()
    book_titles = [book.title for book in books]

    prompt = f"I have read {', '.join(book_titles[:5])}. Based on these, recommend a book I would like."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Or use "gpt-3.5-turbo" for cheaper requests
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50,
        )
        ai_recommendation = response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        ai_recommendation = "Error fetching recommendation."

    return render_template('recommend.html', recommendation=ai_recommendation)


# adding some books as starter pack
# with app.app_context():
#     db.create_all()

# from datetime import date
#
# def seed_data():
#     with app.app_context():
#         if Author.query.first():  # Avoid duplicate entries
#             print("✅ Database already populated!")
#             return
#
#         print("📚 Seeding database with legendary books...")
#
#         authors = {
#             "Douglas Adams": Author(name="Douglas Adams", birth_date=date(1952, 3, 11), date_of_death=date(2001, 5, 11)),
#             "Terry Pratchett": Author(name="Terry Pratchett", birth_date=date(1948, 4, 28), date_of_death=date(2015, 3, 12)),
#             "Philip K. Dick": Author(name="Philip K. Dick", birth_date=date(1928, 12, 16), date_of_death=date(1982, 3, 2)),
#             "Mary Shelley": Author(name="Mary Shelley", birth_date=date(1797, 8, 30), date_of_death=date(1851, 2, 1)),
#             "William Gibson": Author(name="William Gibson", birth_date=date(1948, 3, 17)),
#             "Chuck Palahniuk": Author(name="Chuck Palahniuk", birth_date=date(1962, 2, 21))
#         }
#
#         db.session.add_all(authors.values())
#         db.session.commit()
#
#         books = [
#             Book(title="The Hitchhiker's Guide to the Galaxy", isbn="9780345391803", publication_year=1979, author_id=authors["Douglas Adams"].id, rating=9),
#             Book(title="Dirk Gently's Holistic Detective Agency", isbn="9780671746728", publication_year=1987, author_id=authors["Douglas Adams"].id, rating=8),
#
#             Book(title="Good Omens", isbn="9780060853983", publication_year=1990, author_id=authors["Terry Pratchett"].id, rating=10),
#             Book(title="Hogfather", isbn="9780061059056", publication_year=1996, author_id=authors["Terry Pratchett"].id, rating=9),
#
#             Book(title="Do Androids Dream of Electric Sheep?", isbn="9780345404473", publication_year=1968, author_id=authors["Philip K. Dick"].id, rating=9),
#             Book(title="Ubik", isbn="9780547572294", publication_year=1969, author_id=authors["Philip K. Dick"].id, rating=8),
#
#             Book(title="Frankenstein", isbn="9780486282114", publication_year=1818, author_id=authors["Mary Shelley"].id, rating=10),
#
#             Book(title="Neuromancer", isbn="9780441569595", publication_year=1984, author_id=authors["William Gibson"].id, rating=9),
#
#             Book(title="Fight Club", isbn="9780393327342", publication_year=1996, author_id=authors["Chuck Palahniuk"].id, rating=10)
#         ]
#
#         db.session.add_all(books)
#         db.session.commit()
#         print("✅ Database seeded successfully!")

# Run seeding
# seed_data()
