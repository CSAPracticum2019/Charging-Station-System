#Riley
#8/24/18
#Comp Prog 2

import csv, random

admin_ids=["0000"]
admin_pws=["654321"]

#The default menu for any user
def menu():
    user_id = input("UserID: ")
    user_code = input("Code: ")
    if user_id in admin_ids and user_code in admin_pws:
        print("Admin user")
        admin_menu()
    else:
        print("Regular user")
        read(user_id, user_code)

#Reading the csv file to check if the id and code work.
def read(user_id, user_code):
    with open('user_data.csv', mode='r') as csv_file: #the "as csv" is so it is openable as a .txt file, however it is not necessary in it's current state.
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        id_list = []
        code_list = []
        for row in csv_reader: 
            if line_count == 0:
                line_count += 1
            print("\t ID: " + str(row["id"]) + ", Code: " + str(row["code"]))
            id_list.append(row["id"])
            code_list.append(row["code"])
            if user_id == row["id"] and user_code == row["code"]:
                return True
                # menu()
            line_count += 1
        print("ID: " + str(row["id"]) + ", Code: " + str(row["code"]))
        print("Invalid code")
        print("")
        return False
        # menu()

#A menu only accessable when an admin id and code are inputted.
def admin_menu():
    print("1. Add user")
    print("2. Delete User")
    print("3. View all")
    print("4. Return")
    choice=input("Choose an option: ")
    if choice=="1":
        user_add()
    elif choice=="2":
        user_delete()
    elif choice=="3":
        view_all()
    elif choice=="4":
        menu()
    else:
        print("Invalid input")

def user_add():
    new_id=input("What is the user's ID?:")

    #Randomized password generator.
    passwords = dict()
    for id in range(1, 9999):
        if len(str(id)) < 4:
            id = (4 - len(str(id))) * '0' + str(id)
        password = str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9))
        while password in passwords.keys():
            password = str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9))
        passwords[str(id)] = password
    new_code = password
    print("User code is " + str(new_code))

    #Reading the CSV and putting the contents into a list as to be rewritten to the file.
    with open('user_data.csv', mode='r') as csv_file: #The "as csv" is so it is openable as a .txt file, however it is not necessary in it's current state.
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        id_list = []
        code_list = []
        for row in csv_reader: 
            if line_count == 0:
                line_count += 1
            id_list.append(row["id"])
            code_list.append(row["code"])
            line_count += 1

    id_list.append(new_id)
    code_list.append(new_code)
    print("success!")
            
    #Writing to the csv file
    with open('user_data.csv', mode='w') as csv_file:
        fieldnames = ['id', 'code'] 
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        for row in writer: 
            if line_count == 0:
                line_count += 1
            writer.writeheader()
            writer.writerow({'id': (id_list(row)), 'code': (code_list(row))})
        admin_menu()

def user_delete():
    delete_id=input("What is the user's ID?:")
    #randomized password generator
    #if id not already in ids and
    print("DEBUG")
    admin_menu()

def view_all():
    with open('user_data.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            print("\t ID: " + str(row["id"]) + ", Code: " + str(row["code"]))
            line_count += 1
        return True
    admin_menu()

#put all pws in list
#put all user ids in list 

#if user_id matches pw in index then let them in
#if in admins allow them to change info
