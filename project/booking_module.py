# booking_module.py
"""
Booking Module (uses Pandas + NumPy)
Integrates with:
 - rooms.csv for room data
 - bookings.csv for booking records

Functions:
 - make_booking()
 - cancel_booking()
 - view_all_bookings()
 - open_booking_menu()
"""

import pandas as pd
import numpy as np

ROOM_FILE = "rooms.csv"
BOOKING_FILE = "bookings.csv"

# Columns definition
ROOM_COLUMNS = ["RoomID", "RoomType", "Price", "Status"]
BOOK_COLUMNS = ["BookingID", "CustomerName", "RoomID", "CheckIn", "CheckOut"]


# ---------------------- File Helpers ----------------------
def load_csv(filename, columns):
    """Load CSV into DataFrame (create if missing)."""
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
    """Save DataFrame to CSV file."""
    df.to_csv(filename, index=False)


# ---------------------- Core Booking Functions ----------------------
def make_booking():
    rooms = load_csv(ROOM_FILE, ROOM_COLUMNS)
    bookings = load_csv(BOOKING_FILE, BOOK_COLUMNS)

    available = rooms[rooms["Status"].str.lower() == "available"]
    if available.empty:
        print("❌ No rooms available for booking.")
        return

    print("\n--- AVAILABLE ROOMS ---")
    print(available[["RoomID", "RoomType", "Price"]].to_string(index=False))
    print("------------------------")

    room_id = input("Enter Room ID to book: ").strip()
    if room_id not in available["RoomID"].values:
        print("❌ Invalid or unavailable Room ID.")
        return

    name = input("Enter Customer Name: ").strip()
    check_in = input("Enter Check-in Date (dd-mm-yyyy): ").strip()
    check_out = input("Enter Check-out Date (dd-mm-yyyy): ").strip()

    # Generate booking ID using NumPy random
    booking_id = "B" + str(np.random.randint(1000, 9999))

    # Append booking record
    new_booking = pd.DataFrame(
        [[booking_id, name, room_id, check_in, check_out]],
        columns=BOOK_COLUMNS
    )
    bookings = pd.concat([bookings, new_booking], ignore_index=True)
    save_csv(BOOKING_FILE, bookings)

    # Update room status using vectorized assignment
    rooms.loc[rooms["RoomID"] == room_id, "Status"] = "Booked"
    save_csv(ROOM_FILE, rooms)

    print(f"\n✅ Booking confirmed! Booking ID: {booking_id}")
    print(f"Room {room_id} reserved for {name} from {check_in} to {check_out}.\n")


def cancel_booking():
    rooms = load_csv(ROOM_FILE, ROOM_COLUMNS)
    bookings = load_csv(BOOKING_FILE, BOOK_COLUMNS)

    booking_id = input("Enter Booking ID to cancel: ").strip()
    if booking_id not in bookings["BookingID"].values:
        print("❌ Booking ID not found.")
        return

    # Find booking record
    row = bookings.loc[bookings["BookingID"] == booking_id].iloc[0]
    room_id = row["RoomID"]

    # Remove the booking
    bookings = bookings[bookings["BookingID"] != booking_id].reset_index(drop=True)
    save_csv(BOOKING_FILE, bookings)

    # Mark the room as available again
    rooms.loc[rooms["RoomID"] == room_id, "Status"] = "Available"
    save_csv(ROOM_FILE, rooms)

    print(f"✅ Booking {booking_id} cancelled successfully.")
    print(f"Room {room_id} is now available again.\n")


def view_all_bookings():
    bookings = load_csv(BOOKING_FILE, BOOK_COLUMNS)
    if bookings.empty:
        print("\nNo bookings found.\n")
        return

    print("\n--- ALL BOOKINGS ---")
    print(bookings.to_string(index=False))
    print("--------------------\n")


# ---------------------- Menu Function ----------------------
def open_booking_menu():
    while True:
        print("\n--- BOOKING MODULE ---")
        print("1. Make Booking")
        print("2. Cancel Booking")
        print("3. View All Bookings")
        print("4. Back to Previous Menu")
        choice = input("Enter your choice: ").strip()

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
