from flask.cli import FlaskGroup
from app import apps
cli=FlaskGroup(apps)
if __name__=="__main__":
    cli()
    