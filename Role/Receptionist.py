# Receptionist.py - Receptionist role implementation for HRMS

def register_guest():
    """Register a new guest"""
    print("\n===== REGISTER GUEST =====")
    
    # Get guest details
    name = input("Enter guest name: ")
    email = input("Enter email: ")
    phone = input("Enter phone number: ")
    id_number = input("Enter ID number: ")
    
    # Check if guest already exists
    database = open("database/guest.txt", "r")
    guests = database.readlines()
    database.close()
    
    for guest in guests:
        guest_data = guest.strip().split(",")
        if guest_data[2] == email or guest_data[4] == id_number:
            print(f"Guest already registered with ID: {guest_data[0]}")
            return guest_data[0]
    
    # Generate new guest ID
    guest_id = generate_guest_id()
    
    # Create guest record
    guest_record = f"{guest_id},{name},{email},{phone},{id_number}\n"
    
    # Append to guest.txt
    database = open("database/guest.txt", "a")
    database.write(guest_record)
    database.close()
    
    print(f"\nGuest registered successfully!")
    print(f"Guest ID: {guest_id}")
    
    return guest_id


def update_guest_info():
    """Update existing guest information"""
    print("\n===== UPDATE GUEST INFORMATION =====")
    
    guest_id = input("Enter Guest ID: ")
    
    database = open("database/guest.txt", "r")
    guests = database.readlines()
    database.close()
    
    guest_found = False
    updated_guests = []
    
    for guest in guests:
        guest_data = guest.strip().split(",")
        
        if guest_data[0] == guest_id:
            guest_found = True
            
            # Display current info
            print(f"\nCurrent Information:")
            print(f"Name: {guest_data[1]}")
            print(f"Email: {guest_data[2]}")
            print(f"Phone: {guest_data[3]}")
            print(f"ID Number: {guest_data[4]}")
            
            # Ask what to update
            print("\nWhat would you like to update?")
            print("(1) Name")
            print("(2) Email")
            print("(3) Phone")
            print("(4) ID Number")
            
            update_choice = input("Enter choice (1-4): ")
            
            if update_choice == "1":
                guest_data[1] = input("Enter new name: ")
            elif update_choice == "2":
                guest_data[2] = input("Enter new email: ")
            elif update_choice == "3":
                guest_data[3] = input("Enter new phone: ")
            elif update_choice == "4":
                guest_data[4] = input("Enter new ID number: ")
            else:
                print("Invalid choice!")
                return
            
            updated_line = ",".join(guest_data) + "\n"
            updated_guests.append(updated_line)
            print("Guest information updated successfully!")
        else:
            updated_guests.append(guest)
    
    if guest_found == False:
        print("Guest not found!")
        return
    
    # Write updated data back to file
    database = open("database/guest.txt", "w")
    database.writelines(updated_guests)
    database.close()


def create_booking():
    """Create a new booking"""
    print("\n===== CREATE BOOKING =====")
    
    # Get booking details
    guest_id = input("Enter Guest ID: ")
    
    # Verify guest exists
    guest_exists = False
    database = open("database/guest.txt", "r")
    guests = database.readlines()
    database.close()
    
    for guest in guests:
        if guest.startswith(guest_id):
            guest_exists = True
            break
    
    if guest_exists == False:
        print("Guest not found! Please register the guest first.")
        return
    
    # Get room number or auto-assign
    print("\nEnter room number (or press Enter for auto-assignment): ")
    room_number = input()
    
    check_in_date = input("Enter check-in date (DD/MM/YYYY): ")
    check_out_date = input("Enter check-out date (DD/MM/YYYY): ")
    
    # Auto-assign room if not specified
    if room_number == "":
        room_number = auto_assign_room()
        if room_number == "":
            print("No rooms available!")
            return
        print(f"Auto-assigned Room: {room_number}")
    
    # Check room availability
    room_available = False
    room_price = 0
    
    database = open("database/rooms.txt", "r")
    rooms = database.readlines()
    database.close()
    
    for room in rooms:
        room_data = room.strip().split(",")
        if room_data[0] == room_number and room_data[3] == "Available":
            room_available = True
            room_price = float(room_data[2])
            break
    
    if room_available == False:
        print("Room is not available!")
        return
    
    # Generate booking ID
    booking_id = generate_booking_id()
    
    # Calculate total amount
    total_amount = room_price
    
    # Create booking record
    booking_record = f"{booking_id},{guest_id},{room_number},{check_in_date},{check_out_date},Confirmed,{total_amount},Pending\n"
    
    # Append to bookings.txt
    database = open("database/bookings.txt", "a")
    database.write(booking_record)
    database.close()
    
    # Update room status
    update_room_status(room_number, "Reserved")
    
    print(f"\nBooking created successfully!")
    print(f"Booking ID: {booking_id}")
    print(f"Total Amount: RM{total_amount}")


def check_in():
    """Check in a guest"""
    print("\n===== CHECK-IN =====")
    
    booking_id = input("Enter Booking ID: ")
    
    database = open("database/bookings.txt", "r")
    bookings = database.readlines()
    database.close()
    
    booking_found = False
    updated_bookings = []
    room_number = ""
    status_updated = False
    
    for booking in bookings:
        booking_data = booking.strip().split(",")
        
        if booking_data[0] == booking_id:
            booking_found = True
            
            if booking_data[5] != "Confirmed":
                print(f"Cannot check-in. Booking status is {booking_data[5]}.")
                updated_bookings.append(booking)
                continue

            booking_data[5] = "Checked-In"
            room_number = booking_data[2]
            updated_line = ",".join(booking_data) + "\n"
            updated_bookings.append(updated_line)
            status_updated = True
        else:
            updated_bookings.append(booking)

    if booking_found == False:
        print("Booking not found!")
        return

    if status_updated == False:
        return

    database = open("database/bookings.txt", "w")
    database.writelines(updated_bookings)
    database.close()

    update_room_status(room_number, "Occupied")
    print("Check-in successful!")


def check_out():
    """Check out a guest"""
    print("\n===== CHECK-OUT =====")

    booking_id = input("Enter Booking ID: ")

    database = open("database/bookings.txt", "r")
    bookings = database.readlines()
    database.close()

    booking_found = False
    updated_bookings = []
    room_number = ""
    status_updated = False

    for booking in bookings:
        booking_data = booking.strip().split(",")

        if booking_data[0] == booking_id:
            booking_found = True

            if booking_data[5] != "Checked-In":
                print(f"Cannot check-out. Booking status is {booking_data[5]}.")
                updated_bookings.append(booking)
                continue

            booking_data[5] = "Checked-Out"
            room_number = booking_data[2]
            updated_line = ",".join(booking_data) + "\n"
            updated_bookings.append(updated_line)
            status_updated = True
        else:
            updated_bookings.append(booking)

    if booking_found == False:
        print("Booking not found!")
        return

    if status_updated == False:
        return

    database = open("database/bookings.txt", "w")
    database.writelines(updated_bookings)
    database.close()

    update_room_status(room_number, "Dirty")
    print("Check-out successful! Room marked as Dirty.")


def auto_assign_room():
    """Auto-assign an available room"""
    database = open("database/rooms.txt", "r")
    rooms = database.readlines()
    database.close()

    for room in rooms:
        room_data = room.strip().split(",")
        if room_data[3] == "Available":
            return room_data[0]

    return ""


def generate_booking_id():
    """Generate a unique booking ID"""
    database = open("database/bookings.txt", "r")
    bookings = database.readlines()
    database.close()

    for booking in reversed(bookings):
        clean_line = booking.strip()
        if clean_line == "":
            continue
        last_id = clean_line.split(",")[0]
        if len(last_id) < 2 or last_id[0] != "B":
            continue
        id_number_part = last_id[1:]
        if id_number_part.isdigit() == False:
            continue
        id_number = int(id_number_part) + 1
        return "B" + str(id_number).zfill(3)

    return "B001"


def generate_guest_id():
    """Generate a unique guest ID"""
    database = open("database/guest.txt", "r")
    guests = database.readlines()
    database.close()

    if len(guests) == 0:
        return "G001"

    last_guest = guests[-1].strip().split(",")
    last_id = last_guest[0]

    id_number = int(last_id[1:]) + 1
    new_id = "G" + str(id_number).zfill(3)
    return new_id


def update_room_status(room_number, new_status):
    """Update room status in rooms.txt"""
    database = open("database/rooms.txt", "r")
    rooms = database.readlines()
    database.close()

    updated_rooms = []
    for room in rooms:
        room_data = room.strip().split(",")

        if room_data[0] == room_number:
            room_data[3] = new_status
            updated_line = ",".join(room_data) + "\n"
            updated_rooms.append(updated_line)
        else:
            updated_rooms.append(room)

    database = open("database/rooms.txt", "w")
    database.writelines(updated_rooms)
    database.close()


def receptionist():
    """Display receptionist menu and handle user choices"""
    print("\n" + "=" * 50)
    print("WELCOME TO LOLA HOTEL - RECEPTIONIST PORTAL")
    print("=" * 50)

    while True:
        print("\n===== RECEPTIONIST MENU =====")
        print("(1) Register Guest")
        print("(2) Update Guest Information")
        print("(3) Create Booking")
        print("(4) Check-In Guest")
        print("(5) Check-Out Guest")
        print("(6) Exit")

        choice = input("\nEnter your choice (1-6): ")

        if choice == "1":
            register_guest()
        elif choice == "2":
            update_guest_info()
        elif choice == "3":
            create_booking()
        elif choice == "4":
            check_in()
        elif choice == "5":
            check_out()
        elif choice == "6":
            print("\nExiting receptionist portal.")
            break
        else:
            print("Invalid choice! Please enter 1-6.")
