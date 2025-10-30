import room_module

while True:
    print("\n=== HOTEL MANAGEMENT SYSTEM ===")
    print("1. Admin - Room Management")
    print("2. Client - View Rooms")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        room_module.admin_room_menu()
    elif choice == "2":
        room_module.client_room_menu()
    elif choice == "3":
        print("Goodbye 👋")
        break
    else:
        print("Invalid option!")
