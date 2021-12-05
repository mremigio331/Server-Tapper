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

ray.get([push.remote(), pull.remote()])
	