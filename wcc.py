import tkinter as tk #for GUI
import RPi.GPIO as GPIO #for GPIO pins
import time
from time import sleep
import cv2
import platform  # For getting the operating system name
import subprocess  # For executing a shell command

# Providing easy names for GPIO pins
PWR = 20
HWRS = 21
LED = 16
HDD = 26

# GPIO Setup block. GPIO.BOARD seemed inconsistent. Switched to BCM.
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWR, GPIO.OUT)
GPIO.setup(HWRS, GPIO.OUT)
GPIO.setup(LED, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(HDD, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

main = tk.Tk()
main.title("WCC 1.0")
main.geometry("270x480")
main.configure(bg='#ffffff')

# Global States, colours, and other variables for easy access.
# PWR and HWRS States are set to the off position of the relay board. Diff HW may require 0.
PWR_State = 1
HWRS_State = 1
PWR_Time = 3
PWR_Time_Reset = 3
PWR_Time_On = 2
PWR_Time_Off = 5
Welshi_State = True
#PLED_State = True
#HDD_State = True
IPadd = '192.168.42.33'
# Colours
clrgrey = '#7d7d7d'
clrdarkgrey = '#666666'
clrgreen = '#42ad44'
clrred = '#b52828'
clrdarkred = '#318233'
clrblue = '#2761b3'
clrdarkblue = '#1b427a'


# Idea: Use motherboard LED, and or HDD LED fb to turn off the button once power is received.

PWR_Relay = tk.Label(main,
                     bg=clrgrey,
                     bd=0,
                     height=3,
                     width=2,)
PWR_Relay.place(x=20, y=40)

# Power Logic.
# Checks if Motherboard is on with the Power LED
# If on, changes hold timme of button for a hard shutdown.
# If off, changes to shorter time to restart. Holding will just turn the mobo off again.

def PWRbutton():
    global PWR_State
    global clrgrey
    global clrgreen
    #global PWR_Relay
    if GPIO.input(LED):
        PWR_Time = PWR_Time_Off
    else:
        PWR_Time = PWR_Time_On
    PWR_State = 0
    GPIO.output(PWR, PWR_State)
    #PWR_Relay.config(bg=clrgreen)
    print("Power Relay is On")
    time.sleep(PWR_Time)
    PWR_State = 1
    GPIO.output(PWR, PWR_State)
    #PWR_Relay.config(bg=clrgrey)
    print("Power Relay is Off")
    
# HWRS Logic - Turns relay on, indicates on GUI, holds for 3 sec, then resets.
def HWRSbutton():
    global HWRS_State
    global clrgrey
    global clrblue
    #global PWR_Relay    
    if GPIO.input(LED):
        PWR_Time = PWR_Time_Off
    else:
        PWR_Time = PWR_Time_On
    HWRS_State = 0
    GPIO.output(HWRS, HWRS_State)
    #PWR_Relay.config(bg=clrgreen)
    print("Reset Relay is On")
    time.sleep(PWR_Time)
    HWRS_State = 1
    GPIO.output(HWRS, HWRS_State)
    #PWR_Relay.config(bg=clrgrey)
    print("Reset Relay is Off")
        
# # Power LED fb colour change logic.
# def PLED():
#     #global PLED_State
#     if LED:
#         PLED.config(bg='#42ad44')
#     else:
#         PLED.config(bg='#b52828')
# 
# # HDD LED fb colour change logic.
# def HLED():
#     global HLED_State
#     if HDD:
#         HDDLED.config(bg='#42ad44')
#     else:
#         HDDLED.config(bg='#b52828')

        
#Entry field to insert new IP address variable.
IPChange = tk.Entry(main,
                    width=15)
IPChange.insert(10, IPadd)
IPChange.place(x=32, y=260)

#Changes IP address variable, and text based on text entry.
# Also resets colours for feedback-based variables.
def IP_CHANGE():
    global IPadd
    global clrgrey
    IPadd = IPChange.get()
    Pingtext.configure(text=IPadd)
    #host = IPadd
    PINGbutt.config(bg=clrgrey)
    Pingtext.config(fg=clrgrey)
    
# Button to enable change of IP address global variable.
IPCH_Butt = tk.Button(main,
                      text="Change IP",
                      font="Helvetica 9 bold",
                      bg=clrgrey,
                      fg="#ffffff",
                      activebackground=clrdarkgrey,
                      activeforeground="#ffffff",
                      bd=0,
                      height=1,
                      width=10,
                      command=IP_CHANGE)
IPCH_Butt.place(x=150, y=259)

# Displays IP Address at bottom of GUI
Pingtext = tk.Label(main,
                    text=IPadd,
                    font="Helvetica 12 bold",
                    bg='#ffffff',
                    fg=clrgrey)
Pingtext.place(x=76, y=226)

# Ping command. Determines OS to specify command to host OS.
# Problem: Bool True will still return in Windows since a response is provided at all. Other OS fine.
def PINGIT(host):
    param = '-n' if platform.system().lower()=='windows' else '-c'
    host = IPadd
    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '4', host]
    return subprocess.call(command) == 0    

# Change colour state of IP Address text based on ping result.
def PINGcolour():
    #global PINGColourCode
    if PINGIT(host=IPadd) == True:
        Pingtext.config(fg=clrgreen)
        #print("Green")
    else:
        Pingtext.config(fg=clrred)
        #print("Red")

# Ping GUI Button
PINGbutt = tk.Button(main,
                     text="Ping",
                     font="Helvetica 9 bold",
                     bg=clrgrey,
                     fg="#ffffff",
                     activebackground=clrdarkgrey,
                     activeforeground="#ffffff",
                     bd=0,
                     height=3,
                     width=10,
                     command=lambda: [PINGIT(host=IPadd), PINGcolour()])
PINGbutt.place(x=82, y=160)

# It's a bloody header
Header = tk.Label(main,
                  text="Welshi Control Centre",
                  font="Helvetica 12 bold",
                  bg="#ffffff")
Header.place(x=48, y=4)

# Power GUI Button
PWRbutt = tk.Button(main,
                    text="POWER",
                    font="Helvetica 9 bold",
                    bg=clrgreen,
                    fg="#ffffff",
                    activebackground=clrdarkred,
                    activeforeground="#ffffff",
                    bd=0,
                    height=3,
                    width=10,
                    command=PWRbutton)
PWRbutt.place(x=32, y=40)

# Hardware Reset GUI Button
HWRSbutt = tk.Button(main,
                     text="HW RESET",
                     font="Helvetica 9 bold",
                     bg=clrblue,
                     fg="#ffffff",
                     activebackground=clrdarkblue,
                     activeforeground="#ffffff",
                     bd=0,
                     height=3,
                     width=10,
                     command=HWRSbutton)
HWRSbutt.place(x=128, y=40)

# End program GUI Button. Almost 120% optional.
Exitbutton = tk.Button(main,
                       text="END",
                       font="Helvetica 9 bold",
                       bg=clrred,
                       fg="#ffffff",
                       activebackground=clrdarkred,
                       activeforeground="#ffffff",
                       bd=0,
                       height=3,
                       width=10,
                       command=main.destroy)
#Exitbutton.place(x=32, y=160)

# Power LED fb indicator from mobo.
PLED = tk.Label(main,
                text="P LED",
                font="Helvetica 9 bold",
                bg=clrgrey,
                fg="#ffffff",
                activebackground=clrdarkgrey,
                activeforeground="#ffffff",
                bd=0,
                height=3,
                width=10,
                )
PLED.place(x=46, y=100)

# HDD LED fb indicator from mobo.
HDDLED = tk.Label(main,
                text="HDD LED",
                font="Helvetica 9 bold",
                bg=clrgrey,
                fg="#ffffff",
                activebackground=clrdarkgrey,
                activeforeground="#ffffff",
                bd=0,
                height=3,
                width=10,
                )
HDDLED.place(x=142, y=100)

    
#
# Video Capture for USB-HDMI adapter to see screen.
# Truenas has a tendency to take down the web GUI if anything bad happens.
# But the terminal output is still useful in determining what went wrong.
# cap = cv2.VideoCapture(0)
# 
# def video_cap():
#     while(True):
#         global cap
#         # Capture frame-by-frame
#         ret,frame = cap.read()
#         cv2.rectangle(frame, (100, 100), (200, 200), [255, 0, 0], 1)
#         # Display the resulting frame
#         cv2.imshow('main',frame)
#         if cv2.waitKey(25) & 0xFF == ord('q'):
#             break

VideoButt = tk.Button(main,
                       text="Video",
                       font="Helvetica 9 bold",
                       bg=clrgrey,
                       fg="#ffffff",
                       activebackground=clrdarkgrey,
                       activeforeground="#ffffff",
                       bd=0,
                       height=3,
                       width=10,
                       command=video_cap)
VideoButt.place(x=32, y=160)


#

main.mainloop()
#cap.release()
#cv2.destroyAllWindows()

GPIO.cleanup()

