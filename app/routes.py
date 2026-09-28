from flask import Blueprint, redirect, render_template, url_for
from sqlalchemy import text
from app.extensions import db


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return redirect(url_for("tasks.index"))


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/db-test")
def db_test():
    try:
        result = db.session.execute(text("SELECT VERSION()"))
        version = result.scalar()
        return f"Connected to MySQL successfully! Version: {version}"
    except Exception as e:
        return f"Database connection failed: {e}"