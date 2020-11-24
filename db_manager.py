from sqlalchemy import *
engine = create_engine('sqlite:///test.db', echo = True)

meta = MetaData()

conn = engine.connect()

# tasks = text(f'CREATE TABLE Tasks ('\
#     f'id INTEGER NOT NULL,'\
#     f'content VARCHAR(200) NOT NULL,'\
#     f'completed INTEGER,'\
#     f'date_created DATETIME,'\
#     f'deadline DATETIME,'\
#     f'user VARCHAR(200) NOT NULL)'\
#     )

users = text(f'CREATE TABLE Users ('\
    f'_id VARCHAR(50) NOT NULL,'\
    f'username VARCHAR(200) NOT NULL,'\
    f'password VARCHAR(200) NOT NULL)'
    )

# print(conn.execute(tasks))
print(conn.execute(users))