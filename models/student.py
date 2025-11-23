# models/student.py

class Student:
    __slots__ = ["__roll_no", "__name", "__age", "__grade", "__image"]

    def __init__(self, roll_no, name, age, grade, image=""):
        self.set_roll_no(roll_no)
        self.set_name(name)
        self.set_age(age)
        self.set_grade(grade)
        self.set_image(image)

    # ---- Getters ----
    def get_roll_no(self):
        return self.__roll_no

    def get_name(self):
        return self.__name

    def get_age(self):
        return self.__age

    def get_grade(self):
        return self.__grade

    def get_image(self):
        return self.__image

    # ---- Setters (with validation) ----
    def set_roll_no(self, roll_no):
        if not str(roll_no).isdigit():
            raise ValueError("Roll number must be numeric.")
        self.__roll_no = str(roll_no)

    def set_name(self, name):
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        self.__name = name.strip()

    def set_age(self, age):
        if not str(age).isdigit() or int(age) <= 0:
            raise ValueError("Age must be a positive number.")
        self.__age = int(age)

    def set_grade(self, grade):
        grade = grade.upper()
        if grade not in ["A", "B", "C", "D", "F"]:
            raise ValueError("Grade must be A, B, C, D, or F.")
        self.__grade = grade

    def set_image(self, image):
        # Accept empty string if no image uploaded
        self.__image = image.strip() if image else ""

    # Convert object → list for CSV
    def to_list(self):
        return [self.__roll_no, self.__name, self.__age, self.__grade, self.__image]
