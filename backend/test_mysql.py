from app.database.mysql import get_mysql_connection


connection = get_mysql_connection()

print("MySQL connection successful!")

connection.close()