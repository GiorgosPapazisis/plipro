from tkinter import *
import csv
from functions import *
from tkinter import ttk



class pickUser:
    def __init__(self, master):
        self.master = master
        self.master.geometry("800x600")
        self.master.title("My Application")
        
        #label
        self.label = Label(master, text="Pick your user")
        self.label.pack(pady=20)

        users = list_users()
        if not users:
            print("No users were found")
            cb_state='disabled'
            self.label = Label(master, text="No user found... you can import or create a new user")
            self.label.pack(pady=20)
        else:
            print(users)
            cb_state='readonly'
        


        
        
        #dropdown
        cb = ttk.Combobox(master, values=users)
        cb['state'] = cb_state
        cb.set("Select a user")
        cb.pack()






def main():
    root = Tk()
    #run = pickUser(root)
    pickUser(root)
    root.mainloop()


if __name__=="__main__":
    main()