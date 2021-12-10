from datetime import datetime, timedelta
import random
import time
from multiprocessing import Process, Pool, Manager
import multiprocessing
import sys
import schedule
import pandas as pd
import pysftp
from threading import Thread
import functools

from Additional_py_Files import pi_db_connect as db


global box_info
box_info = db.grab_box_info()

global ranges_info
range_info = db.grab_ranges_info()


def push(starting_box):

    x = box_info.loc[box_info['User'] == starting_box]
    row_list = x.values.tolist()
    box = row_list[0][0]
    ip = row_list[0][1]
    usname = row_list[0][0]
    p_key = row_list[0][2]
    box_port = int(row_list[0][3])

    p = range_info.loc[range_info['Type'] == 'Push']
    p_list = p.values.tolist()
    p_min= p_list[0][1]
    p_max= p_list[0][2]

    iterations_range = range_info.loc[range_info['Type'] == 'Iterations']
    iterations_range_list = iterations_range.values.tolist()
    iterations_min = iterations_range_list[0][1]
    iterations_max = iterations_range_list[0][2]
    
    actions_list = []
    df = pd.DataFrame(columns = ['User','DTG','Access','Action'])
    iterations = random.randint(iterations_min,iterations_max)
    iterations_left = iterations
    message = ('There will be ' + str(iterations) + ' push attempts to ' + box)
    x = 0
    save_name = 'Data/' + box + 'file.txt'

    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    db.message_add(message)
    print(message)

    start_sleep = random.randint(1,20)
    time.sleep(start_sleep)

    while x < iterations:
        try:
            with pysftp.Connection(ip, username=usname, private_key=p_key, port= int(box_port), cnopts=cnopts) as sftp:
                    with sftp.cd('.'):
                        sftp.put('requirements.txt', 'requirements.txt')         # get a remote file
            now = datetime.now()
            time_string = now.strftime("%Y-%m-%d %H:%M:%S")
            new_row = {'User':box,'DTG':time_string,'Access':'Success','Action':'Pushed File'}
            df = df.append(new_row, ignore_index = True)
            message = ('Successfully pushed file from ' + box + ' at ' + str(time_string))
            print(message)
            actions_list.append(message)
            db.message_add(message)
            db.log_add(new_row)
            
        except:
            now = datetime.now()
            time_string = now.strftime("%Y-%m-%d %H:%M:%S")
            new_row = {'User':box,'DTG':time_string,'Access':'Fail','Action':'Pushed File'}
            df = df.append(new_row, ignore_index = True)
            message = ('Failed to push file from ' + box + ' at ' + str(time_string))
            print(message)
            actions_list.append(message)
            db.message_add(message)
            
        sleep_time = random.randint(p_min,p_max)
        x = x + 1
        iterations_left = iterations_left - 1
                
        if iterations_left == 0:
            done_mess = ('***' + box + ' DONE with a total of ' + str(iterations) + ' iterations***')
            print(done_mess)
            db.message_add(done_mess)
            return df  
        else:
            message = ('Next push on ' + box + ' will be in ' + str(sleep_time) + ' seconds. There are ' + str(iterations_left) + ' iterations left.')
            db.message_add(message)
            print(message)
            time.sleep(sleep_time)

def main_push():
    boxes = box_info['User'].tolist()
    print('Will be pushing to the following servers:')
    print(boxes)
    with Manager() as manager:
        with Pool() as pool:
            res = pool.map(push, boxes)
            outputs = [result for result in res]
            pool.close()
            result = pd.concat(outputs)
            print(result)
def run():
    main_push()