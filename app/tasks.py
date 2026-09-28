from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("/")
def index():
    current_filter = request.args.get("filter", "all")

    query = db.select(Task).order_by(Task.created_at.desc())
    if current_filter == "active":
        query = query.where(Task.is_completed.is_(False))
    elif current_filter == "completed":
        query = query.where(Task.is_completed.is_(True))

    tasks = db.session.execute(query).scalars().all()

    total = db.session.scalar(db.select(db.func.count(Task.id)))
    completed = db.session.scalar(
        db.select(db.func.count(Task.id)).where(Task.is_completed.is_(True))
    )

    return render_template(
        "tasks/index.html",
        tasks=tasks,
        current_filter=current_filter,
        total=total,
        completed=completed,
        pending=total - completed,
    )


@tasks_bp.route("/create", methods=["POST"])
def create():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()

    if not title:
        return redirect(url_for("tasks.index"))

    task = Task(title=title, description=description or None)
    try:
        db.session.add(task)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()

    return redirect(url_for("tasks.index"))


@tasks_bp.route("/<int:task_id>/edit", methods=["GET", "POST"])
def edit(task_id):
    task = db.get_or_404(Task, task_id)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if title:
            task.title = title
            task.description = request.form.get("description", "").strip() or None
            db.session.commit()
            return redirect(url_for("tasks.index"))

    return render_template("tasks/edit.html", task=task)


@tasks_bp.route("/<int:task_id>/toggle", methods=["POST"])
def toggle(task_id):
    task = db.get_or_404(Task, task_id)
    task.is_completed = not task.is_completed
    db.session.commit()
    return redirect(url_for("tasks.index"))


@tasks_bp.route("/<int:task_id>/delete", methods=["POST"])
def delete(task_id):
    task = db.get_or_404(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("tasks.index"))