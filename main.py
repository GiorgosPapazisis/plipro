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
        # self.view_mode = 'table' #fixed

        self.button = Button(root, text="Back", command=lambda: pick_user_route(root))
        self.button.pack(pady=10)

        self.button = Button(root, text="Add Activity", command=lambda: add_activity_route(root,username,None,self.load_table_view))
        self.button.pack(pady=10)

        self.update_button = Button(root, text="Update Selected Activity", command=self.update_selected, state=DISABLED)
        self.update_button.pack(pady=10)

        self.delete_button = Button(root, text="Delete Selected Activity", command=self.delete_selected, state=DISABLED)
        self.delete_button.pack(pady=10)
        

        self.child_object = self.load_table_view()
        

    def load_table_view(self):
        if hasattr(self, 'child_object') and self.child_object:
            self.child_object.destroy()
        self.table_obj = activityUserTable(self.root, self.username)
        self.child_object = self.table_obj.tree
        self.table_obj.tree.bind("<<TreeviewSelect>>", self.on_selection_change)
        self.on_selection_change()
        return self.child_object

    def update_selected(self):
        selected = self.table_obj.get_selected_activity()
        if selected:
            # Replace with your actual update popup route
            update_activity_route(self.root, self.username, selected, self.load_table_view)
            self.load_table_view()

    def delete_selected(self):
        selected = self.table_obj.get_selected_activity()
        if selected:
            delete_activity(self.username, selected)
            self.load_table_view()

    def on_selection_change(self, event=None):
        selected = self.table_obj.get_selected_activity()
        state = NORMAL if selected else DISABLED
        self.update_button.config(state=state)
        self.delete_button.config(state=state)





class activityUserTable:
    def __init__(self, root, username):
        activities = load_activities(username)
        self.tree = ttk.Treeview(root, columns=("name", "type", "duration", "priority"), show='headings')
        self.tree.pack(expand=True, fill='both', padx=20, pady=20)

        self.tree.heading("name", text="Activity Name")
        self.tree.heading("type", text="Activity Type")
        self.tree.heading("duration", text="Duration")
        self.tree.heading("priority", text="Priority")
        self.tree.bind("<<TreeviewSelect>>", self.selectItem)


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

    def selectItem(self, event):
        curItem = self.tree.focus()
        print("Selected:", self.tree.item(curItem)['values'])

    def get_selected_activity(self):
        curItem = self.tree.focus()
        if not curItem:
            return None
        return self.tree.item(curItem)['values']

   


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



class addActivity:
    def __init__(self, parent, username, data, load_table_view):
        
        self.top = Toplevel(parent)  #ontop
        self.top.geometry("300x400")
        self.top.title("My Application")
        self.load_table_view = load_table_view


        if data is not None:
            print("Data =",data)
            for value in data:
                print ("value =" , value)
            
            Label(self.top, text=f"Update the activity.").pack(pady=(10, 20))
            # Όνομα
            Label(self.top, text="Όνομα Δραστηριότητας").pack(pady=(0, 0))
            predefined_name = StringVar(value=data[0])
            self.entry_activity_name = Entry(self.top, textvariable=predefined_name)
            self.entry_activity_name.pack()
            # Είδος
            Label(self.top, text="Είδος Δραστηριότητας").pack(pady=(20, 0))
            self.cb_2 = ttk.Combobox(self.top, values=["Ελεύθερου Χρόνου", "Υποχρεωτική"], state='readonly')
            self.cb_2.set(data[1])
            self.cb_2.pack()
            # Προτεραιότητα
            Label(self.top, text="Προτεραιότητα").pack(pady=(20, 0))
            self.cb = ttk.Combobox(self.top, values=[1,2,3,4,5,6,7,8,9,10], state='readonly')
            self.cb.set(data[3])
            self.cb.pack()
             # Δειάρκεια
            Label(self.top, text="Χρόνος Δραστηριότητας").pack(pady=(20, 0))
            time=format_time_reverse(data[2])
            print("mins=",time["mins"])
            print("hours=",time["hours"])
            # Frame to hold both spinboxes
            duration_frame = Frame(self.top)
            duration_frame.pack(pady=10)

            # Hours Spinbox
            Label(duration_frame, text="Ώρες").grid(row=0, column=0, padx=5)
            self.spinbox_hours = Spinbox(duration_frame, from_=0, to=23, width=5, justify="center")
            self.spinbox_hours.grid(row=1, column=0, padx=5)

            # Minutes Spinbox
            Label(duration_frame, text="Λεπτά").grid(row=0, column=1, padx=5)
            self.spinbox_mins = Spinbox(duration_frame, from_=0, to=59, width=5, justify="center")
            self.spinbox_mins.grid(row=1, column=1, padx=5)

            # Optional: Set default to 1h 0m
            self.spinbox_hours.delete(0, END)
            self.spinbox_hours.insert(0, time["hours"])
            self.spinbox_mins.delete(0, END)
            self.spinbox_mins.insert(0, time["mins"])
            self.button = Button(self.top, text="Update Activity", command=lambda: self.on_update_activity(username,data))
            self.button.pack(pady=30)
        else:
            print("no Data")


            Label(self.top, text=f"Add an activity for user {username}.").pack(pady=(10, 20))
            # Όνομα
            Label(self.top, text="Όνομα Δραστηριότητας").pack(pady=(0, 0))
            self.entry_activity_name = Entry(self.top)
            self.entry_activity_name.pack()
            # Είδος
            Label(self.top, text="Είδος Δραστηριότητας").pack(pady=(20, 0))
            self.cb_2 = ttk.Combobox(self.top, values=["Ελεύθερου Χρόνου", "Υποχρεωτική"], state='readonly')
            self.cb_2.set("Ελεύθερου Χρόνου")
            self.cb_2.pack()
        
            # Προτεραιότητα
            Label(self.top, text="Προτεραιότητα").pack(pady=(20, 0))
            self.cb = ttk.Combobox(self.top, values=[1,2,3,4,5,6,7,8,9,10], state='readonly')
            self.cb.set(1)
            self.cb.pack()

            # Δειάρκεια
            Label(self.top, text="Χρόνος Δραστηριότητας").pack(pady=(20, 0))

            # Frame to hold both spinboxes
            duration_frame = Frame(self.top)
            duration_frame.pack(pady=10)

            # Hours Spinbox
            Label(duration_frame, text="Ώρες").grid(row=0, column=0, padx=5)
            self.spinbox_hours = Spinbox(duration_frame, from_=0, to=23, width=5, justify="center")
            self.spinbox_hours.grid(row=1, column=0, padx=5)

            # Minutes Spinbox
            Label(duration_frame, text="Λεπτά").grid(row=0, column=1, padx=5)
            self.spinbox_mins = Spinbox(duration_frame, from_=0, to=59, width=5, justify="center")
            self.spinbox_mins.grid(row=1, column=1, padx=5)

            # Optional: Set default to 1h 0m
            self.spinbox_hours.delete(0, END)
            self.spinbox_hours.insert(0, "1")
            self.spinbox_mins.delete(0, END)
            self.spinbox_mins.insert(0, "0")

            self.button = Button(self.top, text="Add Activity", command=lambda: self.on_add_activity(username))
            self.button.pack(pady=30)


    def on_add_activity(self,username):
        print ("username = ", username)
       
        activity_name = self.entry_activity_name.get()
        activity_type = self.cb_2.get()
        hours = self.spinbox_hours.get()
        mins = self.spinbox_mins.get()
        activity_duration=format_time(hours,mins)
        activity_priority = self.cb.get()
        print(activity_name,activity_type,activity_duration,activity_priority)
        add_activity(username,activity_name,activity_type,activity_duration,activity_priority)
        self.load_table_view()
        self.top.destroy()
        


    def on_update_activity(self,username,data):
        print ("username = ", username)
        activity_name = self.entry_activity_name.get()
        activity_type = self.cb_2.get()
        hours = self.spinbox_hours.get()
        mins = self.spinbox_mins.get()
        activity_duration=format_time(hours,mins)
        activity_priority = self.cb.get()
        print(activity_name,activity_type,activity_duration,activity_priority)
        update_activity(username,activity_name,activity_type,activity_duration,activity_priority,data)
        self.load_table_view()
        self.top.destroy()







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

def add_activity_route(root,username,selected,load_table_view):
    addActivity(root,username,None,load_table_view)


def update_activity_route(root, username, selected,load_table_view):
    print ("UPDATE ROUTE")
    print("username=",username)
    print("selected=",selected)
    addActivity(root,username,selected,load_table_view)




#----------------Main--------------------
def main():
    check_csv_file()
    root = Tk()
    pick_user_route(root)
    root.mainloop()
    


if __name__=="__main__":
    main()