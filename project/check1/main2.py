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
CUSTOMER_COLUMNS = ["CustomerID", "Name", "Phone", "Email", "Room", "StayDays", "CreatedAt"]
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
========================TANVI===============================
# ==========================================================
"""
Customer Management Module
- Pandas DataFrame stored to customers.csv
- Uses NumPy for ID generation & stay duration stats
- Full CRUD + validation + analytics
"""

# Validation 
def validate_phone(phone):
    if not isinstance(phone, str) or len(phone.strip()) != 10:
        return False
    arr = np.array(list(phone))
    return np.all(arr >= "0") and np.all(arr <= "9")

def validate_email(email):
    return isinstance(email, str) and "@" in email and "." in email.split("@")[-1]

#  ID Generation 
def generate_customer_id(df):
    if df.empty or df["CustomerID"].dropna().empty:
        return 1001

    existing_ids = df["CustomerID"].dropna().astype(int).to_numpy()
    new_id = int(np.max(existing_ids) + 1)
    return new_id

#  CRUD 
def add_customer(df):
    cid = generate_customer_id(df)
    print(f"\nAssigned Customer ID: {cid}")

    name = input("Enter Name: ").strip()
    while not name:
        name = input("Name cannot be empty. Enter Name: ").strip()

    while True:
        phone = input("Enter Phone (10 digits): ").strip()
        if validate_phone(phone):
            break
        print("Invalid phone!")

    while True:
        email = input("Enter Email: ").strip()
        if validate_email(email):
            break
        print("Invalid email!")

    room = input("Enter Room No: ").strip() or pd.NA

    #  Stay Days (Hybrid)
    stay = input("Stay Duration (days) — leave blank for auto: ").strip()
    if stay.isdigit():
        staydays = int(stay)
    else:
        staydays = int(np.random.randint(1, 31))
        print(f"Auto-assigned Stay Days: {staydays}")

    # Prevent duplicate phone
    if not df[df["Phone"] == phone].empty:
        print("Phone already exists! Not adding.")
        return df

    new_row = {
        "CustomerID": cid,
        "Name": name,
        "Phone": phone,
        "Email": email,
        "Room": room,
        "StayDays": staydays,
        "CreatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_data(df)
    print("✅ Customer added.\n")
    return df

def view_customers(df):
    if df.empty:
        print("\nNo customers found.\n")
        return
    print("\nCustomer List:")
    print(df.to_string(index=False), "\n")

def search_customer(df):
    key = input("Search by ID / Phone / Name: ").strip()
    if key.isdigit():
        result = df[(df["CustomerID"] == int(key)) | (df["Phone"] == key)]
    else:
        result = df[df["Name"].str.contains(key, case=False, na=False)]

    if result.empty:
        print("No record found.\n")
    else:
        print(result.to_string(index=False), "\n")

def update_customer(df):
    """Update customer details including StayDays & CreatedAt."""
    cid = input("Enter Customer ID to update: ").strip()
    if not cid.isdigit():
        print("Invalid ID.")
        return df
    cid = int(cid)

    idx = df.index[df["CustomerID"] == cid]
    if idx.empty:
        print("Customer not found.\n")
        return df

    i = idx[0]
    print("Leave blank to keep same value.")

    current_phone = df.at[i,"Phone"]
    current_email = df.at[i,"Email"]
    current_room = df.at[i,"Room"]
    current_stay = df.at[i,"StayDays"]
    current_created = df.at[i,"CreatedAt"]

    # --- Phone ---
    new_phone = input(f"New Phone [{current_phone}]: ").strip()
    if new_phone:
        if validate_phone(new_phone):
            df.at[i,"Phone"] = new_phone
        else:
            print("Invalid phone, not updated.")

    # --- Email ---
    new_email = input(f"New Email [{current_email}]: ").strip()
    if new_email:
        if validate_email(new_email):
            df.at[i,"Email"] = new_email
        else:
            print("Invalid email, not updated.")

    # --- Room ---
    new_room = input(f"New Room [{current_room}]: ").strip()
    if new_room:
        df.at[i,"Room"] = new_room

    # --- Stay Days ---
    new_stay = input(f"New Stay Days [{current_stay}]: ").strip()
    if new_stay:
        if new_stay.isdigit():
            df.at[i,"StayDays"] = int(new_stay)
        else:
            print("Invalid stay days, not updated.")

    # --- Created At ---
    new_created = input(f"New CreatedAt (YYYY-MM-DD HH:MM:SS) [{current_created}]: ").strip()
    if new_created:
        try:
            # validate datetime format
            datetime.strptime(new_created, "%Y-%m-%d %H:%M:%S")
            df.at[i,"CreatedAt"] = new_created
        except ValueError:
            print("Invalid datetime format! Correct format: YYYY-MM-DD HH:MM:SS")
            print("Not updated.")

    save_data(df)
    print(" Customer updated successfully.\n")
    return df


def delete_customer(df):
    cid = input("Enter Customer ID to delete: ").strip()
    if not cid.isdigit(): return df
    cid = int(cid)

    idx = df.index[df["CustomerID"] == cid]
    if idx.empty:
        print("Customer not found.\n")
        return df

    if input("Type YES to confirm delete: ") == "YES":
        df = df.drop(idx).reset_index(drop=True)
        save_data(df)
        print("Deleted.\n")
    return df

# Stats
def stay_duration_stats(df):
    if df.empty or df["StayDays"].dropna().empty:
        print("No stay data yet.\n")
        return

    arr = df["StayDays"].dropna().to_numpy()
    print("\n Stay Duration Stats:")
    print(f"- Total Guests: {len(arr)}")
    print(f"- Avg Stay: {np.mean(arr):.2f} days")
    print(f"- Max Stay: {np.max(arr)} days")
    print(f"- Min Stay: {np.min(arr)} days\n")

# Menu 
def main():
    df = load_data()
    while True:
        print("""
⋆꙳•❅‧*₊⋆☃︎‧*❆₊⋆⋆꙳•❅‧*₊⋆☃︎‧*❆₊⋆˚₊𖥧CUSTOMER MANAGEMENT⋆꙳•❅‧*₊⋆☃︎‧*❆₊⋆ ˚₊𖥧⋆꙳•❅‧*₊⋆☃︎‧*❆₊⋆
1. Add Customer
2. View Customers
3. Search Customer
4. Update Customer
5. Delete Customer
6. Customer Analytics (Stay Stats)
7. Exit
""")
        ch = input("Enter choice: ")
        if ch == "1": df = add_customer(df)
        elif ch == "2": view_customers(df)
        elif ch == "3": search_customer(df)
        elif ch == "4": df = update_customer(df)
        elif ch == "5": df = delete_customer(df)
        elif ch == "6": stay_duration_stats(df)
        elif ch == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid.\n")

if __name__ == "__main__":
    main()

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
        print("4. Performance Report")
        print("5. Exit to Main Menu")
        ch = input("Enter choice: ")
        if ch == "1":
            view_all_rooms()
        elif ch == "2":
            view_all_bookings()
        elif ch == "3":
            customer_menu()
        elif ch == "4":
            performance()
        elif ch == "5":
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
# REPORTS AND ANALYSIS
# ==========================================================


def performance():
    while True:
        print("\n ✎ᝰ.ᐟ⋆⑅˚₊ MANAGER MENU ⋆⑅˚₊✎ᝰ.ᐟ")
        print("1. Daily Summary & Occupancy Rate")
        print("2. Client Registration Report")
        print("3. Revenue Growth / Decline")
        print("4. Back to Manager Menu")
        ch = input("Enter choice: ")

        if ch == "1":
            summary()
        elif ch == "2":
            bookings()
        elif ch == "3":
            revenue()
        elif ch == "4":
            manager_menu()   
        elif ch == "5":
            break
        else:
            print("❌ Invalid input.")


def summary():

    rooms = load_csv(ROOM_FILE, ROOM_COLUMNS)
    bookings = load_csv(BOOKING_FILE, BOOK_COLUMNS)

    tot_rooms = len(rooms)
    booked = len(rooms[rooms["Status"].str.lower() == "booked"])
    available_rooms = tot_rooms - booked
    occupancy_rate = (booked / tot_rooms * 100) if tot_rooms > 0 else 0

    print("\nˏ ✄┈┈┈┈┈┈┈┈ Daily Summary ┈┈┈┈┈┈┈┈")
    print()
    print(f"Total Rooms: {tot_rooms}")
    print(f"Booked Rooms: {booked}")
    print(f"Available Rooms: {available_rooms}")
    print(f"Occupancy Rate: {occupancy_rate:.2f}%")
    print(f"Total Bookings Today: {len(bookings)}")

    today = datetime.today().strftime("%d-%m-%Y")
    t_bookings = bookings[bookings["CheckIn"] == today]
    if not t_bookings.empty:
        print("\nToday's Check-ins:")
        print(t_bookings[["BookingID", "CustomerName", "RoomID"]].to_string(index=False))
    else:
        print("\n No check-ins today.")


def bookings():
    df = load_csv(REGISTERED, REGISTERED_COLUMNS)
    if df.empty:
        print("No registered clients yet.")
        return

    print("\n ₊˚🗒 ˎ𖤐 ✎ᝰ. CLIENT REGISTRATION REPORT ✎ᝰ. 𖤐ˎ 🗒")
    print(df.to_string(index=False))



def revenue():
    bookings = load_csv(BOOKING_FILE, BOOK_COLUMNS)
    rooms = load_csv(ROOM_FILE, ROOM_COLUMNS)

    if bookings.empty or rooms.empty:
        print("No data available for revenue analysis.")
        return

    merged = pd.merge(bookings, rooms, on="RoomID", how="left")

    #finding daily revenue 
    merged["Revenue"] = merged["Price"].astype(float)
    revenue_by_date = merged.groupby("CheckIn")["Revenue"].sum().reset_index()

    print("\n ˚₊‧꒰ა $ ໒꒱ ‧₊˚  REVENUE REPORT  ˚₊‧꒰ა $ ໒꒱ ‧₊˚ ")
    print(revenue_by_date.to_string(index=False))

    # growth
    if len(revenue_by_date) > 1:
        growth = revenue_by_date["Revenue"].pct_change() * 100
        revenue_by_date["Growth %"] = growth.round(2)
        print("\n Revenue Growth/Decline Trend:")
        print(revenue_by_date.to_string(index=False))
    else:
        print("\nNot enough data to calculate growth trend.")

def booking_history_report():
    bookings = load_csv(BOOKING_FILE, BOOK_COLUMNS)
    if bookings.empty:
        print("No booking history found.")
        return

    name = input("Enter Client Name to view history: ").strip()
    record = bookings[bookings["CustomerName"].str.lower() == name.lower()]

    if record.empty:
        print("No bookings found for this client.")
    else: 
        print(f"\n ₊˚.🎧 ✩ BOOKING HISTORY FOR {name.upper()}:  ₊˚.🎧 ✩  ")
        print(record.to_string(index=False))

        # Simulate receipts
        rooms = load_csv(ROOM_FILE, ROOM_COLUMNS)
        merged = pd.merge(record, rooms, on="RoomID", how="left")
        merged["Revenue"] = merged["Price"].astype(float)
        total = merged["Revenue"].sum()


# ==========================================================
# RUN 
# ==========================================================

entry()
