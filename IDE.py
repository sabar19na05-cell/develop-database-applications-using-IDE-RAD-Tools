import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
db = sqlite3.connect("employee_database.db")
cursor = db.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id      INTEGER PRIMARY KEY,
        name    TEXT,
        age     INTEGER,
        doj     TEXT,
        email   TEXT,
        gender  TEXT,
        contact TEXT,
        address TEXT
    )
''')
db.commit()
def add_employee():
    if not name_var.get() or not age_var.get():
        messagebox.showerror("Error", "Name and Age are required!")
        return
    cursor.execute(
        "INSERT INTO employees (name,age,doj,email,gender,contact,address) VALUES (?,?,?,?,?,?,?)",
        get_form_values()
    )
    db.commit()
    refresh_table()
    clear_form()
    messagebox.showinfo("Success", "Employee added!")
def update_employee():
    if not tv.focus():
        messagebox.showerror("Error", "Select a record first!")
        return
    row_id = tv.item(tv.focus())["values"][7]
    cursor.execute(
        "UPDATE employees SET name=?,age=?,doj=?,email=?,gender=?,contact=?,address=? WHERE id=?",
        (*get_form_values(), row_id)
    )
    db.commit()
    refresh_table()
    clear_form()
    messagebox.showinfo("Success", "Employee updated!")
def delete_employee():
    if not tv.focus():
        messagebox.showerror("Error", "Select a record first!")
        return
    if messagebox.askyesno("Confirm", "Delete this record?"):
        row_id = tv.item(tv.focus())["values"][7]
        cursor.execute("DELETE FROM employees WHERE id=?", (row_id,))
        db.commit()
        refresh_table()
        clear_form()
def get_form_values():
    return (
        name_var.get(),
        age_var.get(),
        doj_var.get(),
        email_var.get(),
        gender_var.get(),
        contact_var.get(),
        address_box.get("1.0", END).strip()
    )
def clear_form():
    name_var.set("")
    age_var.set("")
    doj_var.set("")
    email_var.set("")
    gender_var.set("Male")
    contact_var.set("")
    address_box.delete("1.0", END)
def load_selected(event):
    selected = tv.focus()
    if not selected:
        return
    v = tv.item(selected)["values"]
    clear_form()
    name_var.set(v[0])
    age_var.set(v[1])
    doj_var.set(v[2])
    email_var.set(v[3])
    gender_var.set(v[4])
    contact_var.set(v[5])
    address_box.insert("1.0", v[6])
def refresh_table():
    tv.delete(*tv.get_children())
    cursor.execute("SELECT name,age,doj,email,gender,contact,address,id FROM employees")
    for row in cursor.fetchall():
        tv.insert("", END, values=row)
root = Tk()
root.title("Employee Management System")
root.geometry("1000x680")
root.config(bg="#2c3e50")
form = Frame(root, bg="#34495e", padx=20, pady=15)
form.pack(fill=X, padx=10, pady=10)
name_var    = StringVar()
age_var     = StringVar()
doj_var     = StringVar()
email_var   = StringVar()
gender_var  = StringVar(value="Male")
contact_var = StringVar()
fields = [
    ("Name",    name_var,    0, 0),
    ("Age",     age_var,     2, 0),
    ("D.O.J",   doj_var,     4, 0),
    ("Email",   email_var,   0, 1),
    ("Contact", contact_var, 2, 1),
]
for label_text, var, col, row in fields:
    Label(form, text=label_text, font=("Calibri", 13, "bold"),
          bg="#34495e", fg="white").grid(row=row, column=col, sticky="e", padx=(10,4), pady=8)
    Entry(form, textvariable=var, font=("Calibri", 13),
          width=18).grid(row=row, column=col+1, sticky="w", padx=(0,10), pady=8)
Label(form, text="Gender", font=("Calibri", 13, "bold"),
      bg="#34495e", fg="white").grid(row=1, column=4, sticky="e", padx=(10,4), pady=8)
ttk.Combobox(form, textvariable=gender_var, values=["Male","Female","Other"],
             font=("Calibri", 13), width=10,
             state="readonly").grid(row=1, column=5, sticky="w", pady=8)
Label(form, text="Address", font=("Calibri", 13, "bold"),
      bg="#34495e", fg="white").grid(row=2, column=0, sticky="ne", padx=(10,4), pady=8)
address_box = Text(form, font=("Calibri", 13), width=60, height=3)
address_box.grid(row=2, column=1, columnspan=5, sticky="w", pady=8)
btn_frame = Frame(form, bg="#34495e")
btn_frame.grid(row=3, column=0, columnspan=6, pady=(5, 0))
buttons = [
    ("Add",    add_employee,    "#16a085"),
    ("Update", update_employee, "#2980b9"),
    ("Delete", delete_employee, "#c0392b"),
    ("Clear",  clear_form,      "#f39c12"),
]
for text, cmd, color in buttons:
    Button(btn_frame, text=text, command=cmd, width=12,
           font=("Calibri", 12, "bold"), bg=color, fg="white",
           bd=0, relief=FLAT, pady=6).pack(side=LEFT, padx=10)
table_frame = Frame(root, bg="#2c3e50")
table_frame.pack(fill=BOTH, expand=True, padx=10, pady=(0,10))
tv = ttk.Treeview(table_frame, show="headings",
                  columns=("1","2","3","4","5","6","7","8"))
Scrollbar(table_frame, orient=VERTICAL,   command=tv.yview).pack(side=RIGHT,  fill=Y)
Scrollbar(table_frame, orient=HORIZONTAL, command=tv.xview).pack(side=BOTTOM, fill=X)
tv.configure(yscrollcommand=lambda *a: None, xscrollcommand=lambda *a: None)
cols = [("Name",150),("Age",60),("D.O.J",100),("Email",180),
        ("Gender",80),("Contact",110),("Address",200),("ID",0)]
for i, (name, width) in enumerate(cols, 1):
    tv.heading(str(i), text=name)
    tv.column(str(i), width=width, minwidth=width, stretch=(i==7))
tv.bind("<ButtonRelease-1>", load_selected)
tv.pack(fill=BOTH, expand=True)
refresh_table()
root.mainloop()
