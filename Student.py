import csv 
import os
import re
from database import create_connection


def get_name():
    while True:
        name = input("Enter student name: ").strip()

        if (
            len(name) >= 2
            and any(ch.isalpha() for ch in name)
            and all(ch.isalpha() or ch.isspace() or ch in ".-'"
                    for ch in name)
        ):
            return name

        print("Invalid name! Enter a real name.")


def get_age():
    while True:
        try:
            age = int(input("Enter student age: "))
            if 1 <= age <= 100:
                return age
            print("Age must be between 1 and 100.")
        except ValueError:
            print("Enter age as a whole number.")


def get_email():
    while True:
        email = input("Enter student email: ").strip().lower()

        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

        if re.fullmatch(pattern, email):
            return email

        print("Invalid email format. Example: student@gmail.com")

def get_course():
    valid_courses = [
        "computer science",
        "cse",
        "diploma in cse",
        "diploma in computer science",
        "b.tech",
        "bca",
        "mca",
        "python",
        "data science",
        "information technology",
        "it",
        "electrical engineering",
        "electronics",
        "mechanical engineering"
    ]

    while True:
        course = input("Enter student course: ").strip()
        normalized_course = " ".join(course.lower().split())

        if normalized_course in valid_courses:
            return course

        print("Invalid course! Enter a valid course name from the accepted list.")
def get_marks():
    while True:
        try:
            marks = float(input("Enter student marks (0-100): "))

            if 0 <= marks <= 100:
                return marks

            print("Marks must be between 0 and 100.")
        except ValueError:
            print("Enter marks as a number.")


def get_student_id():
    while True:
        try:
            student_id = int(input("Enter student ID: "))
            if student_id > 0:
                return student_id
            print("ID must be a positive number.")
        except ValueError:
            print("Enter a valid numeric ID.")


def add_student():
    name = get_name()
    age = get_age()
    email = get_email()
    course = get_course()
    marks = get_marks()

    connection = None
    cursor = None

    try:
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT student_id FROM students WHERE email = %s",
            (email,)
        )

        if cursor.fetchone():
            print("This email is already registered!")
            return

        query = """
        INSERT INTO students (name, age, email, course, marks)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, age, email, course, marks))
        connection.commit()

        print("Student added successfully!")
        print("Generated Student ID:", cursor.lastrowid)

    except Exception as error:
        if connection:
            connection.rollback()
        print("Unable to add student:", error)

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()



def view_students():
    connection = None
    cursor = None

    try:
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT student_id, name, age, course, email, marks
            FROM students
            ORDER BY student_id
        """)

        records = cursor.fetchall()

        if not records:
            print("No student records found.")
            return

        print("\n" + "-" * 105)
        print(
            f"{'ID':<6}{'Name':<25}{'Age':<7}"
            f"{'Course':<22}{'Email':<30}{'Marks':<10}"
        )
        print("-" * 105)

        for student in records:
            student_id, name, age, course, email, marks = student

            print(
                f"{student_id!s:<6}"
                f"{str(name) if name is not None else 'N/A':<25}"
                f"{str(age) if age is not None else 'N/A':<7}"
                f"{str(course) if course is not None else 'N/A':<22}"
                f"{str(email) if email is not None else 'N/A':<30}"
                f"{str(marks) if marks is not None else 'N/A':<10}"
            )

        print("-" * 105)

    except Exception as error:
        print("Unable to view students:", error)

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def search():
    student_id = get_student_id()

    connection = None
    cursor = None

    try:
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM students WHERE student_id = %s",
            (student_id,)
        )
        record = cursor.fetchone()

        if record:
            print("\nStudent record:", record)
        else:
            print("Student not found!")

    except Exception as error:
        print("Unable to search student:", error)

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def update_student():
    student_id = get_student_id()

    print("1. Update name")
    print("2. Update age")
    print("3. Update email")
    print("4. Update course")
    print("5. Update marks")

    field_choice = input("Choose field to update: ").strip()

    fields = {
        "1": ("name", get_name),
        "2": ("age", get_age),
        "3": ("email", get_email),
        "4": ("course", get_course),
        "5": ("marks", get_marks)
    }

    if field_choice not in fields:
        print("Invalid option!")
        return

    column, get_value = fields[field_choice]
    new_value = get_value()

    connection = None
    cursor = None

    try:
        connection = create_connection()
        cursor = connection.cursor()

        if column == "email":
            cursor.execute(
                "SELECT student_id FROM students WHERE email = %s",
                (new_value,)
            )
            existing = cursor.fetchone()

            if existing and existing[0] != student_id:
                print("That email belongs to another student!")
                return

        query = f"UPDATE students SET {column} = %s WHERE student_id = %s"
        cursor.execute(query, (new_value, student_id))
        connection.commit()

        if cursor.rowcount > 0:
            print("Student updated successfully!")
        else:
            print("Student not found or no changes made.")

    except Exception as error:
        if connection:
            connection.rollback()
        print("Unable to update student:", error)

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def delete_student():
    student_id = get_student_id()

    confirm = input(
        f"Delete student ID {student_id}? Type YES to confirm: "
    ).strip()

    if confirm != "YES":
        print("Deletion cancelled.")
        return

    connection = None
    cursor = None

    try:
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM students WHERE student_id = %s",
            (student_id,)
        )
        connection.commit()

        if cursor.rowcount > 0:
            print("Student deleted successfully!")
        else:
            print("Student not found!")

    except Exception as error:
        if connection:
            connection.rollback()
        print("Unable to delete student:", error)

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            
def student_statistics():
    connection = None
    cursor = None

    try:
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                COUNT(*),
                AVG(marks),
                MAX(marks),
                MIN(marks),
                SUM(CASE WHEN marks >= 40 THEN 1 ELSE 0 END),
                SUM(CASE WHEN marks < 40 THEN 1 ELSE 0 END)
            FROM students
            WHERE marks IS NOT NULL
        """)

        total_with_marks, average, highest, lowest, passed, failed = cursor.fetchone()

        cursor.execute("SELECT COUNT(*) FROM students")
        total_students = cursor.fetchone()[0]

        print("\n===== Student Statistics Report =====")
        print("Total Students:", total_students)
        print("Students with Marks:", total_with_marks)

        if total_with_marks == 0:
            print("No marks available to calculate statistics.")
            return

        print(f"Average Marks: {average:.2f}")
        print("Highest Marks:", highest)
        print("Lowest Marks:", lowest)
        print("Passed Students (40+):", passed or 0)
        print("Failed Students (below 40):", failed or 0)
        print("=====================================")

    except Exception as error:
        print("Unable to generate statistics:", error)

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def course_wise_report():
    connection = None
    cursor = None

    try:
        connection = create_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                course,
                COUNT(*) AS total_students,
                AVG(marks) AS average_marks
            FROM students
            WHERE course IS NOT NULL
            GROUP BY course
            ORDER BY average_marks DESC
        """

        cursor.execute(query)
        records = cursor.fetchall()

        if not records:
            print("No course records found.")
            return

        print("\n========== Course-wise Report ==========")
        print(f"{'Course':<30}{'Students':<12}{'Average Marks':<15}")
        print("-" * 57)

        for course, total, average in records:
            average_text = (
                f"{average:.2f}" if average is not None else "N/A"
            )
            print(f"{course:<30}{total:<12}{average_text:<15}")

        print("-" * 57)

    except Exception as error:
        print("Unable to generate course report:", error)

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def export_students_csv():
    connection = None
    cursor = None

    try:
        connection = create_connection()
        cursor = connection.cursor()

        query = """
            SELECT student_id, name, age, email, course, marks
            FROM students
            ORDER BY student_id
        """
        cursor.execute(query)
        records = cursor.fetchall()

        if not records:
            print("No student records available to export.")
            return

        filename = "students_report.csv"

        with open(filename, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)

            writer.writerow([
                "Student ID",
                "Name",
                "Age",
                "Email",
                "Course",
                "Marks"
            ])

            writer.writerows(records)

        print("Student records exported successfully!")
        print("File name:", filename)
        print("Total records exported:", len(records))

    except Exception as error:
        print("Unable to export student records:", error)

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def bulk_import_students():
    connection = None
    cursor = None

    # CSV file ko Student.py ke folder se locate karega
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "students_bulk.csv"
    )

    inserted = 0
    skipped = 0
    errors = []

    try:
        # CSV file check
        if not os.path.exists(file_path):
            print("CSV file nahi mili:", file_path)
            return

        connection = create_connection()
        cursor = connection.cursor()

        # Database mein pehle se registered emails
        cursor.execute("SELECT email FROM students")
        existing_emails = {
            row[0].strip().lower()
            for row in cursor.fetchall()
            if row[0]
        }

        # CSV read karo
        with open(file_path, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            required_columns = {
                "Name", "Age", "Email", "Course", "Marks"
            }

            if not reader.fieldnames or not required_columns.issubset(
                set(reader.fieldnames)
            ):
                print(
                    "CSV headings galat hain. Required headings:",
                    "Name, Age, Email, Course, Marks"
                )
                return

            for row_number, row in enumerate(reader, start=2):
                try:
                    name = (row.get("Name") or "").strip()
                    age_text = (row.get("Age") or "").strip()
                    email = (row.get("Email") or "").strip().lower()
                    course = (row.get("Course") or "").strip()
                    marks_text = (row.get("Marks") or "").strip()

                    # Required fields
                    if not all([
                        name, age_text, email, course, marks_text
                    ]):
                        raise ValueError("Koi field khaali hai")

                    # Basic validation
                    if len(name) < 2 or not any(
                        character.isalpha() for character in name
                    ):
                        raise ValueError("Name valid nahi hai")

                    age = int(age_text)
                    if not 1 <= age <= 100:
                        raise ValueError("Age 1 se 100 ke beech honi chahiye")

                    if "@" not in email or "." not in email.split("@")[-1]:
                        raise ValueError("Email valid nahi hai")

                    if email in existing_emails:
                        raise ValueError("Email pehle se registered hai")

                    marks = float(marks_text)
                    if not 0 <= marks <= 100:
                        raise ValueError("Marks 0 se 100 ke beech hone chahiye")

                    # Insert student
                    cursor.execute(
                        """
                        INSERT INTO students (name, age, email, course, marks)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (name, age, email, course, marks)
                    )

                    existing_emails.add(email)
                    inserted += 1

                except (ValueError, TypeError) as error:
                    skipped += 1
                    errors.append(
                        f"Row {row_number}: {error}"
                    )

                except Exception as error:
                    skipped += 1
                    errors.append(
                        f"Row {row_number}: Database error - {error}"
                    )

        # Saare successful inserts ek saath save honge
        connection.commit()

        print("\n===== Bulk Import Report =====")
        print("Successfully imported:", inserted)
        print("Skipped rows:", skipped)

        if errors:
            print("\nRows requiring correction:")
            for error in errors[:20]:
                print("-", error)

            if len(errors) > 20:
                print("Aur", len(errors) - 20, "errors bhi hain.")

    except Exception as error:
        if connection:
            connection.rollback()
        print("Bulk import failed:", error)

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()
