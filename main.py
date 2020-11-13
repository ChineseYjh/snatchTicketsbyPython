# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 20:28:26 2018

@author: 87767
"""
#from time import sleep
from tkinter import Tk
#from Mytickets import mtkt
from land_on import mainWindow
from stationInformation import stationInf
import land_on as lo

#global

root = Tk()

root.geometry('960x515+300+200')
mainW=mainWindow(root)
root.mainloop()
#root.destroy()
#root.mainloop()

#print(judgeland)

#lo.set_judgeland(1)
if lo.get_judgeland()==1:

    next=Tk()
    #next =tk.Toplevel(root,width=1030,height=960)
    next.geometry('960x1030+300+0')
    station = stationInf(next)
    next.mainloop()


#else