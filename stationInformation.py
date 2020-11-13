#from land_on import globalvalue
import land_on as lo
import datetime
from tkinter import Label,StringVar,Frame,Entry,Button,Canvas,IntVar,Checkbutton,Toplevel,Listbox,END
#from time import sleep
#,Scrollbar  RIGHT,Y,
todaytime = datetime.datetime.today()
maxdaytime = todaytime + datetime.timedelta(days=30)
maxday = (datetime.date.today() + datetime.timedelta(days=30)).strftime('%Y-%m-%d')

strtime='可抢区间：'+todaytime.strftime('%Y-%m-%d')+'----'+ maxdaytime.strftime('%Y-%m-%d')
class stationInf(object):

    def __init__(self,parent):
        self.is_future = False
        #inputday
        hour = StringVar()
        hour.set('0--23')
        minute = StringVar()
        minute.set('0--59')
        self.btncheck_list = []
        self.plistback = []
        #self.judgepas = []
        self.varp = []#num与它有关
        num = -1
        self.page = 0
        self.allpage = 0
        
        
        self.next = parent

        self.next.geometry('960x930+300+0')
        self.canvas=Canvas(self.next)
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

        """
        self.vbar = Scrollbar(self.canvas, orient=VERTICAL)  # 竖直滚动条
        self.vbar.place(x=180, width=20, height=180)
        self.vbar.configure(command=self.canvas.yview)
        self.canvas.config( yscrollcommand=self.vbar.set)  # 设置
        self.canvas.create_window((90, 240), window=self.frame)  # create_window
        """
        self.frameAll = Frame(self.canvas, bg='#f0f0f0')
        self.frameAll.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.next.title('车站信息')
        self.nresulte = StringVar()
        self.nresulte.set('北京')  # 显示面板显示结果1，用于显示默认数字0
        self.nresulte1 = StringVar()
        self.nresulte1.set('天津')
        self.nresulte2 = StringVar()
        self.nresulte2.set('2018')
        self.nresulte3 = StringVar()
        self.nresulte3.set('07')
        self.nresulte4 = StringVar()
        self.nresulte4.set('01')
        self.nresulte5 = StringVar()
        self.nresulte5.set(strtime)
        
        
        
        def sendtimeInfor():
            print('我进来了')
            self.top.destroy()

        
        def show_success():
            self.book_tickets =Toplevel(self.next)
            self.book_tickets.title("抢票")
            self.book_tickets.geometry('480x130+300+0')
            l=Label(self.book_tickets, font=('微软雅黑', 12),  fg='green',bd='1', anchor='w',
                         text='抢票成功！！！')
            l.pack()
        def check_book_f():
            if  lo.myTickets.book_tickets_on_sale(self.tickets_list[5],self.inputday,self.plistback):
                show_success()
            print('future')
        def check_book_t():
            if  lo.myTickets.book_tickets_on_sale(self.tickets_list[5],self.inputday,self.plistback):
                show_success()
            print('on sale')
        # self.nresulte = StringVar()
        # self.nresulte.set('请您输入用户名')
        # self.nresulte1 = StringVar()
        # self.nresulte1.set('请您输入密码')
        def sendInfor():
            
            value=self.entryfromdayyear.get()
            value2=self.entryfromdaymonth.get()
            value3=self.entryfromdayday.get()
            #print(value[0:4])
            print(value.isdigit())
            print(len(value))
            print(len(value2))
            if value.isdigit()==False or value2.isdigit()==False or value3.isdigit()==False or len(value)!=4 or len(value2)!=2 or len(value3)!=2:
                self.nresulte2.set('2018')
                self.nresulte3.set('07')
                self.nresulte3.set('01')
                #print( self.entryfromday.get())
                self.entryfromdayyear = Entry(self.frame, font=('微软雅黑', 9), bg='white', bd='1', fg='red',
                                          textvariable=self.nresulte2)
                self.entryfromdayyear.place(relx=0.59, rely=0.17, width=50, height=30)
                self.entryfromdaymonth = Entry(self.frame, font=('微软雅黑', 9), bg='white', bd='1', fg='red',
                                               textvariable=self.nresulte3)
                self.entryfromdaymonth.place(relx=0.68, rely=0.17, width=30, height=30)
                self.entryfromdayday = Entry(self.frame, font=('微软雅黑', 9), bg='white', bd='1', fg='red',
                                             textvariable=self.nresulte4)
                self.entryfromdayday.place(relx=0.75, rely=0.17, width=30, height=30)

                lo.set_judgecheck(0)

            self.inputday = value + '-' + value2 + '-' + value3
            inputdaydt=datetime.datetime.strptime(self.inputday,'%Y-%m-%d')
            print(self.inputday)
            print(maxday)
            if self.inputday==maxday:
                self.is_future=True
                
            if self.is_future == True:
                self.top =Toplevel(self.next)
                self.top.title("抢票时间")
                self.top.geometry('480x130+300+0')
                l=Label(self.top, font=('微软雅黑', 12),  fg='red',bd='1', anchor='w',
                         text='还无法抢'+self.inputday+'的票，请输入开始抢票时间')
                l.pack()
                
                lh = Label(self.top, font=('微软雅黑', 12), bg='#D2E9FF', bd='1', fg='black', anchor='w',
                            text='时：')
                lh.place(relx=0.15, rely=0.2, width=70, height=30)
                print("我执行了")
                eh = Entry(self.top, font=('微软雅黑', 12), bg='white', bd='1', fg='#828282',
                               textvariable=hour)

                eh.place(relx=0.35, rely=0.2, width=150, height=30)
                lm = Label(self.top, font=('微软雅黑', 12), bg='#D2E9FF', bd='1', fg='black', anchor='w',
                            text='分：')
                lm.place(relx=0.15, rely=0.45, width=70, height=30)
                em = Entry(self.top, font=('微软雅黑', 12), bg='white', bd='1', fg='#828282',
                               textvariable=minute)

                em.place(relx=0.35, rely=0.45, width=150, height=30)
                btnright = Button(self.top, font=('微软雅黑', 12,), bg='#ffa042', fg='white', text='确  定',
                               activeforeground='#00FFFF', command=sendtimeInfor)
                btnright.place(relx=0.35, rely=0.7, width=150, height=30)
            if inputdaydt>=todaytime+ datetime.timedelta(days=-1) and inputdaydt<=maxdaytime:
                print('good')
                self.labeldtx = Label(self.frametx,font=('微软雅黑', 12),  bd='9', fg='red', anchor='w',
                                      text=' ')
                self.labeldtx.place(relx=0.5, rely=0.17, width=90, height=20)
                lo.set_judgecheck(1)
            else:
                self.labeldtx = Label(self.frametx, font=('微软雅黑', 12),  bd='9', fg='red', anchor='w',
                                      text='时间超限')
                self.labeldtx.place(relx=0.5, rely=0.17, width=90, height=20)
                lo.set_judgecheck(0)



            print(lo.get_judgecheck())
            if lo.get_judgecheck()==1:
                self.entryfromday = Entry(self.frame, font=('微软雅黑', 9), bg='white', bd='1', fg='black',
                                          textvariable=self.nresulte2)
                self.entryfromday.place(relx=0.59, rely=0.17, width=50, height=30)
                self.entryfromdayyear.place(relx=0.59, rely=0.17, width=50, height=30)
                self.entryfromdaymonth = Entry(self.frame, font=('微软雅黑', 9), bg='white', bd='1', fg='black',
                                               textvariable=self.nresulte3)
                self.entryfromdaymonth.place(relx=0.68, rely=0.17, width=30, height=30)
                self.entryfromdayday = Entry(self.frame, font=('微软雅黑', 9), bg='white', bd='1', fg='black',
                                             textvariable=self.nresulte4)
                self.entryfromdayday.place(relx=0.75, rely=0.17, width=30, height=30)
                
                self.tickets_list = lo.myTickets.get_tickets_info(self.entryfrom.get(),self.entryto.get(),self.inputday,self.is_future)
                
                numtl=0
                #self.mylb.delete(0,END)
                self.tllen = len(self.tickets_list)
                
                    
                self.page = 1
                self.allpage = int((self.tllen)/20) + 1
                for item in self.tickets_list[0:20]:
                    placey = numtl*0.05
                    string = '  '
                    for k,v in item.items():
                        if  k!='bookable' and k!='book_btn':
                            string = string + '{:^8}'.format(v)
                    #print(string)
                    
                    
                    
                    
                    self.stationtickets_list = Label(self.mylb, font=('微软雅黑', 10), bg='white', bd='9', width=90, height=1, fg='black', anchor='w',
                            text=string)
                    self.stationtickets_list.place(relx=0,rely=placey)
                    
                   
                    if item['bookable'] == False:
                        if self.is_future ==True:
                            
                            self.btncheck = Button(self.mylb, font=('微软雅黑', 11),width=9, height=1,  fg='black', text='预  订',
                               activeforeground='#00FFFF', command=check_book_f)
                            self.btncheck.place(relx=0.88,rely=placey)
                        else :
                                 self.btncheck = Button(self.mylb, font=('微软雅黑', 11),width=9, height=1,  fg='black', text='预  订',
                                         activeforeground='#00FFFF', command=check_book_t)
                                 self.btncheck.place(relx=0.88,rely=placey)
                    else :
                        self.btncheck = Button(self.mylb, font=('微软雅黑', 11), width=9, height=1, bg='#ffa042', fg='black', text='预  订',
                               activeforeground='#00FFFF', command=check_book_t)
                        self.btncheck.place(relx=0.88,rely=placey)
                    
                    #strnum = str(numtl)+'  '+string
                    numtl=numtl+1
                    print('here')
                    #print(strnum)
                    self.mylb.insert(END, self.stationtickets_list)
                    self.mylb.insert(END, self.btncheck)
                    self.labelnum = Label(self.frameAll, font=('微软雅黑', 12,'bold'), fg='black',
                            text=self.page)
                    self.labelnum.place(relx=0.475, rely=0.92, width=20, height=30)
                    self.labelnum3 = Label(self.frameAll, font=('微软雅黑', 12,'bold'), fg='black',
                            text=self.allpage)
                    self.labelnum3.place(relx=0.505, rely=0.92, width=20, height=30)
                    self.btnup = Button(self.frameAll, font=('微软雅黑', 12,),  fg='black', text='上 一 页',
                               activeforeground='#00FFFF', command=page_last)
                    self.btnup.place(relx=0.42, rely=0.92, width=80, height=30)
                    '''
                    self.frame4 = Frame(self.frameAll, width=150, height=300)
                    self.frame4.place(relx=0.03,rely=0.26)
                    '''
                
            lo.set_judgecheck(-1)


        
        def bindcbtnpas():
            
            for num in range(len(self.varp)):
                print(self.varp[num].get())
                if self.varp[num].get() == 1:
                    a=0
                    for num1 in self.plistback:
                        if self.passengers[num] == num1:
                            a=1
                    if a==0:
                        self.plistback.append((self.passengers[num]))
                if self.varp[num].get() == 0:
                    b=0
                    for num1 in self.plistback:
                        if self.passengers[num] == num1:
                            b=1
                    if b==1:
                        self.plistback.remove((self.passengers[num]))
            print(self.plistback)

        self.frame = Frame(self.frameAll, bg='#D2E9FF', width=950, height=45)
        self.frame.place(relx=0.2,rely=0.03)
        self.frametx = Frame(self.frameAll, width=950, height=37)
        self.frametx.place(relx=0.2,rely=0.08)
        # place,pace,grid
        self.labely = Label(self.frame, font=('微软雅黑', 12), bg='#D2E9FF', bd='9', fg='black', anchor='w',
                            text='出发地：')
        self.labely.place(relx=0.05, rely=0.17, width=70, height=30)
        self.labelm = Label(self.frame, font=('微软雅黑', 12), bg='#D2E9FF', bd='9', fg='black', anchor='w',
                            text='目的地：')
        self.labelm.place(relx=0.275, rely=0.17, width=70, height=30)
        self.labeld = Label(self.frame, font=('微软雅黑', 12), bg='#D2E9FF', bd='9', fg='black', anchor='w',
                            text='出发日期：')
        self.labeld.place(relx=0.5, rely=0.17, width=90, height=30)
        self.labeldtx = Label(self.frametx, font=('微软雅黑', 9), bd='9', fg='blue', anchor='w',
                              textvariable=self.nresulte5)
        self.labeldtx.place(relx=0.05, rely=0.1, width=250, height=30)
        self.labeldy = Label(self.frame, font=('微软雅黑', 12), bg='#D2E9FF', bd='9', fg='black', anchor='w',
                            text='年')
        self.labeldy.place(relx=0.64, rely=0.17, width=90, height=30)
        self.labeldm = Label(self.frame, font=('微软雅黑', 12), bg='#D2E9FF', bd='9', fg='black', anchor='w',
                            text='月')
        self.labeldm.place(relx=0.71, rely=0.17, width=90, height=30)
        self.labeldd = Label(self.frame, font=('微软雅黑', 12), bg='#D2E9FF', bd='9', fg='black', anchor='w',
                            text='日')
        self.labeldd.place(relx=0.78, rely=0.17, width=90, height=30)
        self.entryfrom = Entry(self.frame, font=('微软雅黑', 9), bg='white', bd='1', fg='#828282',
                               textvariable=self.nresulte)

        self.entryfrom.place(relx=0.12, rely=0.17, width=150, height=30)
        self.entryto = Entry(self.frame, font=('微软雅黑', 9), bg='white', bd='1', fg='#828282',
                             textvariable=self.nresulte1)
        self.entryto.place(relx=0.345, rely=0.17, width=150, height=30)
        self.entryfromdayyear = Entry(self.frame, font=('微软雅黑', 9), bg='white', bd='1', fg='#828282',
                                  textvariable=self.nresulte2)
        self.entryfromdayyear.place(relx=0.59, rely=0.17, width=50, height=30)
        self.entryfromdaymonth = Entry(self.frame, font=('微软雅黑', 9), bg='white', bd='1', fg='#828282',
                                      textvariable=self.nresulte3)
        self.entryfromdaymonth.place(relx=0.68, rely=0.17, width=30, height=30)
        self.entryfromdayday = Entry(self.frame, font=('微软雅黑', 9), bg='white', bd='1', fg='#828282',
                                      textvariable=self.nresulte4)
        self.entryfromdayday.place(relx=0.75, rely=0.17, width=30, height=30)
        self.btncheck = Button(self.frame, font=('微软雅黑', 12,), bg='#ffa042', fg='white', text='查  询',
                               activeforeground='#00FFFF', command=sendInfor)
        self.btncheck.place(relx=0.85, rely=0.17, width=80, height=30)
        '''
            
        def bindcbtn():

            if var.get() == 1:
                print('a')
                # 跳出函数
            else:
                print('b')
            if var1.get() == 1:
                print('a1')
            else:
                print('b1')
            if var2.get() == 1:
                print('a2')
            else:
                print('b2')
            if var3.get() == 1:
                print('a3')
            else:
                print('b3')
            if var4.get() == 1:
                print('a4')
            else:
                print('b4')
            if var5.get() == 1:
                print('a5')
            else:
                print('b5')


        self.frame1 = Frame(self.frameAll, bg='white', width=950, height=45, bd='1')
        self.frame1.place(relx=0.2, rely=0.12)

        var = IntVar()
        var1 = IntVar()
        var2 = IntVar()
        var3 = IntVar()
        var4 = IntVar()
        var5 = IntVar()
        

        self.checkbutton = Checkbutton(self.frame1, font=('微软雅黑', 9), bg='white', bd='9', fg='black', anchor='w',
                                       text='全部', variable=var, onvalue=1, offvalue=0, command=bindcbtn)
        self.checkbutton.place(relx=0.05, rely=0.17, width=70, height=30)
        #self.checkbutton.select()
        self.checkbutton1 = Checkbutton(self.frame1, font=('微软雅黑', 9), bg='white', bd='9', fg='black', anchor='w',
                                        text='GC-高铁/城际', variable=var1, onvalue=1, offvalue=0, command=bindcbtn)
        self.checkbutton1.place(relx=0.2, rely=0.17, width=110, height=30)
        self.checkbutton2 = Checkbutton(self.frame1, font=('微软雅黑', 9), bg='white', bd='9', fg='black', anchor='w',
                                        text='D-动车', variable=var2, onvalue=1, offvalue=0, command=bindcbtn)
        self.checkbutton2.place(relx=0.35, rely=0.17, width=70, height=30)
        self.checkbutton3 = Checkbutton(self.frame1, font=('微软雅黑', 9), bg='white', bd='9', fg='black', anchor='w',
                                        text='Z-直达', variable=var3, onvalue=1, offvalue=0, command=bindcbtn)
        self.checkbutton3.place(relx=0.5, rely=0.17, width=70, height=30)
        self.checkbutton4 = Checkbutton(self.frame1, font=('微软雅黑', 9), bg='white', bd='9', fg='black', anchor='w',
                                        text='T-特快', variable=var4, onvalue=1, offvalue=0, command=bindcbtn)
        self.checkbutton4.place(relx=0.65, rely=0.17, width=70, height=30)
        self.checkbutton5 = Checkbutton(self.frame1, font=('微软雅黑', 9), bg='white', bd='9', fg='black', anchor='w',
                                        text='K-快速', variable=var5, onvalue=1, offvalue=0, command=bindcbtn)
        self.checkbutton5.place(relx=0.8, rely=0.17, width=70, height=30)

        
        '''
        
      
        self.passengers = lo.myTickets._get_passengers()
        
        self.frame2 = Frame(self.frameAll, width=150, height=300)
        self.frame2.place(relx=0.03,rely=0.03)
        for pas in self.passengers:
            #self.judge.append(0)
            num = num + 1
            self.varp.append(IntVar())
            self.checkbuttonp = Checkbutton(self.frame2,font=('微软雅黑', 9),text=pas,anchor='w',
                                            variable=self.varp[num], onvalue=1, offvalue=0, command=bindcbtnpas)
            self.checkbuttonp.grid()
            '''
        'trainNumber':'',
                'fromStation':'',
                'toStation':'',
                'departTime':'',
                'arriveTime':'',
                'period':'',
                'specialSeat':'',
                'oneClassSeat':'',
                'twoClassSeat':'',
                'advancedSoftSleeper':'',
                'softSleeper':'',
                'hardSleeper':'',
                'motionSleeper':'',
                'softSeat':'',
                'hardSeat':'',
                'noSeat':'',
                'bookable':False,
                'book_btn':None 
        '''
        self.frame3 = Frame(self.frameAll, bg='#D2E9FF', width=950, height=40)
        self.frame3.place(relx=0.2,rely=0.12)
        self.stationlabal = Label(self.frame3,font=('微软雅黑', 10,'bold'), anchor='w',bg='#D2E9FF',fg='black',text = '   车次   出发站   到达站   出发时间   到达时间   历时   特等座   一等座   二等座   高级软卧   软卧   硬卧   动卧   软座   硬座   无座')
        self.stationlabal.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.mylb = Listbox(self.frameAll, font=('微软雅黑', 15), bd='0',width=79,height=20)
        #self.sl = Scrollbar(self.canvas)
        #self.sl.pack(side=RIGHT, fill=Y)
        #self.mylb['yscrollcommand'] = self.sl.set
        #self.sl['command']=self.mylb.yview
        self.mylb.place(relx=0.2, rely=0.21)
        for item in range(0, 20):
            self.mylb.insert(END, ' ')
            
            
        def page_last():
            if self.page > 1:
                
                self.page = self.page - 1
                if self.page<self.allpage:
                    self.btndown = Button(self.frameAll, font=('微软雅黑', 12,), bg='#ffa042', fg='black', text='下 一 页',
                               activeforeground='#00FFFF', command=page_next)
                    self.btndown.place(relx=0.52, rely=0.92, width=80, height=30)
                if self.page == 1:
                    self.btnup = Button(self.frameAll, font=('微软雅黑', 12,),  fg='black', text='上 一 页',
                               activeforeground='#00FFFF', command=page_last)
                    self.btnup.place(relx=0.42, rely=0.92, width=80, height=30)
                self.labelnum = Label(self.frameAll, font=('微软雅黑', 12,'bold'), fg='black',
                            text=self.page)
                self.labelnum.place(relx=0.475, rely=0.92, width=20, height=30)
                numtl=0
                self.begin = (self.page-1)*20
                self.end = self.page *20
                for item in self.tickets_list[self.begin:self.end]:
                    placey = numtl*0.05
                    string = '  '
                    for k,v in item.items():
                        if  k!='bookable' and k!='book_btn':
                            string = string + '{:^8}'.format(v)
                    
                    
                    
                    
                    
                    self.stationtickets_list = Label(self.mylb, font=('微软雅黑', 10), bg='white', bd='9', width=90, height=1, fg='black', anchor='w',
                            text=string)
                    self.stationtickets_list.place(relx=0,rely=placey)
                    
                   
                    if item['bookable'] == False:
                        if self.is_future ==True:
                            
                            self.btncheck = Button(self.mylb, font=('微软雅黑', 11),width=9, height=1,  fg='black', text='预  订',
                               activeforeground='#00FFFF', command=check_book_f)
                            self.btncheck.place(relx=0.88,rely=placey)
                        else :
                                 self.btncheck = Button(self.mylb, font=('微软雅黑', 11),width=9, height=1,  fg='black', text='预  订',
                                         activeforeground='#00FFFF', command=check_book_t)
                                 self.btncheck.place(relx=0.88,rely=placey)
                    else :
                        self.btncheck = Button(self.mylb, font=('微软雅黑', 11), width=9, height=1, bg='#ffa042', fg='black', text='预  订',
                               activeforeground='#00FFFF', command=check_book_t)
                        self.btncheck.place(relx=0.88,rely=placey)
                    #strnum = str(numtl)+'  '+string
                    numtl=numtl+1
                    #print('here')
                    
                    self.mylb.insert(END, self.stationtickets_list)
                    self.mylb.insert(END, self.btncheck)
                
        def page_next():
            if self.page < self.allpage:
                
                self.page = self.page + 1
                if self.page > 1:
                    self.btnup = Button(self.frameAll, font=('微软雅黑', 12,), bg='#ffa042', fg='black', text='上 一 页',
                               activeforeground='#00FFFF', command=page_last)
                    self.btnup.place(relx=0.42, rely=0.92, width=80, height=30)
                if self.page == self.allpage:
                    self.btnup = Button(self.frameAll, font=('微软雅黑', 12,),  fg='black', text='下 一 页',
                               activeforeground='#00FFFF', command=page_next)
                    self.btnup.place(relx=0.52, rely=0.92, width=80, height=30)
                    for item in range(20-self.tllen//20):
                        placeybug=0.95-item*0.05
                        self.stationtickets_list = Label(self.mylb, font=('微软雅黑', 12), bg='white', bd='9', width=100, height=1, fg='black', anchor='w',
                            text=' ')
                        self.stationtickets_list.place(relx=0,rely=placeybug)
                self.labelnum = Label(self.frameAll, font=('微软雅黑', 12,'bold'), fg='black',
                            text=self.page)
                self.labelnum.place(relx=0.475, rely=0.92, width=20, height=30)
                numtl=0
                self.begin = (self.page-1)*20
                self.end = self.page *20
                for item in self.tickets_list[self.begin:self.end]:
                    placey = numtl*0.05
                    string = '  '
                    for k,v in item.items():
                        if  k!='bookable' and k!='book_btn':
                            string = string + '{:^8}'.format(v)
                    
                    
                    
                    
                    
                    self.stationtickets_list = Label(self.mylb, font=('微软雅黑', 10), bg='white', bd='9', width=90, height=1, fg='black', anchor='w',
                            text=string)
                    self.stationtickets_list.place(relx=0,rely=placey)
                    
                   
                    if item['bookable'] == False:
                        if self.is_future ==True:
                            
                            self.btncheck = Button(self.mylb, font=('微软雅黑', 11),width=9, height=1,  fg='black', text='预  订',
                               activeforeground='#00FFFF', command=check_book_f)
                            self.btncheck.place(relx=0.88,rely=placey)
                        else :
                                 self.btncheck = Button(self.mylb, font=('微软雅黑', 11),width=9, height=1,  fg='black', text='预  订',
                                         activeforeground='#00FFFF', command=check_book_t)
                                 self.btncheck.place(relx=0.88,rely=placey)
                    else :
                        self.btncheck = Button(self.mylb, font=('微软雅黑', 11), width=9, height=1, bg='#ffa042', fg='black', text='预  订',
                               activeforeground='#00FFFF', command=check_book_t)
                        self.btncheck.place(relx=0.88,rely=placey)
                    
                    #strnum = str(numtl)+'  '+string
                    numtl=numtl+1
                    #print('here')
                    #print(self.page)
                    self.mylb.insert(END, self.stationtickets_list)
                    self.mylb.insert(END, self.btncheck)    
            else :
                print('wo zai zhe li')
                    
        self.btnup = Button(self.frameAll, font=('微软雅黑', 12,), bg='#ffa042', fg='black', text='上 一 页',
                               activeforeground='#00FFFF', command=page_last)
        self.btnup.place(relx=0.42, rely=0.92, width=80, height=30)
        self.btndown = Button(self.frameAll, font=('微软雅黑', 12,), bg='#ffa042', fg='black', text='下 一 页',
                               activeforeground='#00FFFF', command=page_next)
        self.btndown.place(relx=0.52, rely=0.92, width=80, height=30)
        self.labelnum = Label(self.frameAll, font=('微软雅黑', 12,'bold'), fg='black',
                            text='-')
        self.labelnum.place(relx=0.475, rely=0.92, width=20, height=30)
        self.labelnum2 = Label(self.frameAll, font=('微软雅黑', 12,'bold'), fg='black',
                            text='/')
        self.labelnum2.place(relx=0.493, rely=0.92, width=10, height=30)
        self.labelnum3 = Label(self.frameAll, font=('微软雅黑', 12,'bold'), fg='black',
                            text='-')
        self.labelnum3.place(relx=0.50, rely=0.92, width=20, height=30)
        
            
        """
            def buyTickets():
                if is_future == true:
                    self.dialog =Dialog(parent)
                    
        """





