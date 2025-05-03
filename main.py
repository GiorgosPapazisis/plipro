from tkinter import *
import csv
from functions import *
from tkinter import ttk


#-------------Windows--------------------
class pickUser:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        self.root.title("My Application")
        self.label = Label(root, text="Pick your user")
        self.label.pack(pady=20)
        users = list_users()
        if not users:
            print("No users were found")
            cb_state='disabled'
            self.label = Label(root, text="No user found... you can import or create a new user")
            self.label.pack(pady=20)
        else:
            print(users)
            cb_state='readonly'
        cb = ttk.Combobox(root, values=users)
        cb['state'] = cb_state
        cb.set("Select a user")
        cb.pack()
        
        
        self.button = Button(root, text="Create User", command=lambda:create_user_route(root))
        self.button.pack(pady=20)
        
        def user_selected(event):
                username=event.widget.get()
                print(username)
                file_structure=check_file_stracture(username)
                print(f"file structure: ",file_structure)
                user_activities_route(root,username)

        def file_error(self):
            username = self.entry.get()
            message = create_user(username)
           


        cb.bind('<<ComboboxSelected>>', user_selected)

      

        
    
    
        


class createUser:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        self.root.title("My Application")
        self.entry = Entry(root)
        self.entry.pack(pady=20)
        self.button = Button(root, text="Create User", command=self.on_create_user)
        self.button.pack(pady=20)
        self.message_label = Label(root, text="", fg="green")
        self.message_label.pack(pady=10)
        self.button = Button(root, text="Back", command=lambda:pick_user_route(root))
        self.button.pack(pady=20)

        
    def on_create_user(self):
        username = self.entry.get()
        message = create_user(username)
        self.entry.delete(0, 'end')
        self.message_label.config(text=message, fg="green" if "created" in message else "red")





class activitiesUser:
    def __init__(self, root,username):
        self.root = root
        print(f"{username} dashboard")
        self.root.geometry("800x600")
        self.root.title("My Application")









#--------------Routes-----------------
def pick_user_route(root):
    for child in root.winfo_children():
        child.destroy()
    pickUser(root)
    root.mainloop()

def create_user_route(root):
    for child in root.winfo_children():
        child.destroy()
    createUser(root)
    root.mainloop()


def user_activities_route(root,username):
    for child in root.winfo_children():
        child.destroy()
    activitiesUser(root,username)
    root.mainloop()




#----------------Main--------------------
def main():
    check_csv_file()
    root = Tk()
    #run = pickUser(root)
    pick_user_route(root)
    #root.mainloop()


if __name__=="__main__":
    main()