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
    database = open("guest.txt", "r")
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
    database = open("guest.txt", "a")
    database.write(guest_record)
    database.close()
    
    print(f"\nGuest registered successfully!")
    print(f"Guest ID: {guest_id}")
    
    return guest_id


def update_guest_info():
    """Update existing guest information"""
    print("\n===== UPDATE GUEST INFORMATION =====")
    
    guest_id = input("Enter Guest ID: ")
    
    database = open("guest.txt", "r")
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
    database = open("guest.txt", "w")
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
    
    for booking in bookings:
        booking_data = booking.strip().split(",")
        
        if booking_data[0] == booking_id:
            booking_found = True
            
            if booking_data[5] != "Confirmed":
                print(f"Cannot check-in. Booking status is {booking_data[5]}.")
                updated_bookings.append(booking)