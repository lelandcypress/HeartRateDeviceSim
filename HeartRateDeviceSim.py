import random
import mysql.connector
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import winsound
import time
import os

def start_animation():
# Create a function to generate random heart rate data
    def generate_heart_rate_data(condition):
        match condition:
            case 'normal':
                heart_rate= random.randint(70,80)
                systolic = random.randint(110,120)
                diastolic = random.randint(70,80)
                oxygen = round(random.uniform(96.0,99.00),2)      
        
            case 'tachycardia':
                heart_rate = random.randint(110,130)
                systolic = random.randint(120,130)
                diastolic = random.randint(80,90)
                oxygen = round(random.uniform(95.0,97.00),2)
        
            case 'myocardia infarction':
                heart_rate = random.randint(70,80)
                systolic = random.randint(120,160)
                diastolic = random.randint(70,80)
                oxygen = round(random.uniform(92.0,95.00),2)   
            
            case 'recovery':
                heart_rate = random.randint(70,80)
                systolic = random.randint(110,120)
                diastolic = random.randint(70,80)
                oxygen = round(random.uniform(96.0,99.00),2)
            case 'heart failure':
                heart_rate = 0
                systolic = 0
                diastolic = 0
                oxygen = round(random.uniform(85.00,90.00),2)
        return heart_rate


    
    # Create a function to initialize the plot
    def init():
        line.set_data([], [])
        return line,

# Create a function to update the plot
    def update(frame):
        condition='normal'
        if frame % reset_frame_interval == 0:
            x_data.clear()
            y_data.clear()
        heart_rate = generate_heart_rate_data(condition)
        x_data.append(frame)
        y_data.append(heart_rate)
        line.set_data(x_data, y_data)
        ax.relim()
        ax.autoscale_view()
        return line,

# Define the maximum frame and the frame to reset at
    max_frame = 100
    reset_frame_interval = 99

# Create a figure and an axis
    fig, ax = plt.subplots()
    plt.title('Heart Rate Monitor')
    plt.xlabel('Time')
    plt.ylabel('Heart Rate (bpm)')
    plt.ylim(0, 150)
    plt.xlim(0, max_frame)

# Initialize empty data
    x_data = []
    y_data = []


# Create a line plot
    line, = ax.plot([], [], lw=2)

# Create the animation
    ani = animation.FuncAnimation(fig, update, frames=max_frame, init_func=init, blit=True)


    plt.show()
    
def makebeep():
    bpm = 80
    duration = int(40000 / bpm)
    num_beats = 100
    
    for _ in range(num_beats):
         winsound.Beep(1000, duration)
         time.sleep(duration / 1000.0)
         #os.system(f'beep -f 1000 -l {duration}') linux version
         #time.sleep(duration / 1000.0) linux version

animation_thread = threading.Thread(target=start_animation)
beep_thread = threading.Thread(target=makebeep)
animation_thread.start()
beep_thread.start()

animation_thread.join()
beep_thread.join()





    
        
    

#
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

#set up a list to store the ranges
#   O2, Heart Rate, BP
#  Set up a while true loop
#   Set up a function that changes the values 
        # Increase HR 
            # Account for change in O2 and HR

#Verion 2.0:
    # Add While True
        #Time out to update every 3 minutes
    # Add logging
        # Comments indicating connections opening and closing 
    # Add pygame 
        # Add graphics and sounds
    # Deploy to RPI Image
 #Version 3.0:
    # Add 
