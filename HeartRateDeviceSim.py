import random
import mysql.connector


#set up a list to store the ranges
#   O2, Heart Rate, BP
#  Set up a while true loop
#   Set up a function that changes the values 
        # Increase HR 
            # Account for change in O2 and HR


#Starting point: set up a device that sims normal and fires an insert statement into DB
        # Connect the script into the DB

 


def randomizeStats(lower,upper):
    return random.randint(lower,upper)

def normal(stats):
   stats[0] = randomizeStats(70,80)
   stats[1] = randomizeStats(110,120)
   stats[2] = randomizeStats(70,80)
   stats[3] = randomizeStats(98,99)
   return stats   

def init():
    
    hr = None
    bpsys =  None
    bpdia = None
    oxy = None
    patient_stats = [hr,bpsys,bpdia,oxy]
    normal(patient_stats)
    patient_stats=tuple(patient_stats)
    handledataInsertion(patient_stats) 
    #convert the dictionary into a passable string#

def handledataInsertion(tup):
    

    # creating connection object and passing the values
    mydb = {
    'host' : "localhost",
    'user' : "root",
    'password' : "password",
    'database' : "patient_monitor"}
    
    try:
        conn = mysql.connector.connect(**mydb)
        cursor = conn.cursor()
        cursor.callproc("sp_addstats",args=tup)
        conn.commit();
    except mysql.connector.Error as err:
        print(err)
    finally:
        conn.close()
init()


