from backend.app.database.connection import get_connection

conn = get_connection()
cursor = conn.cursor()

