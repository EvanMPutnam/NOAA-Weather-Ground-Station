import sqlalchemy as db

engine = db.create_engine("sqlite:///satellites.sqlite")
connection = engine.connect()
metadata = db.MetaData()

# TODO
