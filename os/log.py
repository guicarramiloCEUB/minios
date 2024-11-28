import getpass
import os
import hashpass

def create_user():
    here = os.path.dirname(__file__)
    filename = os.path.join(here, 'users.txt')


    username = input("Username: ")
    fp = open(filename, "r")
    users = []
    for line in fp:
        users.append(line.split(" ")[0])
    fp.close()
    while username in users:
        username = input("User already exists, please choose a different name: ")
    password = getpass.getpass("Password: ")
    line = f"{username} {hashpass.hash_password(password)}\n"
    fp = open(filename, "a")
    fp.write(line)
    fp.close()
    print("Sign in complete!")
    os.makedirs("users/"+ username)
    return username, hashpass.hash_password(password)


def login():
    here = os.path.dirname(__file__)
    filename = os.path.join(here, 'users.txt')

    while True:
        username = input("Username: ")
        password = getpass.getpass("Password: ")

        fp = open(filename, "r")
        count =  0
        for line in fp:
            count += 1
            if username == line.split(" ")[0] and hashpass.check_password(line.split(" ")[1].rstrip("\n"), password):
                fp.close()
                return username, hashpass.hash_password(password)
        print("Username or password incorrect.")