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

	