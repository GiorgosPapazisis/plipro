from tkinter import *
import pandas as pd

class Users():

    def __init__(self, id, name, role):
        self.id = id
        self.name = name
        self.role = role


# Εξετάζει αν υπάρχει το αρχείο των users
# Αν υπάρχει και είναι άδειο, δυνατότητα δημιουργίας χρήστη (usersFile_isEmpty)
# Αν έχει εγγραφές, εμφάνιση όλων και επιλογή του χρήστη (display_allUsers)
# Αν το αρχείο δεν υπάρχει, ανάλογο μήνυμα και δυνατότητα δημιουργίας χρήστη (no_usersFile_found)
def check_usersFile():
    try:
        with open("users.csv") as f:
            file = f.read()
            print(file)
            if not file:
                print("File is empty")
                usersFile_isEmpty()
            else:
                print("Opening users.csv file")
                display_allUsers() 
    except FileNotFoundError:
        print("File not found.")
        no_usersFile_found()


# Παράθυρο δημιουργίας νέου χρήστη
def create_user_page(message):
    print("ok")


# Το αρχείο δεν βρέθηκε, ανάλογο μήνυμα
# Create User button
# Quit Button
def no_usersFile_found():
    create_user_page("nofile")


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


def main():
    check_usersFile()

if __name__ == "__main__":
    main()
