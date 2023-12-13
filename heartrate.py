import pygame
import winsound
from datetime import datetime, timedelta
import time
import mysql.connector
import threading
import random


# The end result should be two distinct lines that appear on a black screen; one blue and one green
# The green line should resemble a heartrate and appear approximately 2/3rd from the bottom. The Blue line should resemble a series of waves and appear at the bottom 1/3rd
# Lines should begin a the right most part of the screen and terminate at approximately 80% the width of the screen, a new iteration of said line should appear 
# Both lines should have a "fade out effect" where they slowly fade out into the background so the new iteration of the line does not write over the previous line
# Lines should continue to run until the program is terminated
# Numbers resembling pulse, blood pressure, and 02 should appear on the right 1/5 of the screen
# Numbers should dynamically update every 15 seconds
# A distinct beeping sound, resembling a heart rate monitor should play 
# This beep should repeat every second until the program is terminated
# Once started, a connection should be opened to the patient database where patient stats will be logged
# The visual, beeping, and database are all handled through distinct threads to prevent collision.

#Starts the heart rate monitor visual using pygame library
def heartrateVisual():
    #Boilerplate pygame initializaition
    pygame.init()

        #Sets Display width and height in pixels
    size = (1200,800)
    monitor_screen = pygame.display.set_mode(size, flags=pygame.NOFRAME)
    pygame.display.set_caption("Patient Heart Rate")
    
        #Defines fonts and colors to be used in visual  
    font = pygame.font.Font('freesansbold.ttf',50)
    bpfont = pygame.font.Font('freesansbold.ttf',28)
    red = (255,14,14,255)
    black = (0,0,0,255)
    green =(61,183,33,255)
    blue = (0,0,255,255)
        #Set to dynamically update the numbers in the visual every 15 seconds
    def patient_stats():
        global hr,sys, dia, ox
        while True:
            hr= random.randint(70,80)
            sys = random.randint(110,120)
            dia = random.randint(70,80)
            ox = round(random.uniform(97.00,99.00),2)
            time.sleep(15)
        # Dynamic updates happen as a separate thread to avoid interfering with line visuals
    threading.Thread(target=patient_stats,daemon=True).start()

        # Drawing a nested display to get the fade out effect
    drawing = pygame.Surface(size, flags=pygame.SRCALPHA)
    drawing.fill((0,0,0,255))
    alpha_surf = pygame.Surface(size,flags=pygame.SRCALPHA)
    alpha_surf.fill((0,0,0,80))

        #location tracking values in pixels, variables track speed and position via pointer "ptr"
    
    speed = 5
    ptr= -1
    brptr =-1
    last_height = size[1] //3
    last_breath_height = size[1]*.75
    
        #Keeps track of the breath and pulse effect within the lines, manages the timing of their appearance
    pulse_part = [0,1,0,0,6,0,-5,0,0,-1,0,0,2,0]
    breath_part = [0,1,2,3,4,5,6,7,8,9,9,10,10,10,10,9,9,8,7,6,5,4,3]
    breath_position = -1
    pulse_position = -1
    vert_scale_factor = 10
    time_between_pulse = timedelta(milliseconds=750)
    time_between_breaths = timedelta(milliseconds=1150)
    last_time_triggered= datetime.now()
    last_breath = datetime.now()
    # Standard boilerplate for PyGame
    alive = True

    # Main Loop#
    while alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                alive = False
            elif event.type == pygame.KEYDOWN:
                print("Exiting")
                pygame.display.quit()
                alive=False
        
        #Pulse text management
        hrtext = font.render(f'Pulse {hr}', True, green, black) 
        hrtext_display = hrtext.get_rect()
        hrtext_display.center = (size[0]*.9,size[1]*.33)
        
        #Blood Pressure text management
        bptext = bpfont.render(f'BP {sys}/{dia}', True, red, black) 
        bptext_display = bptext.get_rect()
        bptext_display.center = (size[0]*.9,size[1]//2)
        
        #O2Sat text management
        oxtext = font.render(f'O2 {ox} ', True, blue, black) 
        oxtext_display = oxtext.get_rect()
        oxtext_display.center = (size[0]*.9,size[1]*.75)
        clock = pygame.time.Clock()    
        
        # Manages the movement and height of the pointer for pulse line
        next_ptr = ptr+speed
        next_breathptr = brptr + speed 
        now = datetime.now()
        if now - last_time_triggered > time_between_pulse:
            last_time_triggered = now
            pulse_position = 0

        if pulse_position >= 0:
            if pulse_position >= len(pulse_part):
                pulse_position = -1
                next_height = size[1] //3
            else:
                next_height = (size[1] //3 ) - (pulse_part[pulse_position] * vert_scale_factor)
                pulse_position +=1
        else:
            next_height = last_height
        
        # Manages the movement and height of the pointer for breath line
        if now - last_breath > time_between_breaths:
            last_breath = now
            breath_position = 0

        if breath_position >= 0:
            if breath_position >= len(breath_part):
                breath_position = -1
                next_breath_height = size[1] *.75
            else:
                next_breath_height = (size[1] *.75) - (breath_part[breath_position] * vert_scale_factor)
                breath_position += 1
        else:
            next_breath_height = last_breath_height


        # Tells PyGame to instatiate the lines with the behavior we have previously defined.
        drawing.blit(alpha_surf, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
        pygame.draw.line(drawing,green,(ptr,last_height),(next_ptr,next_height),4)
        pygame.draw.line(drawing,blue,(brptr,last_breath_height),(next_breathptr,next_breath_height),4)
        # Renders our content on the screen
        monitor_screen.blit(drawing,(0,0))
        monitor_screen.blit(hrtext,hrtext_display)
        monitor_screen.blit(bptext,bptext_display)
        monitor_screen.blit(oxtext,oxtext_display)
        #standard boilerplate, lines and text will not render without this.
        pygame.display.flip()
        # Determines when lines will end and reset.        
        if next_ptr > size[0]*0.8:
            ptr= 0
        else:
            ptr=next_ptr
        last_height= next_height

        if next_ptr > size[0]*0.8:
            brptr= 0
        else:
            brptr=next_breathptr
        last_breath_height= next_breath_height
        #Determines framerate
        clock.tick(30) 

# Uses Windows OS to produce the beep 
def makebeep():
    bpm = 80
    duration = int(40000 / bpm)
     # Runs continuously while program is running
    while True:
        winsound.Beep(1000, duration)
        time.sleep(duration / 1000.0)
        
    
# creating connection object and populating table with patient stats
def addToDB():
    heart_rate= random.randint(70,80)
    systolic = random.randint(110,120)
    diastolic = random.randint(70,80)
    oxygen = round(random.uniform(96.0,99.00),2)  
    stats = [heart_rate,systolic,diastolic,oxygen]
    
    mydb = {
    'host' : "10.1.2.8",
    'user' : "root",
    'password' : "jacaladmin",
    'database' : "hospital_info"}
    
    try:
        conn = mysql.connector.connect(**mydb)
        print("Connection opened")
        cursor = conn.cursor()
        cursor.callproc("sp_addstats",args=stats)
        print("Patient stats logged")
        conn.commit()
    except mysql.connector.Error as err:
        print(err)
    finally:
        conn.close()


if __name__ == "__main__":
    try:
        db_thread =threading.Thread(target=addToDB)
        animation_thread = threading.Thread(target=heartrateVisual)
        beep_thread = threading.Thread(target=makebeep)

        #Start Threads
        db_thread.start()
        animation_thread.start()
        beep_thread.start()

        #Join Threads
        db_thread.join()
        animation_thread.join()
        beep_thread.join()
    except Exception as e:
        print(e)



