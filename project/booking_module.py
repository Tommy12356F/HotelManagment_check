import csv
import random
import datetime

ROOM_FILE = "rooms.csv"
BOOKING_FILE = "bookings.csv"


# ---------------------- Helper Functions ----------------------
def load_csv(filename):
    try:
        with open(filename, mode="r") as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        print(f"⚠️ File '{filename}' not found. Creating a new one.")
        with open(filename, mode="w", newline="") as file:
            if "room" in filename:
                writer = csv.writer(file)
                writer.writerow(["RoomID", "RoomType", "Price", "Status"])
            else:
                writer = csv.writer(file)
                writer.writerow(["BookingID", "CustomerName", "RoomID", "CheckIn", "CheckOut"])
        return []


def save_csv(filename, data, headers):
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)


# ---------------------- Booking Logic ----------------------
def make_booking():
    rooms = load_csv(ROOM_FILE)
    bookings = load_csv(BOOKING_FILE)

    available = [r for r in rooms if r["Status"].lower() == "available"]

    if not available:
        print("❌ No rooms available for booking.")
        return

    print("\n--- AVAILABLE ROOMS ---")
    for room in available:
        print(f"Room ID: {room['RoomID']} | Type: {room['RoomType']} | Price: ₹{room['Price']}")
    print("------------------------")

    room_id = input("Enter the Room ID you want to book: ")

    # Check if room exists & is available
    selected = None
    for room in rooms:
        if room["RoomID"] == room_id:
            if room["Status"].lower() != "available":
                print("❌ Room is already booked!")
                return
            selected = room
            break

    if not selected:
        print("❌ Invalid Room ID.")
        return

    # Get customer details
    name = input("Enter Customer Name: ")
    check_in = input("Enter Check-in Date (dd-mm-yyyy): ")
    check_out = input("Enter Check-out Date (dd-mm-yyyy): ")

    # Generate booking ID
    booking_id = "B" + str(random.randint(1000, 9999))

    # Save booking
    bookings.append({
        "BookingID": booking_id,
        "CustomerName": name,
        "RoomID": room_id,
        "CheckIn": check_in,
        "CheckOut": check_out
    })
    save_csv(BOOKING_FILE, bookings, ["BookingID", "CustomerName", "RoomID", "CheckIn", "CheckOut"])

    # Update room status
    for room in rooms:
        if room["RoomID"] == room_id:
            room["Status"] = "Booked"
    save_csv(ROOM_FILE, rooms, ["RoomID", "RoomType", "Price", "Status"])

    print(f"\n✅ Booking confirmed for {name} in Room {room_id}!")
    print(f"Booking ID: {booking_id}")
    print("----------------------------")


def cancel_booking():
    bookings = load_csv(BOOKING_FILE)
    rooms = load_csv(ROOM_FILE)
    booking_id = input("Enter Booking ID to cancel: ")

    found = False
    for booking in bookings:
        if booking["BookingID"] == booking_id:
            found = True
            room_id = booking["RoomID"]
            bookings.remove(booking)
            print(f"✅ Booking {booking_id} cancelled successfully!")

            # Update room status to Available
            for room in rooms:
                if room["RoomID"] == room_id:
                    room["Status"] = "Available"
            break

    if not found:
        print("❌ Booking ID not found.")
        return

    # Save updates
    save_csv(BOOKING_FILE, bookings, ["BookingID", "CustomerName", "RoomID", "CheckIn", "CheckOut"])
    save_csv(ROOM_FILE, rooms, ["RoomID", "RoomType", "Price", "Status"])


def view_all_bookings():
    bookings = load_csv(BOOKING_FILE)
    if not bookings:
        print("No bookings found.")
        return
    print("\n--- ALL BOOKINGS ---")
    for b in bookings:
        print(f"ID: {b['BookingID']} | Name: {b['CustomerName']} | Room: {b['RoomID']} | {b['CheckIn']} → {b['CheckOut']}")
    print("---------------------")


# ---------------------- Booking Menu ----------------------
def open_booking_menu():
    while True:
        print("\n--- BOOKING MODULE ---")
        print("1. Make Booking")
        print("2. Cancel Booking")
        print("3. View All Bookings")
        print("4. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            make_booking()
        elif choice == "2":
            cancel_booking()
        elif choice == "3":
            view_all_bookings()
        elif choice == "4":
            break
        else:
            print("❌ Invalid choice, try again.")
