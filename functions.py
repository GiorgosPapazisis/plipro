import os,csv

base_dir = os.path.dirname(__file__)
csv_path = file_path = os.path.join(base_dir, 'csv')



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
        field = ["activity_name", "activity_type", "activity_duration","activity_importance"]
        writer.writerow(field)
        file.close




def create_user(username):
    try:
        check_user_existance=check_duplicate_file(username)
        if check_user_existance is True:
            print (f"The user '{username}' already exists...")
        else:
            create_csv(username)
            check_user_existance=check_duplicate_file(username)
            if check_user_existance is True:
                print(f"the file for user '{username}' was created")
            else:
                print(f"the file for user '{username}' wasnt created")
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

    
    
    

