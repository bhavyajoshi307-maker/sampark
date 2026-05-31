import sqlite3

conn = sqlite3.connect("vehicles.db")
cursor = conn.cursor()

# vehicles table
cursor.execute("""
CREATE TABLE IF NOT EXISTS vehicles(
vehicle_id TEXT PRIMARY KEY
)
""")

# owner telegram ids
cursor.execute("""
CREATE TABLE IF NOT EXISTS owners(
vehicle_id TEXT PRIMARY KEY,
chat_id TEXT
)
""")

# chat messages
cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_messages(
vehicle TEXT,
message TEXT,
sender TEXT
)
""")

conn.commit()
conn.close()

print("Database ready!")