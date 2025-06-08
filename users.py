from tkinter import *
from tkinter import ttk
from users_helpers import *
import csv
import os
from matplotlib import pyplot as plt
from tkinter import messagebox


base_dir = os.path.dirname(__file__)
csv_path = file_path = os.path.join(base_dir, 'csv')



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


    # Save new Users obj to users.csv
    def save_newUser(self):
        with open(users_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=usersFile_header)
            writer.writerow({'id' : self.id, 'name' : self.name})


    # Create new user object
    # @param frame_root -> parent frame
    # @param entry_widget -> user's entry for username
    # @param label_messageToUser -> label to configure depending the user's entry error (already exists or none username)
    def handle_newUser(self, frame_root, entry_widget):
        # Take user name from entry and delete white spaces
        username = entry_widget.get().strip() 
        
        # White space username
        if not username:
            print("Το όνομα του χρήστη δεν μπορεί να παραμείνει κενό")
            create_popup("Εισάγετε όνομα χρήστη. Δεν μπορεί να είναι κενό", "red")
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
                    create_popup("Ο χρήστης υπάρχει ήδη. παρακαλώ ξαναπροσπαθήστε", "red")
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
                    new_user = Users(new_id, username) 
                    new_user.save_newUser()
                    create_user(username)
                    # Refresh page, after successful save
                    create_users_page('display_all', frame_root)
                    create_popup('Ο χρήστης δημιουργήθηκε με επιτυχία', 'green')


# Create Users Section window
# @param message -> string, to know if file is empty or has saved users already
# @param frame_root -> parent frame
def create_users_page(message, frame_root):
    # Destroy all children of frame_root
    for widget in frame_root.winfo_children():
        widget.destroy()
    

    # Main frame of the root
    page_frame = ttk.Frame(frame_root)
    page_frame.pack(fill='both', expand=True) 

    if (message == 'empty'):
        # Create new user label
        label_createUser = ttk.Label(page_frame, text="Δημιουργήστε τον πρώτο χρήστη")
        label_createUser.pack()
        entry_username = Entry(page_frame, name='entry_username')
        entry_username.pack()
        # Create btn
        btn_createUser = ttk.Button(page_frame, text='Δημιουργία νέου χρήστη', command=lambda: Users(0, "").handle_newUser(page_frame, entry_username))
        btn_createUser.pack(pady=1)
        # Create an "Import File" button
        import_button = ttk.Button(page_frame, text="Ανεβάστε αρχείο", command=lambda: import_file(frame_root))
        import_button.pack(pady=1)
        # Quit btn
        btn_quit = ttk.Button(page_frame, text='Έξοδος', command=frame_root.destroy)
        btn_quit.pack()
    elif (message == 'display_all'):
        # users = []
        # with open(users_file, 'r') as f:
        #     reader = csv.DictReader(f)
        #     for row in reader:
        #         if row['name']:
        #             users.append(row['name'])

        # Create new user label
        label_createUser = ttk.Label(page_frame, text="Δημιουργήστε νέο χρήστη")
        label_createUser.pack()
        # Entry for user's username
        entry_username = Entry(page_frame, name='entry_username')
        entry_username.pack()
        # Create btn
        btn_createUser = ttk.Button(page_frame, text='Δημιουργία νέου χρήστη', command=lambda: Users(0, "").handle_newUser(page_frame, entry_username))
        btn_createUser.pack(pady=1)
        # Label choose user
        label_chooseUser = Label(page_frame, text="Επιλέξτε χρήστη")
        label_chooseUser.pack(pady=5)
        # Combobox for existed users
        # combo_users = ttk.Combobox(page_frame, value=users, state="readonly")
        combo_users = ttk.Combobox(page_frame, value=list_users(), state="readonly")
        combo_users.pack()
        # Select user btn
        btn_selectedUser = ttk.Button(page_frame, text="Επιλογή", command=lambda: selected_user(frame_root, combo_users.get()))
        btn_selectedUser.pack()
        # Create an "Import File" button
        # import_button = ttk.Button(page_frame, text="Ανεβάστε αρχείο", command=lambda: import_file(frame_root, create_users_page))
        import_button = ttk.Button(page_frame, text="Ανεβάστε αρχείο", command=lambda: import_file(frame_root))
        import_button.pack(pady=1)
        # Quit btn
        btn_quit = ttk.Button(page_frame, text='Έξοδος', command=frame_root.destroy)
        btn_quit.pack()



    def import_file(frame_root):
        file_path = filedialog.askopenfilename(title="Select a CSV file", filetypes=[("CSV Files", "*.csv")])

        if not file_path:
            return
        file_name = os.path.basename(file_path)
        username = os.path.splitext(file_name)[0]
        if not username:
            create_popup("Could not extract a valid username from the file name.", "red")
            return
        try:
            dest_dir = os.path.join(base_dir, "csv")
            os.makedirs(dest_dir, exist_ok=True)
            counter = 0
            final_username = username
            dest_path = os.path.join(dest_dir, f"{final_username}.csv")
            while os.path.exists(dest_path):
                counter += 1
                final_username = f"{username}({counter})"
                dest_path = os.path.join(dest_dir, f"{final_username}.csv")
            copyfile(file_path, dest_path)
            create_popup(f"File imported successfully as user '{final_username}'", "green")

        #refresh gui
            # create_users_page("display_all", frame_root)
            user_activities_route(frame_root,final_username)

        except Exception as e:
            print(f"Error during import: {e}")
            create_popup("Failed to import file. Check the logs.", "red")


# Return selected user from combobox as dictionary
# @param frame_root -> frame obj which will destroy
# @param chosenUser -> str from combobox
# @return a dictionary
#Αλλαγή λόγο circular import
# def selected_user(frame_root, chosenUser):
#     # print("3 Root type:", type(frame_root))
#     tk_root = frame_root.winfo_toplevel() 
#     # print("4 Root type:", type(tk_root))
#     with open(users_file, 'r') as f:
#         reader = csv.DictReader(f)
#         data = list(reader)
#         print("data:",data)
    
#         for user in data:
#             if (user['name'] == chosenUser):
#                 # frame_root.destroy()  #refactor
#                 # print("2 the root is :",frame_root)
#                 user_activities_route(tk_root, user['name'])
#                 # print(f"You choose user, with id: {user['id']} and name: {user['name']}")
#                 # return user

def selected_user(frame_root, chosenUser):
    print("Chose is ",chosenUser)
    if chosenUser=="":
        create_users_page("display_all", frame_root)
        return
    real_root = frame_root.winfo_toplevel() #fix
    user_activities_route(real_root, chosenUser)

    

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







#-----------------------Activity Class----------------------
class Activity:
    def __init__(self, activity_name,activity_type,activity_duration,activity_priority):
        self.activity_name=activity_name
        self.activity_type=activity_type
        self.activity_duration=activity_duration
        self.activity_priority=activity_priority

    def to_dict(self):
        return {
            'activity_name': self.activity_name,
            'activity_type': self.activity_type,
            'activity_duration': self.activity_duration,
            'activity_priority': self.activity_priority
        }






#-----------------------ACtivity User Page----------------------
class activitiesUser:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.geometry("800x600")
        self.root.title("My Application")
        # self.view_mode = 'table' #fixed

        self.button = Button(root, text="Πίσω", command=lambda: pick_user_route(root))
        self.button.pack(pady=10)

        self.button = Button(root, text="Προσθέστε Δραστηριοότητα", command=lambda: add_activity_route(root,username,None,self.load_table_view))
        self.button.pack(pady=10)

        self.update_button = Button(root, text="Ενημέρωση επιλεγμένης δραστηριότητας", command=self.update_selected, state=DISABLED)
        self.update_button.pack(pady=10)

        self.delete_button = Button(root, text="Διαγραφή επιλεγμένης δραστηριότητας", command=self.delete_selected, state=DISABLED)
        self.delete_button.pack(pady=10)

        self.sort_button = Button(root, text="Ταξινόμηση δραστηριοτήτων", command=self.sort_activities_and_refresh)
        self.sort_button.pack(pady=10)

        self.button = Button(root, text="Γράφημα", command=lambda: graph_route(root, self.username))
        self.button.pack(pady=10)

        self.sum_button = Button(root, text="Σύνολο διάρκειας δραστηριοτήτων", command=self.calculate_sums)
        self.sum_button.pack(pady=10)

        self.average_button = Button(root, text="Μέσος όρος διάρκειας δραστηριοτήτων", command=self.calculate_averages)
        self.average_button.pack(pady=10)   
        

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

    def sort_activities_and_refresh(self):
        print("hello")
        sort_activities(self.username)
        self.load_table_view()
    
    def show_info_window(self, title, message):
        info_window = Toplevel(self.root)
        info_window.title(title)
        info_window.geometry("400x150")

        label = Label(info_window, text=message, padx=20, pady=20, justify="left")
        label.pack(expand=True) 

    def calculate_sums(self):
        activities = load_activities(self.username)
        obligation_time = 0
        free_time = 0

        for activity in activities:
            try:
                duration = int(activity["activity_duration"])
                activity_type = activity["activity_type"]

                if activity_type == "Υποχρεωτική":
                    obligation_time += duration
                elif activity_type == "Ελεύθερου Χρόνου":
                    free_time += duration
            except (KeyError, ValueError):
                print(KeyError)
                print(ValueError)
                continue
            except Exception as e:
                print(e)
        time_obligation_format=format_time_reverse(obligation_time)
        time_free_format=format_time_reverse(free_time)

        message = f"Υπωχρετικές είναι {time_obligation_format["hours"]} ώρες και {time_obligation_format["mins"]} λεπτά\nΕλεύθερου Χρόνου είναι {time_free_format["hours"]} ώρες και {time_free_format["mins"]} λεπτά"
        self.show_info_window("Total Duration", message)
    
    def calculate_averages(self):
        print("hello")
        activities = load_activities(self.username)
        total_obligation_time = 0
        obligation_count = 0
        total_free_time = 0
        free_time_count = 0

        for activity in activities:
            try:
                duration = int(activity["activity_duration"])
                activity_type = activity["activity_type"]

                if activity_type == "Υποχρεωτική":
                    total_obligation_time += duration
                    obligation_count += 1
                elif activity_type == "Ελεύθερου Χρόνου":
                    total_free_time += duration
                    free_time_count += 1

            except (KeyError, ValueError):
                continue

        average_obligation = total_obligation_time / obligation_count if obligation_count > 0 else 0
        average_free_time = total_free_time / free_time_count if free_time_count > 0 else 0

        message = (
            f"Ο μέσος όρος των Υποχρεωτικών είναι {average_obligation:.2f} λεπτά\n"
            f"Ο μέσος όρος Ελεύθερου Χρόνου είναι {average_free_time:.2f} λεπτά"
        )
        self.show_info_window("Average Duration", message)

    










#--------------response build------------------
class response:
    def __init__(self, message, message_type):
        self.message = message
        self.message_type = message_type

    def __str__(self):
        return f"[{self.message_type.upper()}] {self.message}"

    def to_dict(self):
        return {
            'message': self.message,
            'message_type': self.message_type
        }

#---------------Activities table ----------------------------------
class activityUserTable:
    def __init__(self, root, username):
        activities = load_activities(username)
        self.tree = ttk.Treeview(root, columns=("name", "type", "duration", "priority"), show='headings',selectmode='browse')
        self.tree.pack(expand=True, fill='both', padx=20, pady=20)

        self.tree.heading("name", text="Όνομα Δραστηριότητας")
        self.tree.heading("type", text="Είδος Δραστηριότητας")
        self.tree.heading("duration", text="Χρόνος Δραστηριότητας")
        self.tree.heading("priority", text="Προτεραιότητα")
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


#---------------Add activity--------------------------
class addActivity:
    def __init__(self, parent, username, data, load_table_view):
        
        self.top = Toplevel(parent)  #ontop
        self.top.geometry("300x500")
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
            self.button_submit = Button(self.top, text="Update Activity", command=lambda: self.on_update_activity(username,data))
            self.button_submit.pack(pady=30)
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
    def __init__(self, root, username):
        self.username = username
        self.root = root
        self.root.geometry("800x600")
        self.root.title("My Application")
        
        self.button = Button(root, text="Πίσω", command=lambda: user_activities_route(root, username))
        self.button.pack(pady=10)
        self.weekly_limit_minutes = 10080
        self.generate_graph(username)

    def generate_graph(self, username):
        activities = load_activities(username)
        if not activities:
            Label(self.root, text="Δεν υπάρχουν δραστηριότητες.", fg="red").pack(pady=20)
            return

        obligation_time = 0
        free_time = 0
        total_time = 0

        feasible_activity_names = []
        feasible_activity_durations = []

        for activity in activities:
            try:
                duration = int(activity["activity_duration"])
                activity_type = activity["activity_type"]

                if total_time + duration > self.weekly_limit_minutes:
                    break

                if activity_type == "Υποχρεωτική":
                    obligation_time += duration
                elif activity_type == "Ελεύθερου Χρόνου":
                    free_time += duration

                total_time += duration

                feasible_activity_names.append(activity["activity_name"])
                feasible_activity_durations.append(duration)
            except Exception as e:
                print(e)
                continue

        if total_time == 0:
            Label(self.root, text="Δεν υπάρχουν πιθανές δραστηριότητες μέσα στα όρια.", fg="red").pack(pady=20)
            return

        # Δημιουργία δύο γραφημάτων δίπλα-δίπλα
        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))

        # Pie Chart (τα ποσοστά των εφικτών δραστηριοτήτων)
        labels = ['Obligations', 'Free Time']
        sizes = [obligation_time, free_time]
        colors = ['#7B4BB3', '#D6B8FF']

        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
        ax1.set_title("Possible activities in a week (%)")

        # Bar Chart (αναλυτικά όλες οι εφικτές δραστηριότητες)
        ax2.barh(feasible_activity_names, feasible_activity_durations, color='#7B4BB3')
        ax2.set_xlabel("Duration (minutes)")
        ax2.set_title("Possible Activities in a week")

        plt.tight_layout()
        plt.show()



def load_activities(username):
    file_name=username+'.csv'
    file_path = os.path.join(base_dir, 'csv', file_name)
    print(file_path)
    try:
        with open(file_path,'r',encoding='utf-8')as f:
            activities=[]
            file=f.read()
            print(file)
            lines=file.split('\n')
            for line in lines[:-1]:
                value =line.split(',')
                activity=Activity(
                    activity_name=value[0],
                    activity_type=value[1],
                    activity_duration=value[2],
                    activity_priority=value[3]
                )
                activities.append(activity.to_dict())
        return activities
    except FileNotFoundError:
        print(f"File not found for user: {username}")
        return []
    except Exception as error:
        print(f"Error loading activities: {error}")
        return []


                        
def add_activity(username,activity_name,activity_type,activity_duration,activity_priority):
    file_name=username +'.csv'
    csv_dir = os.path.join(base_dir, 'csv')
    full_path=os.path.join(csv_dir,file_name)
    print(full_path)
    with open(full_path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        row = [activity_name, activity_type, activity_duration, activity_priority]
        writer.writerow(row)
    


def list_users():
    tmp_list = os.listdir(csv_path)
    users=[]
    for file in tmp_list:
        user=file.split('.')
        print(user)
        if user[0] == "users":
            continue
        else:
            users.append(user[0])
    print("user list:",users)
    return users

    

def format_time(hours,mins):
    hours = int(hours)
    mins = int(mins)
    print("hours=",hours)
    print("mins=",mins)
    hours_to_mins=hours*60
    activity_duration=hours_to_mins+mins
    print("final=",activity_duration)
    return activity_duration


def format_time_reverse(activity_duration):
    total_mins=int(activity_duration)
    print("DEBUG total mins:",total_mins)
    hours=total_mins//60
    print("DEBUG hours:",hours)
    mins=total_mins % 60
    print("DEBUG mins:",mins)
    return {"mins": mins , "hours":hours}


def create_csv(username):
    file_name=username +'.csv'
    csv_dir = os.path.join(base_dir, 'csv')
    full_path=os.path.join(csv_dir,file_name)
    print(full_path)
    with open(full_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        field = ["Ύπνος", "Υποχρεωτική", "480","9"]
        writer.writerow(field)
        file.close


def check_duplicate_file(username):
    file_name=username+'.csv'
    file_path = os.path.join(base_dir, 'csv', file_name)
    print ('DEBUG: file_name: ',file_path)
    if os.path.exists(file_path):
        print("it's here...")
        return True
    else:
        print("it's not here...")
        return False


def create_user(username):
    try:
        check_user_existance=check_duplicate_file(username)
        if check_user_existance is True:
            return response("The user already exists","error" )
        else:
            create_csv(username)
            check_user_existance=check_duplicate_file(username)
            if check_user_existance is True:
                return response("The user was created","success" )
            else:
                return response("There was an error when creating the user file","error" )
    except:
        print("The user wasn't create")


def update_activity(username, activity_name, activity_type, activity_duration, activity_priority, old_data):
    file_name = username + '.csv'
    csv_dir = os.path.join(base_dir, 'csv')
    full_path = os.path.join(csv_dir, file_name)
    print("Updating file:", full_path)
    updated_rows = []
    
    with open(full_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if [str(cell).strip() for cell in row] == [str(cell).strip() for cell in old_data]: #serialize παλίας εγγραφης
                continue
            updated_rows.append(row)

    new_row = [activity_name, activity_type, activity_duration, activity_priority]
    updated_rows.append(new_row)

    with open(full_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)
        
    print("Row updated successfully.")
    


def delete_activity(username, selected):
    print("Trying to delete row:", selected)

    file_name = username + '.csv'
    csv_dir = os.path.join(base_dir, 'csv')
    full_path = os.path.join(csv_dir, file_name)
    updated_rows = []
    row_found = False
    with open(full_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            print("Checking row:", row)
            if (row[0] == str(selected[0]) and
                row[1] == str(selected[1]) and
                row[2] == str(selected[2]) and
                row[3] == str(selected[3])):
                print("Match found — skipping row:", row)
                row_found = True
                continue  # skip this row
            updated_rows.append(row)

    if not row_found:
        print("No matching row found.")

    with open(full_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)

    print("Finished updating file.")





def sort_activities(username):
    file_name = username + '.csv'
    csv_dir = os.path.join(base_dir, 'csv')
    full_path = os.path.join(csv_dir, file_name)
    with open(full_path, 'r', encoding='utf-8') as file:
        free_time=[]
        mandatory=[]
        reader = csv.reader(file)
        for row in reader:
            if row[1]=='Υποχρεωτική':
                mandatory.append(row)
            elif row[1]=='Ελεύθερου Χρόνου':
                free_time.append(row)
            else:
                print("error")


        new_free_time = sorted(free_time, key=lambda x: x[3])
        new_mandatory = sorted(mandatory, key=lambda x: x[3])


    print(free_time)
    print(new_free_time)
    print(mandatory)
    print(new_mandatory)
    newlines=new_mandatory+new_free_time
    print(newlines)
    with open(full_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(newlines)
                        




#----------------Routes-------------------------
# def pick_user_route(root):
#     for child in root.winfo_children():
#         child.destroy()
#     pickUser(root)

def pick_user_route(root):
    for child in root.winfo_children():
        child.destroy()
    create_users_page('display_all',root)
   

# def create_user_route(root):
#     for child in root.winfo_children():
#         child.destroy()
#     createUser(root)
    


def user_activities_route(root,username):
    print("the root is:", root)
    for child in root.winfo_children():
        child.destroy()
    activitiesUser(root,username)
    


def add_activity_route(root,username,selected,load_table_view):
    addActivity(root,username,None,load_table_view)


def update_activity_route(root, username, selected,load_table_view):
    print ("UPDATE ROUTE")
    print("username=",username)
    print("selected=",selected)
    addActivity(root,username,selected,load_table_view)



def graph_route(root,username):
    for child in root.winfo_children():
        child.destroy()
    Graph(root,username)

if __name__ == "__main__":
    main()
