from datetime import datetime, timedelta
import random
import time
from multiprocessing import Process, Pool, Manager, freeze_support
import multiprocessing
import sys
import schedule
import pandas as pd
import pysftp
from threading import Thread
import functools

import pi_db_connect as db


global box_info

#new_row = {'User':['yankee','met'],'IP':['149.28.44.187','149.28.44.187'],
#           'Private_Key':['Keys/yankee','Keys/met'],'Port':['3794','3794']}
#box_info = pd.DataFrame(new_row)

box_info = db.grab_box_info()
#print(box_info)

def push(starting_box):
    x = box_info.loc[box_info['User'] == starting_box]
    row_list = x.values.tolist()
    box = row_list[0][0]
    ip = row_list[0][1]
    usname = row_list[0][0]
    p_key = row_list[0][2]
    box_port = int(row_list[0][3])
    
    actions_list = []
    df = pd.DataFrame(columns = ['User','DTG','Access','Action'])
    iterations = random.randint(2,3)
    iterations_left = iterations
    print('There will be ' + str(iterations) + ' push attempts to ' + box)
    x = 0
    save_name = 'Data/' + box + 'file.txt'

    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None


    while x < iterations:
        try:
            new_row = {}
            with pysftp.Connection(ip, username=usname, private_key=p_key, port= int(box_port), cnopts=cnopts) as sftp:
                    with sftp.cd('.'):
                        sftp.put('requirements.txt', 'requirements.txt')         # get a remote file
            now = datetime.now()
            time_string = now.strftime("%Y-%m-%d %H:%M:%S")
            new_row = {'User':box,'DTG':time_string,'Access':'Success','Action':'Pushed File'}
            df = df.append(new_row, ignore_index = True)
            message = ('Successfully put file in ' + box + ' at ' + str(time_string))
            print(message)
            actions_list.append(message)
            
            try:
                db.log_add(new_row)
                print('DB Add Success')
            except:
                db.log_add(new_row)
                print('DB Add Fail')
        
        except:
            now = datetime.now()
            time_string = now.strftime("%Y-%m-%d %H:%M:%S")
            new_row = {'User':box,'DTG':time_string,'Access':'Fail','Action':'Pushed File'}
            df = df.append(new_row, ignore_index = True)
            message = ('Failed to put file into ' + box + ' at ' + str(time_string))
            print(message)
            actions_list.append(message)
            try:
                db.log_add(new_row)
                print('DB Add Success')
            except:
                db.log_add(new_row)
                print('DB Add Fail')

            
        sleep_time = random.randint(3,20)
        x = x + 1
        iterations_left = iterations_left - 1
                
        if iterations_left == 0:
            print('***' + box + ' DONE***')
            with open("test.txt", "a") as f:
                for x in actions_list:
                    f.write(x + '\n')
            return df  
        else:
            print('Next push on ' + box + ' will be in ' + str(sleep_time) + ' seconds. There are ' + str(iterations_left) + ' iterations left.')
            time.sleep(sleep_time)


def main_push():
    boxes = box_info['User'].tolist()
    print(boxes)
    with Manager() as manager:
        #lis = manager.list()
        with Pool() as pool:
            res = pool.map(push, boxes)
            outputs = [result for result in res]
            pool.close()
            #full = []
            #for x in outputs:
                #full.extend(x)
            result = pd.concat(outputs)
            print(result)

            
def run():
    main_push()
    
#if("-r" in  sys.argv):
#    run()

if __name__ == '__main__':
    freeze_support()