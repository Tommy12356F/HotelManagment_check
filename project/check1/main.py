import random
import string
import pandas as pd
import numpy as np
from datetime import datetime


# ==========================================================
# GLOBALS
ROOM_FILE = "rooms.csv"
BOOKING_FILE = "bookings.csv"
CLIENT_FILE = "clients.csv"

ROOM_COLUMNS = ["RoomID", "RoomType", "Price", "Status"]
BOOK_COLUMNS = ["BookingID", "CustomerName", "RoomID", "CheckIn", "CheckOut"]

c_id = 50
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
# 🏨 ROOM MANAGEMENT (Admin/Reception)
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


def search_room_type():
    df = load_csv(ROOM_FILE, ROOM_COLUMNS)
    r_type = input("Enter room type to search: ").capitalize()
    result = df[df["RoomType"].str.lower() == r_type.lower()]
    if result.empty:
        print("❌ No rooms of this type found.")
    else:
        print(result.to_string(index=False))


# ==========================================================
# 📘 BOOKING MANAGEMENT
# ==========================================================
def make_booking():
    rooms = load_csv(ROOM_FILE, ROOM_COLUMNS)
    bookings = load_csv(BOOKING_FILE, BOOK_COLUMNS)

    available = rooms[rooms["Status"].str.lower() == "available"]
    if available.empty:
        print("❌ No rooms available for booking.")
        return

    print("\n--- AVAILABLE ROOMS ---")
    print(available[["RoomID", "RoomType", "Price"]].to_string(index=False))

    room_id = input("Enter Room ID to book: ").strip()
    if room_id not in available["RoomID"].values:
        print("❌ Invalid Room ID.")
        return

    name = input("Enter your Name: ").strip()
    check_in = input("Enter Check-in Date (dd-mm-yyyy): ").strip()
    check_out = input("Enter Check-out Date (dd-mm-yyyy): ").strip()
    booking_id = "B" + str(np.random.randint(1000, 9999))

    new_booking = pd.DataFrame([[booking_id, name, room_id, check_in, check_out]], columns=BOOK_COLUMNS)
    bookings = pd.concat([bookings, new_booking], ignore_index=True)
    save_csv(BOOKING_FILE, bookings)

    rooms.loc[rooms["RoomID"] == room_id, "Status"] = "Booked"
    save_csv(ROOM_FILE, rooms)
    print(f"\n✅ Booking Confirmed! Booking ID: {booking_id}")


def cancel_booking():
    bookings = load_csv(BOOKING_FILE, BOOK_COLUMNS)
    rooms = load_csv(ROOM_FILE, ROOM_COLUMNS)
    booking_id = input("Enter Booking ID to cancel: ").strip()
    if booking_id not in bookings["BookingID"].values:
        print("❌ Booking not found.")
        return
    row = bookings.loc[bookings["BookingID"] == booking_id].iloc[0]
    room_id = row["RoomID"]
    bookings = bookings[bookings["BookingID"] != booking_id]
    save_csv(BOOKING_FILE, bookings)
    rooms.loc[rooms["RoomID"] == room_id, "Status"] = "Available"
    save_csv(ROOM_FILE, rooms)
    print(f"✅ Booking {booking_id} cancelled successfully.")


def view_all_bookings():
    bookings = load_csv(BOOKING_FILE, BOOK_COLUMNS)
    if bookings.empty:
        print("No bookings yet.")
    else:
        print("\n--- ALL BOOKINGS ---")
        print(bookings.to_string(index=False))


# ==========================================================
# 👩‍💼 ROLE MENUS
# ==========================================================
def manager_menu():
    while True:
        print("\n--- MANAGER MENU ---")
        print("1. View All Rooms")
        print("2. View All Bookings")
        print("3. Cancel Booking")
        print("4. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            view_all_rooms()
        elif choice == "2":
            view_all_bookings()
        elif choice == "3":
            cancel_booking()
        elif choice == "4":
            break
        else:
            print("❌ Invalid choice.")


def receptionist_menu():
    while True:
        print("\n--- RECEPTIONIST MENU ---")
        print("1. Add Room")
        print("2. Update Room")
        print("3. View All Rooms")
        print("4. Back")
        choice = input("Enter choice: ")
        if choice == "1":
            add_room()
        elif choice == "2":
            update_room()
        elif choice == "3":
            view_all_rooms()
        elif choice == "4":
            break
        else:
            print("❌ Invalid choice.")


def customer_menu():
    while True:
        print("\n--- CUSTOMER MENU ---")
        print("1. View Available Rooms")
        print("2. Search Room by Type")
        print("3. Make Booking")
        print("4. Cancel Booking")
        print("5. Back")
        choice = input("Enter choice: ")
        if choice == "1":
            show_available_rooms()
        elif choice == "2":
            search_room_type()
        elif choice == "3":
            make_booking()
        elif choice == "4":
            cancel_booking()
        elif choice == "5":
            break
        else:
            print("❌ Invalid choice.")


# ==========================================================
# 🔑 LOGIN / ENTRY
# ==========================================================
def entry():
    print("\n✨  👩🏻‍🍳  🗝️🛏  🧳  🏩️  WELCOME TO DilliDarshan  🏩️  🧳  🛏  🗝️  👩🏻‍🍳  ✨\n")
    while True:
        print("\nI am:\n1. Manager\n2. Receptionist\n3. Customer\n4. Exit")
        c = input("Enter your choice: ")
        if c == "1":
            pwd = input("Enter Manager password: ")
            if pwd == "root":
                manager_menu()
            else:
                print("❌ Wrong password.")
        elif c == "2":
            name = input("Enter your name: ")
            pwd = input("Enter password: ")
            if pwd == f"{name}@python":
                receptionist_menu()
            else:
                print("❌ Invalid credentials.")
        elif c == "3":
            customer_menu()
        elif c == "4":
            print("👋 Exiting system...")
            break
        else:
            print("❌ Invalid input.")


# ==========================================================
# RUN PROGRAM
# ==========================================================
if __name__ == "__main__":
    entry()
