import csv
import booking_module  # for redirect from client side

ROOM_FILE = "rooms.csv"

# ---------------------- Common Helper ----------------------
def load_rooms():
    """Read room data from CSV file"""
    rooms = []
    try:
        with open(ROOM_FILE, mode="r") as file:
            reader = csv.DictReader(file)
            rooms = list(reader)
    except FileNotFoundError:
        print("⚠️ No room file found.")
    return rooms


def save_rooms(rooms):
    """Save updated room data to CSV file"""
    with open(ROOM_FILE, mode="w", newline="") as file:
        fieldnames = ["RoomID", "RoomType", "Price", "Status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rooms)


# ---------------------- ADMIN SIDE ----------------------
def add_room():
    rooms = load_rooms()
    room_id = input("Enter Room ID: ")
    for room in rooms:
        if room["RoomID"] == room_id:
            print("❌ Room ID already exists!")
            return
    room_type = input("Enter Room Type (Single/Double/Suite): ")
    price = input("Enter Price: ")
    status = "Available"
    rooms.append({"RoomID": room_id, "RoomType": room_type, "Price": price, "Status": status})
    save_rooms(rooms)
    print("✅ Room added successfully!")


def update_room():
    rooms = load_rooms()
    room_id = input("Enter Room ID to update: ")
    for room in rooms:
        if room["RoomID"] == room_id:
            new_price = input(f"Enter new price (current {room['Price']}): ") or room["Price"]
            new_status = input(f"Enter new status (Available/Booked, current {room['Status']}): ") or room["Status"]
            room["Price"], room["Status"] = new_price, new_status
            save_rooms(rooms)
            print("✅ Room updated successfully!")
            return
    print("❌ Room not found!")


def delete_room():
    rooms = load_rooms()
    room_id = input("Enter Room ID to delete: ")
    new_rooms = [r for r in rooms if r["RoomID"] != room_id]
    if len(new_rooms) == len(rooms):
        print("❌ Room ID not found!")
    else:
        save_rooms(new_rooms)
        print("✅ Room deleted successfully!")


def view_all_rooms():
    rooms = load_rooms()
    print("\n--- ALL ROOMS ---")
    for room in rooms:
        print(f"ID: {room['RoomID']} | Type: {room['RoomType']} | Price: ₹{room['Price']} | Status: {room['Status']}")
    print("-----------------\n")


def admin_room_menu():
    while True:
        print("\n--- ADMIN ROOM MENU ---")
        print("1. Add Room")
        print("2. Update Room")
        print("3. Delete Room")
        print("4. View All Rooms")
        print("5. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_room()
        elif choice == "2":
            update_room()
        elif choice == "3":
            delete_room()
        elif choice == "4":
            view_all_rooms()
        elif choice == "5":
            break
        else:
            print("❌ Invalid choice, try again.")


# ---------------------- CLIENT SIDE ----------------------
def show_available_rooms():
    rooms = load_rooms()
    available = [r for r in rooms if r["Status"].lower() == "available"]
    print("\n--- AVAILABLE ROOMS ---")
    if not available:
        print("No rooms available 😔")
    else:
        for room in available:
            print(f"Room ID: {room['RoomID']} | Type: {room['RoomType']} | Price: ₹{room['Price']}")
    print("------------------------\n")


def search_room_type():
    rooms = load_rooms()
    r_type = input("Enter room type to search (Single/Double/Suite): ").strip().lower()
    found = False
    print(f"\n--- {r_type.capitalize()} Rooms ---")
    for room in rooms:
        if room["RoomType"].lower() == r_type:
            print(f"ID: {room['RoomID']} | Price: ₹{room['Price']} | Status: {room['Status']}")
            found = True
    if not found:
        print("No rooms found for this type.")
    print("----------------------------\n")


def client_room_menu():
    while True:
        print("\n--- CLIENT ROOM MENU ---")
        print("1. View Available Rooms")
        print("2. Search Rooms by Type")
        print("3. Go to Booking Module")
        print("4. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            show_available_rooms()
        elif choice == "2":
            search_room_type()
        elif choice == "3":
            print("Redirecting to Booking Module...\n")
            booking_module.open_booking_menu()
        elif choice == "4":
            break
        else:
            print("❌ Invalid choice, try again.")
