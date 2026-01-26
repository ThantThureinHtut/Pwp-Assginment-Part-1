import Auth.login as AuthLogin
import Auth.signup as AuthSignup
import Role.manager as RoleManager
import Role.Receptionist as RoleReceptionist
import Role.Accountant as RoleAccountant
import Role.Housekeeping as RoleHousekeeping
import Role.Guest as RoleGuest

AuthStatus = False
while not AuthStatus:
    print(f"(1) Login || (2) Don't have an account? Sign Up")
    choice = input("Enter your choice (1 or 2): ")
    if choice == '1':
        print("Redirecting to Login Page...")
        AuthStatus = AuthLogin.login()
    elif choice == '2':
        print("Redirecting to Signup Page...")
        AuthStatus =  AuthSignup.signup();


while AuthStatus:
    print(f"(1) Manager\n(2) Receptionist\n(3) Accountant\n(4) Housekeeping\n(5) Guest\n(6) Exit")
    role_choice = input("Select your role (1-6): ")
    if role_choice == '1':
       RoleManager.manager()
    elif role_choice == '2':      
        RoleReceptionist.receptionist()
    elif role_choice == '3':
        RoleAccountant.accountant()
    elif role_choice == '4':
        RoleHousekeeping.housekeeping()
    elif role_choice == '5':
        RoleGuest.guest_menu()
    elif role_choice == '6':
        print("Exiting the system. Goodbye!")
        break