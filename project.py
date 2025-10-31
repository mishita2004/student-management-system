import streamlit as st
import csv
import os
from datetime import datetime

# ===============================
# 🎀 Student Management System (Cute Edition)
# ===============================

FILENAME = "students.csv"

# ---------- Custom CSS ----------
# ---------- Custom CSS ----------
st.markdown("""
    <style>
    /* Main Page Style */
    .main {
        background-color: #f9fafc;
        padding: 2rem;
        border-radius: 20px;
    }

    /* Title Style */
    h1 {
        color: #2C3E50;
        text-align: center;
        font-size: 2.5rem;
        background: linear-gradient(to right, #4facfe, #00f2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }

    /* Sidebar Style */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #4facfe, #00f2fe);
        color: white;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Buttons */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        color: white;
        border-radius: 12px;
        height: 3rem;
        font-size: 1rem;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(0, 114, 255, 0.3);
        transition: all 0.3s ease-in-out;
    }
    div.stButton > button:hover {
        transform: scale(1.05);
        background: linear-gradient(90deg, #0072ff, #00c6ff);
        box-shadow: 0px 4px 15px rgba(0,0,0,0.25);
    }

    /* Metrics Cards */
    div[data-testid="stMetricValue"] {
        color: #2C3E50;
        font-size: 1.8rem;
        font-weight: bold;
    }
    div[data-testid="stMetricLabel"] {
        color: #5D6D7E;
        font-size: 1rem;
    }

    /* Data Table */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }

    /* Input boxes */
    .stTextInput input, .stTextArea textarea, .stSelectbox select, .stDateInput input {
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }

    /* Divider line */
    hr, .stMarkdown hr {
        border: none;
        height: 2px;
        background: linear-gradient(to right, #4facfe, #00f2fe);
        border-radius: 2px;
        margin: 1.5rem 0;
    }

    </style>
""", unsafe_allow_html=True)


# ---------- Helper Functions ----------
def load_data():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def save_data(data):
    fieldnames = [
        "Name", "Roll", "Course", "Gender", "DOB", "Email",
        "Phone", "Address", "Subjects", "Attendance", "Marks", "Grade"
    ]
    with open(FILENAME, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def calculate_grade(marks):
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
    data = load_data()
    for s in data:
        if s.get("Roll") == roll:
            st.error(f"⚠️ Roll number '{roll}' already exists.")
            return
    data.append({
        "Name": name,
        "Roll": roll,
        "Course": course,
        "Gender": gender,
        "DOB": dob,
        "Email": email,
        "Phone": phone,
        "Address": address,
        "Subjects": subjects,
        "Attendance": attendance,
        "Marks": marks,
        "Grade": calculate_grade(marks)
    })
    save_data(data)

def delete_student(roll):
    data = load_data()
    updated = [row for row in data if row.get("Roll") != roll]
    save_data(updated)

def search_student(roll):
    data = load_data()
    for row in data:
        if row.get("Roll") == roll:
            return row
    return None

def update_student(roll, updated_info):
    data = load_data()
    for i, row in enumerate(data):
        if row.get("Roll") == roll:
            data[i].update(updated_info)
            save_data(data)
            return True
    return False

# ---------- Streamlit UI ----------
st.set_page_config(page_title="🎀 Student Management System", layout="wide")
st.title("🎀 Student Management System")

menu = [
    "🏠 Dashboard",
    "➕ Add Student",
    "📋 View Students",
    "🔍 Search Student",
    "✏️ Update Student",
    "🗑️ Delete Student"
]
choice = st.sidebar.radio("📁 Menu", menu)

# ---------- Dashboard ----------
if choice == "🏠 Dashboard":
    st.header("📊 System Overview")
    data = load_data()
    total = len(data)
    avg_marks = round(sum(float(s.get("Marks", 0) or 0) for s in data) / total, 2) if total else 0
    avg_att = round(sum(float(s.get("Attendance", 0) or 0) for s in data) / total, 2) if total else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("👩‍🎓 Total Students", total)
    col2.metric("📈 Average Marks", avg_marks)
    col3.metric("🕒 Avg Attendance (%)", avg_att)

    st.markdown("---")
    if os.path.exists(FILENAME):
        with open(FILENAME, "rb") as file:
            st.download_button("📥 Download CSV Data", data=file, file_name="students.csv")

# ---------- Add Student ----------
elif choice == "➕ Add Student":
    st.subheader("💖 Add New Student Record")
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Full Name")
        roll = st.text_input("Roll Number")
        course = st.text_input("Course")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        dob = st.date_input("Date of Birth", value=datetime(2000, 1, 1))
        marks = st.number_input("Marks (0-100)", 0, 100)
        attendance = st.number_input("Attendance (%)", 0, 100)

    with col2:
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        address = st.text_area("Address")
        subjects = st.text_input("Subjects (comma-separated)")

    if st.button("🌸 Add Student"):
        if name and roll and course:
            add_student(name, roll, course, gender, str(dob), email, phone, address, subjects, attendance, marks)
            st.success(f"🎉 Student '{name}' added successfully with Grade '{calculate_grade(marks)}'!")
        else:
            st.warning("⚠️ Please fill all required fields.")

# ---------- View Students ----------
elif choice == "📋 View Students":
    st.subheader("📄 All Student Records")
    data = load_data()
    if data:
        st.dataframe(data, use_container_width=True)
    else:
        st.info("No records found yet.")

# ---------- Search Student ----------
elif choice == "🔍 Search Student":
    st.subheader("🔎 Search Student by Roll Number")
    roll = st.text_input("Enter Roll Number")
    if st.button("💫 Search"):
        student = search_student(roll)
        if student:
            st.success("✅ Student Found:")
            st.json(student)
        else:
            st.error("❌ No student found.")

# ---------- Update Student ----------
elif choice == "✏️ Update Student":
    st.subheader("🎀 Update Student Details")
    roll = st.text_input("Enter Roll Number to Update")
    student = search_student(roll)

    if student:
        st.info(f"Editing details for: {student['Name']}")
        name = st.text_input("Full Name", student["Name"])
        course = st.text_input("Course", student["Course"])
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(student.get("Gender", "Male")))
        dob = st.date_input("Date of Birth", value=datetime.strptime(student["DOB"], "%Y-%m-%d"))
        marks = st.slider("Marks", 0, 100, int(float(student["Marks"])))
        attendance = st.slider("Attendance (%)", 0, 100, int(float(student["Attendance"])))
        address = st.text_area("Address", student["Address"])

        if st.button("💾 Save Changes"):
            updated_info = {
                "Name": name,
                "Course": course,
                "Gender": gender,
                "DOB": str(dob),
                "Marks": marks,
                "Attendance": attendance,
                "Grade": calculate_grade(marks),
                "Address": address
            }
            update_student(roll, updated_info)
            st.success(f"✅ '{name}' updated successfully!")

# ---------- Delete Student ----------
elif choice == "🗑️ Delete Student":
    st.subheader("💔 Delete Student Record")
    roll = st.text_input("Enter Roll Number to Delete")
    if st.button("❌ Delete"):
        before = load_data()
        delete_student(roll)
        after = load_data()
        if len(before) != len(after):
            st.success(f"✅ Roll No '{roll}' deleted successfully.")
        else:
            st.error("❌ Roll number not found.")
