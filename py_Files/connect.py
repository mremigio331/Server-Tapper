import sqlite3
import pandas as pd
import pysftp

global database
database = 'Data/server_tap.db'

def add_connecion():
    users_added = []
    a = True

    while a is True:

        print('You will be asked to input a username, ip, private_key, and port for the connection to your server')
        user = input('What is the username?: ')
        ip = input('What is the IP address?: ')
        private_key = input('Where is the private key stored? (Place in Keys directory for easy setup): ')
        port = input('What is the SSH port number?: ')

        add = username_to_db(user, ip, private_key, port)

        if add is True:
            users_added.append(user)
        else:
            pass

        yes_options = ['y', 'Y', 'Yes', 'YES', 'yes']
        continue_ = input('Would you like to add another user? ')
        if continue_ in yes_options:
            pass
        else:
            a = False

    print('Added the following new users')
    print(users_added)

def change_file(filename,type):
    try:
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute('UPDATE Files SET Name = ? WHERE Type = ?',(filename,type))
        conn.commit()
        c.close()
        conn.close()
        print('Successfully updated database.')
        return True
    except:
        print('Unsuccessfully updated database.')
        return False

def check():
    users_check = []
    box_info = grab_box_info()
    a = True

    while a is True:

        b = True
        while b is True:
            users = box_info['User'].tolist()
            print(users)
            user = input('What is the username would you like to check? ')
            if user in users:
                b = False
            else:
                print('Error, that user is not in the database, please try again.')

        x = box_info.loc[box_info['User'] == user]
        row_list = x.values.tolist()
        ip = row_list[0][1]
        usname = row_list[0][0]
        p_key = row_list[0][2]
        box_port = int(row_list[0][3])

        check = server_connection_check(ip, usname, p_key, box_port)

        if check is True:
            users_check.append(user)
        else:
            pass

        yes_options = ['y', 'Y', 'Yes', 'YES', 'yes']
        continue_ = input('Would you like to check another user? (Y/N) ')
        if continue_ in yes_options:
            pass
        else:
            a = False

    print('Successful connected the following users')
    print(users_check)

def delete_connection():
    users_deleted = []

    a = True
    while a is True:
        box_info = grab_box_info()
        boxes = box_info['User'].tolist()
        print('Server Usernames In Database')
        print(boxes)
        user = input('What is the username for the connection you would like to delete? ')

        db_delete = username_delete_db(user)

        if db_delete is True:
            users_deleted.append(user)
        else:
            pass

        yes_options = ['y', 'Y', 'Yes', 'YES', 'yes']
        continue_ = input('Would you like to delete another user? (Y/N) ')
        if continue_ in yes_options:
            pass
        else:
            a = False

    print('Deleted the following users')
    print(users_deleted)

def grab_box_info():
    try:
        db = sqlite3.connect(database)
        df = pd.read_sql_query('SELECT * FROM Box_Info', db)
        return df
    except:
        print('Failed to connect to the database')

def grab_file_info():
    try:
        db = sqlite3.connect(database)
        df = pd.read_sql_query('SELECT * FROM Files', db)
        return df
    except:
        print('Failed to connect to the database')

def grab_ranges_info():
    try:
        db = sqlite3.connect(database)
        df = pd.read_sql_query('SELECT * FROM Ranges', db)
        return df
    except:
        print('Failed to connect to the database')

def log_add(row):
    df = pd.DataFrame(columns = ['User','DTG','Access','Action'])
    df = df.append(row, ignore_index = True)

    conn = sqlite3.connect(database)
    c = conn.cursor()
    df.to_sql('Logs', conn, if_exists='append', index = False)
    try:
        c.close
        conn.close()
    except:
        print('Database not closed')

def logs_to_csv(filename):
    try:
        db = sqlite3.connect(database)
        df = pd.read_sql_query('SELECT * FROM Logs', db)
        df.to_csv(filename, index=False)
        message = ('Successfully exported logs to csv')
        message_add(message)
        print(message)
    except:
        message = ('Unsuccessfully exported logs to csv')
        message_add(message)
        print(message)

def message_add(message):
    db = sqlite3.connect(database)
    cursor = db.cursor()
    cursor.execute('INSERT OR IGNORE INTO Messages(Output) VALUES (?)',[message])
    db.commit()

def messages_to_txt(filename):
    try:
        db = sqlite3.connect(database)
        df = pd.read_sql_query('SELECT * FROM Messages', db)
        messages = df['Output'].tolist()

        with open(filename, 'w') as f:
            for x in messages:
                f.write(x + '\n')
            f.close()
        print('Successfully exported messages to txt')
    except:
        print('Unsuccessfully exported messages to txt')

def server_connection_check(ip,usname,p_key,box_port):

    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    try:
        with pysftp.Connection(ip, username=usname, private_key=p_key, port=box_port, cnopts=cnopts) as sftp:
            with sftp.cd('.'):
                message = ('Connection Successful to ' + usname)
                print(message)
                message_add(message)
                return True

    except:
        message = ('Connection Unsuccessful to ' + usname)
        print(message)
        message_add(message)
        return False

def update_info():
    users_updated = []

    a = True
    while a is True:
        box_info = grab_box_info()
        print('Server Username Data In Database')
        print(box_info)

        b = True
        while b is True:
            user = input('What is the username would you like to update? ')
            user_info = box_info.loc[box_info['User'] == user]
            users = box_info['User'].tolist()

            if user in users:
                b = False
                print(user_info)
            else:
                print('Error, that user is not in the database, please try again.')

        c = True

        while c is True:
            options = ['User','IP','Private_Key','Port']
            location = input('What would you like to update? (type one of the following: User, IP, Private_Key, Port): ')
            if location in options:
                c = False
            else:
                print('Error, that is not an option, please try again.')

        change_message = 'What would you like to change ' + user + "'s " + location + ' to?: '
        change = input(change_message)

        db_change = update_server_info(change,location,user)

        go_no_go = db_change[0]
        message = db_change[1]

        if go_no_go is True:
            users_updated.append(message)
            box_info = grab_box_info()
            if location == 'User':
                user_info = box_info.loc[box_info['User'] == change]
            else:
                user_info = box_info.loc[box_info['User'] == user]
            print('*** UPDATE ***')
            print(user_info)
        else:
            pass

        yes_options = ['y', 'Y', 'Yes', 'YES', 'yes']
        continue_ = input('Would you like to update another user? (Y/N) ')
        if continue_ in yes_options:
            pass
        else:
            a = False

    print('Updated the following user information')
    print(users_updated)

def update_server_info(change,location,server_name):
    try:
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute('UPDATE Box_Info SET '+ location + ' = ? WHERE User = ?',(change,server_name))
        conn.commit()
        c.close()
        conn.close()
        message = 'Successfully updated ' + server_name + ' ' + location + ' to ' + str(change)
        print(message)
        message_add(message)
        return True, message

    except:
        message = 'Unsuccessfully updated ' + server_name + ' ' + location + ' to ' + str(change)
        print(message)
        message_add(message)
        return False

def update_range_info(type,mm,number):
    try:
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute('UPDATE Ranges SET '+ mm + ' = ? WHERE Type = ?',(number,type))
        conn.commit()
        c.close()
        conn.close()
        change = 'Updated ' + type + ' ' + mm + ' to ' + str(number)
        print(change)
        message_add(change)
        return True, change
    except:
        change = 'Unsuccessfully updated ' + type + ' ' + mm + ' to ' + str(number)
        print(change)
        message_add(change)
        return False

def update_range():
    range_update = []
    a = True

    while a is True:
        range_info = grab_ranges_info()
        print(range_info)

        t_options = ['Pull', 'Push', 'Iterations']
        type = input('What Type would you like to change? ')
        type = type.title()

        b = True
        while b is True:
            if type not in t_options:
                type = input('Error, invalid option. Chose Pull, Push, or Iterations ')
                type = type.title()
            else:
                b = False

        mm_options = ['Min', 'Max']
        mm = input('Would you like to change the Min or Max ')
        mm = mm.title()
        print(mm)
        c = True
        while c is True:
            if mm not in mm_options:
                mm = input('Error, invalid option. Chose Min or Max ')
                mm = mm.title()
            else:
                c = False

        number = int(input('What value would you like to change it to? '))
        d = True
        while d is True:
            if mm == 'Min':
                mm_row = range_info.loc[range_info['Type'] == type]
                row_list = mm_row.values.tolist()
                max_number = row_list[0][2]
                if number >= max_number:
                    number = int(input('Error: Number must not be greater or equal to Max. Enter new number: '))
                else:
                    d = False
            if mm == 'Max':
                mm_row = range_info.loc[range_info['Type'] == type]
                row_list = mm_row.values.tolist()
                min_number = row_list[0][1]
                if min_number >= number:
                    number = int(input('Error: Number must not be less than or equal to Min. Enter new number: '))
                else:
                    d = False
            else:
                d = False

        check = update_range_info(type,mm,number)

        go_or_no_go = check[0]
        message = check[1]

        if go_or_no_go is True:
            range_update.append(message)
        else:
            pass

        yes_options = ['y', 'Y', 'Yes', 'YES', 'yes']
        continue_ = input('Would you like to change another range? (Y/N) ')
        if continue_ in yes_options:
            pass
        else:
            a = False

    print('Successful updated the following ranges')
    print(range_update)

def username_delete_db(server):
    try:
        delresult = '"'+server+'"'
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute('DELETE from Box_Info WHERE User='+str(delresult))
        conn.commit()
        c.close()
        conn.close()
        message = 'Successfully deleted ' + server
        print(message)
        message_add(message)
        return True

    except:
        message = 'Unsuccessfully deleted ' + server
        print(message)
        message_add(message)
        return False

def username_to_db(user, ip, private_key, port):
    try:
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute('INSERT INTO Box_Info(User, IP, Private_Key, Port) VALUES (?,?,?,?)',(user, ip, private_key, port))
        conn.commit()
        c.close()
        conn.close()
        message = message = 'Added ' + user + ' ' + ip + ' ' + private_key + ' ' + str(port) +  ' to database.'
        print(message)
        message_add(message)
        return True
    except:
        message ='Failed to add ' + user + ' ' + ip + ' ' + private_key + ' ' + str(port) + ' to database.'
        print(message)
        message_add(message)
        return False












