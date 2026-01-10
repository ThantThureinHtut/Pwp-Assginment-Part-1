def accountant():
    while True:
        print("------------ Accountant Dashboard -----------")
        print("(1) Record Guest Payment")
        print("(2) Income & Outstanding Payment Report")
        print("(3) Monthly Financial Summary")
        print("(4) Logout")

        choice = input("Select an option (1-4): ")

        # (1) Record Guest Payments
        if choice == '1':
            print("Recording guest payment...")
            guest_name = input("Enter Guest Name: ")
            room_id = input("Enter Room ID: ")
            total_bill = float(input("Enter Total Bill (RM): "))
            amount_paid = float(input("Enter Amount Paid (RM): "))

            outstanding = total_bill - amount_paid

            database = open("database/payments.txt", "a")
            database.write(
                f"{guest_name}:{room_id}:{total_bill}:{amount_paid}:{outstanding}\n"
            )
            database.close()

            print("Payment recorded successfully.")

        # (2) Generate Income & Outstanding Payment Reports
        elif choice == '2':
            print("---- Income & Outstanding Payment Report ----")
            database = open("database/payments.txt", "r")
            payments = database.readlines()

            total_income = 0
            print("\nOutstanding Payments:")
            for payment in payments:
                parts = payment.strip().split(":")
                guest_name = parts[0]
                room_id = parts[1]
                paid = float(parts[3])
                outstanding = float(parts[4])

                total_income += paid

                if outstanding > 0:
                    print(f"Guest: {guest_name}, Room: {room_id}, Outstanding: RM {outstanding}")

            print(f"\nTotal Income Collected: RM {total_income}")
            database.close()

        # (3) Generate Monthly Financial Summary
        elif choice == '3':
            print("---- Monthly Financial Summary ----")
            database = open("database/payments.txt", "r")
            payments = database.readlines()

            total_revenue = 0
            total_outstanding = 0

            for payment in payments:
                parts = payment.strip().split(":")
                paid = float(parts[3].replace("RM ", ""))
                outstanding = float(parts[4])

                total_revenue += paid
                total_outstanding += outstanding

            print(f"Total Revenue: RM {total_revenue}")
            print(f"Total Outstanding Payments: RM {total_outstanding}")
            database.close()

        # (4) Logout
        elif choice == '4':
            break

        else:
            print("Invalid option. Please try again.")


