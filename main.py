from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt

root = Tk(screenName=None, baseName=None, className='TestApp', useTk=True, sync=False, use=None)


<<<<<<< Updated upstream
class Activity:
    def __init__(self, id, name, description, user, priority):
        self.id=id
        self.name=name
        self.description=description
        self.user=user
        self.priority=priority
=======

        

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
        self.message_label.config(text=message.message, fg="green" if message.message_type=="success" else "red")
>>>>>>> Stashed changes




<<<<<<< Updated upstream
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
=======
class activitiesUser:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.geometry("800x600")
        self.root.title("My Application")
        self.view_mode = 'table'
        self.button = Button(root, text="Back", command=lambda: pick_user_route(root))
        self.button.pack(pady=10)
        self.graph_button = Button(root, text="Show Graph", command=lambda: graph_route(root, self.username))
        self.graph_button.pack(pady=10)
        #create activity button
        self.toggle_button = Button(root, text="Change View", command=self.change_view)
        self.toggle_button.pack(pady=10)
        self.child_object = self.load_table_view()

    def change_view(self):
        self.child_object.destroy()
        if self.view_mode == 'table':
            self.child_object = self.load_list_view()
            self.view_mode = 'list'
        else:
            self.child_object = self.load_table_view()
            self.view_mode = 'table'

    def load_table_view(self):
        table = activityUserTable(self.root, self.username)
        return table.tree

    def load_list_view(self):
        frame = Frame(self.root)
        frame.pack(fill=BOTH, expand=True)
        activityUserList(frame, self.username)
        return frame



class activityUserList:
    def __init__(self, parent, username):
        activities = load_activities(username)
        for activity in activities:
            frame = Frame(parent, bg="lightgray", pady=10)
            frame.pack(fill=X, padx=20, pady=5)
            Label(frame, text=f"Name: {activity['activity_name']}", bg="white").pack(anchor='w')
            Label(frame, text=f"Type: {activity['activity_type']}", bg="white").pack(anchor='w')
            Label(frame, text=f"Duration: {activity['activity_duration']}", bg="white").pack(anchor='w')
            Label(frame, text=f"Priority: {activity['activity_priority']}", bg="white").pack(anchor='w')


class activityUserTable:
    def __init__(self, root, username):
        activities = load_activities(username)
        self.tree = ttk.Treeview(root, columns=("name", "type", "duration", "priority"), show='headings')
        self.tree.pack(expand=True, fill='both', padx=20, pady=20)

        self.tree.heading("name", text="Activity Name")
        self.tree.heading("type", text="Activity Type")
        self.tree.heading("duration", text="Duration")
        self.tree.heading("priority", text="Priority")

        self.tree.column("name", width=150)
        self.tree.column("type", width=100)
        self.tree.column("duration", width=80)
        self.tree.column("priority", width=100)

        for activity in activities:
            self.tree.insert('', 'end', values=(
                activity['activity_name'],
                activity['activity_type'],
                activity['activity_duration'],
                activity['activity_priority']
            ))



class fileFixingValidation:
    def __init__(self, parent, username):
        self.top = Toplevel(parent)  #ontop
        self.top.geometry("200x150")
        self.top.title("My Application")
        self.label = Label(self.top, text=f"File for '{username}' needs fixing.", fg="red")
        self.label.pack(pady=20)
        self.fix_button = Button(self.top, text="Fix File", command=lambda: self.fix_file_and_continue(username, parent))
        self.fix_button.pack(pady=10)
        self.close_button = Button(self.top, text="Close", command=self.top.destroy)
        self.close_button.pack(pady=10)

    def fix_file_and_continue(self, username, parent):
        result = fix_file_stracture(username)
        if result.message_type == "success":
            print("File fixed")
            self.top.destroy()
            user_activities_route(parent, username)
        else:
            self.label.config(text=result.message, fg="red")

        

class Graph:
    def __init__(self, root, username):
        self.username = username
        self.root = root
        self.root.geometry("800x600")
        self.root.title("My Application")
        self.button = Button(root, text="Back", command=lambda: user_activities_route(root, username))
        self.button.pack(pady=10)

        self.generate_graph(username)
    def generate_graph(self, username):
        activities = load_activities(username)
        if not activities:
            Label(self.root, text="No activities to display.", fg="red").pack(pady=20)
            return
        
        activity_names = [a["activity_name"] for a in activities]
        durations = [int(a["activity_duration"]) for a in activities]

        plt.figure(figsize=(12, 6))
        plt.bar(activity_names, durations, color='skyblue')
        plt.xlabel("Activities")
        plt.ylabel("Duration (minutes)")
        plt.title(f"Activity Duration for {username}")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()







#--------------Routes-----------------
def pick_user_route(root):
    for child in root.winfo_children():
        child.destroy()
    pickUser(root)


def create_user_route(root):
    for child in root.winfo_children():
        child.destroy()
    createUser(root)
    


def user_activities_route(root,username):
    for child in root.winfo_children():
        child.destroy()
    activitiesUser(root,username)
    


def file_need_fix_route(root,username):
    fileFixingValidation(root,username)


def graph_route(root,username):
    for child in root.winfo_children():
        child.destroy()
    Graph(root,username)



#----------------Main--------------------
def main():
    check_csv_file()
    root = Tk()
    pick_user_route(root)
>>>>>>> Stashed changes
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
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=1)
    root.mainloop()



def initiate_front_end():
    print("hello")
    frm = ttk.Frame(root, padding=200)
    frm.grid()
    ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
    root.mainloop()


def main():
    # initiate_front_end()
    check_for_import()
   

if __name__=="__main__":
    main()