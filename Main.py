
from Student import add_student, bulk_import_students, course_wise_report, export_students_csv, view_students, search, update_student, delete_student

print("===== Student Record Management System =====")

from Student import (
    add_student,
    view_students,
    search,
    update_student,
    delete_student,
    student_statistics,
    course_wise_report,
    export_students_csv,
     bulk_import_students
)


while True:
    print("\n1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Student Statistics")
    print("7. Course-wise Report")
    print("8. Export Students to CSV")
    print("9. Bulk Import Students")
    print("10. Exit")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        add_student()
    elif choice == "2":
        view_students()
    elif choice == "3":
        search()
    elif choice == "4":
        update_student()
    elif choice == "5":
        delete_student()
    elif choice == "6":
        student_statistics()
    elif choice == "7":
        course_wise_report()
    elif choice == "8":
        export_students_csv()

    elif choice == "9":
        print("Exiting program...")
        break
  

    else:
        print("Invalid choice! Try again.")