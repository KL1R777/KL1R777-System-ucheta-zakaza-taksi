import psycopg2
import time


def restore_db():
    time.sleep(2)

    conn = psycopg2.connect(
        dbname="mydatabase",
        user="myuser",
        password="mypassword",
        host="localhost",
        port="5432"
    )

    cursor = conn.cursor()


    cursor.execute("DROP TABLE IF EXISTS Reviews;")
    cursor.execute("DROP TABLE IF EXISTS Orders;")
    cursor.execute("DROP TABLE IF EXISTS Users;")
    cursor.execute("DROP TABLE IF EXISTS Status;")
    cursor.execute("DROP TABLE IF EXISTS UserRoles;")
    cursor.execute("DROP TYPE IF EXISTS order_status_enum;")




    cursor.execute("CREATE TABLE UserRoles (id SERIAL PRIMARY KEY, role VARCHAR(255));")
    cursor.execute("""
        CREATE TABLE Status (
            id SERIAL PRIMARY KEY,
            status VARCHAR(50) CHECK (status IN ('free', 'in_progress', 'cancelled', 'completed'))
        );
    """)


    cursor.execute("""
        CREATE TABLE Users (
            id SERIAL PRIMARY KEY, 
            email VARCHAR(255), 
            name VARCHAR(255), 
            hashed_password VARCHAR(255), 
            userRole INTEGER REFERENCES UserRoles(id), 
            money FLOAT
        );
    """)


    cursor.execute("""
        CREATE TABLE Orders (
            id SERIAL PRIMARY KEY,
            userID INTEGER REFERENCES Users(id),
            price FLOAT,
            driverID INTEGER REFERENCES Users(id),
            address VARCHAR(255),
            orderStatus INTEGER DEFAULT 1 
        );
    """)

    cursor.execute("""
            CREATE TABLE Reviews (
                id SERIAL PRIMARY KEY,
                orderID INTEGER REFERENCES Orders(id),
                userID INTEGER REFERENCES Users(id),
                rating INTEGER CHECK (rating >= 1 AND rating <= 5)
            );
        """)

    conn.commit()
    cursor.close()
    conn.close()

    print("База создана. Таблицы: UserRoles, Status, Users, Orders.")


def get_connection():
    return psycopg2.connect(
        dbname="mydatabase",
        user="myuser",
        password="mypassword",
        host="localhost",
        port="5432"
    )