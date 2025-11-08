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



# ==========================================================
# ---------------------- CSV HELPERS ------------------------
def load_csv(filename, columns):
    """
    Loads a CSV file safely. 
    If file is missing or empty, creates a new one with the given columns.
    """
    try:
        # Check if the file exists and is not empty
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            df = pd.read_csv(filename, dtype=str)
        else:
            print(f"⚠️ File '{filename}' is empty or missing headers. Creating a new one.")
            df = pd.DataFrame(columns=columns)
            df.to_csv(filename, index=False)
        return df

    except pd.errors.EmptyDataError:
        # Handle the specific "no columns" error
        print(f"⚠️ '{filename}' was empty. Creating a new blank file.")
        df = pd.DataFrame(columns=columns)
        df.to_csv(filename, index=False)
        return df

    except FileNotFoundError:
        print(f"⚠️ '{filename}' not found. Creating a new file.")
        df = pd.DataFrame(columns=columns)
        df.to_csv(filename, index=False)
        return df

    except Exception as e:
        print(f"❌ Error loading {filename}: {e}")
        return pd.DataFrame(columns=columns)



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
    df = load_csv(CUSTOMER_FILE,CUSTOMER_COLUMNS)
    #Auto-generates unique Customer ID.
    if df.empty or df["CustomerID"].dropna().empty:
        return 1001
    existing_ids = df["CustomerID"].dropna().astype(int).to_numpy()
    new_id = int(np.max(existing_ids) + 1)
    return new_id

'''
import numpy as np
import pandas as pd

df = load_csv(CUSTOMER_FILE,COLUMNS)
def generate_customer_id(df, column="CustomerID", start=1001):
    if df is None or df.empty or column not in df.columns:
        return start
    
    # Convert to numeric safely, ignoring missing/non-numeric values
    ids = pd.to_numeric(df[column], errors='coerce').dropna().astype(int)
    if ids.empty:
        return start
    else:
        return ids.max() + 1'''


# ==========================================================
# CRUD OPERATIONS
# ==========================================================
def add_customer(df):
    """Adds a new customer entry."""
    df = load_csv(CUSTOMER_FILE,COLUMNS)
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
def stay_duration_stats():
    df = load_csv(CUSTOMER_FILE,CUSTOMER_COLUMNS)
    """Show statistical analytics of stay durations."""
    if df.empty or df["DaysOfStay"].dropna().empty:
        print("No stay data yet.\n")
        return

    arr = pd.to_numeric(df["DaysOfStay"], errors='coerce').dropna().to_numpy()
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
            stay_duration_stats()
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
def book_adventure_activities():
    print("\n=== ADVENTURE ACTIVITIES BOOKING ===")

    # Ask for date
    date_str = input("Enter the date for adventure activities (YYYY-MM-DD): ")
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print("❌ Invalid date format. Please use YYYY-MM-DD.")
        return

    # List of activities
    activities = [
        "Rock Climbing / Rappelling",
        "Zip Lining",
        "Mountain Biking / ATV Ride",
        "Trekking / Nature Trail",
        "Obstacle / Rope Course"
    ]

    # Default 5 slots per activity
    default_slots = 5

    # Display activity list with slot count
    print(f"\nAvailable Adventure Activities for {date_obj}")
    print("----------------------------------------------------------")
    for i, act in enumerate(activities, 1):
        print(f"{i}. {act}  (Slots available: {default_slots})")
    print("----------------------------------------------------------")

    # Ask user to choose an activity
    try:
        act_choice = int(input("Select the activity number (1-5): "))
        if act_choice not in range(1, 6):
            print("Invalid choice.")
            return
    except ValueError:
        print("Invalid input.")
        return

    selected_activity = activities[act_choice - 1]

    # Create time slots for the chosen activity
    possible_times = ["08:00 AM", "09:30 AM", "11:00 AM", "02:00 PM", "04:00 PM"]

    print(f"\nAvailable time slots for {selected_activity} on {date_obj}")
    print("----------------------------------------------------------")
    for i, time in enumerate(possible_times, 1):
        print(f"{i}. {time}")
    print("----------------------------------------------------------")

    # Ask if user wants to book
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

    selected_time = possible_times[slot_choice - 1]
    cust_id = input("Enter your Customer ID: ")

    # Pricing
    print("Note: Each adventure activity booking costs ₹500.")
    confirm = input("Confirm booking? (yes/no): ").lower()
    if confirm != "yes":
        print("Booking cancelled.")
        return

    print("₹500 will be added to your bill for this activity.")
    # update_customer_bill(cust_id, 500)  # Uncomment once billing function ready

    # Prepare record
    record = {
        "date": str(date_obj),
        "activity": selected_activity,
        "time_slot": selected_time,
        "customer_id": cust_id,
        "charge": 500,
        "status": "Booked"
    }

    # Save booking
    filename = "adventure_activities.csv"
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    else:
        df = pd.DataFrame([record])

    df.to_csv(filename, index=False)
    print(f"\n✅ Adventure activity '{selected_activity}' booked for {selected_time} on {date_obj}!")
    print("Record saved in adventure_activities.csv\n")


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
        print("4. Staff Management")  
        print("5. Billing ")
        print("6. Performance")
        print("7. Exit to Main Menu")

        ch = input("Enter choice: ")

        if ch == "1":
            room_tasks()  # Handles room-related tasks
        elif ch == "2":
            view_all_bookings()
        elif ch == "3":
            customer_menu()
        elif ch == "4":
            staff_management()  # 🆕 Connects to the Staff Management Module
        elif ch == "5":
            billing_menu()
        elif ch == "6":
            performance()
        elif ch == "7":
            print("Returning to main menu...")
            break
        else:
            print("❌ Invalid input.")



def room_tasks():
    while True:
        print("\n--- ROOM MANAGEMENT MENU ---")
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
        print("6. Adventure Activities")  # 🆕 Added
        print("7. Back to Main Menu")     # 🆕 Renumbered

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
            book_adventure_activities()   # 🆕 Added call
        elif ch == "7":
            print("Returning to main menu...")
            break
        else:
            print("❌ Invalid input. Please try again.")


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

        if choice == "1":
            add_staff()
        elif choice == "2":
            view_staff()
        elif choice == "3":
            update_staff()
        elif choice == "4":
            remove_staff()
        elif choice == "5":
            search_staff()
        elif choice == "6":
            break
        else:
            print("❌ Invalid choice, please try again.")


def add_staff():
    try:
        df = pd.read_csv("staff.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["StaffID", "Name", "Role", "Contact", "Salary", "JoinDate"])

    sid = f"S{len(df) + 1:03}"
    name = input("Enter staff name: ")
    role = input("Enter role (Manager/Receptionist/Chef/etc.): ")
    contact = input("Enter contact number: ")

    try:
        salary = float(input("Enter salary: "))
    except ValueError:
        print("❌ Invalid salary amount.")
        return

    join_date = datetime.today().strftime('%Y-%m-%d')

    new_staff = pd.DataFrame([{
        "StaffID": sid,
        "Name": name,
        "Role": role,
        "Contact": contact,
        "Salary": salary,
        "JoinDate": join_date
    }])

    df = pd.concat([df, new_staff], ignore_index=True)
    df.to_csv("staff.csv", index=False)

    print(f"✅ Staff member {name} added successfully with ID {sid}.")


def view_staff():
    try:
        df = pd.read_csv("staff.csv")
        if df.empty:
            print("No staff records found.")
        else:
            print("\n📋 Current Staff List:\n")
            print(df.to_string(index=False))
    except FileNotFoundError:
        print("No staff data found yet.")


def update_staff():
    try:
        df = pd.read_csv("staff.csv")
    except FileNotFoundError:
        print("No staff data available.")
        return

    sid = input("Enter Staff ID to update: ")
    if sid not in df["StaffID"].values:
        print("❌ No staff found with that ID.")
        return

    print("Leave blank if no change.")
    new_salary = input("Enter new salary: ")
    new_role = input("Enter new role: ")

    if new_salary:
        try:
            df.loc[df["StaffID"] == sid, "Salary"] = float(new_salary)
        except ValueError:
            print("Invalid salary input — change ignored.")
    if new_role:
        df.loc[df["StaffID"] == sid, "Role"] = new_role

    df.to_csv("staff.csv", index=False)
    print("✅ Staff details updated successfully.")


def remove_staff():
    try:
        df = pd.read_csv("staff.csv")
    except FileNotFoundError:
        print("No staff data available.")
        return

    sid = input("Enter Staff ID to remove: ")
    if sid not in df["StaffID"].values:
        print("❌ No such staff found.")
        return

    df = df[df["StaffID"] != sid]
    df.to_csv("staff.csv", index=False)
    print(f"✅ Staff {sid} removed successfully.")


def search_staff():
    try:
        df = pd.read_csv("staff.csv")
    except FileNotFoundError:
        print("No staff data available.")
        return

    role = input("Enter role to search (e.g., Receptionist, Chef): ")
    results = df[df["Role"].str.lower() == role.lower()]

    if results.empty:
        print("No staff found for this role.")
    else:
        print("\n👩‍🍳 Matching Staff:\n")
        print(results.to_string(index=False))


# ==========================================================
# 🔑 ENTRY  
# ==========================================================

########### DIVYA ##################

def entry():
    print("\n✨🏨 WELCOME TO DilliDarshan 🏨✨")
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
            customer_portal()
        elif role == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice.")

def performance():
    while True:
        print("\n ✎ᝰ.ᐟ⋆⑅˚₊ MANAGER MENU ⋆⑅˚₊✎ᝰ.ᐟ")
        print("1. Daily Summary & Occupancy Rate")
        print("2. Revenue Growth / Decline")
        print("3. Inventory Report")
        print("4. Back to Manager Menu")
        ch = input("Enter choice: ")

        if ch == "1":
            summary()
        elif ch == "2":
            revenue()
        elif ch == "3":
            inventory()
        elif ch == "4":
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
        print("\nNo check-ins today.")




def revenue():
    bookings = load_csv(BOOKING_FILE, BOOK_COLUMNS) 
    rooms = load_csv(ROOM_FILE, ROOM_COLUMNS) 

    if bookings.empty or rooms.empty: 
        print("No data available for revenue analysis.") 
        return
    
    merged = pd.merge(bookings, rooms, on="RoomID", how="left") 
    print(merged.head())

    merged["Price"] = (merged["Price"].astype(str).str.replace(r"[^\d.]", "", regex=True))
    merged["Price"] = pd.to_numeric(merged["Price"], errors="coerce")
    merged["CheckIn"] = pd.to_datetime(merged["CheckIn"], errors="coerce")


# Simulate daily revenue grouping by CheckIn date 
    merged["Revenue"] = merged["Price"]
    revenue_by_date = merged.groupby("CheckIn")["Revenue"].sum().reset_index() 

    print("\n ˚₊‧꒰ა $ ໒꒱ ‧₊˚ REVENUE REPORT ˚₊‧꒰ა $ ໒꒱ ‧₊˚ ") 
    print(revenue_by_date.to_string(index=False)) 

    # Calculate growth rate 
    if len(revenue_by_date) > 1: 
        growth = revenue_by_date["Revenue"].pct_change() * 100 
        revenue_by_date["Growth %"] = growth.round(2) 
        print("\n📈 Revenue Growth/Decline Trend:") 
        print(revenue_by_date.to_string(index=False)) 
    else: 
        print("\nNot enough data to calculate growth trend.") 


# ==========================================================
# 🧺 INVENTORY MANAGEMENT DEPARTMENT
# ==========================================================
INVENTORY_FILE = "inventory.csv"
INVENTORY_COLUMNS = ["ItemID", "ItemName", "Category", "Quantity", "MinThreshold", "UnitPrice", "LastUpdated"]


def load_inventory():
    try:
        df = pd.read_csv(INVENTORY_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=INVENTORY_COLUMNS)
        df.to_csv(INVENTORY_FILE, index=False)
    return df

def save_inventory(df):
    df.to_csv(INVENTORY_FILE, index=False)

def generate_item_id(df):
    if df.empty:
        return "IT1001"
    last_id = df["ItemID"].iloc[-1]
    num = int(last_id.replace("IT", "")) + 1
    return f"IT{num}"

# ADD / UPDATE ITEMS
# ==========================================================
def add_inventory_item():
    df = load_inventory()
    name = input("Enter Item Name: ").strip().capitalize()
    if not name:
        print("❌ Item name cannot be empty.")
        return

    category = input("Enter Category (e.g. Linen, Cleaning, Toiletries, Food): ").capitalize()
    try:
        qty = int(input("Enter Initial Quantity: "))
        min_thr = int(input("Enter Minimum Threshold for Reorder: "))
        price = float(input("Enter Unit Price: "))
    except ValueError:
        print("❌ Invalid number entered.")
        return

    item_id = generate_item_id(df)
    record = {
        "ItemID": item_id,
        "ItemName": name,
        "Category": category,
        "Quantity": qty,
        "MinThreshold": min_thr,
        "UnitPrice": price,
        "LastUpdated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    save_inventory(df)
    print(f"✅ Added {name} to inventory with ID {item_id}.")

def update_inventory():
    df = load_inventory()
    if df.empty:
        print("Inventory is empty.")
        return

    item_id = input("Enter Item ID to update (e.g., IT1001): ").strip()
    if item_id not in df["ItemID"].values:
        print("❌ Item not found.")
        return

    idx = df.index[df["ItemID"] == item_id][0]
    print(f"Current quantity: {df.at[idx, 'Quantity']}")
    try:
        change = int(input("Enter quantity change (positive for add, negative for reduce): "))
    except ValueError:
        print("❌ Invalid number.")
        return

    df.at[idx, "Quantity"] = max(0, df.at[idx, "Quantity"] + change)
    df.at[idx, "LastUpdated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_inventory(df)
    print("✅ Quantity updated successfully.")

def remove_inventory_item():
    df = load_inventory()
    if df.empty:
        print("Inventory is empty.")
        return

    item_id = input("Enter Item ID to remove: ").strip()
    if item_id not in df["ItemID"].values:
        print("❌ Item not found.")
        return

    if input("Type YES to confirm deletion: ") == "YES":
        df = df[df["ItemID"] != item_id]
        save_inventory(df)
        print("🗑️ Item removed successfully.")


def view_all_inventory():
    df = load_inventory()
    if df.empty:
        print("No items in inventory.")
        return
    print("\n--- ALL INVENTORY ITEMS ---")
    print(df.to_string(index=False))
    print("-----------------------------")

def low_stock_alerts():
    df = load_inventory()
    if df.empty:
        print("No items in inventory.")
        return
    low = df[df["Quantity"] <= df["MinThreshold"]]
    if low.empty:
        print("🎉 All items are sufficiently stocked!")
        return
    print("\n⚠️ LOW STOCK ALERT ⚠️")
    print(low[["ItemID", "ItemName", "Quantity", "MinThreshold"]].to_string(index=False))

    choice = input("Do you want to restock any item? (yes/no): ").strip().lower()
    if choice != "yes":
        return df

    try:
        item_id = int(input("Enter the ItemID to restock: "))
    except ValueError:
        print("Invalid input! Must be an integer.")
        return df

    if item_id not in df["ItemID"].values:
        print("ItemID not found.")
        return df

    idx = df.index[df["ItemID"] == item_id][0]
    print(f"Current quantity of '{df.at[idx, 'ItemName']}': {df.at[idx, 'Quantity']}")

    try:
        add_qty = int(input("Enter quantity to add: "))
        if add_qty < 0:
            print("Quantity cannot be negative.")
            return df
    except ValueError:
        print("Invalid input! Must be an integer.")
        return df

    df.at[idx, "Quantity"] += add_qty
    print(f"✅ '{df.at[idx, 'ItemName']}' updated. New quantity: {df.at[idx, 'Quantity']}\n")
    return df



def inventory_value_report():
    df = load_inventory()
    if df.empty:
        print("Inventory empty.")
        return

    df["Value"] = df["Quantity"] * df["UnitPrice"]
    total_value = df["Value"].sum()
    category_wise = df.groupby("Category")["Value"].sum().reset_index()

    print("\n📦 INVENTORY VALUE REPORT 📦")
    print(f"Total Inventory Value: ₹{total_value:,.2f}\n")
    print("Category-wise Breakdown:")
    print(category_wise.to_string(index=False))


### MENU DRIVER

def inventory():
    while True:
        print("""
⛟ ☒ ⋆✴︎˚｡⋆ ✉︎ INVENTORY MANAGEMENT MENU ✉︎ ⋆✴︎˚｡⋆ ☒ ⛟ 
1. Add Item
2. Update Quantity
3. Remove Item
4. View All Items
5. Low Stock Alerts
6. Inventory Value Report
7. Back to Main Menu
""")
        ch = input("Enter choice: ").strip()
        if ch == "1":
            add_inventory_item()
        elif ch == "2":
            update_inventory()
        elif ch == "3":
            remove_inventory_item()
        elif ch == "4":
            view_all_inventory()
        elif ch == "5":
            low_stock_alerts()
        elif ch == "6":
            inventory_value_report()
        elif ch == "7":
            print("Returning to main menu...")
            break
        else:
            print("❌ Invalid input.")


# ==========================================================
# 💰 BILLING & PAYMENTS MODULE
##########  JASRAJ  #############
# ==========================================================
BILLING_FILE = "billings.csv"
PAYMENT_FILE = "payments.csv"

BILL_COLS = ["BillingID", "CustomerID", "RoomID", "RoomCharge", "ServiceCharge", "Tax", "Discount", "Total", "Date"]
PAY_COLS = ["PaymentID", "BillingID", "PaymentMethod", "AmountPaid", "PaymentDate", "Status"]


def load_billing_data():
    try:
        return pd.read_csv(BILLING_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=BILL_COLS)
        df.to_csv(BILLING_FILE, index=False)
        return df
    
def load_data():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=BILL_COLS)
        df.to_csv(CSV_FILE, index=False)

    try:
        df = pd.read_csv(CSV_FILE)
        if df.empty:
            df = pd.DataFrame(columns=BILL_COLS)
    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=BILL_COLS)
    except Exception as e:
        print(f"⚠️ Error loading data: {e}")
        df = pd.DataFrame(columns=BILL_COLS)

    for col in BILL_COLS:
        if col not in df.columns:
            df[col] = pd.NA
    return df



def load_payment_data():
    try:
        return pd.read_csv(PAYMENT_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=PAY_COLS)
        df.to_csv(PAYMENT_FILE, index=False)
        return df


def save_billing_data(df):
    df.to_csv(BILLING_FILE, index=False)


def save_payment_data(df):
    df.to_csv(PAYMENT_FILE, index=False)


# ---------------------- BILL GENERATION ----------------------
def generate_bill():
    customers = load_data()  
    rooms = load_csv(ROOM_FILE, ROOM_COLUMNS)
    billings = load_billing_data()

    if customers.empty:
        print("No customers available.")
        return

    print("\n--- Generate Bill ---")
    cid = input("Enter Customer ID: ").strip()

    if not cid.isdigit() or int(cid) not in customers["CustomerID"].astype(int).values:
        print("Invalid Customer ID.")
        return

    cust = customers[customers["CustomerID"] == int(cid)].iloc[0]

    room_id = cust["RoomID"]
    stay_days = cust["DaysOfStay"]
    room_rate = 0
    if room_id in rooms["RoomID"].values:
        room_rate = float(rooms.loc[rooms["RoomID"] == room_id, "Price"].values[0])

    room_charge = room_rate * stay_days
    service_charge = float(input("Enter service charge (if any): ") or 0)
    discount = float(input("Enter discount (if any): ") or 0)
    tax = round((room_charge + service_charge) * 0.18, 2)
    total = round(room_charge + service_charge + tax - discount, 2)

    billing_id = "BILL" + str(np.random.randint(1000, 9999))
    new_bill = pd.DataFrame([{
        "BillingID": billing_id,
        "CustomerID": cid,
        "RoomID": room_id,
        "RoomCharge": room_charge,
        "ServiceCharge": service_charge,
        "Tax": tax,
        "Discount": discount,
        "Total": total,
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])

    billings = pd.concat([billings, new_bill], ignore_index=True)
    save_billing_data(billings)

    print("\n✅ Bill Generated Successfully!")
    print(f"Billing ID: {billing_id}")
    print(f"Customer: {cust['Name']}")
    print(f"Room: {room_id} | Days: {stay_days} | Rate: ₹{room_rate}")
    print(f"Total Amount (after tax & discount): ₹{total}\n")


# ---------------------- PAYMENT ----------------------
def make_payment():
    bills = load_billing_data()
    if bills.empty:
        print("No bills found.")
        return

    try:
        bill_id = int(input("Enter Billing ID to pay: ").strip())
    except ValueError:
        print("Invalid input. Please enter a valid numeric Billing ID.")
        return

    if bill_id not in bills["BillingID"].astype(int).values:
        print("Invalid Billing ID.")
        return

    bill = bills[bills["BillingID"].astype(int) == bill_id].iloc[0]
    print("\n--- BILL DETAILS ---")
    print(bill.to_string())

    amount = bill["Total"]
    method = input("Enter Payment Method (Cash/UPI/Card): ").strip()
    status = "Paid"
    payment_date = datetime.now().strftime("%Y-%m-%d")

    payments = load_payment_data()
    new_payment = pd.DataFrame([{
        "PaymentID": len(payments) + 1,
        "BillingID": bill_id,
        "PaymentMethod": method,
        "AmountPaid": amount,
        "PaymentDate": payment_date,
        "Status": status
    }])
    payments = pd.concat([payments, new_payment], ignore_index=True)
    save_payment_data(payments)

    print(f"✅ Payment of ₹{amount} for Bill ID {bill_id} recorded successfully.")


def view_bills():
    df = load_billing_data()
    if df.empty:
        print("No bills found.")
        return
    print("\n--- ALL BILLS ---")
    print(df.to_string(index=False))


def view_payments():
    df = load_payment_data()
    if df.empty:
        print("No payments found.")
        return
    print("\n--- ALL PAYMENTS ---")
    print(df.to_string(index=False))


# ---------------------- BILLING MENU ----------------------
def billing_menu():
    while True:
        print("""
==================== BILLING & PAYMENTS ====================
1. Generate Bill
2. Make Payment
3. View Bills
4. View Payments
5. Back
============================================================
""")
        ch = input("Enter your choice: ").strip()
        if ch == "1":
            generate_bill()
        elif ch == "2":
            make_payment()
        elif ch == "3":
            view_bills()
        elif ch == "4":
            view_payments()
        elif ch == "5":
            break
        else:
            print("Invalid choice.")


# ==========================================================
# RUN
# ==========================================================
if __name__ == "__main__":
    entry()
