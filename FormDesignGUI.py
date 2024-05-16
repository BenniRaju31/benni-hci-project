import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import csv

def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  
            database='ITDrivingSchool'
        )
        return connection
    except mysql.connector.Error as e:
        messagebox.showerror("Database Connection Error", str(e))
        return None

class DrivingSchoolApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pass IT Driving School Management System")
        self.geometry("1000x700")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.configure_styles()

        tab_control = ttk.Notebook(self)
        self.instructors_tab = ttk.Frame(tab_control)
        self.students_tab = ttk.Frame(tab_control)
        self.lessons_tab = ttk.Frame(tab_control)
        self.reports_tab = ttk.Frame(tab_control)

        tab_control.add(self.instructors_tab, text='Instructors')
        tab_control.add(self.students_tab, text='Students')
        tab_control.add(self.lessons_tab, text='Lessons')
        tab_control.add(self.reports_tab, text='Reports')

        tab_control.pack(expand=1, fill="both")

        self.create_instructors_ui()
        self.create_students_ui()
        self.create_lessons_ui()
        self.create_reports_ui()

        self.load_instructors_data()
        self.load_students_data()
        self.load_lessons_data()

    def configure_styles(self):
        self.style.configure("TFrame", background="#de4e68")
        self.style.configure("TButton", font=('Arial', 12), background="#0fd454", foreground="black", borderwidth=1)
        self.style.map("TButton", background=[('active','#f5940e')])  
        self.style.configure("TLabel", background="#4edec0", font=('Arial', 12))
        self.style.configure("Treeview", highlightthickness=0, bd=0, font=('Arial', 12))
        self.style.configure("Treeview.Heading", font=('Arial', 14, 'bold'))

    def create_instructors_ui(self):
        ttk.Label(self.instructors_tab, text='Instructor Details', font=('Arial', 15, 'bold')).grid(row=0, column=0, padx=10, pady=10)
        self.instructor_tree = ttk.Treeview(self.instructors_tab, columns=('ID', 'First Name', 'Last Name', 'Contact'), show='headings', selectmode="browse")
        for col in ('ID', 'First Name', 'Last Name', 'Contact'):
            self.instructor_tree.heading(col, text=col)
        self.instructor_tree.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
        ttk.Button(self.instructors_tab, text="Add Instructor", command=self.add_instructor).grid(row=2, column=0, padx=10, pady=10)
        ttk.Button(self.instructors_tab, text="Delete Instructor", command=self.delete_instructor).grid(row=2, column=1, padx=10, pady=10)

    def add_instructor(self):
        def save_instructor():
            first_name = first_name_var.get()
            last_name = last_name_var.get()
            contact = contact_var.get()
            conn = create_db_connection()
            if conn:
                cursor = conn.cursor()
                sql = "INSERT INTO Instructors (FirstName, LastName, PhoneNumber) VALUES (%s, %s, %s)"
                values = (first_name, last_name, contact)
                try:
                    cursor.execute(sql, values)
                    conn.commit()
                    messagebox.showinfo("Success", "Instructor added successfully!")
                    self.load_instructors_data()
                except mysql.connector.Error as e:
                    messagebox.showerror("Database Error", "Failed to add instructor\n" + str(e))
                finally:
                    conn.close()
            new_window.destroy()

        new_window = tk.Toplevel(self)
        new_window.title("Add New Instructor")

        tk.Label(new_window, text="First Name:").grid(row=0, column=0)
        first_name_var = tk.StringVar()
        tk.Entry(new_window, textvariable=first_name_var).grid(row=0, column=1)

        tk.Label(new_window, text="Last Name:").grid(row=1, column=0)
        last_name_var = tk.StringVar()
        tk.Entry(new_window, textvariable=last_name_var).grid(row=1, column=1)

        tk.Label(new_window, text="Contact Number:").grid(row=2, column=0)
        contact_var = tk.StringVar()
        tk.Entry(new_window, textvariable=contact_var).grid(row=2, column=1)

        save_button = tk.Button(new_window, text="Save", command=save_instructor)
        save_button.grid(row=3, column=1, pady=10)

    def delete_instructor(self):
        selected_item = self.instructor_tree.selection()
        if selected_item:
            item_values = self.instructor_tree.item(selected_item, "values")
            instructor_id = item_values[0]
            response = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this instructor?")
            if response:
                conn = create_db_connection()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM Instructors WHERE InstructorID = %s", (instructor_id,))
                    conn.commit()
                    conn.close()
                    self.instructor_tree.delete(selected_item)
                    messagebox.showinfo("Success", "Instructor deleted successfully!")

    def load_instructors_data(self):
        conn = create_db_connection()
        if conn:
            cursor = conn.cursor()
            query = "SELECT InstructorID, FirstName, LastName, PhoneNumber FROM Instructors"
            cursor.execute(query)
            rows = cursor.fetchall()
            self.instructor_tree.delete(*self.instructor_tree.get_children())  # Clear the existing data
            for row in rows:
                self.instructor_tree.insert("", tk.END, values=row)
            conn.close()

    def create_students_ui(self):
        ttk.Label(self.students_tab, text='Student Details', font=('Arial', 15, 'bold')).grid(row=0, column=0, padx=10, pady=10)
        self.student_tree = ttk.Treeview(self.students_tab, columns=('ID', 'First Name', 'Last Name', 'Contact', 'Email'), show='headings', selectmode="browse")
        for col in ('ID', 'First Name', 'Last Name', 'Contact', 'Email'):
            self.student_tree.heading(col, text=col)
        self.student_tree.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
        ttk.Button(self.students_tab, text="Add Student", command=self.add_student).grid(row=2, column=0, padx=10, pady=10)
        ttk.Button(self.students_tab, text="Delete Student", command=self.delete_student).grid(row=2, column=1, padx=10, pady=10)

    def add_student(self):
        def save_student():
            first_name = first_name_var.get()
            last_name = last_name_var.get()
            contact = contact_var.get()
            email = email_var.get()
            conn = create_db_connection()
            if conn:
                cursor = conn.cursor()
                sql = "INSERT INTO Students (FirstName, LastName, PhoneNumber, Email) VALUES (%s, %s, %s, %s)"
                values = (first_name, last_name, contact, email)
                try:
                    cursor.execute(sql, values)
                    conn.commit()
                    messagebox.showinfo("Success", "Student added successfully!")
                    self.load_students_data()
                except mysql.connector.Error as e:
                    messagebox.showerror("Database Error", "Failed to add student\n" + str(e))
                finally:
                    conn.close()
            new_window.destroy()

        new_window = tk.Toplevel(self)
        new_window.title("Add New Student")

        tk.Label(new_window, text="First Name:").grid(row=0, column=0)
        first_name_var = tk.StringVar()
        tk.Entry(new_window, textvariable=first_name_var).grid(row=0, column=1)

        tk.Label(new_window, text="Last Name:").grid(row=1, column=0)
        last_name_var = tk.StringVar()
        tk.Entry(new_window, textvariable=last_name_var).grid(row=1, column=1)

        tk.Label(new_window, text="Contact Number:").grid(row=2, column=0)
        contact_var = tk.StringVar()
        tk.Entry(new_window, textvariable=contact_var).grid(row=2, column=1)

        tk.Label(new_window, text="Email:").grid(row=3, column=0)
        email_var = tk.StringVar()
        tk.Entry(new_window, textvariable=email_var).grid(row=3, column=1)

        save_button = tk.Button(new_window, text="Save", command=save_student)
        save_button.grid(row=4, column=1, pady=10)

    def delete_student(self):
        selected_item = self.student_tree.selection()
        if selected_item:
            item_values = self.student_tree.item(selected_item, "values")
            student_id = item_values[0]
            response = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?")
            if response:
                conn = create_db_connection()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM Students WHERE StudentID = %s", (student_id,))
                    conn.commit()
                    conn.close()
                    self.student_tree.delete(selected_item)
                    messagebox.showinfo("Success", "Student deleted successfully!")

    def load_students_data(self):
        conn = create_db_connection()
        if conn:
            cursor = conn.cursor()
            query = "SELECT StudentID, FirstName, LastName, PhoneNumber, Email FROM Students"
            cursor.execute(query)
            rows = cursor.fetchall()
            self.student_tree.delete(*self.student_tree.get_children())  # Clear the existing data
            for row in rows:
                self.student_tree.insert("", tk.END, values=row)
            conn.close()

    def create_lessons_ui(self):
        ttk.Label(self.lessons_tab, text='Lesson Details', font=('Arial', 15, 'bold')).grid(row=0, column=0, padx=10, pady=10)
        self.lesson_tree = ttk.Treeview(self.lessons_tab, columns=('ID', 'InstructorID', 'StudentID', 'Type', 'Date', 'Duration'), show='headings', selectmode="browse")
        for col in ('ID', 'InstructorID', 'StudentID', 'Type', 'Date', 'Duration'):
            self.lesson_tree.heading(col, text=col)
        self.lesson_tree.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
        ttk.Button(self.lessons_tab, text="Add Lesson", command=self.add_lesson).grid(row=2, column=0, padx=10, pady=10)
        ttk.Button(self.lessons_tab, text="Delete Lesson", command=self.delete_lesson).grid(row=2, column=1, padx=10, pady=10)

    def add_lesson(self):
        def save_lesson():
            instructor_id = instructor_id_var.get()
            student_id = student_id_var.get()
            lesson_type = lesson_type_var.get()
            lesson_date = lesson_date_var.get()
            duration = duration_var.get()
            conn = create_db_connection()
            if conn:
                cursor = conn.cursor()
                sql = "INSERT INTO Lessons (InstructorID, StudentID, LessonType, LessonDate, DurationHours) VALUES (%s, %s, %s, %s, %s)"
                values = (instructor_id, student_id, lesson_type, lesson_date, duration)
                try:
                    cursor.execute(sql, values)
                    conn.commit()
                    messagebox.showinfo("Success", "Lesson added successfully!")
                    self.load_lessons_data()
                except mysql.connector.Error as e:
                    messagebox.showerror("Database Error", "Failed to add lesson\n" + str(e))
                finally:
                    conn.close()
            new_window.destroy()

        new_window = tk.Toplevel(self)
        new_window.title("Add New Lesson")

        tk.Label(new_window, text="Instructor ID:").grid(row=0, column=0)
        instructor_id_var = tk.StringVar()
        tk.Entry(new_window, textvariable=instructor_id_var).grid(row=0, column=1)

        tk.Label(new_window, text="Student ID:").grid(row=1, column=0)
        student_id_var = tk.StringVar()
        tk.Entry(new_window, textvariable=student_id_var).grid(row=1, column=1)

        tk.Label(new_window, text="Lesson Type:").grid(row=2, column=0)
        lesson_type_var = tk.StringVar()
        tk.Entry(new_window, textvariable=lesson_type_var).grid(row=2, column=1)

        tk.Label(new_window, text="Lesson Date (YYYY-MM-DD HH:MM):").grid(row=3, column=0)
        lesson_date_var = tk.StringVar()
        tk.Entry(new_window, textvariable=lesson_date_var).grid(row=3, column=1)

        tk.Label(new_window, text="Duration (Hours):").grid(row=4, column=0)
        duration_var = tk.StringVar()
        tk.Entry(new_window, textvariable=duration_var).grid(row=4, column=1)

        save_button = tk.Button(new_window, text="Save", command=save_lesson)
        save_button.grid(row=5, column=1, pady=10)

    def delete_lesson(self):
        selected_item = self.lesson_tree.selection()
        if selected_item:
            item_values = self.lesson_tree.item(selected_item, "values")
            lesson_id = item_values[0]
            response = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this lesson?")
            if response:
                conn = create_db_connection()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM Lessons WHERE LessonID = %s", (lesson_id,))
                    conn.commit()
                    conn.close()
                    self.lesson_tree.delete(selected_item)
                    messagebox.showinfo("Success", "Lesson deleted successfully!")

    def load_lessons_data(self):
        conn = create_db_connection()
        if conn:
            cursor = conn.cursor()
            query = "SELECT LessonID, InstructorID, StudentID, LessonType, LessonDate, DurationHours FROM Lessons"
            cursor.execute(query)
            rows = cursor.fetchall()
            self.lesson_tree.delete(*self.lesson_tree.get_children())  # Clear the existing data
            for row in rows:
                self.lesson_tree.insert("", tk.END, values=row)
            conn.close()

    def create_reports_ui(self):
        ttk.Label(self.reports_tab, text='Reports and Statistics', font=('Arial', 15, 'bold')).grid(row=0, column=0, padx=10, pady=10)
        ttk.Button(self.reports_tab, text="Generate Instructor Report", command=self.generate_instructor_report).grid(row=1, column=0, padx=10, pady=10)
        ttk.Button(self.reports_tab, text="Generate Revenue Report", command=self.generate_revenue_report).grid(row=2, column=0, padx=10, pady=10)

    def export_to_csv(self, data, headers, filename):
        with open(filename, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(headers)
            for row in data:
                csv_writer.writerow(row)
        messagebox.showinfo("Export Success", f"Data successfully exported to {filename}")

    def export_to_txt(self, data, headers, filename):
        with open(filename, 'w') as file:
            file.write('\t'.join(headers) + '\n')
            for row in data:
                file.write('\t'.join(str(x) for x in row) + '\n')
        messagebox.showinfo("Export Success", f"Data successfully exported to {filename}")

    def generate_instructor_report(self):
        connection = create_db_connection()
        if connection:
            cursor = connection.cursor()
            query = """
            SELECT i.InstructorID, i.FirstName, i.LastName, COUNT(l.LessonID) AS TotalLessons
            FROM Instructors i
            LEFT JOIN Lessons l ON i.InstructorID = l.InstructorID
            GROUP BY i.InstructorID;
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            headers = ['InstructorID', 'FirstName', 'LastName', 'TotalLessons']
            report_window = tk.Toplevel(self)
            report_window.title("Instructor Report")
            tree = ttk.Treeview(report_window, columns=headers, show='headings')
            for col in headers:
                tree.heading(col, text=col)
            for row in rows:
                tree.insert("", tk.END, values=row)
            tree.pack(expand=True, fill='both')
            
            ttk.Button(report_window, text="Export to CSV", command=lambda: self.export_to_csv(rows, headers, 'InstructorReport.csv')).pack(pady=5)
            ttk.Button(report_window, text="Export to TXT", command=lambda: self.export_to_txt(rows, headers, 'InstructorReport.txt')).pack(pady=5)

            connection.close()

    def generate_revenue_report(self):
        connection = create_db_connection()
        if connection:
            cursor = connection.cursor()
            query = """
            SELECT LessonType, COUNT(LessonID) AS TotalLessons, COUNT(LessonID) * 50 AS EstimatedRevenue
            FROM Lessons
            GROUP BY LessonType;
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            headers = ['LessonType', 'TotalLessons', 'EstimatedRevenue']
            report_window = tk.Toplevel(self)
            report_window.title("Revenue Report")
            tree = ttk.Treeview(report_window, columns=headers, show='headings')
            for col in headers:
                tree.heading(col, text=col)
            for row in rows:
                tree.insert("", tk.END, values=row)
            tree.pack(expand=True, fill='both')
            
            ttk.Button(report_window, text="Export to CSV", command=lambda: self.export_to_csv(rows, headers, 'RevenueReport.csv')).pack(pady=5)
            ttk.Button(report_window, text="Export to TXT", command=lambda: self.export_to_txt(rows, headers, 'RevenueReport.txt')).pack(pady=5)

            connection.close()


if __name__ == "__main__":
    app = DrivingSchoolApp()
    app.mainloop()
