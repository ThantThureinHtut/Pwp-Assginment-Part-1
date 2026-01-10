# Receptionist.py - Receptionist role implementation for HRMS

def register_guest():
    """Register a new guest"""
    print("\n===== REGISTER GUEST =====")
    
    # Get guest details
    name = input("Enter guest name: ")
    email = input("Enter email: ")
    phone = input("Enter phone number: ")
    id_number = input("Enter ID number: ")
    
    try:
        # Check if guest already exists
        with open("guest.txt", "r") as file:
            guests = file.readlines()
        
        for guest in guests:
            guest_data = guest.strip().split(",")
            if guest_data[2] == email or guest_data[4] == id_number:
                print(f"Guest already registered with ID: {guest_data[0]}")
                return guest_data[0]
        
    except FileNotFoundError:
        # File doesn't exist, create it
        guests = []
    
    # Generate new guest ID
    guest_id = generate_guest_id()
    
    # Create guest record
    guest_record = f"{guest_id},{name},{email},{phone},{id_number}\n"
    
    # Append to guest.txt
    with open("guest.txt", "a") as file:
        file.write(guest_record)
    
    print(f"\nGuest registered successfully!")
    print(f"Guest ID: {guest_id}")
    
    return guest_id


def update_guest_info():
    """Update existing guest information"""
    print("\n===== UPDATE GUEST INFORMATION =====")
    
    guest_id = input("Enter Guest ID: ")
    
    try:
        with open("guest.txt", "r") as file:
            guests = file.readlines()
        
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
                print("1. Name")
                print("2. Email")
                print("3. Phone")
                print("4. ID Number")
                
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
                
                updated_guests.append(",".join(guest_data) + "\n")
                print("Guest information updated successfully!")
            else:
                updated_guests.append(guest)
        
        if not guest_found:
            print("Guest not found!")
            return
        
        # Write updated data back to file
        with open("guest.txt", "w") as file:
            file.writelines(updated_guests)
            
    except FileNotFoundError:
        print("Error: guest.txt file not found!")


def create_booking():
    """Create a new booking"""
    print("\n===== CREATE BOOKING =====")
    
    # Get booking details
    guest_id = input("Enter Guest ID: ")
    
    # Verify guest exists
    guest_exists = False
    try:
        with open("guest.txt", "r") as file:
            guests = file.readlines()
        
        for guest in guests:
            if guest.startswith(guest_id):
                guest_exists = True
                break
        
        if not guest_exists:
            print("Guest not found! Please register the guest first.")
            return
        
    except FileNotFoundError:
        print("Error: guest.txt file not found!")
        return
    
    # Get room number or auto-assign
    print("\nEnter room number (or press Enter for auto-assignment): ")
    room_number = input()
    
    check_in_date = input("Enter check-in date (DD/MM/YYYY): ")
    check_out_date = input("Enter check-out date (DD/MM/YYYY): ")
    
    # Auto-assign room if not specified
    if room_number == "":
        room_number = auto_assign_room()
        if room_number is None:
            print("No rooms available!")
            return
        print(f"Auto-assigned Room: {room_number}")
    
    # Check room availability
    room_available = False
    room_price = 0
    
    try:
        with open("rooms.txt", "r") as file:
            rooms = file.readlines()
        
        for room in rooms:
            room_data = room.strip().split(",")
            if room_data[0] == room_number and room_data[3] == "Available":
                room_available = True
                room_price = float(room_data[2])
                break
        
        if not room_available:
            print("Room is not available!")
            return
        
    except FileNotFoundError:
        print("Error: rooms.txt file not found!")
        return
    
    # Generate booking ID
    booking_id = generate_booking_id()
    
    # Calculate total amount
    total_amount = room_price
    
    # Create booking record
    booking_record = f"{booking_id},{guest_id},{room_number},{check_in_date},{check_out_date},Confirmed,{total_amount},Pending\n"
    
    # Append to bookings.txt
    with open("bookings.txt", "a") as file:
        file.write(booking_record)
    
    # Update room status
    update_room_status(room_number, "Reserved")
    
    print(f"\nBooking created successfully!")
    print(f"Booking ID: {booking_id}")
    print(f"Total Amount: RM{total_amount}")


def check_in():
    """Check in a guest"""
    print("\n===== CHECK-IN =====")
    
    booking_id = input("Enter Booking ID: ")
    
    try:
        with open("bookings.txt", "r") as file:
            bookings = file.readlines()
        
        booking_found = False
        updated_bookings = []
        room_number = ""
        
        for booking in bookings:
            booking_data = booking.strip().split(",")
            
            if booking_data[0] == booking_id:
                booking_found = True
                
                if booking_data[5] != "Confirmed":
                    print(f"Cannot check-in. Booking status: {booking_data[5]}")
                    return
                
                # Update status to Checked-In
                booking_data[5] = "Checked-In"
                room_number = booking_data[2]
                updated_bookings.append(",".join(booking_data) + "\n")
                
                print("\nCheck-in successful!")
                print(f"Guest ID: {booking_data[1]}")
                print(f"Room Number: {room_number}")
            else:
                updated_bookings.append(booking)
        
        if not booking_found:
            print("Booking not found!")
            return
        
        # Write updated bookings
        with open("bookings.txt", "w") as file:
            file.writelines(updated_bookings)
        
        # Update room status to Occupied
        update_room_status(room_number, "Occupied")
        
    except FileNotFoundError:
        print("Error: bookings.txt file not found!")


def check_out():
    """Check out a guest"""
    print("\n===== CHECK-OUT =====")
    
    booking_id = input("Enter Booking ID: ")
    
    try:
        with open("bookings.txt", "r") as file:
            bookings = file.readlines()
        
        booking_found = False
        updated_bookings = []
        room_number = ""
        
        for booking in bookings:
            booking_data = booking.strip().split(",")
            
            if booking_data[0] == booking_id:
                booking_found = True
                
                if booking_data[5] != "Checked-In":
                    print("Invalid booking for check-out!")
                    return
                
                # Calculate late fee if applicable
                # For simplicity, ask receptionist
                late_fee_choice = input("Is there a late check-out? (y/n): ")
                
                if late_fee_choice.lower() == "y":
                    late_days = int(input("Enter number of late days: "))
                    late_fee = late_days * 50
                    current_amount = float(booking_data[6])
                    booking_data[6] = str(current_amount + late_fee)
                    print(f"Late fee applied: RM{late_fee}")
                
                # Update status to Checked-Out
                booking_data[5] = "Checked-Out"
                room_number = booking_data[2]
                updated_bookings.append(",".join(booking_data) + "\n")
                
                print("\nCheck-out successful!")
                print(f"Total Amount: RM{booking_data[6]}")
                
                # Generate receipt
                generate_receipt(booking_data)
            else:
                updated_bookings.append(booking)
        
        if not booking_found:
            print("Booking not found!")
            return
        
        # Write updated bookings
        with open("bookings.txt", "w") as file:
            file.writelines(updated_bookings)
        
        # Update room status to Cleaning
        update_room_status(room_number, "Cleaning")
        
    except FileNotFoundError:
        print("Error: bookings.txt file not found!")


def cancel_booking():
    """Cancel a booking"""
    print("\n===== CANCEL BOOKING =====")
    
    booking_id = input("Enter Booking ID to cancel: ")
    
    try:
        with open("bookings.txt", "r") as file:
            bookings = file.readlines()
        
        booking_found = False
        updated_bookings = []
        room_to_free = ""
        
        for booking in bookings:
            booking_data = booking.strip().split(",")
            
            if booking_data[0] == booking_id:
                booking_found = True
                
                # Check if can be cancelled
                if booking_data[5] in ["Checked-In", "Checked-Out"]:
                    print("Cannot cancel active or completed bookings!")
                    return
                
                # Update status to Cancelled
                booking_data[5] = "Cancelled"
                room_to_free = booking_data[2]
                updated_bookings.append(",".join(booking_data) + "\n")
            else:
                updated_bookings.append(booking)
        
        if not booking_found:
            print("Booking not found!")
            return
        
        # Write updated bookings
        with open("bookings.txt", "w") as file:
            file.writelines(updated_bookings)
        
        # Free up the room
        update_room_status(room_to_free, "Available")
        
        print("Booking cancelled successfully!")
        
    except FileNotFoundError:
        print("Error: bookings.txt file not found!")


def view_room_availability():
    """View room availability list"""
    print("\n===== ROOM AVAILABILITY =====")
    
    try:
        with open("rooms.txt", "r") as file:
            rooms = file.readlines()
        
        available_rooms = []
        occupied_rooms = []
        reserved_rooms = []
        cleaning_rooms = []
        
        for room in rooms:
            room_data = room.strip().split(",")
            
            if len(room_data) >= 4:
                if room_data[3] == "Available":
                    available_rooms.append(room_data)
                elif room_data[3] == "Occupied":
                    occupied_rooms.append(room_data)
                elif room_data[3] == "Reserved":
                    reserved_rooms.append(room_data)
                elif room_data[3] == "Cleaning":
                    cleaning_rooms.append(room_data)
        
        # Display available rooms
        print(f"\nAvailable Rooms: {len(available_rooms)}")
        for room in available_rooms:
            print(f"  Room {room[0]} | Type: {room[1]} | Price: RM{room[2]}")
        
        print(f"\nOccupied Rooms: {len(occupied_rooms)}")
        for room in occupied_rooms:
            print(f"  Room {room[0]} | Type: {room[1]}")
        
        print(f"\nReserved Rooms: {len(reserved_rooms)}")
        for room in reserved_rooms:
            print(f"  Room {room[0]} | Type: {room[1]}")
        
        print(f"\nCleaning Rooms: {len(cleaning_rooms)}")
        for room in cleaning_rooms:
            print(f"  Room {room[0]} | Type: {room[1]}")
        
    except FileNotFoundError:
        print("Error: rooms.txt file not found!")


def auto_assign_room():
    """Auto-assign an available room"""
    try:
        with open("rooms.txt", "r") as file:
            rooms = file.readlines()
        
        for room in rooms:
            room_data = room.strip().split(",")
            if room_data[3] == "Available":
                return room_data[0]
        
        return None
        
    except FileNotFoundError:
        return None


def generate_receipt(booking_data):
    """Generate a text-based receipt"""
    booking_id = booking_data[0]
    guest_id = booking_data[1]
    room_number = booking_data[2]
    check_in = booking_data[3]
    check_out = booking_data[4]
    total_amount = booking_data[6]
    payment_status = booking_data[7]
    
    receipt_filename = f"receipt_{booking_id}.txt"
    
    try:
        with open(receipt_filename, "w") as file:
            file.write("="*50 + "\n")
            file.write("          LOLA HOTEL - RECEIPT\n")
            file.write("="*50 + "\n\n")
            file.write(f"Booking ID: {booking_id}\n")
            file.write(f"Guest ID: {guest_id}\n")
            file.write(f"Room Number: {room_number}\n")
            file.write(f"Check-in Date: {check_in}\n")
            file.write(f"Check-out Date: {check_out}\n")
            file.write(f"Total Amount: RM{total_amount}\n")
            file.write(f"Payment Status: {payment_status}\n")
            file.write("\n" + "="*50 + "\n")
            file.write("     Thank you for staying with us!\n")
            file.write("="*50 + "\n")
        
        print(f"Receipt generated: {receipt_filename}")
        
    except Exception as e:
        print(f"Error generating receipt: {e}")


def generate_guest_id():
    """Generate a unique guest ID"""
    try:
        with open("guest.txt", "r") as file:
            guests = file.readlines()
        
        if len(guests) == 0:
            return "G001"
        
        last_guest = guests[-1].strip().split(",")
        last_id = last_guest[0]
        id_number = int(last_id[1:]) + 1
        return f"G{id_number:03d}"
        
    except FileNotFoundError:
        return "G001"


def generate_booking_id():
    """Generate a unique booking ID"""
    try:
        with open("bookings.txt", "r") as file:
            bookings = file.readlines()
        
        if len(bookings) == 0:
            return "B001"
        
        last_booking = bookings[-1].strip().split(",")
        last_id = last_booking[0]
        id_number = int(last_id[1:]) + 1
        return f"B{id_number:03d}"
        
    except FileNotFoundError:
        return "B001"


def update_room_status(room_number, new_status):
    """Update room status in rooms.txt"""
    try:
        with open("rooms.txt", "r") as file:
            rooms = file.readlines()
        
        updated_rooms = []
        for room in rooms:
            room_data = room.strip().split(",")
            
            if room_data[0] == room_number:
                room_data[3] = new_status
                updated_rooms.append(",".join(room_data) + "\n")
            else:
                updated_rooms.append(room)
        
        with open("rooms.txt", "w") as file:
            file.writelines(updated_rooms)
            
    except FileNotFoundError:
        print("Error: rooms.txt file not found!")


def receptionist_menu():
    """Display receptionist menu and handle user choices"""
    print("\n" + "="*50)
    print("WELCOME TO LOLA HOTEL - RECEPTIONIST PORTAL")
    print("="*50)
    
    while True:
        print("\n===== RECEPTIONIST MENU =====")
        print("1. Register Guest")
        print("2. Update Guest Information")
        print("3. Create Booking")
        print("4. Check-In")
        print("5. Check-Out")
        print("6. Cancel Booking")
        print("7. View Room Availability")
        print("8. Exit")
        
        choice = input("\nEnter your choice (1-8): ")
        
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
            cancel_booking()
        elif choice == "7":
            view_room_availability()
        elif choice == "8":
            print("\nLogging out...")
            break
        else:
            print("Invalid choice! Please enter 1-8.")


# Run the receptionist menu
if __name__ == "__main__":
    receptionist_menu()
