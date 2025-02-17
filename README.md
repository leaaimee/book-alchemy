📚 Book Alchemy

A Flask-based digital library where you can add, search, and manage books with AI-powered recommendations.

🚀 Features

Add & delete books/authors
Sort books by title or author
Search for books
AI-powered book recommendations
Bootstrap-styled UI

🛠️ Technologies Used

Python & Flask
SQLAlchemy with SQLite
Jinja2 for templating
Bootstrap for styling



🚀 Installation

Clone the repository

git clone <your-repo-url>
cd book_alchemy

Create and activate a virtual environment

python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
.venv\Scripts\activate     # On Windows


Install dependencies
pip install -r requirements.txt


Run the Flask app
flask run --debug


📝 Usage

Visit http://127.0.0.1:5000/home to browse and manage books.

Use /add_book and /add_author to add entries.
Click on a book title to see details.
Delete books directly from the homepage.
Get AI-powered recommendations via the 'Get a Recommendation' button.

📌 Notes

Ensure the virtual environment is activated before running the app.
AI recommendations currently use a basic rule-based suggestion; future updates will integrate an external API.

✨ Happy reading! 🚀

