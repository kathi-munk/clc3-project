import sqlite3

# Function to read SQL file
def read_sql_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as sql_file:
        return sql_file.read()

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('movies.db')

try:
    # Read SQL commands from SQL files
    create_commands = read_sql_file('createDB.sql')
    insert_commands = read_sql_file('insertDB.sql')

    # Execute SQL commands
    with conn:
        cur = conn.cursor()

        # Execute creation commands with IF NOT EXISTS in SQL
        try:
            cur.executescript(create_commands)
        except sqlite3.OperationalError as e:
            print("Operational error while creating tables:", e)

        # Execute insertion commands
        try:
            cur.executescript(insert_commands)
        except sqlite3.OperationalError as e:
            print("Operational error while inserting data:", e)

finally:
    # Close the connection
    conn.close()
