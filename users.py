from tkinter import *

class Users():

    def __init__(self, id, name, role):
        self.id = id
        self.name = name
        self.role = role


# Εξετάζει αν υπάρχει το αρχείο των users
# Αν το αρχείο δεν υπάρχει, ανάλογο μήνυμα και δυνατότητα δημιουργίας χρήστη (no_usersFile_found)
# Αν υπάρχει και είναι άδειο, δυνατότητα δημιουργίας χρήστη (usersFile_isEmpty)
# Αν έχει εγγραφές, εμφάνιση όλων και επιλογή του χρήστη (display_allUsers)
def check_usersFile():
    try:
        with open("Users.csv") as f:
            file = f.read()
            print(file)
            if not file:
                print("File is empty")
                create_user_page("empty")
            else:
                print("Opening Users.csv file")
                display_allUsers() 
    except FileNotFoundError:
        print("File not found.")
        create_user_page("nofile")


# Παράθυρο δημιουργίας νέου χρήστη
def create_user_page(message):
    print("ok")


# Το αρχείο δεν βρέθηκε, ανάλογο μήνυμα
# Create User button
# Quit Button
def no_usersFile_found():
    pass


# Το αρχείο βρέθηκε αλλά είναι άδειο, ανάλογο μήνυμα
# Create User button
# Quit Button
def usersFile_isEmpty():
    pass


# Παράθυρο με όλους τους users
# Checklist, για επιλογή χρήστη
# Next button, για σύνδεση του χρήστη με το file του
def display_allUsers():
    pass


def main():
    check_usersFile()

if __name__ == "__main__":
    main()
