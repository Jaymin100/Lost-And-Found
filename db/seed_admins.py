# Owner: Jackson
# Creates the 5 admin logins with hashed passwords (typed in at runtime, never committed)

import getpass #To enter passwords
import pymysql # Database functionality
from werkzeug.security import generate_password_hash

from backend.db import get_db_connection

# Creates one new admin account in the database
def create_admin(username, password):

    #Hash the password before storing it.
    password_hash = generate_password_hash(password)

    #Connect to the Lost and Found database.
    connection = get_db_connection()

    try:
        # Open a cursor to exectue SQL commands.
        with connection.cursor() as cursor:

            # Insert the username and hashed password
            sql = """
                INSERT INTO admins (username, password_hash)
                VALUES (%s, %s)
            """

            cursor.execute(sql, (username, password_hash))

        # Save the new admin account.
        connection.commit()

        print(f"Administrator '{username}' created successfully!")
        return True

    # Handle a usernmae that already exists.
    except pymysql.IntegrityError:
        connection.rollback()
        print(f"Username '{username}' already exists.")
        return False

    # Handle any other database error
    except Exception:
        connection.rollback()
        raise

    # Close database when finished
    finally:
        connection.close()


# Main program: creates five admin accounts.
if __name__ == "__main__":

    # Counts number of accounts created.
    created_count = 0

    #Continues until five accounts have been created.
    while created_count < 5:

        # Ask for the admin's username.
        username = input(f"Enter username for admin {created_count + 1}: ")

        # Ask for the admin's password.
        password = getpass.getpass("Enter password: ")

        # Create the admin account using the entered credentials.
        if create_admin(username,password):

            # Increase the counter only if the account was created.
            created_count += 1