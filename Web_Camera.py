import argparse
import datetime as dt
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import pickle
import tkinter as tk
from datetime import date, datetime

import cv2
import face_recognition
import numpy as np
import PIL
from PIL import Image, ImageTk
from tensorflow import *
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array


class Video:
    def __init__(self,selfvideo_source=0, vid_typ:str="", face_recog:bool=False):
        win = tk.Toplevel()
        self.root = win
        self.root.title("window_title")
        self.video_source = 0
        self.ok=False
        self.vid_typ = vid_typ
        self.is_facerecogntion=face_recog
        #timer
        self.timer=ElapsedTimeClock(self.root)

        # open video source (by default this will try to open the computer webcam)
        self.vid = VideoCapture(self.video_source,vid_typ=self.vid_typ,face_recog=self.is_facerecogntion)

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(self.root, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        Image_Capture = ImageTk.PhotoImage(Image.open("Image_Capture.ico"))
        self.btn_snapshot=tk.Button(self.root,image=Image_Capture ,text="Snapshot", command=self.snapshot)
        self.btn_snapshot.pack(side=tk.LEFT)

        #video control buttons
        player_record = ImageTk.PhotoImage(Image.open("player_record.ico"))
        self.btn_start=tk.Button(self.root, text='START',image=player_record, command=self.open_camera)
        self.btn_start.pack(side=tk.LEFT)

        stop_play = ImageTk.PhotoImage(Image.open("stop_play.ico"))  
        self.btn_stop=tk.Button(self.root, text='STOP',image=stop_play, command=self.close_camera)
        self.btn_stop.pack(side=tk.LEFT)

        # quit button
        quit_ico = ImageTk.PhotoImage(Image.open("quit_ico.ico"))
        self.btn_quit=tk.Button(self.root, text='QUIT',image=quit_ico, command=self.vid.__del__)
        self.btn_quit.pack(side=tk.LEFT)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay=10
        self.update()
        self.root.mainloop()
        
        
    def snapshot(self):
        # Get a frame from the video source
        ret,frame=self.vid.get_frame()

        if ret:
            today = date.today()
            path='./images'
            cur_time = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            print(cv2.imwrite(os.path.join(path , cur_time+".jpg"),cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)))

    def open_camera(self):
        self.ok = True
        self.timer.start()
        print("camera opened => Recording")



    def close_camera(self):
        self.ok = False
        self.timer.stop()
        print("camera closed => Not Recording")

       
    def update(self):

        # Get a frame from the video source
        try:
            ret, frame = self.vid.get_frame()
            if self.ok:
                self.vid.out.write(cv2.cvtColor(frame,cv2.COLOR_RGB2BGR))

            if ret:
                self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
                self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
            self.root.after(self.delay,self.update)
        except AttributeError:
            print("video stoped")

class VideoCapture:
    def __init__(self,video_source=0,vid_typ:str="",face_recog:bool=False):
        # Open the video source
        self.vid_typ=vid_typ
        self.is_facerecogntion=face_recog
        self.vid = cv2.VideoCapture(video_source,cv2.CAP_DSHOW)
        self.cascPath = "haarcascade_frontalface_alt2.xml"
        self.faceCascade = cv2.CascadeClassifier(self.cascPath)
        self.model = load_model("mask_recog.h5")
        
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Command Line Parser
        args=CommandLineParser().args

        
        #create videowriter

        # 1. Video Type
        VIDEO_TYPE = {
            'avi': cv2.VideoWriter_fourcc(*'XVID'),
            #'mp4': cv2.VideoWriter_fourcc(*'H264'),
            'mp4': cv2.VideoWriter_fourcc(*'XVID'),
        }

        self.fourcc=VIDEO_TYPE[args.type[0]]

        # 2. Video Dimension
        STD_DIMENSIONS =  {
            '480p': (640, 480),
            '720p': (1280, 720),
            '1080p': (1920, 1080),
            '4k': (3840, 2160),
        }
        vid_path = './videos'
        cur_time = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        res=STD_DIMENSIONS[args.res[0]]
        print(args.name,self.fourcc,res)
        self.out = cv2.VideoWriter(vid_path+'/'+cur_time+'.'+args.type[0],self.fourcc,10,res)

        #set video sourec width and height
        self.vid.set(3,res[0])
        self.vid.set(4,res[1])

        # Get video source width and height
        self.width,self.height=res

        

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                if(self.vid_typ.__eq__("Normal Camera")):
                    return (ret, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                elif(self.vid_typ.__eq__("Mask Detctor")):    
                    # Return a boolean success flag and the current frame converted to BGR
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = self.faceCascade.detectMultiScale(frame,1.1,4)
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    faces_list=[]
                    preds=[]
                    for (x, y, w, h) in faces:
                        face_frame = frame[y:y+h,x:x+w]
                        face_frame = cv2.cvtColor(face_frame, cv2.COLOR_BGR2RGB)
                        face_frame = cv2.resize(face_frame, (224, 224))
                        face_frame = img_to_array(face_frame)
                        
                        face_frame =  preprocess_input(face_frame)
                        face_frame = np.expand_dims(face_frame, axis=0)
                        (mask, withoutMask) = self.model.predict(face_frame)[0]

                        label = "Mask" if mask > withoutMask else "No Mask"
                        color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
                        label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)
                        cv2.putText(frame, label, (x, y- 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)

                        name = ""
                        if(self.is_facerecogntion):
                            
                            name = self.getFaceRecognation(frame,'face_enc')    
                        #face recognation 
                        cv2.putText(frame, name , (x+50 , y - 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                
                        cv2.rectangle(frame, (x, y), (x + w, y + h),color, 2)
                        # Display the resulting frame
                    return (ret, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

            else:
                return (ret, None)
        
    def getFaceRecognation(self, frame,typ):
        data = pickle.loads(open(typ, "rb").read())
        # the facial embeddings for face in input
        encodings = face_recognition.api.face_encodings(frame, known_face_locations=None, num_jitters=2,model='small')
        names = []
        name = "Unknown"
        # loop over the facial embeddings incase
        # we have multiple embeddings for multiple fcaes
        for encoding in encodings:
            #Compare encodings with encodings in data["encodings"]
            #Matches contain array with boolean values and True for the embeddings it matches closely
            #and False for rest
            matches = face_recognition.compare_faces(data["encodings"],
            encoding)
            #set name =inknown if no encoding matches
            # check to see if we have found a match
            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    #Check the names at respective indexes we stored in matchedIdxs
                    name = data["names"][i]
                    #increase count for the name we got
                    counts[name] = counts.get(name, 0) + 1
                    #set name which has highest count
                    name = max(counts, key=counts.get)
                    names.append(name)
                    return name    
            return name    
        return name
     
    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
            self.out.release()
            cv2.destroyAllWindows()


class ElapsedTimeClock:
    def __init__(self,root):
        self.T=tk.Label(root,text='00:00:00',font=('times', 20, 'bold'), bg='green')
        self.T.pack(fill=tk.BOTH, expand=1)
        self.elapsedTime=dt.datetime(1,1,1)
        self.running=0
        self.lastTime=''
        t = 10
        self.zeroTime = dt.timedelta(hours=10, minutes=10, seconds=10)
        # self.tick()

 
    def tick(self):
        # get the current local time from the PC
        self.now = dt.datetime(1, 1, 1).now()
        self.elapsedTime = self.now - self.zeroTime
        self.time2 = self.elapsedTime.strftime('%H:%M:%S')
        # if time string has changed, update it
        if self.time2 != self.lastTime:
            self.lastTime = self.time2
            self.T.config(text=self.time2)
        # calls itself every 200 milliseconds
        # to update the time display as needed
        # could use >200 ms, but display gets jerky
        self.updwin=self.T.after(100, self.tick)


    def start(self):
            if not self.running:
                self.zeroTime=dt.datetime(1, 1, 1).now()-self.elapsedTime
                self.tick()
                self.running=1

    def stop(self):
            if self.running:
                self.T.after_cancel(self.updwin)
                self.elapsedTime=dt.datetime(1, 1, 1).now()-self.zeroTime
                self.time2=self.elapsedTime
                self.running=0


class CommandLineParser:
    
    def __init__(self):

        # Create object of the Argument Parser
        parser=argparse.ArgumentParser(description='Script to record videos')

        # Create a group for requirement 
        # for now no required arguments 
        # required_arguments=parser.add_argument_group('Required command line arguments')

        # Only values is supporting for the tag --type. So nargs will be '1' to get
        parser.add_argument('--type', nargs=1, default=['avi'], type=str, help='Type of the video output: for now we have only AVI & MP4')

        # Only one values are going to accept for the tag --res. So nargs will be '1'
        parser.add_argument('--res', nargs=1, default=['480p'], type=str, help='Resolution of the video output: for now we have 480p, 720p, 1080p & 4k')

        # Only one values are going to accept for the tag --name. So nargs will be '1'
        parser.add_argument('--name', nargs=1, default=['output'], type=str, help='Enter Output video title/name')

        # Parse the arguments and get all the values in the form of namespace.
        # Here args is of namespace and values will be accessed through tag names
        self.args = parser.parse_args()
