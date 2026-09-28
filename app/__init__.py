from datetime import timezone
from zoneinfo import ZoneInfo

from flask import Flask
from config import config
from app.extensions import db, migrate


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from app import models  # noqa: F401

    from app.routes import main_bp
    from app.tasks import tasks_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(tasks_bp)

    @app.template_filter("localtime")
    def localtime_filter(value, fmt="%d %b %Y, %I:%M %p"):
        if value is None:
            return ""
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        local_zone = ZoneInfo(app.config["TIMEZONE"])
        return value.astimezone(local_zone).strftime(fmt)

    return app