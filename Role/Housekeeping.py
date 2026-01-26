def view_tasks():
    print("\n" + "="*40)
    print("      HOUSEKEEPING TO-DO LIST")
    print("="*40)
    print(f"{'Room ID':<10} | {'Status':<15}")
    print("-" * 30)

    # Directly open the file. We assume it exists.
    f = open("database/rooms.txt", "r")
    lines = f.readlines()
    f.close()

    count = 0 

    for line in lines:
        clean_line = line.strip()
        
        # If line is empty, skip to next loop
        if len(clean_line) == 0:
            continue
        
        data = clean_line.split(":") 

        # If line is broken/short, skip it
        if len(data) < 4:
            continue

        room_id = data[0]
        status = data[3]

        if status == "Dirty" or status == "Maintenance":
            print(f"{room_id:<10} | {status:<15}")
            count = count + 1
    
    if count == 0:
        print("No active tasks. All rooms are clean.")


def update_status():
    print("\n" + "="*40)
    print("      UPDATE ROOM STATUS")
    print("="*40)

    target_id = input("Enter Room ID to update: ")
    
    # Read all lines
    f = open("database/rooms.txt", "r")
    lines = f.readlines()
    f.close()

    found = False
    new_file_content = []

    for line in lines:
        clean_line = line.strip()
        
        # Skip empty lines
        if len(clean_line) == 0:
            continue

        data = clean_line.split(":")

        # Skip broken lines but save them back
        if len(data) < 4:
            new_file_content.append(line)
            continue

        current_id = data[0]
        current_status = data[3]

        if current_id == target_id:
            found = True
            print(f"Current Status: {current_status}")
            print("1. Available\n2. Dirty\n3. Maintenance")
            choice = input("Select Status: ")

            if choice == "1": current_status = "Available"
            elif choice == "2": current_status = "Dirty"
            elif choice == "3": current_status = "Maintenance"
            
            print(f"Room {target_id} updated.")

        # Rebuild the line
        new_line = f"{data[0]}:{data[1]}:{data[2]}:{current_status}\n"
        new_file_content.append(new_line)

    # Write changes back
    if found:
        f = open("database/rooms.txt", "w")
        for line in new_file_content:
            f.write(line)
        f.close()
    else:
        print("Error: Room ID not found.")

# ==============================================================================
# MAIN MENU
# ==============================================================================
def housekeeping():
    while True:
        print("\n=== HOUSEKEEPING DASHBOARD ===")
        print("1. View Tasks")
        print("2. Update Room Status")
        print("3. Back")
        
        choice = input("Enter choice: ")
        
        if choice == '1': view_tasks()
        elif choice == '2': update_status()
        elif choice == '3': break
        else: print("Invalid input.")


