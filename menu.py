
import psycopg2
import sys

# Define the connection parameters to the PostgreSQL database
DATABASE = "StudentDrivingHabits"
USER = "postgres"
PASSWORD = "password"
HOST = "localhost"

# Function to connect to the database
def get_connection():
    return psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST)

# Function to execute a query
def execute_query(sql, params=None, fetch=False, commit=False):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params or ())
        if commit:
            conn.commit()
            print("Operation successful.")
        if fetch:
            return cur.fetchall()
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        if conn:
            cur.close()
            conn.close()

# Insert Data Function
def insert_data():
    print("Inserting student and vehicle data...")
    conn = get_connection()
    try:
        cur = conn.cursor()

        # Collect student data from user
        student_id = input("Enter student ID: ")
        name = input("Enter name: ")
        age = int(input("Enter age: "))
        gender = input("Enter gender (Male, Female, Non-Binary): ").lower()
        year = input("Enter academic year (e.g., Freshman, Sophomore, Junior, Senior): ").lower()
        major = input("Enter major (e.g., Computer Science, Engineering, Nursing, Art): ").lower()
        monthly_gas_expenses = float(input("Enter monthly gas expenses: "))
        vehicle_type = input("Enter vehicle type (Sedan, Truck, Exotic): ").lower()

        # Convert descriptive inputs to IDs (gender, year, major)
        gender_id = get_gender_id(gender)  # Assuming this function converts gender to a gender ID
        year_id = get_year_id(year)        # Assuming this function converts academic year to a year ID
        major_id = get_major_id(major)     # Assuming this function converts major to a major ID

        # Insert student data
        sql_student = """
        INSERT INTO student_schema.students (student_id, name, age, gender_id, year_id, major_id, monthly_gas_expenses, vehicle_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        cur.execute(sql_student, (student_id, name, age, gender_id, year_id, major_id, monthly_gas_expenses, vehicle_type))
        print("Student data inserted successfully.")

        # Collect vehicle information from user
        make = input("Enter vehicle make (e.g., Toyota, Ford): ")
        model = input("Enter vehicle model (e.g., Camry, Mustang): ")
        year = int(input("Enter vehicle year: "))
        # Use previously entered student_id for vehicle's owner
        sql_vehicle = """
        INSERT INTO student_schema.vechile (make, model, year, student_id)
        VALUES (%s, %s, %s, %s);
        """
        cur.execute(sql_vehicle, (make, model, year, student_id))
        conn.commit()
        print("Vehicle data inserted successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        if conn:
            cur.close()
            conn.close()



# Delete Data Function
def delete_data():
    print("Select the criterion for deletion:")
    print("1. Delete by Student ID")
    print("2. Delete by Name")
    print("3. Delete by Major")
    print("4. Delete by Age")

    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        student_id = int(input("Enter student ID to delete: "))
        sql = "DELETE FROM student_schema.students WHERE student_id = %s;"
        params = (student_id,)
    elif choice == '2':
        name = input("Enter name of the student(s) to delete: ")
        sql = "DELETE FROM student_schema.students WHERE name = %s;"
        params = (name,)
    elif choice == '3':
        major = input("Enter major of the student(s) to delete: ")
        sql = "DELETE FROM student_schema.students WHERE major = %s;"
        params = (major,)
    elif choice == '4':
        age = int(input("Enter age of the student(s) to delete: "))
        sql = "DELETE FROM student_schema.students WHERE age = %s;"
        params = (age,)
    else:
        print("Invalid choice.")
        return

    # Confirm before deletion
    confirm = input(f"Are you sure you want to delete these records? (yes/no): ")
    if confirm.lower() == 'yes':
        execute_query(sql, params, commit=True)
        print("Data deleted successfully.")
    else:
        print("Deletion canceled.")


# Update Data Function
def update_data():
    student_id = int(input("Enter student ID to update: "))
    print("Select the attribute to update:")
    print("1. Age")
    print("2. Name")
    print("3. Major")
    print("4. Gender")

    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        new_age = int(input("Enter new age: "))
        sql = "UPDATE student_schema.students SET age = %s WHERE student_id = %s;"
        params = (new_age, student_id)
    elif choice == '2':
        new_name = input("Enter new name: ")
        sql = "UPDATE student_schema.students SET name = %s WHERE student_id = %s;"
        params = (new_name, student_id)
    elif choice == '3':
        new_major = input("Enter new major: ")
        sql = "UPDATE student_schema.students SET major = %s WHERE student_id = %s;"
        params = (new_major, student_id)
    elif choice == '4':
        new_gender = input("Enter new gender (Male, Female, Non-Binary): ").lower()
        sql = "UPDATE student_schema.students SET gender = %s WHERE student_id = %s;"
        params = (new_gender, student_id)
    else:
        print("Invalid choice.")
        return

    execute_query(sql, params, commit=True)
    print("Data updated successfully.")


# Search Data Function
def search_data():
    print("Select the search criterion:")
    print("1. Name")
    print("2. Student ID")
    print("3. Major")

    choice = input("Enter your choice (1-3): ")

    if choice == '1':
        name_search = input("Enter name to search: ")
        sql = "SELECT * FROM student_schema.students WHERE name ILIKE %s;"
        params = (f"%{name_search}%",)
    elif choice == '2':
        student_id_search = int(input("Enter student ID to search: "))
        sql = "SELECT * FROM student_schema.students WHERE student_id = %s;"
        params = (student_id_search,)
    elif choice == '3':
        major_search = input("Enter major to search: ")
        sql = "SELECT * FROM student_schema.students WHERE major ILIKE %s;"
        params = (f"%{major_search}%",)
    else:
        print("Invalid choice.")
        return

    results = execute_query(sql, params, fetch=True)
    for row in results:
        print(row)


# Aggregate Functions Example
def aggregate_functions():
    print("Select an aggregate function to perform:")
    print("1. Average Age")
    print("2. Minimum Age")
    print("3. Maximum Age")
    print("4. Total Number of Students")

    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        sql = "SELECT AVG(age) FROM student_schema.students;"
        description = "Average age"
    elif choice == '2':
        sql = "SELECT MIN(age) FROM student_schema.students;"
        description = "Minimum age"
    elif choice == '3':
        sql = "SELECT MAX(age) FROM student_schema.students;"
        description = "Maximum age"
    elif choice == '4':
        sql = "SELECT COUNT(*) FROM student_schema.students;"
        description = "Total number of students"
    else:
        print("Invalid choice.")
        return

    result = execute_query(sql, fetch=True)
    print(f"{description}: {result[0][0]}")


# Sorting Example
def sorting_data():
    print("Select a column to sort by:")
    print("1. Age (Descending)")
    print("2. Name (Alphabetical)")
    print("3. Gender")
    print("4. Major")

    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        sql = "SELECT * FROM student_schema.students ORDER BY age DESC;"
        description = "Students sorted by Age (Descending):"
    elif choice == '2':
        sql = "SELECT * FROM student_schema.students ORDER BY name;"
        description = "Students sorted by Name (Alphabetical):"
    elif choice == '3':
        sql = "SELECT * FROM student_schema.students ORDER BY gender;"
        description = "Students sorted by Gender:"
    elif choice == '4':
        sql = "SELECT * FROM student_schema.students ORDER BY major;"
        description = "Students sorted by Major:"
    else:
        print("Invalid choice.")
        return

    results = execute_query(sql, fetch=True)
    print(description)
    for row in results:
        print(row)


# Join Example
def perform_joins():
    print("Select the type of join:")
    print("1. Inner Join")
    print("2. Left Join")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        # SQL for an Inner Join
        sql = "SELECT a.*, b.* FROM table_a a INNER JOIN table_b b ON a.id = b.a_id;"
    elif choice == '2':
        # SQL for a Left Join
        sql = "SELECT a.*, b.* FROM table_a a LEFT JOIN table_b b ON a.id = b.a_id;"
    else:
        print("Invalid choice.")
        return

    execute_query(sql, fetch=True)  # execute_query would be a predefined function to handle SQL execution


# Grouping Example
def perform_grouping():
    print("Select the category to group by:")
    print("1. Group by Category")
    print("2. Group by Date")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        # SQL for Grouping by Category
        sql = "SELECT category, COUNT(*) FROM products GROUP BY category;"
    elif choice == '2':
        # SQL for Grouping by Date
        sql = "SELECT DATE(transaction_date), SUM(sales) FROM transactions GROUP BY DATE(transaction_date);"
    else:
        print("Invalid choice.")
        return

    execute_query(sql, fetch=True)  # execute_query would handle the execution and possibly display results


# Transactions Example
def manage_transactions():
    try:
        conn = get_connection()
        conn.autocommit = False
        cur = conn.cursor()
        cur.execute("INSERT INTO student_schema.students (name, age) VALUES ('Transactional Test', 25);")
        cur.execute("UPDATE student_schema.students SET age = age + 1 WHERE name = 'Transactional Test';")
        # Uncomment the next line to simulate an error and test rollback
        # raise Exception("Something went wrong!")
        conn.commit()
        print("Transaction completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        if conn:
            cur.close()
            conn.close()

# Error Handling Example
def handle_errors():
    try:
        execute_query("SELECT * FROM non_existing_table;")
    except Exception as e:
        print(f"Handled error: {e}")

def get_gender_id(gender_name):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT gender_id FROM student_schema.genders WHERE lower(gender_name) = lower(%s);", (gender_name,))
            result = cur.fetchone()
            if result:
                return result[0]
            else:
                raise ValueError("Invalid gender provided.")
    finally:
        conn.close()

def get_year_id(year_name):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT year_id FROM student_schema.years_in_school WHERE lower(year_name) = lower(%s);", (year_name,))
            result = cur.fetchone()
            if result:
                return result[0]
            else:
                raise ValueError("Invalid academic year provided.")
    finally:
        conn.close()

def get_major_id(major_name):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT major_id FROM student_schema.majors WHERE lower(major_name) = lower(%s);", (major_name,))
            result = cur.fetchone()
            if result:
                return result[0]
            else:
                raise ValueError("Invalid major provided.")
    finally:
        conn.close()
# Function to show all tables in the database
def show_tables():
    conn = get_connection()
    try:
        cur = conn.cursor()
        # Execute SQL query to retrieve table names
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'student_schema';")
        tables = cur.fetchall()
        table_names = [table[0] for table in tables]  # Extract table names from the result set
        print("Tables in 'student_schema':")
        for name in table_names:
            print(name)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

# Show Students Function
def show_students():
    conn = get_connection()
    try:
        cur = conn.cursor()
        # Execute SQL query to retrieve data from students table
        cur.execute("SELECT * FROM student_schema.students;")
        students = cur.fetchall()
        # Display the data
        print("Students:")
        for student in students:
            # Format each student record: convert Decimal to float for the monthly_gas_expenses field
            formatted_student = list(student)  # Convert tuple to list to manipulate data
            if formatted_student[6] is not None:  # Assuming the 7th field (index 6) is monthly_gas_expenses
                formatted_student[6] = float(formatted_student[6])  # Convert Decimal to float
            print(tuple(formatted_student))  # Print as a tuple
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

# Main Menu Function
def main_menu():
    print("\nWelcome to the Database CLI Interface!")
    print("Please select an option:")
    print("1. Insert Data")
    print("2. Delete Data")
    print("3. Update Data")
    print("4. Search Data")
    print("5. Aggregate Functions")
    print("6. Sorting")
    print("7. Joins")
    print("8. Grouping")
    print("9. Subqueries")
    print("10. Transactions")
    print("11. Error Handling")
    print("12. Show Tables")
    print("13. Show Students")
    print("14. Quit")  # Moved "Quit" to the last option

    choice = input("Enter your choice (1-14): ")
    return choice

def main():
    while True:
        choice = main_menu()
        if choice == '14':  # Quit is now option 14
            print("Exiting the program.")
            break  # Exit the loop to quit the program
        elif choice == '1':
            insert_data()
        elif choice == '2':
            delete_data()
        elif choice == '3':
            update_data()
        elif choice == '4':
            search_data()
        elif choice == '5':
            aggregate_functions()
        elif choice == '6':
            sorting_data()
        elif choice == '7':
            perform_joins()
        elif choice == '8':
            perform_grouping()
        elif choice == '9':
            print("Subquery operations placeholder")
        elif choice == '10':
            manage_transactions()
        elif choice == '11':
            handle_errors()
        elif choice == '12':
            show_tables()
        elif choice == '13':
            show_students()
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()


  
    
