import sys
import multiprocessing
from multiprocessing import Process, Pool, Manager, freeze_support
from Additional_py_Files import pi_pull
from Additional_py_Files import pi_push
sys.path.append('Additional_py_Files/')

def push():
    pi_push.run()

def pull():
    pi_pull.run()

if __name__ == '__main__':
    freeze_support()
    p1 = multiprocessing.Process(target=push)
    p2 = multiprocessing.Process(target=pull)
    p1.start()
    p2.start()
    p1.join()
    p2.join()