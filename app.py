from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://todo_user:todo_pass123@localhost:3306/todo_db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


@app.route("/")
def home():
    return "Hello, Flask! My Todo App is starting..."


@app.route("/about")
def about():
    return "This is a Todo app built with Flask and MySQL."


@app.route("/db-test")
def db_test():
    try:
        result = db.session.execute(text("SELECT VERSION()"))
        version = result.scalar()
        return f"Connected to MySQL successfully! Version: {version}"
    except Exception as e:
        return f"Database connection failed: {e}"


if __name__ == "__main__":
    app.run(debug=True)