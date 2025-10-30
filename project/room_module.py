import csv

ROOM_FILE = "rooms.csv"

# ---------------------- BASIC FILE HELPERS ----------------------
def load_rooms():
    rooms = []
    try:
        with open(ROOM_FILE, mode="r") as file:
            reader = csv.DictReader(file)
            rooms = list(reader)
    except FileNotFoundError:
        print("⚠️ No rooms file found. Creating a new one...")
        with open(ROOM_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["RoomID", "RoomType", "Price", "Status"])
    return rooms


def save_rooms(rooms):
    with open(ROOM_FILE, mode="w", newline="") as file:
        fieldnames = ["RoomID", "RoomType", "Price", "Status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rooms)


# ---------------------- ADMIN SIDE ----------------------
def add_room():
    rooms = load_rooms()
    room_id = input("Enter Room ID: ")
    room_type = input("Enter Room Type (Single/Double/Suite): ")
    price = input("Enter Price: ")
    status = "Available"
    
    # Check if room already exists
    for room in rooms:
        if room["RoomID"] == room_id:
            print("❌ Room ID already exists!")
            return

    rooms.append({"RoomID": room_id, "RoomType": room_type, "Price": price, "Status": status})
    save_rooms(rooms)
    print("✅ Room added successfully!")


def update_room():
    rooms = load_rooms()
    room_id = input("Enter Room ID to update: ")
    for room in rooms:
        if room["RoomID"] == room_id:
            new_price = input(f"Enter new price (current {room['Price']}): ")
            new_status = input(f"Enter new status (Available/Booked, current {room['Status']}): ")
            room["Price"] = new_price or room["Price"]
            room["Status"] = new_status or room["Status"]
            save_rooms(rooms)
            print("✅ Room updated successfully!")
            return
    print("❌ Room ID not found!")


def delete_room():
    rooms = load_rooms()
    room_id = input("Enter Room ID to delete: ")
    new_rooms = [room for room in rooms if room["RoomID"] != room_id]
    if len(new_rooms) == len(rooms):
        print("❌ Room ID not found!")
    else:
        save_rooms(new_rooms)
        print("✅ Room deleted successfully!")


def view_rooms():
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
        print("5. Exit to Main Menu")
        choice = input("Enter choice: ")

        if choice == "1":
            add_room()
        elif choice == "2":
            update_room()
        elif choice == "3":
            delete_room()
        elif choice == "4":
            view_rooms()
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
        print("No rooms available right now 😔")
    else:
        for room in available:
            print(f"ID: {room['RoomID']} | Type: {room['RoomType']} | Price: ₹{room['Price']}")
    print("------------------------\n")


def search_room_type():
    rooms = load_rooms()
    r_type = input("Enter room type to search (Single/Double/Suite): ").strip().lower()
    found = False
    print(f"\n--- {r_type.capitalize()} Rooms ---")
    for room in rooms:
        if room["RoomType"].lower() == r_type and room["Status"].lower() == "available":
            print(f"ID: {room['RoomID']} | Price: ₹{room['Price']}")
            found = True
    if not found:
        print("No available rooms found for this type.")
    print("----------------------------\n")


def client_room_menu():
    while True:
        print("\n--- CLIENT ROOM MENU ---")
        print("1. View Available Rooms")
        print("2. Search by Room Type")
        print("3. Exit to Main Menu")
        choice = input("Enter choice: ")

        if choice == "1":
            show_available_rooms()
        elif choice == "2":
            search_room_type()
        elif choice == "3":
            break
        else:
            print("❌ Invalid choice, try again.")
