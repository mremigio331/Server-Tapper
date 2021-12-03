from datetime import datetime, timedelta
import random
import time
from multiprocessing import Process, Pool, Manager
import sys
import schedule
import pandas as pd

global lis
lis = []

def hi_time(letter):
    df = pd.DataFrame(columns = ['Letters','Time'])
    lis = []
    iterations = random.randint(10,30)
    iterations_left = iterations
    print(letter + ' There will be ' + str(iterations) + ' iterations.')
    x = 0 
    while x < iterations:
        sleep_time = random.randint(3,20)
        x = x + 1
        iterations_left = iterations_left - 1
        print(letter + ' It is ' + str(datetime.now()) + '. Wait time is ' + str(sleep_time) + ' seconds and there are ' + str(iterations_left) + ' iterations left.')
        time.sleep(sleep_time)
        lis.append(letter + str(datetime.now()))
        new_row = {'Letters':letter,'Time':datetime.now()}
        df = df.append(new_row, ignore_index = True)
        if iterations_left == 0:
            print('***' + letter + 'DONE***')
            #print(lis)
            #print(df)
            go = False
            while go == False:
                try:
                    with open("test.txt", "a") as f:
                        for x in lis:
                            f.write(x + '\n')
                    f.close()
                    go = True
                except:
                    time.sleep(5)
            return df  
        else:
            pass
        
def main_pool():
    letters = ['AAA','BBB','CCC']
    with Manager() as manager:
        #lis = manager.list()
        with Pool() as pool:
            res = pool.map(hi_time, letters)
            outputs = [result for result in res]
            pool.close()
            #full = []
            #for x in outputs:
                #full.extend(x)
            result = pd.concat(outputs)
            print(result)
            #return result
            

if __name__ == '__main__':
    main_pool()