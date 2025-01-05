import subprocess
import os
import signal
import json
import glob
import multiprocessing
import time
import pygetwindow
from tkinter import *
import speech_recognition as sr
from word2number import w2n
from PIL import ImageGrab, Image
import torch
import os.path
import numpy as np
import requests
from io import BytesIO
from diffusers import StableDiffusionImg2ImgPipeline
outputpath = r'C:\Users\ctawo\OneDrive\Desktop\OpenposeOutput\\'
destroyfiles = glob.glob(outputpath+r'*')
for f in destroyfiles:
    os.remove(f)
r = sr.Recognizer()
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'brown', 'white', 'black', 'gray']
drawlist = ['begin', 'stop']
linecolor = 'black'
drawing = 'stop'
thickness = '1'
done = 'no'
if os.path.exists("enhanced-image.png"):
    os.remove("enhanced-image.png")
f = open("commands.txt", "w+")
f.truncate(0)
f.write(linecolor + '\n')
f.write(drawing + '\n')
f.write(thickness + '\n')
f.write(done + '\n')
f.flush()
f.close()
f = open("check.txt", "w+")
f.truncate(0)
f.flush()
f.close()
f = open("description.txt", "w+")
f.truncate(0)
f.flush()
f.close()
f = open("whentotalk.txt", "w+")
f.truncate(0)
f.flush()
f.close()
f = open("prompt.txt", "w+")
f.truncate(0)
f.flush()
f.close()

def imagetoimage():
    # load the pipeline

    device = "cuda"
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16).to(
        device
    )

    # let's download an initial image
    # url = r"C:\Users\ctawo\OneDrive\Desktop\ScienceResearch\image.png"
    #
    # response = requests.get(url)
    init_image = Image.open(r"C:\Users\ctawo\OneDrive\Desktop\ScienceResearch\image.png").convert("RGB")
    init_image.thumbnail((768, 768))
    with open("prompt.txt") as f:
        promptreadlines = f.readlines()
    prompt = promptreadlines[0].strip()

    images = pipe(prompt=prompt, image=init_image, strength=0.75, guidance_scale=7.5).images

    images[0].save("enhanced-image.png")

def getter(widget):
    x=widget.winfo_rootx()+widget.winfo_x()
    y=widget.winfo_rooty()+widget.winfo_y()
    x1=x+widget.winfo_width()
    y1=y+widget.winfo_height()
    ImageGrab.grab().crop((x,y-240,x1,y1-240)).save(r"C:\Users\ctawo\OneDrive\Desktop\ScienceResearch\image.png")

from subprocess import Popen, PIPE
def openpose(conn):

    os.chdir(r'C:\Users\ctawo\OneDrive\Desktop\OpenPose\openpose-1.7.0-binaries-win64-gpu-python3.7-flir-3d_recommended\openpose')
    #subprocess.call(['bin\OpenPoseDemo.exe', '--write_json', r'C:\Users\ctawo\OneDrive\Desktop\OpenposeOutput', '--frame_flip'], shell=True)
    openposeprocess = Popen(['bin\OpenPoseDemo.exe', '--write_json', r'C:\Users\ctawo\OneDrive\Desktop\OpenposeOutput', '--frame_flip'],stdout=PIPE, stderr=PIPE)
    while len(os.listdir(outputpath)) == 0:
        pass
    os.chdir(r'C:\Users\ctawo\OneDrive\Desktop\ScienceResearch')
    while True:
        if os.path.getsize("check.txt") > 0:
            openposeprocess.kill()
global loop
loop = 0
def output():
    xpos = 0
    ypos = 0
    global loop
    while len(os.listdir(outputpath)) == 0:
        pass
    while True:
        loop+=1
        # print(loop)
        if loop == 1:
            win = pygetwindow.getWindowsWithTitle('Openpose 1.7.0')[0]
            win.size = (650, 384)
            win.moveTo(1150, 500)
        files = glob.glob(outputpath + r'*')
        latestfile = max(files, key=os.path.getctime)
        with open(latestfile, 'r') as j:
            data = json.loads(j.read())
        people = data["people"]
        if len(people) == 1:
            keypoints = people[0]
            pk2 = keypoints.get("pose_keypoints_2d")
            # print(pk2[21], pk2[22])
            xpos = pk2[21]
            ypos = pk2[22]
            return xpos, ypos
        else:
            pass
        j.close()
        time.sleep(0.1)

def draw():
    global linecolor
    master = Tk()
    w = Canvas(master, width=1000, height=300)

    w.grid_propagate(False)
    w.pack_propagate(0)
    master.geometry("+145+90")
    iconimg = PhotoImage(file="icon.png")
    icon = Label(master, image=iconimg)
    instructions = Button(master, text="When finished, say \"save the drawing\" \n Use any voice command if needed \n Putting voice commands in a sentence can help if not working", bg="green", fg="white", font=(None, 15))
    instructions.pack()
    # text = Button(master,
    #              text="", highlightthickness = 0, bd = 0, font=(None, 20))
    # text.pack(side=TOP)
    confirm = Button(master,
                  text="", highlightthickness=0, bd=0, font=(None, 20))
    confirm.pack()
    talk = Button(master,
                  text="")
    talk.pack(side=TOP)

    text = Button(master,
                  text="")
    text.pack(side=TOP)
    w.pack()
    voicecommands = Button(master,
                           text="List of Voice Commands: \n Change color: Red, Orange,\n Yellow, Green,\n Blue, Purple,\n Black, White,\n Gray, Brown,\n Pink \n Stop Drawing: Stop \n Resume Drawing: Begin \n Finish Drawing: Save",
                           bg="yellow", fg="black", font=(None, 10))
    voicecommands.pack(side=RIGHT)
    done_finished = False
    global repeat
    repeat = 0
    def line():
        if not os.path.exists("enhanced-image.png"):
            finished = ''
            xpos, ypos = output()
            while len(os.listdir(outputpath)) == 0:
                pass
            try:
                draw.counter += 1
            except AttributeError:
                draw.counter = 1
            # print("line counter is: %s" % draw.counter)
            if draw.counter == 1:
                global firstx
                global firsty
                global secondx
                global secondy
                global linecolor
                global repeat
                firstx = 0
                firsty = 0
                secondx = 0
                secondy = 0
            if xpos != 0 and ypos != 0:  # make sure there is a real keypoint
                if firstx == 0:
                    firstx = xpos
                if firsty == 0:
                    firsty = ypos
                if firstx != 0 and firstx != xpos:
                    secondx = firstx
                    firstx = xpos
                if firsty != 0 and firsty != ypos:
                    secondy = firsty
                    firsty = ypos
            if (0, 0) != (secondx, secondy):
                with open("commands.txt") as f:
                    commands = f.readlines()
                colordeline = commands[0].strip()
                startorstop = commands[1].strip()
                thickness = commands[2].strip()
                finished = commands[3].strip()
                if finished == 'yes':
                    repeat += 1
                    if repeat == 1:
                        f = open("check.txt", "w")
                        f.write("kill")
                        f.close()

                        talk.pack_forget()
                        voicecommands.pack_forget()
                        getter(w)
                        w.delete('all')
                        f = open("description.txt", "w+")
                        f.truncate(0)
                        f.flush()
                        f.close()
                        print("repeated once")
                    with open("description.txt") as f:
                        description = f.readlines()
                    if len(description) > 0:
                        confirm.config(text="Confirm the prompt? Use voice command confirm to confirm it", bg="orange", fg="black", highlightthickness=1, bd=1)
                        confirm.pack()
                    text.config(text=description, bg="blue", fg="white", highlightthickness = 1, bd = 1, font=(None, 20))
                    text.pack()
                    text.pack(side=TOP)
                    instructions.config(text="Describe out loud what you have drawn and you can add any extra descriptions for the enhancer to add", bg="red")
                    instructions.pack()
                    with open("whentotalk.txt") as f:
                        whentotalk = f.readlines()
                    talk.config(text=whentotalk, bg="yellow", fg="black", highlightthickness=1, bd=1)
                    talk.pack()

                    # getter(w)
                    # imagetoimage()
                    # photo = PhotoImage(file="enhanced-image.png")
                    # image = Label(image=photo)
                    # image.pack()
                    # w.pack()
                else:
                    with open("description.txt") as f:
                        description = f.readlines()
                    # text.config(text=description, bg="blue", fg="white", highlightthickness = 1, bd = 1)
                    # text.pack()
                    with open("whentotalk.txt") as f:
                        whentotalk = f.readlines()
                    talk.config(text=whentotalk, bg="yellow", fg="black", highlightthickness=1, bd=1)
                    talk.pack()
                    if startorstop == 'begin':
                        w.create_line(firstx/2+200, firsty/2, secondx/2+200, secondy/2, fill=colordeline, width=10)
                        icon.place(x=-100, y=-100)
                    if startorstop == 'stop':
                        icon.place(x=secondx/2+200, y=secondy / 2 +200)
            w.after(10, line)
            # talk.pack_forget()
            # instructions.pack_forget()
            # confirm.pack_forget()
            # text.pack_forget()
            # time.sleep(2)
            # displayimg = PhotoImage(file='enhanced-image.png')
            # display.config(image=displayimg)
            # display.pack(side=TOP)
            # print("sleeping")
            # time.sleep(10)
            # print("sleep done")
            # from PIL import Image
            # im = Image.open('enhanced-image.png')
            # im.show()


    line()
    global repeat2
    repeat2 = 0
    def check():
        global repeat2
        if os.path.exists("enhanced-image.png"):
            print("Exists")
            print(time.time() - os.path.getctime("enhanced-image.png"))
            print(time.time())
            print(os.path.getctime("enhanced-image.png"))
            if time.time() - os.path.getctime("enhanced-image.png") > 2 and repeat2 == 0:
                repeat2+=1
                w.theimage = PhotoImage(file="enhanced-image.png")
                display = Button(master, image=w.theimage)
                display.pack()
                print("waited 2 secs")
                img = Image.open("aaaaa.png")
                numpy_array = np.array(img)
                print(numpy_array[:,:,0:3].sum()/numpy_array.shape[0]/numpy_array.shape[1]/3)
                # if numpy_array[:,:,0:3].sum()/numpy_array.shape[0]/numpy_array.shape[1]/3 < 1:
                #     repeat2 = 0
                #     print("resetted repeat")
                #     imagetoimage()
                #     if os.path.exists("enhanced-image.png"):
                #         os.remove("enhanced-image.png")


        w.after(400,check)
    check()
    w.mainloop()
def voice_recognition():
    global linecolor
    global drawing
    global thickness
    global done
    while True:
        if os.path.exists("enhanced-image.png"):
            break
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            print("Say something!")
            f = open("whentotalk.txt", "w")
            f.write("Say something")
            f.flush()
            f.close()
            audio = r.listen(source)
            f = open("whentotalk.txt", "w")
            f.write("Processing...")
            f.flush()
            f.close()

        # recognize speech using Google Speech Recognition
        try:
            sound = r.recognize_google(audio)
            sounder = sound.split()
            for i in range(len(sounder)):
                if sounder[i].lower() in colors:
                    linecolor = sounder[i]
                    print("changed to orange")
                if sounder[i].lower() in drawlist:
                    drawing = sounder[i]
                if sounder[i].lower() == 'save' and done != 'yes':
                    done = 'yes'
                if done == 'yes' and sounder[i].lower()=='confirm' or done =='yes' and sounder[i].lower()=='confirmed':
                    with open("description.txt") as g:
                        description = g.readlines()
                    description = str(description)
                    description = description[:-1]
                    description = description[1:]
                    print(description)
                    print(type(description))
                    f = open('prompt.txt', 'w')
                    f.write(description)
                    f.flush()
                    f.close()
                    f = open('completelyfinished.txt', 'w')
                    f.write('done')
                    f.flush()
                    f.close()
                    imagetoimage()
                try:
                    if w2n.word_to_num(sounder[i]) > 0 and w2n.word_to_num(sounder[i]) <= 10:
                        thickness = sounder[i]
                except:
                    pass
            f = open("description.txt", "w")

            f.write(sound)
            f.flush()
            f.close()

            print(linecolor)
            f = open("commands.txt", "w+")
            f.truncate(0)
            f.write(linecolor + '\n')
            f.write(drawing + '\n')
            f.write(thickness + '\n')
            f.write(done + '\n')
            f.flush()
            f.close()




        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            waveData = audio.get_wav_data()
            with open("failed.wav", "wb") as waveFile:
                #newFileByteArray = bytearray(waveData)
                waveFile.write(waveData)

        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
from multiprocessing import Process, Pipe
def main():
    parent_conn, child_conn = Pipe()
    run = Process(name='run', target=openpose, args=(child_conn,))
    runoutput = multiprocessing.Process(name='runoutput', target=output)
    drawer = multiprocessing.Process(name='drawer', target=draw)
    run.start()
    runoutput.start()
    drawer.start()
    #voice recognition
    voicerecognition = multiprocessing.Process(name='voicerecognition', target=voice_recognition())
    voicerecognition.start()

if __name__ == '__main__':
    main()
