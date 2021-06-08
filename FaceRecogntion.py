import os
import pickle
import shutil
import tkinter as tk
# GUI
from tkinter import *
from tkinter import filedialog, ttk

import cv2
import face_recognition
import numpy as np
from imutils import paths
from PIL import Image, ImageTk
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array


class Window(Tk):
 
    #constructor
    def __init__(self):
        super(Window, self).__init__()
        
        self.title("Face Recogntion")
        self.minsize(800, 500)
     
        #background_image=tk.PhotoImage("shutter.png")
        self.img = ImageTk.PhotoImage(Image.open("shutter.png"))
        self.label = Label(self,image=self.img)
        self.label.place(x=0, y=0)         
        #self.wm_iconbitmap("clienticon.ico")     
        self.creat_combox()

        self.Creat_Menu()

        self.label_frame = ttk.LabelFrame(self, text = "Add New Images")
        self.label_frame.grid(column=0, row=1, padx=20, pady=20)

        self.add_img_buton()

        # click listener
    def Click_Me(self):
        self.label.configure(text = "Selected :" + self.languages.get())
        if self.languages.get().__eq__("Mask Detctor"):
            self.Mask_Detctor(is_facerecogntion=False)
        elif self.languages.get().__eq__("Normal Camera"):
            pass  
        elif self.languages.get().__eq__("Face Recogntion"):
            self.Mask_Detctor(is_facerecogntion=True)   
    
    # creat combox
    def creat_combox(self):
        
        self.languages = StringVar()
        self.combobox = ttk.Combobox(self, width = 20, textvariable = self.languages)
        self.combobox['values'] = ("Normal Camera", "Mask Detctor", "Face Recogntion")
        self.combobox.grid(column = 1, row = 0)  

        self.label = ttk.Label(self, text ="Select Camera Status")  
        self.label.grid(column = 0, row = 0)

        self.button = ttk.Button(self, text = "Run", command = self.Click_Me)
        self.button.grid(column = 2, row = 0)

        #add new image to the dataset
    def add_img_buton(self):
        button = ttk.Button(self.label_frame, text = "Browse A File", command= self.file_dialog)

        #self.label.configure(text = "Selected :" + self.languages.get())
        button.grid(column=1,row=1) 

        #file dialog
    def file_dialog(self):
        root = tk.Tk()
        root.withdraw() #use to hide tkinter window
        # current dir path
        currdir = os.getcwd()
        # file name to copy to current directory
        file_name = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
        label = ttk.Label(self.label_frame, text = "")
        label.grid(column=1, row=2)
        label.configure(text=file_name)    

        original = file_name
        target = os.getcwd() + '\DATASET1'
        self.copytree(self,original,target)    

        #mask detcor
    def Mask_Detctor(self, is_facerecogntion: bool):
        cascPath = "haarcascade_frontalface_alt2.xml"
        faceCascade = cv2.CascadeClassifier(cascPath)
        model = load_model("mask_recog.h5")
        
        video_capture = cv2.VideoCapture(0)
            # to use your mobile’s camera
        # video_capture= cv2.VideoCapture(1)
        while True:
            # Capture frame-by-frame
            ret, frame = video_capture.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray,1.1,4)
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
                (mask, withoutMask) = model.predict(face_frame)[0]

                label = "Mask" if mask > withoutMask else "No Mask"
                color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
                label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)
                cv2.putText(frame, label, (x, y- 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)

                name = ""
                if(is_facerecogntion):
                    name = self.getFaceRecognation(rgb,'face_enc')    
                #face recognation 
                cv2.putText(frame, name , (x+50 , y - 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
                cv2.rectangle(frame, (x, y), (x + w, y + h),color, 2)
                # Display the resulting frame
                
            cv2.imshow('Video', frame)
            key = cv2.waitKey(1)
            if key == 27: # exit on ESC
                break
        video_capture.release()
        # cap.release()
        cv2.destroyAllWindows()
    #find path of xml file containing haarcascade file 
#function to get the images and label data
    def getFaceRecognation(self, frame,typ):
        data = pickle.loads(open(typ, "rb").read())
    
        # the facial embeddings for face in input
        encodings = face_recognition.api.face_encodings(frame, known_face_locations=None, num_jitters=2,model='large')
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
    #     print(name)
        return name

    def train_facerecogntion(self):

        #get paths of each file in folder named Images
        #Images here contains my data(folders of various persons)
        imagePaths = list(paths.list_images(r"DATASET1"))
        knownEncodings = []
        knownNames = []
            # loop over the image paths
        for (i, imagePath) in enumerate(imagePaths):
            # extract the person name from the image path
            name = imagePath.split(os.path.sep)[-2]
            # load the input image and convert it from BGR (OpenCV ordering)
            # to dlib ordering (RGB)
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            #Use Face_recognition to locate faces
            boxes = face_recognition.face_locations(rgb,model='hog')
            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)
            # loop over the encodings
            for encoding in encodings:
                knownEncodings.append(encoding)
                knownNames.append(name)
            #save emcodings along with their names in dictionary data
        data = {"encodings": knownEncodings, "names": knownNames}
            #use pickle to save data into a file for later use
        f = open("face_enc", "wb")
        f.write(pickle.dumps(data))
        f.close()   

    def creat_directory(self, name:str, parent_dir:str):

        # Directory
        dir_name =  name

        # Parent Directory path or current dir path

        # Path
        path = os.path.join(parent_dir, dir_name)
        os.mkdir(path)

    # copy new directory to dist directory   
    def copytree(self,src, dst, symlinks=False, ignore=None):
        #creat new directory name the last part of path
        self.creat_directory(self, name=os.path.basename(os.path.normpath(src)),parent_dir=dst)

        # distnation is now the new directory
        dst = dst + "/" + os.path.basename(os.path.normpath(src))
        
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(self, s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)

        # creat menu bar
    def Creat_Menu(self):
            Menu_Bar = Menu(self)
            self.config(menu = Menu_Bar)


            file_menu = Menu(Menu_Bar, tearoff = 0)
            Menu_Bar.add_cascade(label = "File", menu = file_menu)
            #file_menu.add_command(label = "New")
            #exit
            file_menu.add_command(label = "Exit", command = self.window_close)

            file_menu.add_separator()
            file_menu.add_command(label = "About")

        #close windows
    def window_close(self):
        self.quit()
        self.destroy()
        exit()

#class camera_window():
    

Window = Window() 
Window.mainloop()  
