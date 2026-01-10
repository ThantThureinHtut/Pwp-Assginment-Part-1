def room_add():
    print("Adding a new room...")
            # Check for duplicate Room ID
    rooms_check = open("database/rooms.txt", "r")
    rooms = rooms_check.readlines()
    room_id = input("Enter Room ID: ")
    if any(room_id in line for line in rooms):
        print("Room ID already exists. Please try again.")
    # If no duplicate, proceed to add room
    room_type = input("Enter Room Type: ")
    price = input("Enter Price RM: ")
    database = open("database/rooms.txt", "a")
    database.write(f"{room_id}:{room_type}:RM {price}\n")
    database.close()
def room_update():
    print("Updating room details...")
    # Display current rooms
    database = open("database/rooms.txt", "r")
    lines = database.readlines()
    print("--- Current Rooms ---")
    for line in lines:
        print(line.strip())
    database.close()
    print("---------------------")

    # Get Room ID to update
    database = open("database/rooms.txt", "a")
    room_id = input("Enter Room ID to update: ")
    new_lines = []
    for line in lines:
        parts = line.strip().split(":")
        # Update the room details if Room ID matches
        if parts[0] == room_id:
            new_room_type = input("Enter new Room Type: ")
            new_price = input("Enter new Price RM: ")
            new_lines.append(f"{room_id}:{new_room_type}:RM {new_price}\n")
        else:
            # Keep the line unchanged if Room ID does not match
            print("Room ID not found. No changes made.")
            new_lines.append(line)
            database = open("database/rooms.txt", "w")
            database.writelines(new_lines)
            database.close()
            break
            
            

    # Write updated lines back to the file
    database = open("database/rooms.txt", "w")
    database.writelines(new_lines)
    database.close()

def room_delete():
    print("Deleting a room...")
    # Display current rooms
    database = open("database/rooms.txt", "r")
    lines = database.readlines()
    print("--- Current Rooms ---")
    for line in lines:
        print(line.strip())
    database.close()
    print("---------------------")

    # Get Room ID to delete
    room_id = input("Enter Room ID to delete: ")
    new_lines = []
    found = False
    for line in lines:
        parts = line.strip().split(":")
        # Skip the line if Room ID matches (i.e., delete it)
        if parts[0] == room_id:
            found = True
            continue
        else:
            new_lines.append(line)

    if not found:
        print("Room ID not found. No changes made.")
    else:
        # Write updated lines back to the file
        database = open("database/rooms.txt", "w")
        database.writelines(new_lines)
        database.close()
        print(f"Room ID {room_id} deleted successfully.")

def view_all_bookings():
    print("---- All Bookings ----")
    database = open("database/bookings.txt", "r")
    bookings = database.readlines()
    for booking in bookings:
        print(booking.strip())
    database.close()

def monthly_report():
    print("---- Monthly Report ----")
    database = open("database/bookings.txt", "r")
    bookings = database.readlines()
    total_revenue = 0
    for booking in bookings:
        print(booking.strip())
        parts = booking.strip().split(":")
        price_part = parts[3]  # Assuming price is the 4th element
        price_value = float(price_part)
        total_revenue += price_value

    print(f"Total Revenue for the Month: RM {total_revenue}")
def occupancy_report():
    print("---- Occupancy Report ----")
    # Calculate occupancy rate
    database_rooms = open("database/rooms.txt", "r")
    rooms = database_rooms.readlines()
    total_rooms = len(rooms)
    database_bookings = open("database/bookings.txt", "r")
    bookings = database_bookings.readlines()
    booked_rooms = len(bookings)
    # Calculate occupancy rate
    occupancy_rate = (booked_rooms / total_rooms) * 100 if total_rooms > 0 else 0
    print(f"Total Rooms: {total_rooms}")
    print(f"Booked Rooms: {booked_rooms}")
    print(f"Occupancy Rate: {occupancy_rate:.2f}%")
    database_rooms.close()
    database_bookings.close()


def manager():
    while True:
        print("------------ Manager Dashboard -----------")
        print(f"(1) Room Add\n(2) Room Update\n(3) Room Delete\n(4) View All Bookings\n(5) Monthly Report\n(6) Occupancy Report\n(7) Logout")
        choice = input("Select an option (1-7): ")
        if choice == '1':   
           room_add();
        elif choice == '2':
            room_update();
        elif choice == '3':
           room_delete();
        elif choice == '4':
            view_all_bookings();
        elif choice == '5':
            monthly_report();
        elif choice == '6':
            occupancy_report();
        elif choice == '7':
            break


