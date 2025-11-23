# ui/app.py

import streamlit as st
import pandas as pd
import os
import sys

# Make models & services importable
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.student import Student
from services.student_manager import StudentManager

DATA_PATH = "students.csv"
IMG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images")
os.makedirs(IMG_DIR, exist_ok=True)

manager = StudentManager(DATA_PATH)

st.title("Student Management System")

menu = st.sidebar.selectbox(
    "Menu",
    ["Add Student", "View Students", "Search", "Update", "Delete", "Filter", "Sort", "Analytics"]
)

# -------------------------------- ADD --------------------------------
if menu == "Add Student":
    st.header("Add Student")
    roll = st.text_input("Roll No")
    name = st.text_input("Name")
    age = st.text_input("Age")
    grade = st.selectbox("Grade", ["A", "B", "C", "D", "F"])

    uploaded_image = st.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"])

    if st.button("Add"):
        image_path = ""
        if uploaded_image:
            image_path = os.path.join(IMG_DIR, uploaded_image.name)
            with open(image_path, "wb") as f:
                f.write(uploaded_image.getbuffer())

        try:
            stu = Student(roll, name, age, grade, image_path)
            if manager.add_student(stu):
                st.success("Student added successfully!")
            else:
                st.error("Roll number already exists!")
        except Exception as e:
            st.error(f"Validation error: {e}")

# -------------------------------- VIEW --------------------------------
elif menu == "View Students":
    st.header("All Students")

    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)

        for _, row in df.iterrows():
            cols = st.columns([1, 2, 1, 1, 2])
            cols[0].write(row["Roll No"])
            cols[1].write(row["Name"])
            cols[2].write(row["Age"])
            cols[3].write(row["Grade"])

            if os.path.exists(str(row["Image"])):
                cols[4].image(row["Image"], width=80)
            else:
                cols[4].write("No image")
    else:
        st.info("No student records found.")

# -------------------------------- SEARCH --------------------------------
elif menu == "Search":
    st.header("Search Student by Roll No")
    q = st.text_input("Roll No")

    if st.button("Search"):
        res = manager.search_student(q)
        if res:
            st.write(f"**Name:** {res[1]}")
            st.write(f"**Age:** {res[2]}")
            st.write(f"**Grade:** {res[3]}")

            if res[4] and os.path.exists(res[4]):
                st.image(res[4], width=150)
            else:
                st.info("No profile picture.")
        else:
            st.warning("Student not found.")

# -------------------------------- UPDATE --------------------------------
elif menu == "Update":
    st.header("Update Student")

    roll = st.text_input("Roll No to update")
    name = st.text_input("New Name")
    age = st.text_input("New Age")
    grade = st.selectbox("New Grade", ["A", "B", "C", "D", "F"])
    new_img = st.file_uploader("New Profile Picture (optional)", type=["jpg", "jpeg", "png"])

    if st.button("Update"):
        exists = manager.search_student(roll)

        if not exists:
            st.warning("Student not found.")
        else:
            image_path = exists[4]

            if new_img:
                image_path = os.path.join(IMG_DIR, new_img.name)
                with open(image_path, "wb") as f:
                    f.write(new_img.getbuffer())

            updated = manager.update_student(
                roll,
                {
                    "name": name or exists[1],
                    "age": age or exists[2],
                    "grade": grade or exists[3],
                    "image": image_path
                }
            )

            if updated:
                st.success("Student updated successfully!")
            else:
                st.error("Update failed.")

# -------------------------------- DELETE --------------------------------
elif menu == "Delete":
    st.header("Delete Student")

    roll = st.text_input("Roll No to delete")

    if st.button("Delete"):
        if manager.delete_student(roll):
            st.success("Student deleted.")
        else:
            st.warning("Student not found.")

# -------------------------------- FILTER --------------------------------
elif menu == "Filter":
    st.header("Filter Students")
    grade = st.selectbox("Grade", ["", "A", "B", "C", "D", "F"])
    min_age = st.number_input("Min Age", min_value=0, value=0)
    max_age = st.number_input("Max Age", min_value=0, value=0)

    if st.button("Apply"):
        results = manager.filter_students(
            grade if grade else None,
            min_age if min_age else None,
            max_age if max_age else None
        )
        if results:
            st.table(pd.DataFrame(results))
        else:
            st.info("No matching records.")

# -------------------------------- SORT --------------------------------
elif menu == "Sort":
    st.header("Sort Students")
    by = st.selectbox("Sort by", ["Name", "Age", "Grade", "Roll No"])

    if st.button("Sort"):
        sorted_list = manager.sort_students(by)
        st.table(pd.DataFrame(sorted_list))

# -------------------------------- ANALYTICS --------------------------------
elif menu == "Analytics":
    st.header("Analytics")

    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)

        st.subheader("Grade Distribution")
        st.bar_chart(df["Grade"].value_counts())

        st.subheader("Top Performers")
        order = {"A": 4, "B": 3, "C": 2, "D": 1, "F": 0}
        df["score"] = df["Grade"].map(order)
        st.table(df.sort_values("score", ascending=False).head(5))
    else:
        st.info("No data available.")
