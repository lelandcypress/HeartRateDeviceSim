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
    patient_stats={
    'hr' : None,
    'bpsys' : None,
    'bpdia' : None,
    'oxy' : None}
    normal(patient_stats)
    querystring =''
    #convert the dictionary into a passable string#
    for stat in dict:
        querystring = stat[1]
        print (querystring)
    

def handledataInsertion(dict):
    querystring =''
    #convert the dictionary into a passable string#
    for stat in dict:
        querystring = stat[1]

    # creating connection object and passing the string
    mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password",
    database = "patient_monitor"
    )
    cursor = mydb.cursor()
    cursor.callproc("sp_addstats",args=(querystring))
    mydb.commit();
    



