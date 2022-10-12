import sqlite3
from contextlib import closing

class Database:
  def __init__(self, database_name):
    try:
      self._connection = sqlite3.connect(database_name, check_same_thread=False)

      def init_tables(cursor):
        cursor.execute('''
          CREATE TABLE IF NOT EXISTS 'users' (
            id INTEGER PRIMARY KEY,
            telegram_id INTEGER NOT NULL UNIQUE
          )
        ''')

        cursor.execute('''
          CREATE TABLE IF NOT EXISTS 'categories' (
            id INTEGER PRIMARY KEY,
            name VARCHAR(64) NOT NULL UNIQUE,
            api_name VARCHAR(64) NOT NULL UNIQUE
          )
        ''')

        cursor.execute('''
          CREATE TABLE IF NOT EXISTS 'subscriptions' (
            user_id INTEGER REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE,
            category_id INTEGER REFERENCES categories(id) ON UPDATE CASCADE ON DELETE CASCADE,
            PRIMARY KEY(user_id, category_id)
          )
        ''')
      
      self.execute_with_cursor(init_tables)

    except sqlite3.Error as error:
      print('Не удалось подключиться к базе данных: ' + error)

  def __enter__(self):
    return self
  
  def __exit__(self, exc_type, exc_value, traceback):
    self._connection.close()

  def execute_with_cursor(self, function):
    with self._connection:
      with closing(self._connection.cursor()) as cursor:
        return function(cursor)