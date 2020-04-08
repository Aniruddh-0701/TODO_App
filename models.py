import sqlite3


class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('todo.db')
        self.create_user_table()
        self.create_to_do_table()
        # Why are we calling user table before to_do table
        # what happens if we swap them?

    def create_to_do_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS Todo (
          id INTEGER PRIMARY KEY,
          Title TEXT,
          Description TEXT,
          _is_done boolean,
          _is_deleted boolean,
          CreatedOn Date DEFAULT CURRENT_DATE,
          DueDate Date,
          UserId INTEGER FOREIGNKEY REFERENCES User(_id)
        );"""

        return self.conn.execute(query)

    def create_user_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS User(
          Name TEXT,
          Email EMAIL,
          id INTEGER PRIMARY KEY);
        """
        return self.conn.execute(query)


class ToDoModel:
    TABLENAME = "TODO"

    def __init__(self):
        self.conn = sqlite3.connect('todo.db')

    def create(self, text, description, ddate):
        query = f'insert into {ToDoModel.TABLENAME}' \
                f'(Title, Description, DueDate) ' \
                f'values ("{text}","{description}","{ddate}")'

        self.conn.execute(query)
        print("Successfully added")
        return 1

    def select(self, text, date, integer):
        query = f'select * from {ToDoModel.TABLENAME}' \
                f'where( id={integer} and Title={text} and DueDate{date}' \
                f');'
        result = self.conn.execute(query)
        return result

    def delete(self, integer):
        query = f'delete from {ToDoModel.TABLENAME} ' \
                f'where id={integer}'
        result = self.conn.execute(query)
        return result

    def update(self, integer, text, description, cdate, ddate):
        query = f'update {ToDoModel.TABLENAME} ' \
                f'set Title="{text}", Description="{description}", CreatedOn="{cdate}", DueDate="{ddate}"'
        result = self.conn.execute(query)
        return result