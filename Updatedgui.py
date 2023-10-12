import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Step 1: Create a Database
def create_database():
    conn = sqlite3.connect('blood_database.db')
    conn.close()

# Step 2: Define Tables
def create_tables():
    conn = sqlite3.connect('blood_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY,
            unique_id TEXT UNIQUE,
            name TEXT,
            blood_group TEXT,
            age INTEGER,
            contact_number TEXT,
            blood_amount REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipients (
            id INTEGER PRIMARY KEY,
            unique_id TEXT UNIQUE,
            name TEXT,
            blood_group TEXT,
            contact_number TEXT,
            blood_amount REAL
        )
    ''')

    conn.commit()
    conn.close()

# Step 3: Implement CRUD Operations for Donors
def add_donor(unique_id, name, blood_group, age, contact_number, blood_amount):
    conn = sqlite3.connect('blood_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO donors (unique_id, name, blood_group, age, contact_number, blood_amount)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (unique_id, name, blood_group, age, contact_number, blood_amount))

    conn.commit()
    conn.close()

def view_donors():
    conn = sqlite3.connect('blood_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM donors')
    donors = cursor.fetchall()

    conn.close()
    return donors

def update_donor(donor_id, unique_id, name, blood_group, age, contact_number, blood_amount):
    conn = sqlite3.connect('blood_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE donors
        SET unique_id=?, name=?, blood_group=?, age=?, contact_number=?, blood_amount=?
        WHERE id=?
    ''', (unique_id, name, blood_group, age, contact_number, blood_amount, donor_id))

    conn.commit()
    conn.close()

def delete_donor(donor_id):
    conn = sqlite3.connect('blood_database.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM donors WHERE id=?', (donor_id,))

    conn.commit()
    conn.close()

# Step 4: Implement CRUD Operations for Recipients
def create_recipient_table():
    conn = sqlite3.connect('blood_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipients (
            id INTEGER PRIMARY KEY,
            unique_id TEXT UNIQUE,
            name TEXT,
            blood_group TEXT,
            contact_number TEXT,
            blood_amount REAL
        )
    ''')

    conn.commit()
    conn.close()

def add_recipient(unique_id, name, blood_group, contact_number, blood_amount):
    conn = sqlite3.connect('blood_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO recipients (unique_id, name, blood_group, contact_number, blood_amount)
        VALUES (?, ?, ?, ?, ?)
    ''', (unique_id, name, blood_group, contact_number, blood_amount))

    conn.commit()
    conn.close()

def request_blood():
    unique_id = unique_id_entry.get()
    name = recipient_name_entry.get()
    blood_group = recipient_blood_group_entry.get()
    contact_number = recipient_contact_entry.get()
    blood_amount = blood_amount_entry.get()

    if unique_id and name and blood_group and contact_number and blood_amount:
        add_recipient(unique_id, name, blood_group, contact_number, blood_amount)
        messagebox.showinfo("Success", "Request submitted successfully!")
    else:
        messagebox.showerror("Error", "All fields are required.")

# Create the database and tables
create_database()
create_tables()

# GUI Functions
def add_donor_gui():
    unique_id = unique_id_entry.get()
    name = name_entry.get()
    blood_group = blood_group_entry.get()
    age = age_entry.get()
    contact_number = contact_entry.get()
    blood_amount = blood_amount_entry.get()

    if unique_id and name and blood_group and age and contact_number and blood_amount:
        add_donor(unique_id, name, blood_group, age, contact_number, blood_amount)
        messagebox.showinfo("Success", "Donor added successfully!")
    else:
        messagebox.showerror("Error", "All fields are required.")

def view_donors_gui():
    all_donors = view_donors()
    donor_listbox.delete(*donor_listbox.get_children())
    for donor in all_donors:
        donor_listbox.insert('', 'end', values=donor)

def update_donor_gui():
    selected_item = donor_listbox.selection()
    if not selected_item:
        messagebox.showerror("Error", "No donor selected.")
        return

    donor_id = donor_listbox.item(selected_item, 'values')[0]
    unique_id = unique_id_entry.get()
    name = name_entry.get()
    blood_group = blood_group_entry.get()
    age = age_entry.get()
    contact_number = contact_entry.get()
    blood_amount = blood_amount_entry.get()

    if donor_id and unique_id and name and blood_group and age and contact_number and blood_amount:
        update_donor(donor_id, unique_id, name, blood_group, age, contact_number, blood_amount)
        messagebox.showinfo("Success", "Donor updated successfully!")
        view_donors_gui()
    else:
        messagebox.showerror("Error", "All fields are required.")

def delete_donor_gui():
    selected_item = donor_listbox.selection()
    if not selected_item:
        messagebox.showerror("Error", "No donor selected.")
        return

    donor_id = donor_listbox.item(selected_item, 'values')[0]
    if donor_id:
        delete_donor(donor_id)
        messagebox.showinfo("Success", "Donor deleted successfully!")
        view_donors_gui()

# Create the GUI
root = tk.Tk()
root.title("Blood Donor Database")

style = ttk.Style()
style.configure('TLabel', font=('Helvetica', 12))
style.configure('TButton', font=('Helvetica', 12))
style.configure('TEntry', font=('Helvetica', 12))

# Labels and Entry fields for donors
name_label = ttk.Label(root, text="Name")
name_label.grid(row=0, column=0, padx=5, pady=5)
blood_group_label = ttk.Label(root, text="Blood Group")
blood_group_label.grid(row=0, column=1, padx=5, pady=5)
age_label = ttk.Label(root, text="Age")
age_label.grid(row=0, column=2, padx=5, pady=5)
contact_label = ttk.Label(root, text="Contact Number")
contact_label.grid(row=0, column=3, padx=5, pady=5)
unique_id_label = ttk.Label(root, text="Unique ID")
unique_id_label.grid(row=0, column=4, padx=5, pady=5)
blood_amount_label = ttk.Label(root, text="Blood Amount")
blood_amount_label.grid(row=0, column=5, padx=5, pady=5)

name_entry = ttk.Entry(root)
name_entry.grid(row=1, column=0, padx=5, pady=5)
blood_group_entry = ttk.Entry(root)
blood_group_entry.grid(row=1, column=1, padx=5, pady=5)
age_entry = ttk.Entry(root)
age_entry.grid(row=1, column=2, padx=5, pady=5)
contact_entry = ttk.Entry(root)
contact_entry.grid(row=1, column=3, padx=5, pady=5)
unique_id_entry = ttk.Entry(root)
unique_id_entry.grid(row=1, column=4, padx=5, pady=5)
blood_amount_entry = ttk.Entry(root)
blood_amount_entry.grid(row=1, column=5, padx=5, pady=5)

add_button = ttk.Button(root, text="Add Donor", command=add_donor_gui)
add_button.grid(row=2, column=0, padx=5, pady=5)
view_button = ttk.Button(root, text="View Donors", command=view_donors_gui)
view_button.grid(row=2, column=1, padx=5, pady=5)
update_button = ttk.Button(root, text="Update Donor", command=update_donor_gui)
update_button.grid(row=2, column=2, padx=5, pady=5)
delete_button = ttk.Button(root, text="Delete Donor", command=delete_donor_gui)
delete_button.grid(row=2, column=3, padx=5, pady=5)

donor_listbox = ttk.Treeview(root, columns=('ID', 'Unique ID', 'Name', 'Blood Group', 'Age', 'Contact Number', 'Blood Amount'), show='headings')
donor_listbox.heading('ID', text='ID')
donor_listbox.heading('Unique ID', text='Unique ID')
donor_listbox.heading('Name', text='Name')
donor_listbox.heading('Blood Group', text='Blood Group')
donor_listbox.heading('Age', text='Age')
donor_listbox.heading('Contact Number', text='Contact Number')
donor_listbox.heading('Blood Amount', text='Blood Amount')
donor_listbox.grid(row=3, column=0, columnspan=6, padx=5, pady=5)

# Labels and Entry fields for recipients
recipient_name_label = ttk.Label(root, text="Recipient Name")
recipient_name_label.grid(row=4, column=0, padx=5, pady=5)
recipient_name_entry = ttk.Entry(root)
recipient_name_entry.grid(row=4, column=1, padx=5, pady=5)

recipient_blood_group_label = ttk.Label(root, text="Blood Group")
recipient_blood_group_label.grid(row=4, column=2, padx=5, pady=5)
recipient_blood_group_entry = ttk.Entry(root)
recipient_blood_group_entry.grid(row=4, column=3, padx=5, pady=5)

recipient_contact_label = ttk.Label(root, text="Contact Number")
recipient_contact_label.grid(row=4, column=4, padx=5, pady=5)
recipient_contact_entry = ttk.Entry(root)
recipient_contact_entry.grid(row=4, column=5, padx=5, pady=5)

recipient_request_button = ttk.Button(root, text="Request Blood", command=request_blood)
recipient_request_button.grid(row=4, column=6, padx=5, pady=5)

root.mainloop()
