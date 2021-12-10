import sys
import multiprocessing
from multiprocessing import Process, Pool, Manager, freeze_support
from Additional_py_Files import pi_pull
from Additional_py_Files import pi_push
from Additional_py_Files import pi_db_connect as db
sys.path.append('Additional_py_Files/')

def push():
    pi_push.run()

def pull():
    pi_pull.run()

if ('-a' in  sys.argv) or ('-add' in  sys.argv):
    print('*** ADD CONNECTION ***')
    db.add_connecion()

if ('-c' in  sys.argv) or ('-check' in  sys.argv):
    print('*** CHECK CONNECTION ***')
    db.check()

if ('-d' in  sys.argv) or ('-delete' in  sys.argv):
    print('*** DELETE CONNECTION ***')
    db.delete_connection()

if ('-h' in  sys.argv) or ('-help' in  sys.argv):
    print('*** Commands ***')
    print('-a  -add        adds a server to the database')
    print('-c  -check      checks to see if a connection can be made to server')
    print('-d  -delete     deletes a server to the database ')
    print('-h  -help       brings up help screen')
    print('-i  -iterations change ranges and iterations')
    print('-l  -pull       will only pull files to your servers')
    print('-lf -pullf      change file you will be pulling')
    print('-om -messages   exports message table in database to a filename you define to txt file')
    print('-ol -logs       export logs table in database to a filename you define to a csv')
    print('-r  -run        runs entire code to push and pull files')
    print('-s  -push       will only push files to your servers')
    print('-sf -pushf      change file you want to push')
    print('-u  -update     updates a server in the database')

if ('-i' in  sys.argv) or ('-iterations' in  sys.argv):
    print('*** CHANGE RANGE OR ITERATIONS INFO ***')
    db.update_range()

if ('-l' in  sys.argv) or ('-pull' in  sys.argv):
    if __name__ == '__main__':
        pi_pull.run()

if ('-lf' in  sys.argv) or ('-pullf' in  sys.argv):
    print('*** CHANGE PULL FILE ***')

    try:
        filename = sys.argv[2]
    except:
        filename = ''

    if filename == '':
        file_info = db.grab_file_info()
        print(file_info)

        a = True
        while a is True:
            if filename == '':
                filename = input('What is the name of the file you want to pull? ')
            else:
                a = False

    db.change_file(filename,'Pull_File')

if ('-ol' in sys.argv) or ('-logs' in sys.argv):
    print('*** EXPORT LOGS ***')
    try:
        filename = sys.argv[2]
    except:
        filename = ''

    if filename == '' or '.csv' not in filename:
        a = True
        while a is True:
            if filename == '':
                filename = input('What do you want to name the output? Make sure .csv is in filename: ')
            if '.csv' not in filename:
                filename = input('Filename needs a .csv extension, what do you want to name your file?: ')
            else:
                a = False

    db.logs_to_csv(filename)

if ('-om' in sys.argv) or ('-messages' in sys.argv):
    print('*** EXPORT Messages ***')
    try:
        filename = sys.argv[2]
    except:
        filename = ''

    if filename == '' or '.txt' not in filename:
        a = True
        while a is True:
            if filename == '':
                filename = input('What do you want to name the output? Make sure .txt is in filename: ')
            if '.txt' not in filename:
                filename = input('Filename needs a .txt extension, what do you want to name your file?: ')
            else:
                a = False

    db.messages_to_txt(filename)

if ('-r' in  sys.argv) or ('-run' in sys.argv):
    if __name__ == '__main__':
        freeze_support()
        p1 = multiprocessing.Process(target=push)
        p2 = multiprocessing.Process(target=pull)
        p1.start()
        p2.start()
        p1.join()
        p2.join()

if ('-s' in  sys.argv) or ('-push' in  sys.argv):
    if __name__ == '__main__':
        pi_push.run()

if ('-sf' in  sys.argv) or ('-pushf' in  sys.argv):
    print('*** CHANGE PUSH FILE ***')

    try:
        filename = sys.argv[2]
    except:
        filename = ''

    if filename == '':
        file_info = db.grab_file_info()
        print(file_info)

        a = True
        while a is True:
            if filename == '':
                filename = input('What is the name of the file you want to push? ')
            else:
                a = False

    db.change_file(filename,'Push_File')

if('-u' in  sys.argv) or ('-update' in  sys.argv):
    print('*** UPDATE CONNECTION ***')
    db.update_info()


