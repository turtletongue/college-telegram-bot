class UsersRepository:
  def __init__(self, db):
    self.db = db

  def create(self, telegram_id):
    existing_user = self.select_by_telegram_id(telegram_id)

    if existing_user != None:
      return

    self.db.execute_with_cursor(lambda cursor: cursor.execute('''
      INSERT INTO 'users' (telegram_id) VALUES (?)
    ''', (telegram_id,)))

  def select_by_telegram_id(self, telegram_id):
    rows = self.db.execute_with_cursor(lambda cursor: cursor.execute('''
      SELECT id, telegram_id FROM users WHERE telegram_id = ?
    ''', (telegram_id,)).fetchall())

    return list(map(lambda row: { 'id': row[0], 'telegram_id': row[1] }, rows))