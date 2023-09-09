import mysql.connector

# Replace these values with your MySQL database credentials
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '9915005175',
    'database': 'mammm'
}

def create_table():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Define your table schema here
        table_schema = (
            "CREATE TABLE IF NOT EXISTS employees ("
            "id INT AUTO_INCREMENT PRIMARY KEY,"
            "name VARCHAR(255),"
            "age INT,"
            "position VARCHAR(255)"
            ")"
        )

        cursor.execute(table_schema)
        print("Table 'employees' created successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def insert_data(name, age, position):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        insert_query = "INSERT INTO employees (name, age, position) VALUES (%s, %s, %s)"
        data = (name, age, position)

        cursor.execute(insert_query, data)
        conn.commit()
        print(f"Data inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def retrieve_data():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        select_query = "SELECT * FROM employees"

        cursor.execute(select_query)
        rows = cursor.fetchall()

        if rows:
            print("Retrieved data:")
            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Position: {row[3]}")
        else:
            print("No data found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_table()

    insert_data("John Doe", 30, "Software Engineer")
    insert_data("Jane Smith", 28, "Data Analyst")

    retrieve_data()
