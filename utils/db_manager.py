import sqlite3

class DatabaseManager:
    def __init__(self, db_path='database/notifications.db'):
        self.connection = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        with self.connection:
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS notifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    app_name TEXT,
                    message TEXT,
                    time TEXT
                )
                """
            )

    def insert_notification(self, app_name, message, time):
        with self.connection:
            self.connection.execute(
                "INSERT INTO notifications (app_name, message, time) VALUES (?, ?, ?)",
                (app_name, message, time)
            )

    def get_all_notifications(self):
        with self.connection:
            cursor = self.connection.execute("SELECT id, app_name, message, time FROM notifications")
            return [{"id": row[0], "app_name": row[1], "message": row[2], "time": row[3]} for row in cursor.fetchall()]

    def get_notification_id_by_message(self, message):
        with self.connection:
            cursor = self.connection.execute("SELECT id FROM notifications WHERE message = ?", (message,))
            result = cursor.fetchone()
            return result[0] if result else None

    def delete_notification(self, notification_id):
        with self.connection:
            self.connection.execute("DELETE FROM notifications WHERE id = ?", (notification_id,))
