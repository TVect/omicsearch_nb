from flask import Flask

from .herb import herb_cli
from .ttd import ttd_cli

def init_script(app: Flask):
    app.cli.add_command(herb_cli)
    app.cli.add_command(ttd_cli)