**📚 Book Alchemy**

A Flask-based digital library where you can add, search, 
and manage books—with optional AI-powered recommendations.


🚀 **Features**

✔ Add & delete books and authors
✔ Sort books by title or author
✔ Search for books by keyword
✔ View book details on individual pages
✔ Bootstrap-styled UI for clean and modern design
✔ (Optional) AI-powered recommendations


**🛠️ Technologies Used**

Python & Flask – Backend framework
SQLAlchemy & SQLite – Database management
Jinja2 – Dynamic templating
Bootstrap – UI styling
(Optional) OpenAI API – AI-powered recommendations (not enabled by default)



🚀 **Installation**

Clone the repository

git clone <your-repo-url>
cd book_alchemy


Create and Activate a Virtual Environment

python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
.venv\Scripts\activate     # On Windows


Install dependencies

pip install -r requirements.txt


Run the Flask app

flask run --debug


📝 **Usage**

Visit http://127.0.0.1:5000/home to browse and manage books.

Use /add_book and /add_author to add entries.
Click on a book title to see details.
Delete books directly from the homepage.
Get AI-powered recommendations via the 'Get a Recommendation' button.

📌 **Notes**

Ensure the virtual environment is activated before running the app.
AI recommendations are optional and currently use a placeholder rule-based suggestion. Future updates may integrate an external AI API.
If using OpenAI’s API, update .env with OPENAI_API_KEY and add openai to requirements.txt.


**✨ Happy reading! 🚀**

