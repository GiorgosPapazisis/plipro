import csv
import os
from tkinter import filedialog
from tkinter import messagebox


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
        with open(users_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=usersFile_header)
            writer.writeheader()
        print('users.csv created successfully')
        print("\t- File check passed successfully")
    


# Create headers of users.csv
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
    

# Check if valid is valid, 2 cols, headers = ['id', 'name'], id = digit, no empty or invalid rows
# @param file -> str path to file
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
                print(f"File: {file}, is empty\nFile is invalid\n\tValidation check failed")
                msg = 'need_fix'
                return msg

            # Error headers check
            headers = lines[0]
            if (headers != ['id', 'name']):
                print(f"Wrong headers\nYour file: {file}, is invalid\n\tValidation check failed")
                msg = 'need_fix'
                return msg

            # Invalid rows check
            for row in lines[1:]:
                if len(row) == 2 and row[1].strip() and row[0].isdigit():
                    valid_rows.append({'id': row[0], 'name': row[1]})
                else:
                    invalid_rows.append(row)
            
            if invalid_rows:
                print(f"Invalid row/s in file\nYour file: {file}, is invalid\n\t- Validation check failed")
                msg = 'need_fix'
                return msg
            
            print(f"Your file: {file}, is valid\n\t- Validation check passed successfully")
            msg = 'valid'
            return msg
        
    except Exception as error:
        print(f"An error has occurred {error}")


# Check if file is valid, has headers, right number o cols, no blank rows
# @param file -> file to check
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

            print("Your file is valid\n\t- Validation check passed successfully")    

            if valid_rows:
                msg = 'display_all'   
                return msg
            else:
                msg = 'empty'
                return msg
    except Exception as error:
        print(f"An error has occurred {error}")    



def import_file(window_root):
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Csv files", ".csv")])

    if file_path:
        print("selected file: ", file_path)
        
        if file_path:

            msg = file_validation(file_path)
            if msg == 'need_fix':
                response = messagebox.askyesno("File needs fixing.\nClick yes to fix or no to cancel th import.", icon='warning')

                if response:
                    fixedFile_msg = invalidFile_fix(file_path)
                    print(fixedFile_msg)

            


        # msg = csvFile_validation(file_path)
        # print(msg)
        # with open(file_path, 'r')as f:
        #     reader = csv.DictReader(f)
        #     with open(users_file, 'w') as fileNew:
        #         pass

    
