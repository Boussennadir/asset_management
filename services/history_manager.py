from database.db_manager import DatabaseManager


class HistoryManager:
    def __init__(self):
        self.db = DatabaseManager()

    def get_all(self):
        return self.db.fetch_all("""
            SELECT date_action, action, table_nom, details
            FROM journal
            ORDER BY date_action DESC
        """)