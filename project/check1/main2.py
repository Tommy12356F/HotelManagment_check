import pandas as pd
import numpy as np
from datetime import datetime
import random
import string
import os

# ==========================================================
# GLOBAL FILES
ROOM_FILE = "rooms.csv"
BOOKING_FILE = "bookings.csv"
CUSTOMER_FILE = "customers.csv"


ROOM_COLUMNS = ["RoomID", "RoomType", "Price", "Status"]
BOOK_COLUMNS = ["BookingID", "CustomerName", "RoomID", "CheckIn", "CheckOut"]
CUSTOMER_COLUMNS = ["CustomerID", "Name", "Phone", "Email", "RoomID", "DaysOfStay", "RegDate"]
CSV_FILE = "customers.csv"
COLUMNS = ["CustomerID", "Name", "Phone", "Email", "RoomID", "DaysOfStay", "RegDate"]




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
#======================TANVI================================
# ==========================================================
def load_data():
    """Loads the customer data safely, creating the CSV if missing."""
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(CSV_FILE, index=False)
        return df.astype({
            "CustomerID": "Int64", "Name": "string", "Phone": "string",
            "Email": "string", "RoomID": "string", "DaysOfStay": "Int64",
            "RegDate": "string"
        })

    try:
        df = pd.read_csv(CSV_FILE)
        if df.empty:
            df = pd.DataFrame(columns=COLUMNS)
    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=COLUMNS)
    except Exception as e:
        print(f"⚠️ Error loading data: {e}")
        df = pd.DataFrame(columns=COLUMNS)

    for col in COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA

    return df.astype({
        "CustomerID": "Int64", "Name": "string", "Phone": "string",
        "Email": "string", "RoomID": "string", "DaysOfStay": "Int64",
        "RegDate": "string"
    })


def save_data(df):
    """Saves customer data safely to CSV."""
    out = df.copy()
    out.to_csv(CSV_FILE, index=False)


# ==========================================================
# VALIDATION FUNCTIONS
# ==========================================================
def validate_phone(phone):
    """Ensures phone number is exactly 10 digits."""
    if not isinstance(phone, str) or len(phone.strip()) != 10:
        return False
    arr = np.array(list(phone))
    return np.all(arr >= "0") and np.all(arr <= "9")


def validate_email(email):
    """Checks basic email pattern."""
    return isinstance(email, str) and "@" in email and "." in email.split("@")[-1]


# ==========================================================
# ID GENERATION
# ==========================================================
def generate_customer_id(df):
    """Auto-generates unique Customer ID."""
    if df.empty or df["CustomerID"].dropna().empty:
        return 1001
    existing_ids = df["CustomerID"].dropna().astype(int).to_numpy()
    new_id = int(np.max(existing_ids) + 1)
    return new_id


# ==========================================================
# CRUD OPERATIONS
# ==========================================================
def add_customer(df):
    """Adds a new customer entry."""
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

    room = input("Enter Room ID (if any): ").strip() or pd.NA

    stay = input("Stay Duration (days) — leave blank for auto: ").strip()
    if stay.isdigit():
        staydays = int(stay)
    else:
        staydays = int(np.random.randint(1, 31))
        print(f"Auto-assigned Stay Days: {staydays}")

    if not df[df["Phone"] == phone].empty:
        print("Phone already exists! Not adding.")
        return df

    new_row = {
        "CustomerID": cid,
        "Name": name,
        "Phone": phone,
        "Email": email,
        "RoomID": room,
        "DaysOfStay": staydays,
        "RegDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_data(df)
    print("✅ Customer added.\n")
    return df


def view_customers(df):
    """Displays all customers."""
    if df.empty:
        print("\nNo customers found.\n")
        return
    print("\nCustomer List:")
    print(df.to_string(index=False), "\n")


def search_customer(df):
    """Search for a customer by ID, name, or phone."""
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
    """Update customer details including stay duration and reg date."""
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

    current_phone = df.at[i, "Phone"]
    current_email = df.at[i, "Email"]
    current_room = df.at[i, "RoomID"]
    current_stay = df.at[i, "DaysOfStay"]
    current_reg = df.at[i, "RegDate"]

    new_phone = input(f"New Phone [{current_phone}]: ").strip()
    if new_phone:
        if validate_phone(new_phone):
            df.at[i, "Phone"] = new_phone
        else:
            print("Invalid phone, not updated.")

    new_email = input(f"New Email [{current_email}]: ").strip()
    if new_email:
        if validate_email(new_email):
            df.at[i, "Email"] = new_email
        else:
            print("Invalid email, not updated.")

    new_room = input(f"New Room ID [{current_room}]: ").strip()
    if new_room:
        df.at[i, "RoomID"] = new_room

    new_stay = input(f"New Stay Days [{current_stay}]: ").strip()
    if new_stay:
        if new_stay.isdigit():
            df.at[i, "DaysOfStay"] = int(new_stay)
        else:
            print("Invalid stay days, not updated.")

    new_reg = input(f"New RegDate (YYYY-MM-DD HH:MM:SS) [{current_reg}]: ").strip()
    if new_reg:
        try:
            datetime.strptime(new_reg, "%Y-%m-%d %H:%M:%S")
            df.at[i, "RegDate"] = new_reg
        except ValueError:
            print("Invalid datetime format! Use YYYY-MM-DD HH:MM:SS")
            print("Not updated.")

    save_data(df)
    print("✅ Customer updated successfully.\n")
    return df


def delete_customer(df):
    """Deletes a customer by ID."""
    cid = input("Enter Customer ID to delete: ").strip()
    if not cid.isdigit():
        return df
    cid = int(cid)

    idx = df.index[df["CustomerID"] == cid]
    if idx.empty:
        print("Customer not found.\n")
        return df

    if input("Type YES to confirm delete: ") == "YES":
        df = df.drop(idx).reset_index(drop=True)
        save_data(df)
        print("🗑️ Deleted.\n")
    return df


# ==========================================================
# ANALYTICS
# ==========================================================
def stay_duration_stats(df):
    """Show statistical analytics of stay durations."""
    if df.empty or df["DaysOfStay"].dropna().empty:
        print("No stay data yet.\n")
        return

    arr = df["DaysOfStay"].dropna().to_numpy()
    print("\n📊 Stay Duration Stats 📊")
    print(f"- Total Guests: {len(arr)}")
    print(f"- Avg Stay: {np.mean(arr):.2f} days")
    print(f"- Max Stay: {np.max(arr)} days")
    print(f"- Min Stay: {np.min(arr)} days\n")


# ==========================================================
# MENU DRIVER
# ==========================================================
def customer_menu():
    """Interactive customer management menu."""
    df = load_data()
    while True:
        print("""
⋆꙳•❅‧*₊⋆☃︎‧*❆₊⋆⋆꙳•❅‧*₊⋆☃︎‧*❆₊⋆˚₊𖥧 CUSTOMER MANAGEMENT ⋆꙳•❅‧*₊⋆☃︎‧*❆₊⋆˚₊𖥧
1. Add Customer
2. View Customers
3. Search Customer
4. Update Customer
5. Delete Customer
6. Customer Analytics (Stay Stats)
7. Exit
""")
        ch = input("Enter choice: ")
        if ch == "1":
            df = add_customer(df)
        elif ch == "2":
            view_customers(df)
        elif ch == "3":
            search_customer(df)
        elif ch == "4":
            df = update_customer(df)
        elif ch == "5":
            df = delete_customer(df)
        elif ch == "6":
            stay_duration_stats(df)
        elif ch == "7":
            print("Returning to main menu...\n")
            break
        else:
            print("Invalid.\n")

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

def room_service():
    print("\n=== ROOM SERVICE BOOKING ===")

    # Ask user for a date (format: YYYY-MM-DD)
    date_str = input("Enter the date for room service (YYYY-MM-DD): ")

    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print("❌ Invalid date format. Please use YYYY-MM-DD.")
        return

    # Generate 5 random time slots for the day
    possible_times = ["08:00 AM", "10:00 AM", "12:00 PM", "03:00 PM", "06:00 PM"]
    random.shuffle(possible_times)
    time_slots = possible_times[:5]

    # Define 3 free and 2 paid slots
    slots = []
    for i, time in enumerate(time_slots):
        slot_type = "Free" if i < 3 else "Paid"
        slots.append({"time": time, "type": slot_type})

    print("\nAvailable Room Service Slots for", date_obj)
    print("------------------------------------------------")
    for i, slot in enumerate(slots, 1):
        print(f"{i}. {slot['time']} - {slot['type']} Service")
    print("------------------------------------------------")

    # Ask if user wants to book one
    choice = input("Would you like to book a slot? (yes/no): ").lower()
    if choice != "yes":
        print("No booking made.")
        return

    try:
        slot_choice = int(input("Enter the slot number (1-5): "))
        if slot_choice not in range(1, 6):
            print("Invalid slot number.")
            return
    except ValueError:
        print("Invalid input.")
        return

    selected_slot = slots[slot_choice - 1]
    cust_id = input("Enter your Customer ID: ")

    # Billing logic
    if selected_slot["type"].lower() == "paid":
        print("₹200 will be added to your bill (paid service).")
        # Billing integration placeholder
        # update_customer_bill(cust_id, 200)

    # Prepare data
    record = {
        "date": str(date_obj),
        "time_slot": selected_slot["time"],
        "slot_type": selected_slot["type"],
        "customer_id": cust_id,
        "status": "Booked"
    }

    # Save booking
    filename = "room_services.csv"
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    else:
        df = pd.DataFrame([record])

    df.to_csv(filename, index=False)
    print(f"\n✅ Room service booked successfully for {selected_slot['time']} on {date_obj}!")
    print("Record saved in room_services.csv\n")
def book_swimming_pool():
    print("\n=== SWIMMING POOL BOOKING ===")

    # Ask user for date
    date_str = input("Enter the date for swimming pool booking (YYYY-MM-DD): ")
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print("❌ Invalid date format. Please use YYYY-MM-DD.")
        return

    # Create 8 random time slots
    possible_times = ["06:00 AM", "07:30 AM", "09:00 AM", "10:30 AM", 
                      "12:00 PM", "02:00 PM", "04:00 PM", "06:00 PM"]
    random.shuffle(possible_times)
    time_slots = possible_times[:8]

    # Define 5 free and 3 paid slots
    slots = []
    for i, time in enumerate(time_slots):
        slot_type = "Free" if i < 5 else "Paid"
        slots.append({"time": time, "type": slot_type})

    print("\nAvailable Swimming Pool Slots for", date_obj)
    print("------------------------------------------------")
    for i, slot in enumerate(slots, 1):
        print(f"{i}. {slot['time']} - {slot['type']} Session")
    print("------------------------------------------------")

    # Booking prompt
    choice = input("Would you like to book a slot? (yes/no): ").lower()
    if choice != "yes":
        print("No booking made.")
        return

    try:
        slot_choice = int(input("Enter the slot number (1-8): "))
        if slot_choice not in range(1, 9):
            print("Invalid slot number.")
            return
    except ValueError:
        print("Invalid input.")
        return

    selected_slot = slots[slot_choice - 1]
    cust_id = input("Enter your Customer ID: ")

    if selected_slot["type"].lower() == "paid":
        print("₹300 will be added to your bill (paid swimming slot).")
        # update_customer_bill(cust_id, 300)

    # Record booking
    record = {
        "date": str(date_obj),
        "time_slot": selected_slot["time"],
        "slot_type": selected_slot["type"],
        "customer_id": cust_id,
        "status": "Booked"
    }

    # Save to CSV
    filename = "swimming_pool_bookings.csv"
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    else:
        df = pd.DataFrame([record])

    df.to_csv(filename, index=False)
    print(f"\n✅ Swimming Pool slot booked successfully for {selected_slot['time']} on {date_obj}!")
    print("Record saved in swimming_pool_bookings.csv\n")
def book_banquet_hall():
    print("\n=== BANQUET HALL BOOKING ===")

    # Ask for date
    date_str = input("Enter the date for banquet hall booking (YYYY-MM-DD): ")
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print("❌ Invalid date format. Please use YYYY-MM-DD.")
        return

    # Create 3 time slots
    possible_times = ["10:00 AM - 01:00 PM", "02:00 PM - 05:00 PM", "06:00 PM - 09:00 PM"]
    slots = []
    for i, time in enumerate(possible_times):
        slot_type = "Free" if i < 1 else "Paid"
        slots.append({"time": time, "type": slot_type})

    print("\nAvailable Banquet Hall Slots for", date_obj)
    print("------------------------------------------------")
    for i, slot in enumerate(slots, 1):
        print(f"{i}. {slot['time']} - {slot['type']} Booking")
    print("------------------------------------------------")

    # Booking prompt
    choice = input("Would you like to book a slot? (yes/no): ").lower()
    if choice != "yes":
        print("No booking made.")
        return

    try:
        slot_choice = int(input("Enter the slot number (1-3): "))
        if slot_choice not in range(1, 4):
            print("Invalid slot number.")
            return
    except ValueError:
        print("Invalid input.")
        return

    selected_slot = slots[slot_choice - 1]
    cust_id = input("Enter your Customer ID: ")

    if selected_slot["type"].lower() == "paid":
        print("₹1000 will be added to your bill (paid banquet slot).")
        # update_customer_bill(cust_id, 1000)

    # Record booking
    record = {
        "date": str(date_obj),
        "time_slot": selected_slot["time"],
        "slot_type": selected_slot["type"],
        "customer_id": cust_id,
        "status": "Booked"
    }

    # Save to CSV
    filename = "banquet_hall_bookings.csv"
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    else:
        df = pd.DataFrame([record])

    df.to_csv(filename, index=False)
    print(f"\n✅ Banquet Hall slot booked successfully for {selected_slot['time']} on {date_obj}!")
    print("Record saved in banquet_hall_bookings.csv\n")


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
        print("1. Room Management")
        print("2. View All Bookings")
        print("3. Customer Records")
        print("4. Exit to Main Menu")
        ch = input("Enter choice: ")
        if ch == "1":
            room_tasks()
        elif ch == "2":
            view_all_bookings()
        elif ch == "3":
            customer_menu()
        elif ch == "4":
            break
        else:
            print("❌ Invalid input.")


def room_tasks():
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
        print("3. Room Service")
        print("4. Swimming Pool Booking")
        print("5. Banquet Hall Booking")
        print("6. Back to Main Menu")

        ch = input("Enter your choice: ")

        if ch == "1":
            show_available_rooms()
        elif ch == "2":
            make_booking()
        elif ch == "3":
            room_service()
        elif ch == "4":
            book_swimming_pool()
        elif ch == "5":
            book_banquet_hall()
        elif ch == "6":
            print("Returning to main menu...")
            break
        else:
            print("❌ Invalid input. Please try again.")



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
            if pwd == "root":
                manager_menu()
            else:
                print("❌ Wrong password.")
        elif role == "2":
            customer_portal()
        elif role == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice.")


# ==========================================================
# RUN
# ==========================================================
if __name__ == "__main__":
    entry()
