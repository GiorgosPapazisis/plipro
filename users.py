from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from users_helpers import *

# base directory of the project
base_dir = os.path.dirname(__file__)
# csv folder directory
csv_folder = os.path.join(base_dir, 'csv')
# users.csv file directory
users_file = os.path.join(csv_folder, 'users.csv')
# users.csv headers
usersFile_header = ['id', 'name']


# Users class to initiate user
class Users():
    # Object initialize 
    def __init__(self, id, name):
        self.id = id
        self.name = name

    # Create new user object
    # @param frame_root -> parent frame
    # @param entry_widget -> user's entry for username
    # @param label_messageToUser -> label to configure depending the user's entry error (already exists or none username)
    def create_newUser(self, frame_root, entry_widget, label_messageToUser):
        # Take user name from entry and delete white spaces
        username = entry_widget.get().strip() 
        
        # White space username
        if not username:
            print("Username can not be empty")
            create_popup("Enter username. Can not be empty", "red")
        else:
            with open(users_file, 'r', newline='') as f:
                username_exists = False
                reader = csv.DictReader(f)

                # Name already exists, handling
                for row in reader:
                    if row['name'].strip() == username.strip():
                        username_exists = True
                        break
            
                # Username already exists, delete entry
                if username_exists:
                    create_popup("This Username already exists. Please type another", "red")
                    entry_widget.delete(0, END)
                # New name handling
                else:
                    entry_widget.delete(0, END)
                    last_id = None
                    with open(users_file, 'r', newline='') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            if row and row['id'].isdigit():
                                last_id = int(row['id'])
                        if last_id is None:
                            new_id = 10
                        else:
                            new_id = last_id + 1
                    new_user = {'id' : new_id, 'name' : username}
                    with open(users_file, 'a', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=usersFile_header)
                        writer.writerow(new_user)

                    # Refresh page, after successful save
                    create_users_page('display_all', frame_root)
                    create_popup('Your username saved successfully', 'green')


# Create Users Section window
# @param message -> string, to know if file is empty or has users already
# @param frame_root -> parent frame
def create_users_page(message, frame_root):

    # Destroy all children of frame_root
    for widget in frame_root.winfo_children():
        widget.destroy()

    # Main frame of the root
    page_frame = ttk.Frame(frame_root)
    page_frame.pack(fill='both', expand=True) 

    # Label, msg to user for errors(already user exist / white spaces username)
    label_messageToUser = Label(page_frame, text='', fg='red')
    label_messageToUser.pack()

    if (message == 'empty'):
        # Create new user label
        label_createUser = ttk.Label(page_frame, text="Create the first user")
        label_createUser.pack()
        entry_username = Entry(page_frame, name='entry_username')
        entry_username.pack()
        # Create btn
        btn_createUser = ttk.Button(page_frame, text='Create New User', command=lambda: Users(0, "").create_newUser(page_frame, entry_username, label_messageToUser))
        btn_createUser.pack(pady=1)
        # Create an "Import File" button
        import_button = ttk.Button(page_frame, text="Import File", command=import_file)
        import_button.pack(pady=1)
        # Quit btn
        btn_quit = ttk.Button(page_frame, text='Quit', command=frame_root.destroy)
        btn_quit.pack()
    elif (message == 'display_all'):
        users = []
        with open(users_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['name']:
                    users.append(row['name'])

        # Create new user label
        label_createUser = ttk.Label(page_frame, text="Create new user")
        label_createUser.pack()
        # Entry for user's username
        entry_username = Entry(page_frame, name='entry_username')
        entry_username.pack()
        # Create btn
        btn_createUser = ttk.Button(page_frame, text='Create New User', command=lambda: Users(0, "").create_newUser(page_frame, entry_username, label_messageToUser))
        btn_createUser.pack(pady=1)
        # Label choose user
        label_chooseUser = Label(page_frame, text="Choose user")
        label_chooseUser.pack(pady=5)
        # Combobox for existed users
        combo_users = ttk.Combobox(page_frame, value=users, state="readonly")
        combo_users.pack()
        # Select user btn
        btn_selectedUser = ttk.Button(page_frame, text="Choose", command=lambda: print(combo_users.get()))
        btn_selectedUser.pack()
        # Create an "Import File" button
        import_button = ttk.Button(page_frame, text="Import File", command=lambda: import_file(frame_root, create_users_page))
        import_button.pack(pady=1)
        # Quit btn
        btn_quit = ttk.Button(page_frame, text='Quit', command=frame_root.destroy)
        btn_quit.pack()


def main():
    check_csvFolder()
    check_usersFile()
    msg = invalidFile_fix(users_file)
    root = Tk()
    root.title("Select User Section")
    root.geometry('800x800')
    if (msg == 'display_all'):
        try:
            create_users_page(msg, root)
        except Exception as error:
            print(f"An error has occurred: {error}")
    elif (msg == 'empty'): 
        try:
            create_users_page(msg, root)
        except Exception as error:
            print(f"An error has occurred: {error}")
    root.mainloop()


if __name__ == "__main__":
    main()
