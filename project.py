import streamlit as st
import csv
import os
from datetime import datetime

# ===============================
#  Student Management System
# ===============================

FILENAME = "students.csv"

# ---------- Helper Functions ----------

def load_data():
    """Load student data from CSV file."""
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = list(reader)

        # Ensure all expected keys exist
        fieldnames = [
            "Name", "Roll", "Course", "Gender", "DOB", "Email",
            "Phone", "Address", "Subjects", "Attendance", "Marks", "Grade"
        ]
        for row in data:
            for field in fieldnames:
                if field not in row:
                    row[field] = ""  # Fill missing fields
        return data

def save_data(data):
    """Save student data to CSV file."""
    fieldnames = [
        "Name", "Roll", "Course", "Gender", "DOB", "Email",
        "Phone", "Address", "Subjects", "Attendance", "Marks", "Grade"
    ]
    with open(FILENAME, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def calculate_grade(marks):
    """Auto-grade system based on marks."""
    try:
        marks = float(marks)
    except (ValueError, TypeError):
        marks = 0
    if marks >= 90:
        return "A"
    elif marks >= 75:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 40:
        return "D"
    else:
        return "F"

def add_student(name, roll, course, gender, dob, email, phone, address, subjects, attendance, marks):
    """Add new student record."""
    data = load_data()

    # Prevent duplicate roll numbers
    for s in data:
        if s.get("Roll") == roll:
            st.error(f"Roll number '{roll}' already exists. Please use a unique one.")
            return

    new_student = {
        "Name": name,
        "Roll": roll,
        "Course": course,
        "Gender": gender,
        "DOB": dob,
        "Email": email,
        "Phone": phone,
        "Address": address,
        "Subjects": subjects,
        "Attendance": str(attendance),
        "Marks": str(marks),
        "Grade": calculate_grade(marks)
    }
    data.append(new_student)
    save_data(data)

def delete_student(roll):
    """Delete a student by roll number."""
    data = load_data()
    updated_data = [row for row in data if row.get("Roll") != roll]
    save_data(updated_data)

def search_student(roll):
    """Search for a student by roll number."""
    data = load_data()
    for row in data:
        if row.get("Roll") == roll:
            return row
    return None

def update_student(roll, updated_info):
    """Update student details by roll number."""
    data = load_data()
    for i, row in enumerate(data):
        if row.get("Roll") == roll:
            data[i].update(updated_info)
            save_data(data)
            return True
    return False

# ---------- Streamlit UI ----------

st.set_page_config(page_title="🎓 Student Management System", layout="wide")
st.title("🎓 Student Management System")

menu = [
    "Dashboard",
    "Add Student",
    "View Students",
    "Search Student",
    "Update Student",
    "Delete Student"
]
choice = st.sidebar.radio("Menu", menu)

# ---------- Dashboard ----------
if choice == "Dashboard":
    st.header("📊 System Overview")

    data = load_data()
    total_students = len(data)

    avg_marks = round(
        sum(float(s.get("Marks", 0) or 0) for s in data) / total_students, 2
    ) if total_students else 0

    attendance_avg = round(
        sum(float(s.get("Attendance", 0) or 0) for s in data) / total_students, 2
    ) if total_students else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students", total_students)
    col2.metric("Average Marks", avg_marks)
    col3.metric("Avg Attendance %", attendance_avg)

    st.markdown("---")

    if os.path.exists(FILENAME):
        with open(FILENAME, "rb") as file:
            st.download_button("📥 Download Current CSV", data=file, file_name="students.csv")

# ---------- Add Student ----------
elif choice == "Add Student":
    st.subheader("Add New Student Record")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
        roll = st.text_input("Roll Number")
        course = st.text_input("Course")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])

        # Limit DOB between 1999 and 2020
        dob = st.date_input(
            "Date of Birth",
            value=datetime(2000, 1, 1).date(),
            min_value=datetime(1999, 1, 1).date(),
            max_value=datetime(2020, 12, 31).date()
        )

        marks = st.text_input("Marks (out of 100)")
        attendance = st.text_input("Attendance (%)")

    with col2:
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        address = st.text_area("Address")
        subjects = st.text_input("Subjects (comma-separated)")

    if st.button("✅ Add Student"):
        if name and roll and course:
            try:
                marks_val = float(marks) if marks else 0.0
                attendance_val = float(attendance) if attendance else 0.0

                add_student(
                    name, roll, course, gender, str(dob), email, phone, address, subjects, attendance_val, marks_val
                )

                st.success(f"🎉 Student '{name}' added successfully with grade '{calculate_grade(marks_val)}'!")
            except ValueError:
                st.error("❌ Please enter valid numeric values for Marks and Attendance.")
        else:
            st.warning("⚠️ Please fill all required fields.")

# ---------- View Students ----------
elif choice == "View Students":
    st.subheader("📋 All Student Records")
    data = load_data()
    if data:
        st.dataframe(data, use_container_width=True)
    else:
        st.info("No student records found yet.")

# ---------- Search Student ----------
elif choice == "Search Student":
    st.subheader("🔍 Search Student by Roll Number")
    roll = st.text_input("Enter Roll Number")
    if st.button("Search"):
        student = search_student(roll)
        if student:
            st.success("✅ Student Found:")
            st.json(student)
        else:
            st.error("❌ No student found with that Roll Number.")

# ---------- Update Student ----------
elif choice == "Update Student":
    st.subheader("✏️ Update Student Details")
    roll = st.text_input("Enter Roll Number to Update")
    student = search_student(roll)

    if student:
        st.info(f"Editing details for: {student['Name']}")
        name = st.text_input("Full Name", student.get("Name", ""))
        course = st.text_input("Course", student.get("Course", ""))

        gender_list = ["Male", "Female", "Other"]
        current_gender = student.get("Gender", "Male").strip().capitalize()
        if current_gender not in gender_list:
            current_gender = "Male"
        gender = st.selectbox("Gender", gender_list, index=gender_list.index(current_gender))

        try:
            existing_dob = datetime.strptime(student.get("DOB", ""), "%Y-%m-%d").date() if student.get("DOB") else datetime.today().date()
        except ValueError:
            existing_dob = datetime.today().date()

        dob = st.date_input("Date of Birth", value=existing_dob)
        marks = st.slider("Marks", 0, 100, int(float(student.get("Marks", 0) or 0)))
        attendance = st.slider("Attendance (%)", 0, 100, int(float(student.get("Attendance", 0) or 0)))
        address = st.text_area("Address", student.get("Address", ""))

        if st.button("💾 Save Changes"):
            updated_info = {
                "Name": name,
                "Course": course,
                "Gender": gender,
                "DOB": str(dob),
                "Marks": str(marks),
                "Attendance": str(attendance),
                "Grade": calculate_grade(marks),
                "Address": address
            }
            update_student(roll, updated_info)
            st.success(f"✅ Details for '{name}' updated successfully!")
    elif roll:
        st.warning("⚠️ No student found with that Roll Number.")

# ---------- Delete Student ----------
elif choice == "Delete Student":
    st.subheader("🗑️ Delete Student Record")
    roll = st.text_input("Enter Roll Number to Delete")
    if st.button("Delete"):
        data_before = load_data()
        delete_student(roll)
        data_after = load_data()
        if len(data_before) != len(data_after):
            st.success(f"✅ Student with Roll No '{roll}' deleted successfully.")
        else:
            st.error("❌ Roll number not found.")
