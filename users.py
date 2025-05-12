from tkinter import *
import pandas as pd
import csv 

class Users():

    def __init__(self, id, name, role):
        self.id = id
        self.name = name
        self.role = role


# function που εξετάζει αν υπάρχει το αρχείο των users
# Αν υπάρχει και είναι άδειο, δυνατότητα δημιουργίας χρήστη (usersFile_isEmpty)
# Αν έχει εγγραφές, εμφάνιση όλων και επιλογή του χρήστη (display_allUsers)
# Αν το αρχείο δεν υπάρχει, ανάλογο μήνυμα και δυνατότητα δημιουργίας χρήστη (no_usersFile_found)
def check_usersFile():
    try:
        with open("users.csv") as f:
            file = f.readline()
            print(file)
            if not file:
                print("File is empty")
                usersFile_isEmpty()
            else:
                print("Opening users.csv file")
                csvFile_validation()
                display_allUsers() 
    except FileNotFoundError:
        print("File not found.")
        no_usersFile_found()


# Function που εξετάζει αν το αρχείο που ανοίχτηκε είναι valid
def csvFile_validation():
    with open("users.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = next(csv_reader)

        if ((header[0].strip() == 'id') and (header[1].strip() == 'name') and (header[2].strip() == 'role')):
            print("Valid headers")
        else: 
            print("Invalid headers")

        for row in csv_reader:
            if (len(row) > 3):
                print("File invalid, too many columns")


# Το αρχείο βρέθηκε αλλά είναι άδειο, ανάλογο μήνυμα
# Create User button
# Quit Button
def usersFile_isEmpty():
    create_user_page("empty")


# Παράθυρο με όλους τους users
# Checklist, για επιλογή χρήστη
# Next button, για σύνδεση του χρήστη με το file του
def display_allUsers():
    pass


# Το αρχείο δεν βρέθηκε, ανάλογο μήνυμα
# Create User button
# Quit Button
def no_usersFile_found():
    create_user_page("nofile")


# Παράθυρο δημιουργίας νέου χρήστη
def create_user_page(message):
    print("ok")



def main():
    check_usersFile()

if __name__ == "__main__":
    main()
