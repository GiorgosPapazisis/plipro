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
        self.frame.pack(pady=20)
        self.label = Label(self.frame, text="There are no users or activities")
        self.label.pack()
        self.label = Label(self.frame, text="Lets create a user")
        self.label.pack(pady=20)
        self.entry = Entry(self.frame)
        self.entry.pack(pady=20)
        self.button = Button(self.frame, text="Create User", command=lambda:username_entry(self.entry.get(),master))
        self.button.pack(pady=20)
        
class userDashboard:
    def __init__(self, master, username):
         #-----Title---------
        self.master=master
        self.master.geometry("800x600")
        self.master.title("My Application")
        text="Hi there "+ username
        self.label = Label(self.master, text=text)
        self.label.pack()


        #-----User Entries---------
        self.frameEntries = Frame(master)
        self.labelActivityName=Label(self.frameEntries,text="Name").grid(row=0,column=0,padx=(20,0))
        self.labelDescription=Label(self.frameEntries,text="Description").grid(row=0,column=1,padx=(20,0))
        self.labelPriority=Label(self.frameEntries,text="Priority").grid(row=0,column=2,padx=(20,0))
        self.labelTime=Label(self.frameEntries,text="Time").grid(row=0,column=3,padx=(20,0))

        #--------depracated-------------
        # self.entryActivityName=Entry(self.frameEntries).grid(row=1,column=0,padx=(20,0))
        # self.entryDescription=Entry(self.frameEntries).grid(row=1,column=1,padx=(20,0))
        # self.entryPriority=Entry(self.frameEntries).grid(row=1,column=2,padx=(20,0))
        # self.entryTime=Entry(self.frameEntries).grid(row=1,column=3,padx=(20,0))

        self.entryActivityName = Entry(self.frameEntries)
        self.entryActivityName.grid(row=1, column=0, padx=(20, 0))

        self.entryDescription = Entry(self.frameEntries)
        self.entryDescription.grid(row=1, column=1, padx=(20, 0))

        self.entryPriority = Entry(self.frameEntries)
        self.entryPriority.grid(row=1, column=2, padx=(20, 0))

        self.entryTime = Entry(self.frameEntries)
        self.entryTime.grid(row=1, column=3, padx=(20, 0))

        self.frameEntries.pack(pady=40)

        self.buttonAddActivity=Button(self.master, text="Create Activity", command=lambda:addActivity(self.entryActivityName.get(),
                                                                                                      self.entryDescription.get(),
                                                                                                      self.entryPriority.get(),
                                                                                                      self.entryTime.get()
        ))
        self.buttonAddActivity.pack()



        

def addActivity(name, description, priority, time):
    print(name)
    print(description)
    print(priority)
    print(time)      


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