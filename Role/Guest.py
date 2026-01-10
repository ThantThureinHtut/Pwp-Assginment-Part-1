
def view_available_rooms():
    """Display all available rooms"""
    print("\n===== AVAILABLE ROOMS =====")
    
    try:
        # Read rooms from file
        with open("rooms.txt", "r") as file:
            rooms = file.readlines()
        
        available_count = 0
        for room in rooms:
            # Split room data by comma
            room_data = room.strip().split(",")
            
            if len(room_data) >= 4:
                room_number = room_data[0]
                room_type = room_data[1]
                price = room_data[2]
                status = room_data[3]
                
                # Only show available rooms
                if status == "Available":
                    print(f"Room {room_number} | Type: {room_type} | Price: RM{price} | Status: {status}")
                    available_count += 1
        
        if available_count == 0:
            print("No rooms available at the moment.")
        else:
            print(f"\nTotal available rooms: {available_count}")
            
    except FileNotFoundError:
        print("Error: rooms.txt file not found!")


def make_reservation(guest_id):
    """Make a new reservation"""
    print("\n===== MAKE RESERVATION =====")
    
    # Get reservation details from user
    room_number = input("Enter room number: ")
    check_in_date = input("Enter check-in date (DD/MM/YYYY): ")
    check_out_date = input("Enter check-out date (DD/MM/YYYY): ")
    
    # Check if room is available
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
            print("Sorry, this room is not available.")
            return
        
        # Generate booking ID
        booking_id = generate_booking_id()
        
        # Calculate total amount (simple calculation)
        total_amount = room_price
        
        # Create booking record
        booking_record = f"{booking_id},{guest_id},{room_number},{check_in_date},{check_out_date},Confirmed,{total_amount},Pending\n"
        
        # Append to bookings.txt
        with open("bookings.txt", "a") as file:
            file.write(booking_record)
        
        # Update room status to Reserved
        update_room_status(room_number, "Reserved")
        
        print(f"\nReservation successful!")
        print(f"Booking ID: {booking_id}")
        print(f"Total Amount: RM{total_amount}")
        
    except FileNotFoundError:
        print("Error: Required files not found!")


def cancel_reservation(guest_id):
    """Cancel an existing reservation"""
    print("\n===== CANCEL RESERVATION =====")
    
    booking_id = input("Enter booking ID to cancel: ")
    
    try:
        # Read all bookings
        with open("bookings.txt", "r") as file:
            bookings = file.readlines()
        
        booking_found = False
        updated_bookings = []
        room_to_free = ""
        
        for booking in bookings:
            booking_data = booking.strip().split(",")
            
            # Check if this is the booking to cancel
            if booking_data[0] == booking_id and booking_data[1] == guest_id:
                booking_found = True
                
                # Check if already cancelled
                if booking_data[5] == "Cancelled":
                    print("This booking is already cancelled.")
                    return
                
                # Update status to Cancelled
                booking_data[5] = "Cancelled"
                room_to_free = booking_data[2]
                updated_bookings.append(",".join(booking_data) + "\n")
            else:
                updated_bookings.append(booking)
        
        if not booking_found:
            print("Booking not found or you don't have permission to cancel it.")
            return
        
        # Write updated bookings back to file
        with open("bookings.txt", "w") as file:
            file.writelines(updated_bookings)
        
        # Free up the room
        update_room_status(room_to_free, "Available")
        
        print("Reservation cancelled successfully!")
        
    except FileNotFoundError:
        print("Error: bookings.txt file not found!")


def view_billing_summary(guest_id):
    """View billing summary and payment history"""
    print("\n===== BILLING SUMMARY =====")
    
    try:
        with open("bookings.txt", "r") as file:
            bookings = file.readlines()
        
        total_amount = 0
        paid_amount = 0
        outstanding_amount = 0
        guest_bookings = []
        
        # Find all bookings for this guest
        for booking in bookings:
            booking_data = booking.strip().split(",")
            
            if booking_data[1] == guest_id:
                guest_bookings.append(booking_data)
                amount = float(booking_data[6])
                total_amount += amount
                
                # Check payment status
                if booking_data[7] == "Paid":
                    paid_amount += amount
                else:
                    outstanding_amount += amount
        
        if len(guest_bookings) == 0:
            print("No bookings found for your account.")
            return
        
        # Display summary
        print(f"Total Amount: RM{total_amount:.2f}")
        print(f"Paid Amount: RM{paid_amount:.2f}")
        print(f"Outstanding: RM{outstanding_amount:.2f}")
        
        print("\n===== PAYMENT HISTORY =====")
        for booking in guest_bookings:
            print(f"Booking ID: {booking[0]}")
            print(f"Room: {booking[2]}")
            print(f"Check-in: {booking[3]} | Check-out: {booking[4]}")
            print(f"Status: {booking[5]}")
            print(f"Amount: RM{booking[6]} | Payment: {booking[7]}")
            print("-" * 50)
        
    except FileNotFoundError:
        print("Error: bookings.txt file not found!")


def generate_booking_id():
    """Generate a unique booking ID"""
    try:
        with open("bookings.txt", "r") as file:
            bookings = file.readlines()
        
        if len(bookings) == 0:
            return "B001"
        
        # Get last booking ID
        last_booking = bookings[-1].strip().split(",")
        last_id = last_booking[0]
        
        # Extract number and increment
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


def guest_menu():
    """Display guest menu and handle user choices"""
    print("\n" + "="*50)
    print("WELCOME TO LOLA HOTEL - GUEST PORTAL")
    print("="*50)
    
    # Login or get guest ID
    guest_id = input("\nEnter your Guest ID: ")
    
    while True:
        print("\n===== GUEST MENU =====")
        print("1. View Available Rooms")
        print("2. Make Reservation")
        print("3. Cancel Reservation")
        print("4. View Billing Summary")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == "1":
            view_available_rooms()
        elif choice == "2":
            make_reservation(guest_id)
        elif choice == "3":
            cancel_reservation(guest_id)
        elif choice == "4":
            view_billing_summary(guest_id)
        elif choice == "5":
            print("\nThank you for using LOLA HOTEL system!")
            break
        else:
            print("Invalid choice! Please enter 1-5.")


# Run the guest menu
if __name__ == "__main__":
    guest_menu()
