#ATTRIBUTE: TUTORIAL From InvalidEntry
import pygame
import winsound
from datetime import datetime, timedelta
import time
import mysql.connector
import threading
import random
import math

def heartrateVisual():
# Initialize Pygame
    pygame.init()

    #Sets Display width and height in pixels
    size = (1200,800)
    monitor_screen = pygame.display.set_mode(size, flags=pygame.NOFRAME)
    pygame.display.set_caption("Patient Heart Rate")
    
    #Font Ovelays
    font = pygame.font.Font('freesansbold.ttf',50)
    bpfont = pygame.font.Font('freesansbold.ttf',28)
    red = (255,14,14,255)
    black = (0,0,0,255)
    green =(61,183,33,255)
    blue = (0,0,255,255)
       #BPM
    hrtext = font.render('Pulse 60', True, green, black) 
    hrtext_display = hrtext.get_rect()
    hrtext_display.center = (size[0]*.9,size[1]*.33)
        #Blood Pressure
    bptext = bpfont.render('BP 120/80', True, red, black) 
    bptext_display = bptext.get_rect()
    bptext_display.center = (size[0]*.9,size[1]//2)
        #O2Sat
    oxtext = font.render('O2 90.0', True, blue, black) 
    oxtext_display = oxtext.get_rect()
    oxtext_display.center = (size[0]*.9,size[1]*.75)
    clock = pygame.time.Clock()
    alive = True

    # Drawing a nested display to get the fade out effect
    drawing = pygame.Surface(size, flags=pygame.SRCALPHA)
    drawing.fill((0,0,0,255))
    alpha_surf = pygame.Surface(size,flags=pygame.SRCALPHA)
    alpha_surf.fill((0,0,0,80))

    #location tracking values in pixels
    speed = 5
    #pointer
    ptr= -1
    last_height = size[1] //3 
    # OG : pulse_part = [0,1,0,0,6,0,-5,0,0,-1,0,0,2,0]
    #pulse tracker
    pulse_part = [0,1,0,0,6,0,-5,0,0,-1,0,0,2,0]
    pulse_position = -1
    vert_scale_factor = 10

    time_between_pulse = timedelta(milliseconds=750)
    last_time_triggered= datetime.now()


    # Main Loop#
    while alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                alive = False
            elif event.type == pygame.KEYDOWN:
                print("Exiting")
                pygame.display.quit()
                alive=False
        
        next_ptr = ptr+speed

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
        


        drawing.blit(alpha_surf, (0,0), special_flags=pygame.BLEND_RGBA_MULT)

        pygame.draw.line(drawing,green,(ptr,last_height),(next_ptr,next_height),4)
        # Increments pointer to the end of the screen and resets the line to 0 pixels on x axis
        
        monitor_screen.blit(drawing,(0,0))
        monitor_screen.blit(hrtext,hrtext_display)
        monitor_screen.blit(bptext,bptext_display)
        monitor_screen.blit(oxtext,oxtext_display)
        pygame.display.flip()
        
        if next_ptr > size[0]*0.8:
            ptr= 0
        else:
            ptr=next_ptr
        last_height= next_height
        clock.tick(30) 


def makebeep():
    bpm = 80
    duration = int(40000 / bpm)
        
     
    while True:
        winsound.Beep(1000, duration)
        time.sleep(duration / 1000.0)
        
    
def addToDB():
     # creating connection object and passing the values
    heart_rate= random.randint(70,80)
    systolic = random.randint(110,120)
    diastolic = random.randint(70,80)
    oxygen = round(random.uniform(96.0,99.00),2)  
    stats = [heart_rate,systolic,diastolic,oxygen]
    
    mydb = {
    'host' : "localhost",
    'user' : "root",
    'password' : "password",
    'database' : "patient_monitor"}
    
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



heartrateVisual()

#db_thread =threading.Thread(target=addToDB)
#animation_thread = threading.Thread(target=heartrateVisual)
#beep_thread = threading.Thread(target=makebeep)

#Start Threads
#db_thread.start()
#animation_thread.start()
#beep_thread.start()

#Join Threads
#db_thread.join()
#animation_thread.join()
#beep_thread.join()




#def generate_heart_rate_data(condition):
# match condition:
#     case 'normal':
#         heart_rate= random.randint(70,80)
#         systolic = random.randint(110,120)
#         diastolic = random.randint(70,80)
#         oxygen = round(random.uniform(96.0,99.00),2)      
# 
#     case 'tachycardia':
#         heart_rate = random.randint(110,130)
#         systolic = random.randint(120,130)
#         diastolic = random.randint(80,90)
#         oxygen = round(random.uniform(95.0,97.00),2)
# 
#     case 'myocardia infarction':
#         heart_rate = random.randint(70,80)
#         systolic = random.randint(120,160)
#         diastolic = random.randint(70,80)
#         oxygen = round(random.uniform(92.0,95.00),2)   
#     
#     case 'recovery':
#         heart_rate = random.randint(70,80)
#         systolic = random.randint(110,120)
#         diastolic = random.randint(70,80)
#         oxygen = round(random.uniform(96.0,99.00),2)
#     case 'heart failure':
#         heart_rate = 0
#         systolic = 0
#         diastolic = 0
#         oxygen = round(random.uniform(85.00,90.00),2)
# return heart_rate