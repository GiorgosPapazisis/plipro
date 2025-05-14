from tkinter import *
from tkinter import ttk
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
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def create_newUser(self, frame_root, entry_widget):
        username = entry_widget.get().strip() 
        
        if not username:
            print("Username can not be empty")
            label_error = Label(frame_root, text="Enter username. Can not be empty", fg="red")
            label_error.pack()
        else:
            with open(users_file, 'r', newline='') as f:
                username_exists = False
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    print(row[1].strip())
                    if row[1].strip() == username.strip():
                        username_exists = True
                        print("ok")
                        break

                if username_exists:
                    label_error = Label(frame_root, text="This Username already exists. Please type another", fg="red")
                    label_error.pack()
                    entry_widget.delete(0, END)
                else:
                    label_error = Label(frame_root, text="Nice name", fg="green")
                    label_error.pack()
                    entry_widget.delete(0, END)
                    with open(users_file, 'r', newline='') as f:
                        reader = csv.reader(f)
                        next(reader)
                        for row in reader:
                            last_id = row[0]
                    new_user = [int(last_id) + 1, username]
                    with open(users_file, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(new_user)

            
  


# Check if csv folder exists
# True -> calls check_usersFile()
# False -> create folder and calls check_usersFile()
def check_csvFolder():
    csv_folder = os.path.join(base_dir, 'csv')
    if os.path.exists(csv_folder):
        print('Csv folder exists')
    else:
        print('csv folder do not exists. Creating...')
        try:
            os.mkdir('csv')
            print('csv folder created successfully')
        except Exception as error:
            print(f'An error has occurred: {error}')
    print("\t- Folder check passed successfully")


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
                print("\t- File check passed successfully")
            else:
                print("Opening users.csv file")
                print("\t- File check passed successfully")
    except FileNotFoundError:
        print("File not found. users.csv is creating...")
        with open(users_file, 'w') as f:
            f.write('')
        print('users.csv created successfully')
        print("\t- File check passed successfully")
    


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
    

# Check if file is valid, has headers, right number o cols, no blank rows
def csvFile_validation(file):
    valid_rows = []
    invalid_rows = []

    try:
        with open(file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            # Empty file check
            if is_file_empty(file):
                print("File is empty. Creating headers...")
                create_headers(file)
                print("Headers created successfully")
                print("Your file is valid")    
                print("\t- Validation check passed successfully") 
                msg = 'empty'
                return msg    
        
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

            print("Your file is valid")    
            print("\t- Validation check passed successfully") 

            if (len(valid_rows) != 0):
                msg = 'display_all'   
                return msg
    except Exception as error:
        print(f"An error has occurred {error}")

                        

# Το αρχείο βρέθηκε αλλά είναι άδειο, ανάλογο μήνυμα
# Create User button
# Quit Button
def usersFile_isEmpty():
    msg = csvFile_validation(users_file)
    try:
        if (msg == 'csv_ok'):
            window_msg = "empty"
            create_users_page(window_msg)
    except Exception as error:
        print(f"An error has occurred: {error}")


# Παράθυρο με όλους τους users
# Checklist, για επιλογή χρήστη
# Next button, για σύνδεση του χρήστη με το file του
def display_allUsers():
    msg = csvFile_validation(users_file)
    try:
        if (msg == 'csv_ok'):
            window_msg = "display_all"
            create_users_page(window_msg)
    except Exception as error:
        print(f"An error has occurred: {error}")
    


# Create Users Section window
def create_users_page(message, frame_root):
    if (message == 'empty'):
        frame_empty = ttk.Frame(frame_root, padding=10)
        frame_empty.pack(pady=10)
        label_createUser = ttk.Label(frame_empty, text="Create the first user")
        label_createUser.pack()
        entry_username = Entry(frame_empty, name='entry_username')
        entry_username.pack()
        btn_createUser = ttk.Button(frame_root, text='Create New User', command=lambda: Users(0, "").create_newUser(frame_empty, entry_username))
        btn_createUser.pack(pady=1)
        btn_quit = ttk.Button(frame_root, text='Quit', command=frame_root.destroy)
        btn_quit.pack()
    elif (message == 'display_all'):
        frame_empty = ttk.Frame(frame_root, padding=10)
        frame_empty.pack(pady=10)
        label_createUser = ttk.Label(frame_empty, text="Create new user")
        label_createUser.pack()
        entry_username = Entry(frame_empty, name='entry_username')
        entry_username.pack()
        btn_createUser = ttk.Button(frame_root, text='Create New User', command=lambda: Users(0, "").create_newUser(frame_empty, entry_username))
        btn_createUser.pack(pady=1)
        btn_quit = ttk.Button(frame_root, text='Quit', command=frame_root.destroy)
        btn_quit.pack()
    else:
        pass



def main():
    check_csvFolder()
    check_usersFile()
    msg = csvFile_validation(users_file)
    root = Tk()
    root.title("Select User Section")
    root.geometry('800x800')
    if (msg == 'display_all'):
        create_users_page(msg, root)
    elif (msg == 'empty'): 
        create_users_page(msg, root)
    root.mainloop()


if __name__ == "__main__":
    main()
