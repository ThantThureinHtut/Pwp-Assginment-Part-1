def signup():
    database = open("database/auth.txt", "a")
    name = str(input("Enter your name: "))
    password = str(input("Enter your password: "))
    database.write(f"{name},{password}\n")
    database.close()
    print("Signup successful!")
    return True

