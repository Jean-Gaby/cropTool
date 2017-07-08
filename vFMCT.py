# -*- coding: utf-8 -*-
"""
@author: Jean-Gabriel JOLLY
"""

#===============
#Importing modules
#===============

#modules for GUI
#from tkinter import *
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showwarning

#modules for image processing
import PIL
from PIL import Image

#module for Manage files and use system commands
import os
import glob

#===============
#variables declaration
#===============


#List of rectangles displays on screen
global rectangleList
rectangleList=[]

#Counters for managing rectangles and pictures
global numberImage, numberRectangle,totalRectangle,numberPicture
numberImage, numberRectangle,totalRectangle,numberPicture = 0,0,0,0

#Square position
global x1,x2,y1,y2
x1,x2,y1,y2=0,0,0,0

#===============
#===============
#===============


#Square position
def leftClick(event):
    chaine.configure(text = str(event.x)+" "+str(event.y))
    global x1,y1
    x1=event.x
    y1=event.y

def holdLeftClick(event):
    global numberRectangle
    chaine.configure(text = str(event.x)+" "+str(event.y)+"Frame object number "+str(numberRectangle))
    cadre.coords(rectangle, x1,y1,event.x,event.y)
    
def releaseLeftClick(event):
    cadre.coords(rectangle, 0, 0, 0, 0)
    global x2,y2,numberRectangle,rectangleList,totalRectangle,hpercent
    chaine.configure(text = "Number of frames:" + str(numberRectangle+1))
    x2=event.x
    y2=event.y
    rectangleList.append(cadre.create_rectangle(x1,y1,x2,y2))
    numberRectangle += 1
    totalRectangle += 1

    
    ####Selection orientation management PART#####
    if x1 < x2 and y1 < y2:
        area = (int(x1/hpercent), int(y1/hpercent), int(x2/hpercent), int(y2/hpercent))
    elif x2 < x1 and y2 < y1:
        area = (int(x2/hpercent), int(y2/hpercent), int(x1/hpercent), int(y1/hpercent))
    elif x2 < x1 and y1 < y2:
        area = (int(x2/hpercent), int(y1/hpercent), int(x1/hpercent),int(y2/hpercent))
    elif x1 < x2 and y2 < y1:
        area = (int(x1/hpercent), int(y2/hpercent), int(x2/hpercent), int(y1/hpercent))
    
    ####CROPPING PART#####
    cropped_img = img.crop(area)
    cropped_img.save(outputDirectory+'/name' + str(totalRectangle) + '.png') #test bug here
    ######################
    
def middleClick(event):
    global numberPicture,photo,photo2,img,rectangle,numberRectangle
    numberPicture += 1
    if numberPicture < len(listPictures):

        imageDisplay()

        cadre.delete(aff)
        cadre.create_image(0, 0, anchor=NW, image=photo2)
        rectangle=cadre.create_rectangle(0,0,0,0)
        numberRectangle = 0
        
        #Removing old rectangles
        for i in rectangleList:
            cadre.delete(i)
        ########################

    else:
        chaine.configure(text = "No More pictures")
        showwarning("No More pictures")
        
        

##########################
##########################
##########################
def rightClick(event):
    global rectangleList, numberRectangle, totalRectangle
    if numberRectangle > 0:
        chaine.configure(text = "Erasing frame number ="+str(numberRectangle))
        cadre.delete(rectangleList[len(rectangleList)-1])
        del rectangleList[len(rectangleList)-1]
        os.remove(outputDirectory+'/name' + str(totalRectangle) + '.png')
        numberRectangle -= 1
        totalRectangle -= 1
    else:
        chaine.configure(text = "Nothing to erase")

def imageDisplay():
    global numberPicture,photo,photo2,img,rectangle,hpercent
    
    #photo = PhotoImage(file=listPictures[numberPicture])
    im=Image.open(listPictures[numberPicture]) #test test test
    photo = PhotoImage(im)

    ###DISPLAY RESIZE MODULE###
    baseheight = (int(fen.winfo_screenheight()*0.85))#size of the height of the screen
    ############ A MOFIFIER PLUS TARD  ^^^^^^^^
    img = Image.open(listPictures[numberPicture])
    hpercent = ((baseheight / float(img.size[1])))
    wsize = int((float(img.size[0]) * float(hpercent)))
    img2 = img.resize((wsize, baseheight), PIL.Image.ANTIALIAS)
    ###########################
    
    ############ A MOFIFIER PLUS TARD
    img2.save("temporaryFile.png")
    #photo2 = PhotoImage(file="image32bis.png")
    photo2 = PhotoImage(file="temporaryFile.png")
    ############ A MOFIFIER PLUS TARD
    
    
##########################
##########################
##########################
##########################
##########################
##########################
    



fen = Tk()
fen.title('Very Fast Multiple Cropping Tool')

#Ask for directory
showwarning('Instructions', 'Enter the image folder')
inputDirectory = askdirectory(initialdir='C:/Users/%s')
showwarning('Instructions', 'Enter the destination folder')
outputDirectory = askdirectory(initialdir='C:/Users/%s')
#=================

#list images in the forlder
listPictures = sorted(glob.glob(inputDirectory + '/*.png'))
listPictures2 = sorted(glob.glob(inputDirectory + '/*.jpg'))
listPictures = listPictures + listPictures2
print(listPictures)

###
if len(listPictures)>0:
    imageDisplay()
    cadre = Canvas(fen, width=photo2.width(), height=photo2.height(), bg="light yellow")
    
    w, h = photo2.width(), photo2.height()+20
    fen.geometry("%dx%d+0+0" % (w, h))
    
    aff=cadre.create_image(0, 0, anchor=NW, image=photo2) #BUG
    cadre.bind("<Button-1>", leftClick)
    cadre.bind("<B1-Motion>", holdLeftClick)
    cadre.bind("<ButtonRelease-1>", releaseLeftClick)
    cadre.bind("<Button-2>", middleClick)
    cadre.bind("<ButtonRelease-3> ", rightClick)
    cadre.pack()
    chaine = Label(fen)
    chaine.pack() 
    rectangle=cadre.create_rectangle(0,0,0,0)
    fen.mainloop()
    os.remove("temporaryFile.png")
else:
    showwarning('Error', 'There are no images in the folder')
    fen.destroy()
    


