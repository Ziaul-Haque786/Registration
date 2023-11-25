import streamlit as st
import pyodbc

# Function to create a database connection using a connection string
def create_connection(connection_string):
    conn = None
    try:
        conn = pyodbc.connect(connection_string)
        st.success("Connection to Azure SQL Database successful")
    except pyodbc.Error as e:
        st.error(e)

    return conn

# Function to create a new user in the database
def create_user(conn, username, password):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        st.success(f"User {username} successfully registered")
    except pyodbc.Error as e:
        st.error(e)

# Function to create the users table if it does not exist
def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT IDENTITY(1,1) PRIMARY KEY,
                username NVARCHAR(255) NOT NULL,
                password NVARCHAR(255) NOT NULL
            )
        ''')
        st.success("Table created successfully")
    except pyodbc.Error as e:
        st.error(e)

# Main function
def main():
    st.title("User Registration Page")

    # Replace these values with your Azure SQL Database details
    server = 'sqlappserverreg.database.windows.net'
    database = 'registration'
    username = 'sqluser'
    password = 'Azure@12345'
    driver = '{ODBC Driver 17 for SQL Server}'  # Use the appropriate ODBC driver

    # Creating the connection string
   # connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

    # Create a connection to Azure SQL Database using the connection string
    conn = create_connection("connection_string") 

    # Create the users table if it does not exist
    create_table(conn)

    # Get user input for registration
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")

    # Register button
    if st.button("Register"):
        if username and password:
            create_user(conn, username, password)

# Run the app
if __name__ == "__main__":
    main()
