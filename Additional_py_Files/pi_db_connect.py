import os
import glob
import pandas as pd
import pysftp
from time import strptime
from pytz import timezone
from time import strptime
from datetime import *
import pytz
import pydeck as pdk
from alive_progress import alive_bar, config_handler
import numpy as np
import sqlite3
from stqdm import stqdm
import random
import time
import sys
import schedule
import pandas as pd

def grab_box_info():
    print('Loading Box Information')
    try:
        db = sqlite3.connect('Data/logs.db')
        df = pd.read_sql_query("SELECT * FROM Box_Info", db) 
        return df
        print('Box Information successfully')
    except:
        print('Failed to connect to the database')

def log_add(row):
	df = pd.DataFrame(columns = ['User','DTG','Access','Action'])
	df = df.append(row, ignore_index = True)

	conn = sqlite3.connect('Data/logs.db')
	c = conn.cursor()
	df.to_sql('Logs', conn, if_exists='append', index = False)
	try:
		c.close
		conn.close()
		print('Database closed')
	except:
		print('Database not closed')