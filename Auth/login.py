def login():
    name = str(input("Enter your name: "))
    password = str(input("Enter your password: "))
    database = open("database/auth.txt", "r")
    data = database.readlines();
    for line in data:
        name_db , password_db  = line.strip().split(",")
        if name_db == name and password_db == password:
            print("Login successful!")
            return True
    print("Login failed! Incorrect name or password." , end="\n")
    return False
