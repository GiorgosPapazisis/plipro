from tkinter import *
from tkinter import ttk


root = Tk(screenName=None, baseName=None, className='TestApp', useTk=True, sync=False, use=None)


class Activity:
    def __init__(self, id, name, description, user, priority):
        self.id=id
        self.name=name
        self.description=description
        self.user=user
        self.priority=priority







def check_for_import():
    try:
        with open("Activities.csv") as f:
            file=f.read(1)
            print(file)
            if not file:
                print("File is empty")
                file_is_empty()
            else:
                print("Opening file Activites.csv...")
                file_found_page()
    except FileNotFoundError:
        print("no file found")
        no_file_found_page()


def no_file_found_page():
    print("Opening the no_file_found_page")
    frm = ttk.Frame(root, padding=200)
    frm.grid()
    ttk.Label(frm, text="No file found!").grid(column=0, row=0)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=1)
    root.mainloop()



def file_found_page():
    print("Opening the file_found_page window")
    frm = ttk.Frame(root, padding=200)
    frm.grid()
    ttk.Label(frm, text="Found the file!").grid(column=0, row=0)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
    root.mainloop()


def file_is_empty():
    print("Opening the file_is_empty window")
    frm = ttk.Frame(root, padding=200)
    frm.grid()
    ttk.Label(frm, text="File is empty!").grid(column=0, row=0)
    ttk.Label(frm, text="Lets create a new user first!").grid(column=0, row=1)
    username = ttk.Entry(frm)
    username.grid(column=0, row=2)
    ttk.Button(frm, text="Create User", command=lambda:answer(username)).grid(column=0, row=4)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=5)
    root.mainloop()



def initiate_front_end():
    print("hello")
    frm = ttk.Frame(root, padding=200)
    frm.grid()
    ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
    root.mainloop()



def answer(username):
    root.destroy
    answer_text = username.get()
    print("User created:", answer_text)
    activity_main_page(username)

def activity_main_page(username):
    print("Opening the file_found_page window")
    frm = ttk.Frame(root, padding=200)
    frm.grid()
    ttk.Label(frm, text="Welcome {username}").grid(column=0, row=0)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
    root.mainloop()

def main():
    # initiate_front_end()
    check_for_import()
   




if __name__=="__main__":
    main()