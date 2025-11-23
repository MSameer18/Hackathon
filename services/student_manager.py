# services/student_manager.py

import csv
import os
from collections import Counter
import matplotlib.pyplot as plt

class StudentManager:
    def __init__(self, filename="students.csv"):
        self.filename = filename
        
        # services/student_manager.py
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Roll No", "Name", "Age", "Grade", "Image"])
 

    # ---------------- CREATE -----------------
    def add_student(self, student):
        if self.search_student(student.get_roll_no()):
            print(f"Student with roll no {student.get_roll_no()} already exists!")
            return
        with open(self.filename, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(student.to_list())
        print("Student added successfully!")

    # ---------------- READ -----------------
    def view_students(self):
        if not os.path.exists(self.filename):
            print("No student records found.")
            return
        with open(self.filename, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                print(row)

    # ---------------- SEARCH -----------------
    def search_student(self, roll_no):
        if not os.path.exists(self.filename):
            return None
        with open(self.filename, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == roll_no:
                    return row
        return None

    # ---------------- UPDATE -----------------
    def update_student(self, roll_no, updated_data):
        updated = False
        with open(self.filename, "r") as file:
            reader = csv.reader(file)
            rows = list(reader)

        for i in range(1, len(rows)):
            if rows[i][0] == roll_no:
                rows[i] = [
                    roll_no,
                    updated_data["name"],
                    updated_data["age"],
                    updated_data["grade"]
                ]
                updated = True

        if updated:
            with open(self.filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            print("Student updated successfully!")
        else:
            print("Student not found.")

    # ---------------- DELETE -----------------
    def delete_student(self, roll_no):
        deleted = False
        with open(self.filename, "r") as file:
            reader = csv.reader(file)
            rows = list(reader)

        new_rows = [rows[0]]  # keep header
        for row in rows[1:]:
            if row[0] != roll_no:
                new_rows.append(row)
            else:
                deleted = True

        if deleted:
            with open(self.filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(new_rows)
            print("Student deleted successfully!")
        else:
            print("Student not found.")

    # ---------------- FILTER -----------------
    def filter_students(self, grade=None, min_age=None, max_age=None):
        results = []
        if not os.path.exists(self.filename):
            return results
        with open(self.filename, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if grade and row["Grade"].upper() != grade.upper():
                    continue
                if min_age and int(row["Age"]) < min_age:
                    continue
                if max_age and int(row["Age"]) > max_age:
                    continue
                results.append(row)
        return results

    # ---------------- SORT -----------------
    def sort_students(self, by="Name"):
        students = []
        if not os.path.exists(self.filename):
            return students
        with open(self.filename, "r") as file:
            reader = csv.DictReader(file)
            students = list(reader)
        return sorted(students, key=lambda x: x[by])

    # ---------------- ANALYTICS -----------------
    def grade_distribution(self):
        if not os.path.exists(self.filename):
            print("No student data.")
            return
        with open(self.filename, "r") as file:
            reader = csv.DictReader(file)
            grades = [row["Grade"] for row in reader]
        dist = Counter(grades)
        print("Grade Distribution:", dict(dist))

        # Plot chart
        plt.figure(figsize=(6,4))
        plt.bar(dist.keys(), dist.values(), color='skyblue')
        plt.title("Grade Distribution")
        plt.xlabel("Grade")
        plt.ylabel("Number of Students")
        plt.show()

    def top_performers(self, n=3):
        if not os.path.exists(self.filename):
            print("No student data.")
            return
        grade_order = {"A":4, "B":3, "C":2, "D":1, "F":0}
        with open(self.filename, "r") as file:
            reader = csv.DictReader(file)
            students = list(reader)
        students_sorted = sorted(students, key=lambda x: grade_order[x["Grade"]], reverse=True)
        print(f"Top {n} Performers:")
        for student in students_sorted[:n]:
            print(student)

    def bottom_performers(self, n=3):
        if not os.path.exists(self.filename):
            print("No student data.")
            return
        grade_order = {"A":4, "B":3, "C":2, "D":1, "F":0}
        with open(self.filename, "r") as file:
            reader = csv.DictReader(file)
            students = list(reader)
        students_sorted = sorted(students, key=lambda x: grade_order[x["Grade"]])
        print(f"Bottom {n} Performers:")
        for student in students_sorted[:n]:
            print(student)
