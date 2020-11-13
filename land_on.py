# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 14:42:11 2018
  Label,PhotoImage,BOTH,StringVar,Frame,Entry,Button
@author: mengj
"""

import tkinter as tk
from Mytickets import mtkt
#from main import myTickets

class globalvalue:
        judgeclick=-1
        judgeland=-1
        judgecheck=-1


def set_judgeclick(jc):
    globalvalue.judgeclick = jc


def set_judgeland(jl):
    globalvalue.judgeland = jl


def get_judgeclick():
    return globalvalue.judgeclick


def get_judgeland():
    return globalvalue.judgeland

def set_judgecheck(jck):
    globalvalue.judgecheck=jck

def get_judgecheck():
    return globalvalue.judgecheck


myTickets = mtkt()
  



class  mainWindow(object):

    def __init__(self,parent):
        # 函数
        def sendvalue():
            print("你按我")
            myTickets.reset_info(self.entryy.get(),self.entrym.get())
            a=int(myTickets.log_in())
            #print(a)
            set_judgeland(a)
            #print(a)
            print(get_judgeland())
            if get_judgeland()==0:
                print("乱来")
                self.labelerr=tk.Label(self.frame,font = ('微软雅黑',9),bg='white',bd ='9',fg = 'red',anchor = 'w',text='用户名或密码错误')
                self.labelerr.place(relx=0.31, rely=0.25, width=150, height=20)
            elif get_judgeland()==1:
                print("打的很棒")
                self.root.destroy()
                self.root.mainloop()
        self.root = parent
        #root.minsize(500,500)
        self.root.geometry('960x515+300+200')
        self.root.title('登录界面')
        self.frameAll = tk.Frame(parent)
        self.img = tk.PhotoImage(file = 'true.gif')
        self.bbg = tk.Label(self.frameAll, image = self.img)
        self.bbg.pack(fill=tk.BOTH,expand=1)
        self.frameAll.place(relx=0, rely=0, relwidth=1, relheight=1)
        #1.界面布局
        #显示面板
        self.resultl = tk.StringVar()
        self.resultl.set('用户名:')                           #显示面板显示结果1，用于显示默认数字0
        self.resultl1 = tk.StringVar()
        self.resultl1.set('密码:')
        self.resultl2 = tk.StringVar()
        self.resultl2.set('用户登录')
        self.resulte = tk.StringVar()
        self.resulte.set('')
        self.resulte1 = tk.StringVar()
        self.resulte1.set('')
        #self.jg='请您输入用户名'
        #self.jg1='请您输入密码'
        #显示版
        self.frame = tk.Frame(parent,bg='white')
        
        self.frame.place(relx=0.17, rely= 0.20,height=280,width=400)
        
        #place,pace,grid
        self.labely = tk.Label(self.frame,font = ('微软雅黑',12),bg='white',bd ='9',fg = 'black',anchor = 'w',textvariable = self.resultl)
        self.labely.place(relx=0.16,rely=0.35,width = 70,height = 30)
        self.labelm = tk.Label(self.frame,font = ('微软雅黑',12),bg='white',bd ='9',fg = 'black',anchor = 'w',textvariable = self.resultl1)
        self.labelm.place(relx=0.16,rely=0.525,width = 70,height = 30)
        self.labeld = tk.Label(self.frame,font = ('微软雅黑',15),bg='white',bd ='9',fg = '#00FFFF',anchor = 'w',textvariable = self.resultl2)
        self.labeld.place(relx=0.37,rely=0.12,width = 150,height = 35)
        self.entryy = tk.Entry(self.frame,font = ('微软雅黑',10),bg='white',bd ='1',fg = '#828282',textvariable = self.resulte)
        self.entryy.place(relx=0.33,rely=0.35,width = 200,height = 30)
        self.entrym = tk.Entry(self.frame,font = ('微软雅黑',10),bg='white',bd ='1',fg = '#828282',textvariable = self.resulte1)
        self.entrym.place(relx=0.33,rely=0.525,width = 200,height = 30)
        self.entrym['show'] = '*'
        #用户输入用户名和密码
        print("我要输入了")
        
        #print("输入了")
        self.btnland = tk.Button(self.frame,font = ('微软雅黑',12,'bold'),bg='#00FFFF',fg = 'white',text = '登    录',
                             activeforeground='#00FFFF',command=sendvalue)
        self.btnland.place(relx=0.25,rely=0.70,width = 200,height = 30)
        #print('a')
 
