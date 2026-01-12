# Guest.py - Guest role implementation for HRMS

def view_available_rooms():
    """Display all available rooms"""
    print("\n===== AVAILABLE ROOMS =====")

    # Read rooms from file
    database = open("database/rooms.txt", "r")
    rooms = database.readlines()
    database.close()

    available_count = 0
    for room in rooms:
        # Split room data by comma
        room_data = room.strip().split(",")

        room_number = room_data[0]
        room_type = room_data[1]
        price = room_data[2]
        status = room_data[3]

        # Only show available rooms
        if status == "Available":
            print(f"Room {room_number} | Type: {room_type} | Price: RM{price}")
            available_count = available_count + 1

    if available_count == 0:
        print("No rooms available at the moment.")
    else:
        print(f"\nTotal available rooms: {available_count}")


def make_reservation(guest_id):
    """Make a new reservation"""
    print("\n===== MAKE RESERVATION =====")

    # Get reservation details from user
    print("Enter room number (or press Enter for auto-assignment): ")
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

    # Check if room is available
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
        print("Sorry, this room is not available.")
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

    # Update room status to Reserved
    update_room_status(room_number, "Reserved")

    print(f"\nReservation successful!")
    print(f"Booking ID: {booking_id}")
    print(f"Total Amount: RM{total_amount}")


def cancel_reservation(guest_id):
    """Cancel an existing reservation"""
    print("\n===== CANCEL RESERVATION =====")

    booking_id = input("Enter booking ID to cancel: ")

    # Read all bookings
    database = open("database/bookings.txt", "r")
    bookings = database.readlines()
    database.close()

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
            updated_line = ",".join(booking_data) + "\n"
            updated_bookings.append(updated_line)
        else:
            updated_bookings.append(booking)

    if booking_found == False:
        print("Booking not found or you don't have permission to cancel it.")
        return

    # Write updated bookings back to file
    database = open("database/bookings.txt", "w")
    database.writelines(updated_bookings)
    database.close()

    # Free up the room
    update_room_status(room_to_free, "Available")

    print("Reservation cancelled successfully!")


def view_billing_summary(guest_id):
    """View billing summary and payment history"""
    print("\n===== BILLING SUMMARY =====")

    database = open("database/bookings.txt", "r")
    bookings = database.readlines()
    database.close()

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
            total_amount = total_amount + amount

            # Check payment status
            if booking_data[7] == "Paid":
                paid_amount = paid_amount + amount
            else:
                outstanding_amount = outstanding_amount + amount

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


def guest_menu():
    """Display guest menu and handle user choices"""
    print("\n" + "="*50)
    print("WELCOME TO LOLA HOTEL - GUEST PORTAL")
    print("="*50)

    # Login or get guest ID
    guest_id = str(input("\nEnter your Guest ID: "))

    while True:
        print("\n===== GUEST MENU =====")
        print("(1) View Available Rooms")
        print("(2) Make Reservation")
        print("(3) Cancel Reservation")
        print("(4) View Billing Summary")
        print("(5) Exit")

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

