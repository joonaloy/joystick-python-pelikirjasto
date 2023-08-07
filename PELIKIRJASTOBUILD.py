import os
from tkinter import *
from tkinter import ttk
import subprocess
from functools import partial
import pygame
import sys
import threading
import wmi
import time

rootdir = r"C:\Users\arcade machine/Documents"
paths = []
executables = []
buttons = []
btnindexX = 0
btnindexY = 0
FoundGame = False
pygame.init()

joystick_count = pygame.joystick.get_count()

if joystick_count == 0:
    print("No joysticks detected.")
    sys.exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

# print("Joystick name: {}".format(joystick.get_name()))
# print("Number of axes: {}".format(joystick.get_numaxes()))
# print("Number of buttons: {}".format(joystick.get_numbuttons()))
def rungame(id):
    subprocess.Popen(paths[id])
def tkinter_loop():
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith('.exe') and file != "UnityCrashHandler64.exe" and file != "UnityCrashHandler32.exe" :
                paths.append(os.path.join(subdir, file))
                executables.append(file)
    # print(executables)
    # print(paths)

    root = Tk()
    root.geometry("500x500")
    root.attributes('-fullscreen', True)
    root.title("Pelikirjasto")
    frm = ttk.Frame(root, padding=20,)
    frm.grid()
    ttk.Label(frm,text="Pelikirjasto",padding=5,font=("Arial",14)).grid(column= 0,row=0)
    style = ttk.Style()
    style.configure("Yellow.TButton", background="red")

    
    for i in range(len(executables)):
        col = 0
        offset = 0
        if(i > 20):
            col += 2
            offset += 21
        lab = ttk.Label(frm, text=executables[i][0:-4],width=14,font=("Arial",11))
        lab.grid(column=col, row=i+1-offset)
        print(i+1-offset)
        but = ttk.Button(frm, text="Pelaa", command= partial(rungame,i),padding=3)
        but.grid(column=col+1, row=i+1-offset)
        buttons.append(but)
    # print("BUTTONIT:",buttons)
    buttons[0].configure(style="Yellow.TButton")
    root.mainloop()
def while_loop():
    global btnindexX
    global btnindexY
    global FoundGame
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                # print("Axis {} value: {}".format(event.axis, event.value))
                if event.axis == 0 and event.value > 0.9 and FoundGame == False:
                    btnindexX +=1
                    print("X:{} Y:{}".format(btnindexX,btnindexY))
                elif event.axis == 0 and event.value < -0.9 and FoundGame == False:
                    btnindexX -=1
                    print("X:{} Y:{}".format(btnindexX,btnindexY))
                elif event.axis == 1 and event.value < -0.9 and FoundGame == False:
                    btnindexY -=1
                    buttons[btnindexY+1].configure(style="")
                    buttons[btnindexY].configure(style="Yellow.TButton")
                    print("X:{} Y:{}".format(btnindexX,btnindexY))
                elif event.axis == 1 and event.value > 0.9 and FoundGame == False:
                    btnindexY +=1
                    buttons[btnindexY-1].configure(style="")
                    buttons[btnindexY].configure(style="Yellow.TButton")
                    print("X:{} Y:{}".format(btnindexX,btnindexY))
            elif event.type == pygame.JOYBUTTONDOWN and FoundGame == False:
                print("Button {} pressed.".format(event.button))
                if FoundGame == False:
                    buttons[btnindexY].invoke()
                    time.sleep(3)
                    print(FoundGame)
            elif event.type == pygame.JOYBUTTONUP and FoundGame == False:
                print("Button {} released.".format(event.button))
def process_loop():
    global FoundGame
    c = wmi.WMI()
    process_watcher = c.Win32_Process.watch_for("creation")
    FoundGame = False
    while True:
        new_process = process_watcher()
        print(new_process.Name)
        
        if(new_process.Name in executables):
            print("Peli Käynnistettiin "+ new_process.Name)
            FoundGame = True
            print(FoundGame)
            watcher = c.watch_for (
                notification_type = "Deletion",
                wmi_class = "Win32_Process",
                delay_secs = 1,
                ProcessId = new_process.ProcessId
            )
        
        if(FoundGame == True):
            watcher()
            FoundGame=False
            print("Peli Sammutettiin "+ new_process.Name)
            # en tiiä mitä tekee
            # process_id, result = c.Win32_Process.Create(
            #     CommandLine = "\"D:\\UnityProjektit\\WMItesti.exe\" "
            # )
tkinter_thread = threading.Thread(target=tkinter_loop)
tkinter_thread.start()
process_thread = threading.Thread(target=while_loop)
process_thread.start()
process_loop()