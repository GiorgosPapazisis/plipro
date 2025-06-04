import csv
import os
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from shutil import copyfile
from users import create_users_page,user_activities_route






# base directory of the project
base_dir = os.path.dirname(__file__)
# csv folder directory
csv_folder = os.path.join(base_dir, 'csv')
# users.csv file directory
users_file = os.path.join(csv_folder, 'users.csv')
# users.csv headers
usersFile_header = ['id', 'name']


# Check if csv folder exists
# True -> calls check_usersFile()
# False -> create folder and calls check_usersFile()
def check_csvFolder():
    # If csv folder exists
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
# If not found -> create users.csv file with headers
def check_usersFile():
    try:
        with open(users_file, 'r') as f:
            file = f.readline()
            if not file:
                print("File is empty")
            else:
                print(f"Opening file: {f.name}")
        print("\t- File check passed successfully")
    except FileNotFoundError:
        print("File not found. users.csv is creating...")
        create_headers(users_file)
        print('users.csv created successfully')
        print("\t- File check passed successfully")
    

# Create headers of users.csv
# @param file -> str full path to file, in order to create headers
# @return void
def create_headers(file):
    with open(file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=usersFile_header)
        writer.writeheader()


# Check if a file is empty or has white spaces
# @param file -> file to check
# @return boolean 
def is_file_empty(file):
    with open(file, 'r') as f:
        first_line = f.readline()
        return not first_line.strip()
    

# Check if valid is valid, has 2 cols, headers = ['id', 'name'], id = digit, no empty or invalid rows
# @param file -> str full path to file
# @return str
def file_validation(file):
    valid_rows = []
    invalid_rows = []
    try: 
        with open(file, 'r') as file_toCheck:
            reader = csv.reader(file_toCheck)
            lines = list(reader)
            # Empty file check
            is_empty = False
            if not lines:
                is_empty = True
            else:
                found_content = False
                for line in lines:
                    join_items = ''.join(line)
                    if join_items.strip():
                        found_content = True
                        break
                if not found_content:
                    is_empty = True
            if is_empty:
                print(f"\nFile: {file}, is empty\nFile is invalid\n\tValidation check failed")
                msg = 'need_fix'
                return msg
            # Error headers check
            headers = lines[0]
            if (headers != usersFile_header):
                print(f"\nWrong headers\nYour file: {file}, is invalid\n\tValidation check failed")
                msg = 'need_fix'
                return msg

            # Invalid rows check
            for row in lines[1:]:
                if len(row) == 2 and row[0].isdigit() and row[1].strip():
                    valid_rows.append({'id': row[0], 'name': row[1]})
                else:
                    invalid_rows.append(row)
            if invalid_rows:
                print(f"\nInvalid row/s in file\nYour file: {file}, is invalid\n\t- Validation check failed")
                msg = 'need_fix'
                return msg
            print(f"\nYour file: {file}, is valid\n\t- Validation check passed successfully")
            msg = 'valid'
            return msg
    except Exception as error:
        print(f"An error has occurred {error}")


# Check if file is valid, has headers, right number o cols, no blank rows
# @param file -> full path to file in order to fix it
# @return msg -> string
def invalidFile_fix(file):
    valid_rows = []
    invalid_rows = []

    try:
        with open(file, 'r', newline='') as csv_file:
            reader = csv.reader(csv_file)
            lines = list(reader)

            # Empty file check
            is_empty = False
            if not lines:
                is_empty = True
            else:
                found_content = False
                for line in lines:
                    join_items = ''.join(line)
                    if join_items.strip():
                        found_content = True
                        break
                if not found_content:
                    is_empty = True
                
            if is_empty:
                print("File is empty. Creating headers...")
                create_headers(file)
                print("Headers created successfully\nYour file is valid\n\t- Validation check passed successfully")
                msg = 'empty'
                return msg    
            
            # Error headers check
            headers = lines[0]
            if (headers != ['id', 'name']):
                print("Wrong headers. Fixing headers...")
                create_headers(file)
                print("Headers fixed successfully\nYour file is valid\n\t- Validation check passed successfully")
                msg = 'empty'
                return msg
        
            # Invalid rows check 
            for row in lines[1:]:
                if len(row) == 2 and row[1].strip() and row[0].isdigit():
                    valid_rows.append({'id' : row[0], 'name' : row[1]})
                else:
                    invalid_rows.append(row)

            # Invalid rows delete
            if invalid_rows:
                print("Deleting error rows...")
                with open(file, 'w', newline ='') as f:
                    writer = csv.DictWriter(f, fieldnames=usersFile_header)
                    writer.writeheader()
                    writer.writerows(valid_rows)

            print(f"Your file: {file} is valid\n\t- Validation check passed successfully")    

            if valid_rows:
                msg = 'display_all'   
                return msg
            else:
                msg = 'empty'
                return msg
    except Exception as error:
        print(f"An error has occurred {error}")    


# Create a popup window
# @param msg -> str for the shown msg
# @param color -> str for the color of fg attribute 
# @return void
def create_popup(msg, color):
    # create a popup window
    popup = Toplevel()
    popup.title("Message")
    popup.geometry('400x100')
    Label(popup, text=msg, fg=color).pack()

    # Continue btn on popup
    Button(popup, text='Continue', command=popup.destroy).pack()



# Copy file's content to another file
# @param users_imported_file -> str full path of file, user imported
# @param new_usersFile -> str full path of csv/users.csv in order to copy all imported file's data
# @return void
def copy_files_content(users_imported_file, new_usersFile):
    try:
        with open(users_imported_file, 'r') as users_oldFile:
            reader = csv.DictReader(users_oldFile)
            usersData = list(reader)
            with open(new_usersFile, 'w', newline='') as newUsers_csv:
                writer = csv.DictWriter(newUsers_csv, fieldnames=usersFile_header)
                writer.writeheader()
                for row in usersData:
                    writer.writerow(row)
    except Exception as error:
        print(f"An error has occurred {error}")



# User imports a csv file. validation and fixing errors
# @param window_root -> pass main frame root
# @param refresh_callback -> pass a function, in order to handle undefined error
# @return 
# def import_file(window_root, refresh_callback):
#     # Initial var in file's path
#     file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Csv files", ".csv")])
     
#     # If file's path exist  
#     if file_path:
#         # Validation check of file
#         msg = file_validation(file_path)
    
#         # If file needs fix
#         if msg == 'need_fix':
#             # create a popup window
#             popup = Toplevel()
#             popup.title("Warning")
#             popup.geometry('400x100')
#             Label(popup, text="Errors need fixing. Do you want to fix them for you?", fg='red').pack()

#             # Yes btn function, in order to fix imported file
#             def fix_refresh(): 
#                 try:
#                     # Fix file
#                     fixedFile_msg = invalidFile_fix(file_path)
#                     # Copy file's data
#                     copy_files_content(file_path, users_file)
#                     popup.destroy()
#                     # Refresh window
#                     refresh_callback(fixedFile_msg, window_root)
#                     # Create popup, success msg
#                     create_popup('File imported successfully', 'green')
#                 except Exception as error:
#                     print(f"An error has occurred {error}")

#             # Yes / No btns on popup
#             Button(popup, text='Yes', command=lambda: fix_refresh()).pack()
#             Button(popup, text='Cancel', command=popup.destroy).pack()
#         else:
#             try:
#                 # Copy file's data
#                 copy_files_content(file_path, users_file)
#                 # Fix file(optional), in order to save returned msg of what kind window to create(empty / display_all)
#                 fixedFile_msg = invalidFile_fix(users_file)
#                 # Refresh window
#                 refresh_callback(fixedFile_msg, window_root)
#                 # Create popup, success msg
#                 create_popup(f"Your file: {file_path}, is valid\nImported successful", "green")
#             except Exception as error:
#                print(f"An error has occurred {error}") 


# Return selected user from combobox as dictionary
# @param frame_root -> frame obj which will destroy
# @param chosenUser -> str from combobox
# @return a dictionary
# def selected_user(frame_root, chosenUser):
#     with open(users_file, 'r') as f:
#         reader = csv.DictReader(f)
#         data = list(reader)
    
#         for user in data:
#             if (user['name'] == chosenUser):
#                 # frame_root.destroy()  #refactor
                
#                 user_activities_route(frame_root,user['name'])
#                 print(f"You choose user, with id: {user['id']} and name: {user['name']}")
#                 return user
    


# def import_file(frame_root):
#     file_path = filedialog.askopenfilename(title="Select a CSV file", filetypes=[("CSV Files", "*.csv")])

#     if not file_path:
#         return
#     file_name = os.path.basename(file_path)
#     username = os.path.splitext(file_name)[0]
#     if not username:
#         create_popup("Could not extract a valid username from the file name.", "red")
#         return
#     try:
#         dest_dir = os.path.join(base_dir, "csv")
#         os.makedirs(dest_dir, exist_ok=True)
#         counter = 0
#         final_username = username
#         dest_path = os.path.join(dest_dir, f"{final_username}.csv")
#         while os.path.exists(dest_path):
#             counter += 1
#             final_username = f"{username}({counter})"
#             dest_path = os.path.join(dest_dir, f"{final_username}.csv")
#         copyfile(file_path, dest_path)
#         create_popup(f"File imported successfully as user '{final_username}'", "green")

#     #refresh gui
#         # create_users_page("display_all", frame_root)
#         user_activities_route(frame_root,final_username)

#     except Exception as e:
#         print(f"Error during import: {e}")
#         create_popup("Failed to import file. Check the logs.", "red")
































