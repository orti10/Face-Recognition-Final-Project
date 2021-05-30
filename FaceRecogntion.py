from numpy.core.numeric import True_
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelBinarizer
from tensorflow.keras.models import load_model
from sklearn.model_selection import train_test_split
from imutils import paths
import matplotlib.pyplot as plt
import face_recognition
import numpy as np
import os   
import imutils
import pickle
import time
import cv2

# GUI
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

class Window(Tk):
    #constructor
    def __init__(self):
        super(Window, self).__init__()

        self.title("Face Recogntion")
        self.minsize(500, 400)
        self.wm_iconbitmap("clienticon.ico")     
        self.creat_combox()

        


        self.label_frame = ttk.LabelFrame(self, text = "Add New Image")
        self.label_frame.grid(column=0, row=1, padx=20, pady=20)

        self.add_img_buton()
    def Click_Me(self):
        self.label.configure(text = "Selected :" + self.languages.get())
        if self.languages.get().__eq__("Mask Detctor"):
            self.Mask_Detctor(is_facerecogntion=False)
        elif self.languages.get().__eq__("Normal Camera"):
            pass  
        elif self.languages.get().__eq__("Face Recogntion"):
            self.Mask_Detctor(is_facerecogntion=True)   
    
    def creat_combox(self):
        self.languages = StringVar()
        self.combobox = ttk.Combobox(self, width = 20, textvariable = self.languages)
        self.combobox['values'] = ("Normal Camera", "Mask Detctor", "Face Recogntion")
        self.combobox.grid(column = 1, row = 0)  

        self.label = ttk.Label(self, text ="Select Camera Status")  
        self.label.grid(column = 0, row = 0)

        self.button = ttk.Button(self, text = "Click Me", command = self.Click_Me)
        self.button.grid(column = 2, row = 0)

        #add new image to the dataset
    def add_img_buton(self):
        button = ttk.Button(self.label_frame, text = "Browse A File", command= self.file_dialog)
        button.grid(column=1,row=1) 
    
    def file_dialog(self):
        file_name = filedialog.askopenfilename(initialdir = "/", title = "Select Afile", filetype = (("jpeg", "*.jpg"),("All Files", "*.*")) )
        label = ttk.Label(self.label_frame, text = "")
        label.grid(column=1, row=2)
        label.configure(text=file_name)    

    def Mask_Detctor(self, is_facerecogntion: bool):
        cascPath = os.path.dirname(
            cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
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
                    name = getFaceRecognation(self,rgb,'face_enc')    
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
# function to get the images and label data
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
    imagePaths = list(paths.list_images(r"C:\Users\User\Desktop\finalpro\DATASET1"))
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
        
       

   
Window = Window() 
Window.mainloop()  