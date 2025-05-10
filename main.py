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
                file_structure=check_file_stracture(username)
                print("file_structure.message_type is ",file_structure.message_type)
                if file_structure.message_type=="error":
                    file_need_fix_route(root,username) #routes
                else:
                    user_activities_route(root,username) #routes
                

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
        self.message_label.config(text=message.message, fg="green" if message.message_type=="success" else "red")




class activitiesUser:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.geometry("800x600")
        self.root.title("My Application")
        self.view_mode = 'table'
        self.button = Button(root, text="Back", command=lambda: pick_user_route(root))
        self.button.pack(pady=10)
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
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        self.root.title("My Application")
       










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






#----------------Main--------------------
def main():
    check_csv_file()
    root = Tk()
    pick_user_route(root)
    root.mainloop()
    


if __name__=="__main__":
    main()