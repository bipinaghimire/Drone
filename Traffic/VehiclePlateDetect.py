from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import object_detection as od
import imageio
import cv2

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pos =[]
        self.line = []
        self.rect = []
        self.master.title("Vehicle Plate Detection")
        self.pack(fill=BOTH, expand=1)
        self.counter =0
        menu = Menu(self.master)
        self.master.config(menu=menu)
        file = Menu(menu)
        file.add_command(label="Open", command=self.open_file)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)
        analyze = Menu(menu)
        analyze.add_command(label="Region of interest", command=self.regionOfInterest)
        menu.add_cascade(label="Analyze", menu=analyze)
        self.filename = "images/demo.jpg"
        self.imgSize =Image.open(self.filename)
        self.tkimage = ImageTk.PhotoImage(self.imgSize)
        self.w, self.h = (1366, 768)
        self.canvas = Canvas(master = root , width = self.w, height = self.h)
        self.canvas.create_image(20,20, image = self.tkimage, anchor = NW)
        self.canvas.pack()

    def open_file(self):
        self.filename = filedialog.askopenfilename()
        cap = cv2.VideoCapture(self.filename)
        reader = imageio.get_reader(self.filename)
        fps = reader.get_meta_data()['fps']
        ret, image  = cap.read()
        

