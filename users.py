from tkinter import *
import pandas as pd
import csv 
import os

# base directory of the project
base_dir = os.path.dirname(__file__)
# csv folder directory
csv_folder = os.path.join(base_dir, 'csv')
# users.csv file directory
users_file = os.path.join(csv_folder, 'users.csv')


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
            file = f.readline()
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


# Create columns of users.csv
def create_headers(file):
    with open(file, 'w', newline='') as csvfile:
        header = ['id', 'name']
        writer = csv.writer(csvfile)
        writer.writerow(header)


# Check if a file is empty or has wite spaces
def is_file_empty(file):
    with open(file, 'r') as f:
        first_line = f.readline()
        return not first_line.strip()
    

# Function που εξετάζει αν το αρχείο που ανοίχτηκε είναι valid
def csvFile_validation(file):
    valid_rows = []
    invalid_rows = []
    with open(file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        #header = next(csv_reader)

        # Empty file check
        if is_file_empty(file):
            print("File is empty. Creating headers...")
            create_headers(file)
            print("Headers created successfully")
        
        # Invalid rows check 
        for row in csv_reader:
            if (len(row) == 2):
                valid_rows.append(row)
            else:
                invalid_rows.append(row)

        # Invalid rows delete
        if (len(invalid_rows) != 0):
            print("Deleting error rows...")
            with open(file, 'w', newline ='') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'name'])
                writer.writerows(valid_rows)
                        
    


# Το αρχείο βρέθηκε αλλά είναι άδειο, ανάλογο μήνυμα
# Create User button
# Quit Button
def usersFile_isEmpty():
    csvFile_validation(users_file)
    create_users_page("empty")


# Παράθυρο με όλους τους users
# Checklist, για επιλογή χρήστη
# Next button, για σύνδεση του χρήστη με το file του
def display_allUsers():
    csvFile_validation(users_file)
    
    


# Παράθυρο δημιουργίας νέου χρήστη
def create_users_page(message):
    print("ok")



def main():
    check_csvFolder()

if __name__ == "__main__":
    main()
