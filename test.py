from tkinter import *

default_activities=["Ύπνος", ]


class Activities:
    def __init__(self, name, description, priority, time_in_mins, user_associated):
        self.name=name
        self.description=description
        self.priority=priority
        self.time_in_mins=time_in_mins
        self.user_associated=user_associated


class Window1:
    def __init__(self, master):
        # keep `root` in `self.master`
        self.master = master 

        self.label = Button(self.master, text="Example", command=self.load_new)
        self.label.pack()

    def load_new(self):
        self.label.destroy()
        # use `root` with another class
        self.another = Window2(self.master)


class Window2:
    def __init__(self, master):
        # keep `root` in `self.master`
        self.master = master
        self.label = Label(self.master, text="Example")
        self.label.pack()



class fileFoundEmpty:
    def __init__(self, master):
        self.master=master
        self.master.geometry("800x600")
        self.master.title("My Application")
        self.frame = Frame(master)
        self.frame.pack(expand=True, fill="both") 
        self.frame.pack()
        self.label = Label(self.frame, text="There are no users or activities")
        self.label.pack()
        self.label = Label(self.frame, text="Lets create a user")
        self.label.pack()
        self.entry = Entry(self.frame)
        self.entry.pack()
        self.button = Button(self.frame, text="Create User", command=lambda:username_entry(self.entry.get(),master))
        self.button.pack()
        
class userDashboard:
    def __init__(self, master,username):
        self.master=master
        self.master.geometry("800x600")
        self.master.title("My Application")
        text="Hi there "+ username
        self.frame = Frame(master)
        self.frame.pack(expand=True, fill="both")
        self.label = Label(self.frame, text=text)
        self.label.pack()
        print(text)


def username_entry(username, root):
    print(username)
    for child in root.winfo_children():
        child.destroy()
    run = userDashboard(root, username)






def check_for_import():
    try:
        with open("Activities.csv") as f:
            file=f.read(1)
            print(file)
            if not file:
                print("File is empty")
                return "file_empty"
            else:
                print("Opening file Activites.csv...")
                return "file_okay"
    except FileNotFoundError:
        print("no file found")
        return "file_not_found"





def main():
    # initiate_front_end()
    root = Tk()
    check_import = check_for_import()
    if check_import == "file_empty":
        run = fileFoundEmpty(root)
    else:
        run = Window1(root)
    root.mainloop()
    print(check_import)
   




if __name__=="__main__":
    main()