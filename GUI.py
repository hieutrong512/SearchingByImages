import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from img_search import search_image
import tracking
from urllib.parse import urlparse
from os.path import splitext, basename

my_w = tk.Tk()
my_w.geometry("1500x800")  # Size of the window 
my_w.title('Searching Images')

my_font1=('times', 18, 'bold')
l1 = tk.Label(my_w,text='Upload Files & Detect',width=30,font=my_font1)  
l1.grid(row=1,column=1,columnspan=4)

b1 = tk.Button(my_w, text='Upload Files', 
   width=20,command = lambda:upload_file())
b1.grid(row=3,column=1,columnspan=4,rowspan=3)

global newPhoto_labels
newPhoto_labels = []

def get_file_name(picture_page):
    disassembled = urlparse(picture_page)
    filename, file_ext = splitext(basename(disassembled.path))
    return filename, file_ext


def on_click(img):
    list_result = search_image.predict(img)
    k=0
    y=10
    x=950
    for img in list_result:
        image = Image.open('Image_Search\\'+img)
        image = image.resize((250,250))
        if k==0:
            displayImg_Search(image,x,y)
            k=2
        elif k==2:
            x+=300
            displayImg_Search(image,x,y)
            k=1
        elif k==1:
            x=950
            y+=260
            displayImg_Search(image,x,y)
            k=2




def displayImg_Search(img,x,y):
    photo = ImageTk.PhotoImage(img)
    newPhoto_label = Label(my_w,image=photo)
    newPhoto_label.image = photo
    newPhoto_label.place(x=x,y=y)
    newPhoto_labels.append(newPhoto_label)

def displayImg_Detect(img,y):
    photo = ImageTk.PhotoImage(img)
    newPhoto_label = Label(my_w,image=photo)
    newPhoto_label.image = photo
    # newPhoto_label.place(x=650,y=y)
    button=Button(my_w,image=photo, command=lambda :on_click(img))
    button.place(x=650,y=y)
    newPhoto_labels.append(button)

def read_boxes(lines,img):
    box = []
    for line in lines:
        line = line.split(' ')
        left,top,right,bottom = int(float(line[1])),int(float(line[2])),int(float(line[3])),int(float(line[4]))
        box.append((left, top, right, bottom))
    print('List box: ',box)
    return box

def read_file(img):
    image = Image.open(img)
    labels = 'Result/labels/'+get_file_name(img)[0]+'.txt'
    box=[]
    # try:
    with open(labels,'r') as rf:
        readlines = rf.readlines()
    box = read_boxes(readlines,image)
    print(labels)
    # except:
    #     pass
    return box

def upload_file():
    #=====Load Image=====
    f_types = [('Jpg Files', '*.jpg'),
    ('PNG Files','*.png')]   # type of files to select
    filename = filedialog.askopenfilename(multiple=True,filetypes=f_types)[0]
    # cmd = 'py yolov7/detect.py --save-txt --source '+ filename
    # os.system(cmd)
    if newPhoto_labels:
        print("Len of labels: ",len(newPhoto_labels))
        for lb in newPhoto_labels:
            lb.destroy()
    tracking.predict(filename)
    file_img,_ = get_file_name(filename)
    # get_fileIMG_after_detetc()
    
    img=Image.open('Result/images/'+file_img+'.jpg') # read the image file
    img=img.resize((524,524)) # new width & height
    img=ImageTk.PhotoImage(img)
    e1 =tk.Label(my_w)
    e1.grid(row=2,column=1)
    e1.image = img
    e1['image']=img # garbage collection 

    #====Crop Image======
    boxes = read_file(filename)
    row = 0 
    if len(boxes) <= 3 :
        row = 60
        for box in boxes:
            image = Image.open(filename)
            new_img = image.crop(box)
            new_img = new_img.resize((200,200))
            displayImg_Detect(new_img,row)
            row += 240 
    else:
        row = 10
        space = int((790/len(boxes))*0.2)
        size_img = int((790-space*(len(boxes)-1))/len(boxes))
        for box in boxes:
            image = Image.open(filename)
            new_img = image.crop(box)
            new_img = new_img.resize((size_img,size_img))
            displayImg_Detect(new_img,row)
            row+=space+size_img

my_w.mainloop()  # Keep the window open

# from PIL import Image

# img = Image.open('yolov7/inference/images/bus.jpg')
# img = img.crop((88, 136, 555, 435))

# img.show()