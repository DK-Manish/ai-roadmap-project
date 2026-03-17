def calculate_grade(avg):
    if avg >= 90:
        return "A"
    elif avg >= 75:
        return "B"
    elif avg >= 50:
        return "C"
    else:
        return "Fail"


def get_student_data():
    student_id = input("Enter Student ID: ")
    name = input("Enter Name: ")

    subjects = ["Maths", "Science", "English"]
    marks = []

    for subject in subjects:
        mark = int(input(f"Enter marks for {subject}: "))
        marks.append(mark)

    return student_id, name, marks


def create_student(student_id, name, marks):
    total = sum(marks)
    avg = total / len(marks)
    grade = calculate_grade(avg)

    return {
        "id": student_id,
        "name": name,
        "marks": marks,
        "average": avg,
        "grade": grade
    }


def print_report(student):
    print("\n--- Report Card ---")
    print(f"ID: {student['id']}")
    print(f"Name: {student['name']}")
    print(f"Marks: {student['marks']}")
    print(f"Average: {student['average']}")
    print(f"Grade: {student['grade']}")


def main():
    students = []
    num_students = int(input("Enter number of students: "))

    for _ in range(num_students):
        print("\nEnter student details:")
        student_id, name, marks = get_student_data()
        student = create_student(student_id, name, marks)
        students.append(student)

    print("\n====== All Report Cards ======")

    for student in students:
        print_report(student)


if __name__ == "__main__":
    main()