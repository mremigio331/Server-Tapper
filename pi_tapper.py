import sys
import multiprocessing
from Additional_py_Files import pi_pull
from Additional_py_Files import pi_push

sys.path.append('Additional_py_Files/')


def push():
    sys.path.append('Additional_py_Files/')
    pi_push.run()


def pull():
    sys.path.append('Additional_py_Files/')
    pi_pull.run()


if __name__ == "main":
    p1 = multiprocessing.Process(target=push)
    p2 = multiprocessing.Process(target=pull)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
