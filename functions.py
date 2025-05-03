import os,csv

base_dir = os.path.dirname(__file__)
csv_path = file_path = os.path.join(base_dir, 'csv')



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




def create_csv(username):
    file_name=username +'.csv'
    csv_dir = os.path.join(base_dir, 'csv')
    full_path=os.path.join(csv_dir,file_name)
    print(full_path)
    with open(full_path, 'w', newline='') as file:
        writer = csv.writer(file)
        field = ["activity_name", "activity_type", "activity_duration","activity_priority"]
        writer.writerow(field)
        file.close




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


def check_csv_file():
    file_path = os.path.join(base_dir, 'csv')
    if os.path.exists(file_path):
        print("The csv file exists")
    else:
        print("the csv file doesn't exist")
        try:
            os.mkdir('csv')
        except Exception as error:
            print(f"An error occurred: {error}")
    



def list_users():
    tmp_list = os.listdir(csv_path)
    users=[]
    for file in tmp_list:
        user=file.split('.')
        print(user)
        users.append(user[0])
    print("user list:",users)
    return users



def check_file_stracture(username):
    print("hello")
    file_name=username+'.csv'
    file_path = os.path.join(base_dir, 'csv', file_name)
    try:
        with open(file_path) as f:
            file=f.read()
            lines=file.split('\n')
            if lines and lines[-1].strip() == '': #the last line '' if the last line has 1 element and is '' then remove it from the check
                print("Skipping final empty line")
                lines = lines[:-1]
            for line in lines:
                value_counter=0
                for value in line.split(','):
                    value_counter+=1
                    print(value_counter,value)
                if value_counter==1 and value=='' or value_counter!=4:
                    raise Exception("There is an error in the file")
        return response("File looks good", "success" )
    except Exception as error:
        print(error)
        return response(str(error), "error" )
        

     
def fix_file_stracture(username):
    file_name = username + '.csv'
    file_path = os.path.join(base_dir, 'csv', file_name)
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        # Only keep lines that are not empty after stripping
        data_lines=[]
        for line in lines:
            stripped = line.strip()
            if stripped == '':
                continue  # Skip empty lines

            values = stripped.split(',')
            if len(values) != 4:
                print(f"Skipping malformed line: {stripped}")
                continue  # Skip lines with incorrect structure

            data_lines.append(stripped)

        # Add back '\n' to each cleaned line
        cleaned_lines=[]
        for line in data_lines:
            cleaned_lines.append(line + '\n')


        with open(file_path, 'w', newline='') as f:
            f.writelines(cleaned_lines)

        print("Empty rows removed successfully.")
        return response("Empty rows deleted successfully", "success")
    except Exception as error:
        print(f"Error while cleaning file: {error}")
        return response(str(error), "error")


    
def load_activities(username):
    file_name=username+'.csv'
    file_path = os.path.join(base_dir, 'csv', file_name)
    print(file_path)
    try:
        with open(file_path,'r')as f:
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


                        

# def change_view(root,view):
#     children=root.winfo_children()
#     print(children)
#     tree.destroy()
#     if view=='table':
#         view_mode='list'

#     elif view=='list':
#         view_mode='table'

#     return view_mode
    

