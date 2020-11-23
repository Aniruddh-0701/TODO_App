from sqlalchemy import *
engine = create_engine('sqlite:///test.db', echo = True)

meta = MetaData()

t = text('ALTER TABLE Cats ADD COLUMN DOB;')
