import pandas as pd
import numpy as np
from datetime import datetime
import random
import string

# ==========================================================
# GLOBAL FILES
ROOM_FILE = "rooms.csv"
BOOKING_FILE = "bookings.csv"
CUSTOMER_FILE = "customers.csv"
REGISTERED = "regist.csv"


ROOM_COLUMNS = ["RoomID", "RoomType", "Price", "Status"]
BOOK_COLUMNS = ["BookingID", "CustomerName", "RoomID", "CheckIn", "CheckOut"]
CUSTOMER_COLUMNS = ["CustomerID", "Name", "Phone", "Email", "RoomID", "DaysOfStay", "RegDate"]
REGISTERED_COLUMNS = ["Cust_ID", "Name", "Age", "Phone", "Email"]


cust_id = "C" + str(np.random.randint(1000, 9999))
# ==========================================================

# ---------------------- CSV HELPERS ------------------------
def load_csv(filename, columns):
    try:
        df = pd.read_csv(filename, dtype=str)
    except FileNotFoundError:
        df = pd.DataFrame(columns=columns)
        df.to_csv(filename, index=False)
    for col in columns:
        if col not in df.columns:
            df[col] = ""
    return df[columns]


def save_csv(filename, df):
    df.to_csv(filename, index=False)

# ==========================================================
# 🧾 CUSTOMER MANAGEMENT (from customer.py)
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

    new_row = pd.DataFrame([[cust_id, name, phone, email, room_id, days, reg_date]],
                           columns=CUSTOMER_COLUMNS)
    df = pd.concat([df, new_row], ignore_index=True)
    save_csv(CUSTOMER_FILE, df)
    print(f" Customer {name} added successfully! Customer ID: {cust_id}")


def view_customers():
    df = load_csv(CUSTOMER_FILE, CUSTOMER_COLUMNS)
    if df.empty:
        print(" No customers found.")
        return
    print("\n--- CUSTOMER RECORDS ---")
    print(df.to_string(index=False))
    print("------------------------")


def search_customer():
    df = load_csv(CUSTOMER_FILE, CUSTOMER_COLUMNS)
    key = input("Enter Customer ID / Name / Phone to search: ").strip().lower()
    result = df[df.apply(lambda row: key in row.astype(str).str.lower().values, axis=1)]
    if result.empty:
        print(" No matching customer found.")
    else:
        print(result.to_string(index=False))


def update_customer():
    df = load_csv(CUSTOMER_FILE, CUSTOMER_COLUMNS)
    cid = input("Enter Customer ID to update: ").strip()
    if cid not in df["CustomerID"].values:
        print(" Customer not found.")
        return
    print("Leave fields blank to keep old values.")
    new_phone = input("New Phone: ").strip()
    new_email = input("New Email: ").strip()
    new_room = input("New Room ID: ").strip()
    new_days = input("New Days of Stay: ").strip()

    mask = df["CustomerID"] == cid
    if new_phone:
        df.loc[mask, "Phone"] = new_phone
    if new_email:
        df.loc[mask, "Email"] = new_email
    if new_room:
        df.loc[mask, "RoomID"] = new_room
    if new_days:
        df.loc[mask, "DaysOfStay"] = new_days

    save_csv(CUSTOMER_FILE, df)
    print(" Customer updated successfully.")


def delete_customer():
    df = load_csv(CUSTOMER_FILE, CUSTOMER_COLUMNS)
    cid = input("Enter Customer ID to delete: ").strip()
    if cid not in df["CustomerID"].values:
        print("Customer not found.")
        return
    df = df[df["CustomerID"] != cid]
    save_csv(CUSTOMER_FILE, df)
    print(" Customer deleted successfully.")


def customer_menu():
    while True:
        print("\n⋆꙳•❅‧*₊⋆☃︎‧*❆₊⋆ ˚₊𖥧⋆꙳•❅‧*₊⋆☃︎‧*❆₊⋆CUSTOMER MANAGEMENT ⋆꙳•❅‧*₊⋆☃︎‧*❆₊⋆ ˚₊𖥧⋆꙳•❅‧*₊⋆☃︎‧*❆₊⋆")
        print("1. Add Customer")
        print("2. View Customers")
        print("3. Search Customer")
        print("4. Update Customer")
        print("5. Delete Customer")
        print("6. Back")
        ch = input("Enter your choice: ")
        if ch == "1":
            add_customer()
        elif ch == "2":
            view_customers()
        elif ch == "3":
            search_customer()
        elif ch == "4":
            update_customer()
        elif ch == "5":
            delete_customer()
        elif ch == "6":
            break
        else:
            print(" Invalid input.")

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
        return
    print("\n--- ALL ROOMS ---")
    print(df.to_string(index=False))
    print("-----------------")


def show_available_rooms():
    df = load_csv(ROOM_FILE, ROOM_COLUMNS)
    available = df[df["Status"].str.lower() == "available"]
    if available.empty:
        print("❌ No available rooms.")
    else:
        print("\n--- AVAILABLE ROOMS ---")
        print(available[["RoomID", "RoomType", "Price"]].to_string(index=False))


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
    print(available[["RoomID", "RoomType", "Price"]].to_string(index=False))
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
        return
    print("\n--- ALL BOOKINGS ---")
    print(df.to_string(index=False))


# ==========================================================
# 👨‍💼 MENUS
# ==========================================================
def manager_menu():
    while True:
        print("\n--- MANAGER MENU ---")
        print("1. View All Rooms")
        print("2. View All Bookings")
        print("3. Customer Records")
        print("4. Exit to Main Menu")
        ch = input("Enter choice: ")
        if ch == "1":
            view_all_rooms()
        elif ch == "2":
            view_all_bookings()
        elif ch == "3":
            customer_menu()
        elif ch == "4":
            break
        else:
            print("❌ Invalid input.")


def receptionist_menu():
    while True:
        print("\n--- RECEPTIONIST MENU ---")
        print("1. Add Room")
        print("2. Update Room")
        print("3. View All Rooms")
        print("4. Manage Customers")
        print("5. Back to Main Menu")
        ch = input("Enter choice: ")
        if ch == "1":
            add_room()
        elif ch == "2":
            update_room()
        elif ch == "3":
            view_all_rooms()
        elif ch == "4":
            customer_menu()
        elif ch == "5":
            break
        else:
            print("❌ Invalid input.")


def customer_portal():
    while True:
        print("\n--- CUSTOMER PORTAL ---")
        print("1. View Available Rooms")
        print("2. Make Booking")
        print("3. Back to Main Menu")
        ch = input("Enter choice: ")
        if ch == "1":
            show_available_rooms()
        elif ch == "2":
            make_booking()
        elif ch == "3":
            break
        else:
            print("❌ Invalid input.")


# ==========================================================
# 🔑 ENTRY
# ==========================================================

####### DIVYA #########
def entry():
    print("\n✨🏨 WELCOME TO DilliDarshan 🏨✨")
    print("Your gateway to the heart of Delhi")
    while True:
        print("\nI am:\n1. Manager\n2. Customer\n3. Exit")
        role = input("Enter choice: ")
        if role == "1":
            pwd = input("Enter Manager password: ")
            if pwd == "root":
                manager_menu()
            else:
                print("❌ Wrong password.")
        elif role == "2":
            customer_entry()
        elif role == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice.")

def customer_entry():
    ch=input("You would like to login or register? L/R:")
    if ch.lower()== 'r':
        register()
    else:
        login()
        customer_portal()
        
        
def register():
    df = load_csv(REGISTERED, REGISTERED_COLUMNS)
    email=input("Enter your email address:")
    
    if email in df['Email'].values:
        print("Email already registered! Please login.")
        login()  
        return
    else:
        try:
            name=input("Enter your name:")                              
            age=int(input("Enter your age:"))
            contact=int(input("Enter your contact number:"))
        except ValueError:
            print("❌ Invalid input")
            return
        cust_id = generate_unique_customer_id()
        psswd = f"{name}@python"

        print("YOU HAVE BEEN REGISTERED !!")
        print() 
        print ("Your password is-->\n", psswd)

        
        new = {
            "CustomerID": cust_id,
            'Name': name,
            'Age': age,
            'Phone': contact,
            'Email': email,
            }

        # Convert to DataFrame
        new_df = pd.DataFrame([new])


        # Append to CSV (add header only if file is new)
        try:
            new_df.to_csv(REGISTERED, mode='a', index=False, header=False)
        except FileNotFoundError:
            new_df.to_csv(REGISTERED, mode='a', index=False, header=not file_exists)

    print(f"Registration successful! Your Customer ID is {cust_id}.")


def login():
    while True:
        df = load_csv(REGISTERED, REGISTERED_COLUMNS)
        x=input('Enter your name\n')
        y=input('Enter your registered number\n')
        if y in df["Phone"].values:
            record = df[df["Phone"] == y].iloc[0]
            print ("🏥 💊 🤝 WELCOME 🤝 💊 🏥")
            print(f"Hello, {record['Name']}! You are now logged in.\n")
            return
        else:
            print("x x INCORRECT MOBILE NUMBER x x")
            print("ACCESS DENIED! TRY AGAIN\n")

            break

        
def generate_unique_customer_id():
    customers_df = load_csv(REGISTERED, REGISTERED_COLUMNS)
    
    existing_ids = set(customers_df["Cust_ID"].dropna().astype(str))
    
    # Generate until unique ID found
    while True:
        cust_id = "C" + str(np.random.randint(1000, 9999))
        if cust_id not in existing_ids:
            return cust_id

# ==========================================================
# RUN 
# ==========================================================

entry()
