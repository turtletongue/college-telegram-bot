class CategoriesRepository:
  def __init__(self, db):
    self.db = db

  def create(self, name, api_name):
    self.db.execute_with_cursor(lambda cursor: cursor.execute('''
      INSERT INTO 'categories' (name, api_name) VALUES (?, ?)
    ''', (name, api_name)))

  def select_all(self):
    rows = self.db.execute_with_cursor(lambda cursor: cursor.execute('''
      SELECT id, name, api_name FROM categories
    ''').fetchall())

    return list(map(lambda row: { 'id': row[0], 'name': row[1] }, rows))

  def select_by_id(self, id):
    row = self.db.execute_with_cursor(lambda cursor: cursor.execute('''
      SELECT id, name, api_name FROM categories WHERE id = ?
    ''', (id,)).fetchone())

    if row == None:
      return None

    return { 'id': row[0], 'name': row[1], 'api_name': row[2] }