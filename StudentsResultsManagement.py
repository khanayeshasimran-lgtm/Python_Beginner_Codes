import os

FILE_NAME = "students.txt"

def calculate_grade(percentage):
    if percentage >= 90:
        return "A"
    elif percentage >= 75:
        return "B"
    elif percentage >= 60:
        return "C"
    else:
        return "D"

def add_student():
    name = input("Enter student name: ")
    marks = []

    for i in range(1, 4):
        mark = float(input(f"Enter marks for subject {i}: "))
        marks.append(mark)

    total = sum(marks)
    percentage = total / 3
    grade = calculate_grade(percentage)

    with open(FILE_NAME, "a") as file:
        file.write(f"{name},{marks[0]},{marks[1]},{marks[2]},{total},{percentage:.2f},{grade}\n")

    print("Student record added successfully!\n")

def view_students():
    if not os.path.exists(FILE_NAME):
        print("\nNo records found.\n")
        return

    print("\n--- Student Records ---")
    with open(FILE_NAME, "r") as file:
        for line in file:
            name, m1, m2, m3, total, percent, grade = line.strip().split(",")
            print(f"""
Name       : {name}
Marks      : {m1}, {m2}, {m3}
Total      : {total}
Percentage : {percent}%
Grade      : {grade}
-------------------------
""")

def main():
    while True:
        print("=== STUDENT RESULT SYSTEM ===")
        print("1. Add Student")
        print("2. View Students")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid choice.\n")

if __name__ == "__main__":
    main()

