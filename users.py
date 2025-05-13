from tkinter import *
import pandas as pd
import csv 
import os

# base directory of the project
base_dir = os.path.dirname(__file__)
# csv folder directory
csv_folder = os.path.join(base_dir, 'csv')


# Users class to initiate user
class Users():
    def __init__(self, id, name, role):
        self.id = id
        self.name = name
        self.role = role


# Check if csv folder exists
# True -> calls check_usersFile()
# False -> create folder and calls check_usersFile()
def check_csvFolder():
    csv_folder = os.path.join(base_dir, 'csv')
    if os.path.exists(csv_folder):
        print('Csv folder exists')
        check_usersFile()
    else:
        print('csv folder do not exists. Creating...')
        try:
            os.mkdir('csv')
            print('csv folder created successfully')
            check_usersFile()
        except Exception as error:
            print(f'An error has occurred: {error}')


# Check if users.csv exists in csv folder
# If exists and is empty -> msg and calls usersFile_isEmpty
# If exists and is not empty -> calls display_allUsers
# If not found -> msg, create empty users.csv file and calls usersFile_isEmpty
def check_usersFile():
    csv_folder = os.path.join(base_dir, 'csv')
    users_file = os.path.join(csv_folder, 'users.csv')
    
    try:
        with open(users_file) as f:
            file = f.read()
            if not file:
                print("File is empty")
                usersFile_isEmpty()
            else:
                print("Opening users.csv file")
                display_allUsers() 
    except FileNotFoundError:
        print("File not found. users.csv is creating...")
        with open(users_file, 'w') as f:
            f.write('')
        print('users.csv created successfully')
        usersFile_isEmpty()


# Function που εξετάζει αν το αρχείο που ανοίχτηκε είναι valid
def csvFile_validation():
    with open("users.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = next(csv_reader)
        valid_headers = 0
        valid_rows = 0

        if ((header[0].strip() == 'id') and (header[1].strip() == 'name') and (header[2].strip() == 'role')):
            valid_headers = 1

        for row in csv_reader:
            if (len(row) == 3):
                valid_rows = 1
        
        if ((valid_headers == 1) and (valid_rows == 1)):
            print("Valid csv file")
        else:
            if ((valid_headers == 1) and (valid_rows == 0)):
                print("Invalid rows")
            elif ((valid_headers == 0) and (valid_rows == 1)):
                print("Invalid headers")
            else:
                print("File has invalid headers and rows")


# Το αρχείο βρέθηκε αλλά είναι άδειο, ανάλογο μήνυμα
# Create User button
# Quit Button
def usersFile_isEmpty():
    create_users_page("empty")


# Παράθυρο με όλους τους users
# Checklist, για επιλογή χρήστη
# Next button, για σύνδεση του χρήστη με το file του
def display_allUsers():
    csvFile_validation()
    


# Παράθυρο δημιουργίας νέου χρήστη
def create_users_page(message):
    print("ok")



def main():
    check_csvFolder()

if __name__ == "__main__":
    main()
