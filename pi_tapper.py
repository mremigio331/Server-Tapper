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
import subprocess
import ray


import sys
sys.path.append('Additional_py_Files/')
import pi_db_connect as db
import pi_pull
import pi_push

ray.init()

@ray.remote
def push():
	sys.path.append('Additional_py_Files/')
	import pi_push
	pi_push.run()

@ray.remote
def pull():
	sys.path.append('Additional_py_Files/')
	import pi_pull
	pi_pull.run()

#def smap(f):
    #return f()

ray.get([push.remote(), pull.remote()])

#if __name__ == '__main__':
#	print('Starting')
#	multiprocessing.freeze_support()
#
#3	main_pull = functools.partial(push)
#	main_push = functools.partial(pull)
#
#	with Pool() as pool:
#		res = pool.map(smap, [main_pull, main_push])
#		pool.close()
#		pool.join()
	