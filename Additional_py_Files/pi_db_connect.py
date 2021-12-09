
import sqlite3
import pandas as pd

def grab_box_info():
    print('Loading Box Information')
    try:
        db = sqlite3.connect('Data/logs.db')
        df = pd.read_sql_query('SELECT * FROM Box_Info', db) 
        print('Box Information successfully')
        return df
    except:
        print('Failed to connect to the database')

def grab_ranges_info():
    print('Loading Ranges Information')
    try:
        db = sqlite3.connect('Data/logs.db')
        df = pd.read_sql_query('SELECT * FROM Ranges', db) 
        print('Box Information successfully')
        return df
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

def message_add(message):
    db = sqlite3.connect('Data/logs.db')
    cursor = db.cursor()
    cursor.execute('INSERT OR IGNORE INTO Messages(Output) VALUES (?)',[message])
    db.commit()