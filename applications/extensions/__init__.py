from flask import Flask
from .init_sqlalchemy import db, ma, init_databases
from .init_error_views import init_error_views
from .init_migrate import init_migrate
from .init_session import init_session


def init_plugs(app: Flask) -> None:
    init_databases(app)
    init_error_views(app)
    init_migrate(app)
    init_session(app)