"""
Developed by MASA
All Rights Reserved.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

conn = sqlite3.connect("class_schedule.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT UNIQUE,
    name TEXT,
    course TEXT,
    year TEXT,
    section TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT,
    teacher TEXT,
    course TEXT,
    year TEXT,
    section TEXT,
    day TEXT,
    start_time TEXT,
    end_time TEXT,
    room TEXT
)
""")

cursor.execute("SELECT * FROM admin")
if not cursor.fetchall():
    cursor.execute("INSERT INTO admin (username,password) VALUES (?,?)", ("admin", "admin123"))

cursor.execute("SELECT * FROM students")
if not cursor.fetchall():
    cursor.executemany(
        "INSERT INTO students (student_id,name,course,year,section) VALUES (?,?,?,?,?)",
        [
            ("2023-001", "Juan Dela Cruz", "BSCS", "1", "A"),
            ("2023-002", "Maria Santos", "BSIT", "2", "B"),
            ("2023-003", "Pedro Reyes", "BSCS", "1", "A"),
        ],
    )

conn.commit()


def apply_style():
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", rowheight=28)
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
    style.configure("TButton", padding=6)


def login_screen():
    root = tk.Tk()
    root.title("MASA - Class Scheduling System")
    root.geometry("400x320")
    apply_style()

    ttk.Label(root, text="Class Scheduling System", font=("Segoe UI", 16, "bold")).pack(pady=20)
    ttk.Button(root, text="Admin Login", command=lambda: [root.destroy(), admin_login()]).pack(
        fill="x", padx=60, pady=10
    )
    ttk.Button(root, text="Student Access", command=lambda: [root.destroy(), student_login()]).pack(
        fill="x", padx=60
    )
    root.mainloop()


def admin_login():
    root = tk.Tk()
    root.title("MASA - Admin Login")
    root.geometry("350x250")
    apply_style()
    user = tk.StringVar()
    pwd = tk.StringVar()

    def login():
        cursor.execute("SELECT * FROM admin WHERE username=? AND password=?", (user.get(), pwd.get()))
        if cursor.fetchone():
            root.destroy()
            admin_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    frame = ttk.Frame(root, padding=20)
    frame.pack(expand=True)
    ttk.Label(frame, text="Admin Login", font=("Segoe UI", 14, "bold")).pack(pady=10)
    ttk.Entry(frame, textvariable=user).pack(fill="x", pady=5)
    ttk.Entry(frame, textvariable=pwd, show="*").pack(fill="x", pady=5)
    ttk.Button(frame, text="Login", command=login).pack(fill="x", pady=10)
    ttk.Button(frame, text="Back", command=lambda: [root.destroy(), login_screen()]).pack(fill="x")
    root.mainloop()


def student_login():
    root = tk.Tk()
    root.title("MASA - Student Access")
    root.geometry("350x250")
    apply_style()
    sid = tk.StringVar()

    def access():
        cursor.execute("SELECT * FROM students WHERE student_id=?", (sid.get(),))
        student = cursor.fetchone()
        if student:
            root.destroy()
            student_view(student)
        else:
            messagebox.showerror("Denied", "Invalid Student ID")

    frame = ttk.Frame(root, padding=20)
    frame.pack(expand=True)
    ttk.Label(frame, text="Student Access", font=("Segoe UI", 14, "bold")).pack(pady=10)
    ttk.Entry(frame, textvariable=sid).pack(fill="x", pady=5)
    ttk.Button(frame, text="View Schedule", command=access).pack(fill="x", pady=10)
    ttk.Button(frame, text="Back", command=lambda: [root.destroy(), login_screen()]).pack(fill="x")
    root.mainloop()


def admin_dashboard():
    root = tk.Tk()
    root.title("MASA - Admin Dashboard")
    root.geometry("400x320")
    apply_style()
    frame = ttk.Frame(root, padding=20)
    frame.pack(expand=True)
    ttk.Label(frame, text="Admin Dashboard", font=("Segoe UI", 16, "bold")).pack(pady=15)
    ttk.Button(frame, text="Manage Schedule", command=lambda: [root.destroy(), admin_schedule()]).pack(
        fill="x", pady=5
    )
    ttk.Button(frame, text="Manage Students", command=lambda: [root.destroy(), manage_students()]).pack(
        fill="x", pady=5
    )
    ttk.Button(frame, text="Logout", command=lambda: [root.destroy(), login_screen()]).pack(fill="x", pady=20)
    root.mainloop()


def manage_students():
    root = tk.Tk()
    root.title("MASA - Manage Students")
    root.geometry("750x500")
    apply_style()
    sid = tk.StringVar()
    name = tk.StringVar()
    course = tk.StringVar()
    year = tk.StringVar()
    section = tk.StringVar()

    def load():
        tree.delete(*tree.get_children())
        cursor.execute("SELECT * FROM students")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    def add():
        try:
            cursor.execute(
                "INSERT INTO students (student_id,name,course,year,section) VALUES (?,?,?,?,?)",
                (sid.get(), name.get(), course.get(), year.get(), section.get()),
            )
            conn.commit()
            load()
            sid.set("")
            name.set("")
            course.set("")
            year.set("")
            section.set("")
        except:
            messagebox.showerror("Error", "Student ID already exists")

    def delete():
        selected = tree.focus()
        if not selected:
            return
        cursor.execute("DELETE FROM students WHERE id=?", (tree.item(selected)["values"][0],))
        conn.commit()
        load()

    header = ttk.Frame(root, padding=10)
    header.pack(fill="x")
    ttk.Label(header, text="Manage Students", font=("Segoe UI", 16, "bold")).pack(side="left")
    ttk.Button(header, text="Back", command=lambda: [root.destroy(), admin_dashboard()]).pack(side="right")

    form = ttk.LabelFrame(root, text="Add Student", padding=10)
    form.pack(fill="x", padx=10)
    ttk.Label(form, text="Student ID").grid(row=0, column=0)
    ttk.Entry(form, textvariable=sid).grid(row=0, column=1, padx=5)
    ttk.Label(form, text="Name").grid(row=0, column=2)
    ttk.Entry(form, textvariable=name).grid(row=0, column=3, padx=5)
    ttk.Label(form, text="Course").grid(row=1, column=0)
    ttk.Entry(form, textvariable=course).grid(row=1, column=1, padx=5)
    ttk.Label(form, text="Year").grid(row=1, column=2)
    ttk.Entry(form, textvariable=year).grid(row=1, column=3, padx=5)
    ttk.Label(form, text="Section").grid(row=2, column=0)
    ttk.Entry(form, textvariable=section).grid(row=2, column=1, padx=5)
    ttk.Button(form, text="Add Student", command=add).grid(row=2, column=3, padx=10, pady=5)

    table_frame = ttk.Frame(root, padding=10)
    table_frame.pack(fill="both", expand=True)
    scrollbar = ttk.Scrollbar(table_frame)
    tree = ttk.Treeview(
        table_frame,
        columns=("ID", "Student ID", "Name", "Course", "Year", "Section"),
        show="headings",
        yscrollcommand=scrollbar.set,
    )
    scrollbar.config(command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)
    for col in ("ID", "Student ID", "Name", "Course", "Year", "Section"):
        tree.heading(col, text=col)
        tree.column(col, width=120)
    ttk.Button(root, text="Delete Selected", command=delete).pack(pady=5)
    load()
    root.mainloop()


def admin_schedule():
    root = tk.Tk()
    root.title("MASA - Manage Schedule")
    root.geometry("1050x600")
    apply_style()

    subject = tk.StringVar()
    teacher = tk.StringVar()
    course = tk.StringVar()
    year = tk.StringVar()
    section = tk.StringVar()
    day = tk.StringVar()
    start_hour = tk.StringVar(value="08")
    start_minute = tk.StringVar(value="00")
    end_hour = tk.StringVar(value="09")
    end_minute = tk.StringVar(value="00")
    room = tk.StringVar()

    def load_data():
        tree.delete(*tree.get_children())
        cursor.execute("SELECT * FROM schedule")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    def add_schedule():
        start_time = f"{start_hour.get()}:{start_minute.get()}"
        end_time = f"{end_hour.get()}:{end_minute.get()}"
        cursor.execute(
            """INSERT INTO schedule 
            (subject,teacher,course,year,section,day,start_time,end_time,room)
            VALUES (?,?,?,?,?,?,?,?,?)""",
            (
                subject.get(),
                teacher.get(),
                course.get(),
                year.get(),
                section.get(),
                day.get(),
                start_time,
                end_time,
                room.get(),
            ),
        )
        conn.commit()
        load_data()

    def update_schedule():
        selected = tree.focus()
        if not selected:
            return
        rid = tree.item(selected)["values"][0]
        start_time = f"{start_hour.get()}:{start_minute.get()}"
        end_time = f"{end_hour.get()}:{end_minute.get()}"
        cursor.execute(
            """UPDATE schedule SET 
            subject=?,teacher=?,course=?,year=?,section=?,day=?,start_time=?,end_time=?,room=? 
            WHERE id=?""",
            (
                subject.get(),
                teacher.get(),
                course.get(),
                year.get(),
                section.get(),
                day.get(),
                start_time,
                end_time,
                room.get(),
                rid,
            ),
        )
        conn.commit()
        load_data()

    def delete_schedule():
        selected = tree.focus()
        if not selected:
            return
        cursor.execute("DELETE FROM schedule WHERE id=?", (tree.item(selected)["values"][0],))
        conn.commit()
        load_data()

    def select_row(e):
        values = tree.item(tree.focus())["values"]
        if values:
            subject.set(values[1])
            teacher.set(values[2])
            course.set(values[3])
            year.set(values[4])
            section.set(values[5])
            day.set(values[6])
            start_hour.set(values[7].split(":")[0])
            start_minute.set(values[7].split(":")[1])
            end_hour.set(values[8].split(":")[0])
            end_minute.set(values[8].split(":")[1])
            room.set(values[9])

    header = ttk.Frame(root, padding=10)
    header.pack(fill="x")
    ttk.Label(header, text="Schedule Management", font=("Segoe UI", 16, "bold")).pack(side="left")
    ttk.Button(header, text="Back", command=lambda: [root.destroy(), admin_dashboard()]).pack(side="right")

    form = ttk.LabelFrame(root, text="Schedule Details", padding=10)
    form.pack(fill="x", padx=10, pady=5)

    ttk.Label(form, text="Subject").grid(row=0, column=0)
    ttk.Entry(form, textvariable=subject).grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(form, text="Teacher").grid(row=0, column=2)
    ttk.Entry(form, textvariable=teacher).grid(row=0, column=3, padx=5, pady=5)
    ttk.Label(form, text="Course").grid(row=1, column=0)
    ttk.Entry(form, textvariable=course).grid(row=1, column=1)
    ttk.Label(form, text="Year").grid(row=1, column=2)
    ttk.Entry(form, textvariable=year).grid(row=1, column=3)
    ttk.Label(form, text="Section").grid(row=2, column=0)
    ttk.Entry(form, textvariable=section).grid(row=2, column=1)
    ttk.Label(form, text="Day").grid(row=2, column=2)
    ttk.Combobox(
        form,
        textvariable=day,
        values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        state="readonly",
    ).grid(row=2, column=3)
    ttk.Label(form, text="Start Time").grid(row=3, column=0)
    ttk.Combobox(form, textvariable=start_hour, values=[f"{i:02d}" for i in range(24)], width=5).grid(
        row=3, column=1, sticky="w"
    )
    ttk.Combobox(form, textvariable=start_minute, values=["00", "15", "30", "45"], width=5).grid(
        row=3, column=1, sticky="e"
    )
    ttk.Label(form, text="End Time").grid(row=3, column=2)
    ttk.Combobox(form, textvariable=end_hour, values=[f"{i:02d}" for i in range(24)], width=5).grid(
        row=3, column=3, sticky="w"
    )
    ttk.Combobox(form, textvariable=end_minute, values=["00", "15", "30", "45"], width=5).grid(
        row=3, column=3, sticky="e"
    )
    ttk.Label(form, text="Room").grid(row=4, column=0)
    ttk.Entry(form, textvariable=room).grid(row=4, column=1, padx=5, pady=5)
    ttk.Button(form, text="Add", command=add_schedule).grid(row=5, column=0, pady=10)
    ttk.Button(form, text="Update", command=update_schedule).grid(row=5, column=1)
    ttk.Button(form, text="Delete", command=delete_schedule).grid(row=5, column=2)

    table_frame = ttk.Frame(root, padding=10)
    table_frame.pack(fill="both", expand=True, padx=10, pady=5)
    scrollbar = ttk.Scrollbar(table_frame)
    tree = ttk.Treeview(
        table_frame,
        columns=("ID", "Subject", "Teacher", "Course", "Year", "Section", "Day", "Start", "End", "Room"),
        show="headings",
        yscrollcommand=scrollbar.set,
    )
    scrollbar.config(command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)
    for col in ("ID", "Subject", "Teacher", "Course", "Year", "Section", "Day", "Start", "End", "Room"):
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.bind("<<TreeviewSelect>>", select_row)
    load_data()
    root.mainloop()


def student_view(student):
    root = tk.Tk()
    root.title("MASA - Student Schedule")
    root.geometry("1050x500")
    apply_style()

    course, year, section = student[3], student[4], student[5]

    tree = ttk.Treeview(
        root,
        columns=("ID", "Subject", "Teacher", "Course", "Year", "Section", "Day", "Start", "End", "Room"),
        show="headings",
    )
    tree.pack(fill="both", expand=True, padx=10, pady=10)
    for col in ("ID", "Subject", "Teacher", "Course", "Year", "Section", "Day", "Start", "End", "Room"):
        tree.heading(col, text=col)
        tree.column(col, width=100)

    cursor.execute("SELECT * FROM schedule WHERE course=? AND year=? AND section=?", (course, year, section))
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

    ttk.Button(root, text="Logout", command=lambda: [root.destroy(), login_screen()]).pack(pady=10)
    root.mainloop()


login_screen()
conn.close()
