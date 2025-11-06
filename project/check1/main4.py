import pandas as pd
import numpy as np
from datetime import datetime
from tabulate import tabulate
import os

# ==========================================================
# GLOBAL FILES
ROOM_FILE = "rooms.csv"
BOOKING_FILE = "bookings.csv"
CUSTOMER_FILE = "customers.csv"
BILL_FILE = "bills.csv"
STAFF_FILE = "staff.csv"

ROOM_COLUMNS = ["RoomID", "RoomType", "Price", "Status"]
BOOK_COLUMNS = ["BookingID", "CustomerName", "RoomID", "CheckIn", "CheckOut"]
CUSTOMER_COLUMNS = ["CustomerID", "Name", "Phone", "Email", "RoomID", "DaysOfStay", "RegDate"]
BILL_COLUMNS = ["BillID", "CustomerID", "Name", "RoomID", "DaysOfStay", "PricePerDay", "TotalAmount", "BillDate"]
STAFF_COLUMNS = ["StaffID", "Name", "Role", "Contact", "Salary", "JoinDate"]

# ==========================================================
# 🧰 Helper Functions
# ==========================================================
def load_csv(filename, columns):
    # Auto-create or repair missing/empty CSVs
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        df = pd.DataFrame(columns=columns)
        df.to_csv(filename, index=False)
        return df
    try:
        df = pd.read_csv(filename, dtype=str)
    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=columns)
        df.to_csv(filename, index=False)
    for col in columns:
        if col not in df.columns:
            df[col] = ""
    return df[columns]

def save_csv(filename, df):
    df.to_csv(filename, index=False)

# ==========================================================
# 🧾 CUSTOMER MANAGEMENT
# ==========================================================
def add_customer():
    df = load_csv(CUSTOMER_FILE, CUSTOMER_COLUMNS)
    name = input("Enter Customer Name: ").strip()
    phone = input("Enter Phone Number: ").strip()
    email = input("Enter Email: ").strip()
    room_id = input("Enter Room ID (if any): ").strip()
    try:
        days = int(input("Enter Days of Stay: "))
    except ValueError:
        days = 0
    cust_id = "C" + str(np.random.randint(1000, 9999))
    reg_date = datetime.today().strftime("%Y-%m-%d")
    new_row = pd.DataFrame([[cust_id, name, phone, email, room_id, days, reg_date]], columns=CUSTOMER_COLUMNS)
    df = pd.concat([df, new_row], ignore_index=True)
    save_csv(CUSTOMER_FILE, df)
    print(f"✅ Customer {name} added successfully! Customer ID: {cust_id}")

def view_customers():
    df = load_csv(CUSTOMER_FILE, CUSTOMER_COLUMNS)
    if df.empty:
        print("❌ No customers found.")
    else:
        print("\n📋 CUSTOMER RECORDS 📋")
        print(tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))

def search_customer():
    df = load_csv(CUSTOMER_FILE, CUSTOMER_COLUMNS)
    key = input("Enter Customer ID / Name / Phone to search: ").strip().lower()
    result = df[df.apply(lambda row: key in row.astype(str).str.lower().values, axis=1)]
    if result.empty:
        print("❌ No matching customer found.")
    else:
        print(tabulate(result, headers="keys", tablefmt="fancy_grid", showindex=False))

def update_customer():
    df = load_csv(CUSTOMER_FILE, CUSTOMER_COLUMNS)
    cid = input("Enter Customer ID to update: ").strip()
    if cid not in df["CustomerID"].values:
        print("❌ Customer not found.")
        return
    print("Leave fields blank to keep old values.")
    new_phone = input("New Phone: ").strip()
    new_email = input("New Email: ").strip()
    new_room = input("New Room ID: ").strip()
    new_days = input("New Days of Stay: ").strip()

    mask = df["CustomerID"] == cid
    if new_phone: df.loc[mask, "Phone"] = new_phone
    if new_email: df.loc[mask, "Email"] = new_email
    if new_room: df.loc[mask, "RoomID"] = new_room
    if new_days: df.loc[mask, "DaysOfStay"] = new_days
    save_csv(CUSTOMER_FILE, df)
    print("✅ Customer updated successfully.")

def delete_customer():
    df = load_csv(CUSTOMER_FILE, CUSTOMER_COLUMNS)
    cid = input("Enter Customer ID to delete: ").strip()
    if cid not in df["CustomerID"].values:
        print("❌ Customer not found.")
        return
    df = df[df["CustomerID"] != cid]
    save_csv(CUSTOMER_FILE, df)
    print("✅ Customer deleted successfully.")

def customer_menu():
    while True:
        print("\n--- CUSTOMER MANAGEMENT ---")
        print("1. Add Customer")
        print("2. View Customers")
        print("3. Search Customer")
        print("4. Update Customer")
        print("5. Delete Customer")
        print("6. Back")
        ch = input("Enter your choice: ")
        if ch == "1": add_customer()
        elif ch == "2": view_customers()
        elif ch == "3": search_customer()
        elif ch == "4": update_customer()
        elif ch == "5": delete_customer()
        elif ch == "6": break
        else: print("❌ Invalid input.")

# ==========================================================
# 🏨 ROOM MANAGEMENT
# ==========================================================
def add_room():
    df = load_csv(ROOM_FILE, ROOM_COLUMNS)
    room_id = input("Enter Room ID: ").strip()
    if room_id in df["RoomID"].values:
        print("❌ Room already exists.")
        return
    room_type = input("Enter Room Type (Single/Double/Suite): ").capitalize()
    price = float(input("Enter Price: "))
    new_row = pd.DataFrame([[room_id, room_type, price, "Available"]], columns=ROOM_COLUMNS)
    df = pd.concat([df, new_row], ignore_index=True)
    save_csv(ROOM_FILE, df)
    print("✅ Room added successfully.")

def update_room():
    df = load_csv(ROOM_FILE, ROOM_COLUMNS)
    room_id = input("Enter Room ID to update: ").strip()
    if room_id not in df["RoomID"].values:
        print("❌ Room not found.")
        return
    new_price = float(input("Enter new Price: "))
    new_status = input("Enter new Status (Available/Booked): ").capitalize()
    df.loc[df["RoomID"] == room_id, ["Price", "Status"]] = [new_price, new_status]
    save_csv(ROOM_FILE, df)
    print("✅ Room updated successfully.")

def view_all_rooms():
    df = load_csv(ROOM_FILE, ROOM_COLUMNS)
    if df.empty:
        print("No rooms available yet.")
    else:
        print("\n🏨 ALL ROOMS 🏨")
        print(tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))

def show_available_rooms():
    df = load_csv(ROOM_FILE, ROOM_COLUMNS)
    available = df[df["Status"].str.lower() == "available"]
    if available.empty:
        print("❌ No available rooms.")
    else:
        print("\n--- AVAILABLE ROOMS ---")
        print(tabulate(available[["RoomID", "RoomType", "Price"]], headers="keys", tablefmt="fancy_grid", showindex=False))

# ==========================================================
# 📘 BOOKING MANAGEMENT
# ==========================================================
def make_booking():
    rooms = load_csv(ROOM_FILE, ROOM_COLUMNS)
    bookings = load_csv(BOOKING_FILE, BOOK_COLUMNS)
    available = rooms[rooms["Status"].str.lower() == "available"]
    if available.empty:
        print("❌ No rooms available.")
        return
    print(tabulate(available[["RoomID", "RoomType", "Price"]], headers="keys", tablefmt="fancy_grid", showindex=False))
    room_id = input("Enter Room ID: ").strip()
    if room_id not in available["RoomID"].values:
        print("❌ Invalid Room ID.")
        return
    name = input("Enter Customer Name: ").strip()
    check_in = input("Enter Check-in (dd-mm-yyyy): ").strip()
    check_out = input("Enter Check-out (dd-mm-yyyy): ").strip()
    booking_id = "B" + str(np.random.randint(1000, 9999))
    new = pd.DataFrame([[booking_id, name, room_id, check_in, check_out]], columns=BOOK_COLUMNS)
    bookings = pd.concat([bookings, new], ignore_index=True)
    save_csv(BOOKING_FILE, bookings)
    rooms.loc[rooms["RoomID"] == room_id, "Status"] = "Booked"
    save_csv(ROOM_FILE, rooms)
    print(f"✅ Booking Confirmed! ID: {booking_id}")

def view_all_bookings():
    df = load_csv(BOOKING_FILE, BOOK_COLUMNS)
    if df.empty:
        print("No bookings yet.")
    else:
        print("\n📘 ALL BOOKINGS 📘")
        print(tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))

# ==========================================================
# 💰 BILLING MODULE
# ==========================================================
def generate_bill():
    customers = load_csv(CUSTOMER_FILE, CUSTOMER_COLUMNS)
    rooms = load_csv(ROOM_FILE, ROOM_COLUMNS)
    bills = load_csv(BILL_FILE, BILL_COLUMNS)

    cid = input("Enter Customer ID or Name: ").strip()
    customer = customers[customers.apply(lambda row: cid.lower() in row.astype(str).str.lower().values, axis=1)]
    if customer.empty:
        print("❌ Customer not found.")
        return

    cust = customer.iloc[0]
    name = cust["Name"]
    cust_id = cust["CustomerID"]
    room_id = cust["RoomID"]
    days = int(cust["DaysOfStay"]) if str(cust["DaysOfStay"]).isdigit() else 0
    room = rooms[rooms["RoomID"] == room_id]
    if room.empty:
        print("❌ Room not found for this customer.")
        return

    price = float(room.iloc[0]["Price"])
    total = price * days
    bill_id = "BL" + str(np.random.randint(1000, 9999))
    bill_date = datetime.today().strftime("%Y-%m-%d")

    new_bill = pd.DataFrame([[bill_id, cust_id, name, room_id, days, price, total, bill_date]], columns=BILL_COLUMNS)
    bills = pd.concat([bills, new_bill], ignore_index=True)
    save_csv(BILL_FILE, bills)

    print("\n🧾 --- BILL GENERATED ---")
    print(tabulate(new_bill, headers="keys", tablefmt="fancy_grid", showindex=False))
    print("✅ Bill saved successfully in bills.csv\n")

def view_bills():
    df = load_csv(BILL_FILE, BILL_COLUMNS)
    if df.empty:
        print("❌ No bills generated yet.")
    else:
        print("\n💰 ALL BILLS 💰")
        print(tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))

# ==========================================================
# 👨‍🍳 STAFF MANAGEMENT MODULE
# ==========================================================
def staff_management():
    print("\n📋 STAFF MANAGEMENT MENU 📋")
    while True:
        print("\n1. Add Staff Member")
        print("2. View All Staff")
        print("3. Update Staff Details")
        print("4. Remove Staff")
        print("5. Search Staff by Role")
        print("6. Back to Manager Menu")

        choice = input("Enter your choice: ")
        if choice == "1": add_staff()
        elif choice == "2": view_staff()
        elif choice == "3": update_staff()
        elif choice == "4": remove_staff()
        elif choice == "5": search_staff()
        elif choice == "6": break
        else: print("❌ Invalid choice, please try again.")

def add_staff():
    df = load_csv(STAFF_FILE, STAFF_COLUMNS)
    sid = f"S{len(df)+1:03}"
    name = input("Enter staff name: ")
    role = input("Enter role (Manager/Receptionist/Chef/etc.): ")
    contact = input("Enter contact number: ")
    salary = float(input("Enter salary: "))
    join_date = datetime.today().strftime('%Y-%m-%d')

    new_staff = pd.DataFrame([[sid, name, role, contact, salary, join_date]], columns=STAFF_COLUMNS)
    df = pd.concat([df, new_staff], ignore_index=True)
    save_csv(STAFF_FILE, df)
    print(f"✅ Staff member {name} added successfully with ID {sid}.")

def view_staff():
    df = load_csv(STAFF_FILE, STAFF_COLUMNS)
    if df.empty:
        print("No staff records found.")
    else:
        print("\n📋 Current Staff List:\n")
        print(tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))

def update_staff():
    df = load_csv(STAFF_FILE, STAFF_COLUMNS)
    sid = input("Enter Staff ID to update: ")
    if sid not in df["StaffID"].values:
        print("❌ No staff found with that ID.")
        return
    print("Leave blank if no change.")
    new_salary = input("Enter new salary: ")
    new_role = input("Enter new role: ")
    if new_salary: df.loc[df["StaffID"] == sid, "Salary"] = float(new_salary)
    if new_role: df.loc[df["StaffID"] == sid, "Role"] = new_role
    save_csv(STAFF_FILE, df)
    print("✅ Staff details updated successfully.")

def remove_staff():
    df = load_csv(STAFF_FILE, STAFF_COLUMNS)
    sid = input("Enter Staff ID to remove: ")
    if sid not in df["StaffID"].values:
        print("❌ No such staff found.")
        return
    df = df[df["StaffID"] != sid]
    save_csv(STAFF_FILE, df)
    print(f"✅ Staff {sid} removed successfully.")

def search_staff():
    df = load_csv(STAFF_FILE, STAFF_COLUMNS)
    role = input("Enter role to search (e.g., Receptionist, Chef): ")
    results = df[df["Role"].str.lower() == role.lower()]
    if results.empty:
        print("No staff found for this role.")
    else:
        print("\n👩‍🍳 Matching Staff:\n")
        print(tabulate(results, headers="keys", tablefmt="fancy_grid", showindex=False))

# ==========================================================
# 👨‍💼 MENUS
# ==========================================================
def manager_menu():
    while True:
        print("\n--- MANAGER MENU ---")
        print("1. View All Rooms")
        print("2. View All Bookings")
        print("3. Customer Records")
        print("4. Staff Management")
        print("5. View All Bills")
        print("6. Exit to Main Menu")

        ch = input("Enter choice: ")
        if ch == "1": view_all_rooms()
        elif ch == "2": view_all_bookings()
        elif ch == "3": customer_menu()
        elif ch == "4": staff_management()
        elif ch == "5": view_bills()
        elif ch == "6": break
        else: print("❌ Invalid input.")

def receptionist_menu():
    while True:
        print("\n--- RECEPTIONIST MENU ---")
        print("1. Add Room")
        print("2. Update Room")
        print("3. View All Rooms")
        print("4. Manage Customers")
        print("5. Back to Main Menu")
        ch = input("Enter choice: ")
        if ch == "1": add_room()
        elif ch == "2": update_room()
        elif ch == "3": view_all_rooms()
        elif ch == "4": customer_menu()
        elif ch == "5": break
        else: print("❌ Invalid input.")

def customer_portal():
    while True:
        print("\n--- CUSTOMER PORTAL ---")
        print("1. View Available Rooms")
        print("2. Make Booking")
        print("3. Billing & Invoice 💰")
        print("4. Back to Main Menu")
        ch = input("Enter choice: ")
        if ch == "1": show_available_rooms()
        elif ch == "2": make_booking()
        elif ch == "3": generate_bill()
        elif ch == "4": break
        else: print("❌ Invalid input.")

# ==========================================================
# 🔑 ENTRY
# ==========================================================
def entry():
    print("\n✨🏨 WELCOME TO DilliDarshan 🏨✨")
    while True:
        print("\nI am:\n1. Manager\n2. Receptionist\n3. Customer\n4. Exit")
        role = input("Enter choice: ")
        if role == "1":
            pwd = input("Enter Manager password: ")
            if pwd == "root": manager_menu()
            else: print("❌ Wrong password.")
        elif role == "2":
            name = input("Enter your name: ")
            pwd = input("Enter password: ")
            if pwd == f"{name}@python": receptionist_menu()
            else: print("❌ Invalid credentials.")
        elif role == "3": customer_portal()
        elif role == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice.")

# ==========================================================
# RUN
# ==========================================================
if __name__ == "__main__":
    entry()
