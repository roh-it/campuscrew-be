import pymysql
from flask import current_app
from .config import Config

def grant_privileges(username, password, db_name):
    """Grant privileges to the user for the specified database."""
    
    connection = pymysql.connect(
        host='localhost',
        user='root',      
        password='campuscr3W.'
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION;")
            cursor.execute(f"""
                GRANT ALL PRIVILEGES ON `{db_name}`.* TO '{username}'@'localhost';
            """)
            cursor.execute("FLUSH PRIVILEGES;")
            connection.commit()
            print(f"Privileges granted for user '{username}' on database '{db_name}'.")
    except Exception as e:
        print("An error occurred while granting privileges:", e)
    finally:
        connection.close()

def init_db():
    """Initialize the database and create tables if they do not exist."""

    db_user = Config.DB_USER
    db_password = Config.DB_PASSWORD
    db_host = Config.DB_HOST
    db_name = Config.DB_NAME
    
    grant_privileges(db_user, db_password, db_name)
    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
            cursor.execute(f"USE `{db_name}`")
            create_users_table(cursor)
        connection.commit()  
        print(f"Database '{db_name}' initialized successfully.")
    finally:
        connection.close()

def create_users_table(cursor):
    """Create the users table if it does not exist."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(120) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,  
        first_name VARCHAR(80) NOT NULL,
        last_name VARCHAR(80) NOT NULL,
        user_id VARCHAR(80) NOT NULL
    );
    """
    cursor.execute(create_table_query)
