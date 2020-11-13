# -*- coding: utf-8 -*-
"""
Created on Fri May 18 15:15:21 2018

@author: ChineseYjh
"""
import datetime
import json
from time import sleep
import PIL
import requests
from splinter.browser import Browser
from bs4 import BeautifulSoup as bs
from scrape_the_station_names import getAbbr

class Tickets():
    """
    one object "Tickets" means one person's snatching tickets
    """
    
    def __init__(self,username,pwd):
        """
        Input your username and password to this function to create a object
        
        @para: username,pwd are str
        @return: None
        """
        self.username = username
        self.password = pwd
        self.ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init"
        self.login_page_url = "https://kyfw.12306.cn/otn/login/init"
        self.my_homepage_url = "https://kyfw.12306.cn/otn/index/initMy12306"
        self.browser = Browser(driver_name='chrome',user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36')
        self.captcha_path = 'info/captcha.jpg'
        self.query_logs = []
        self.passengers_list = []
        
    
    def _captcha_identify(self):
        """
# =============================================================================
#         This function will identify the captcha of 12306.
#         The captcha problem in this site is identifying the objects
#         in the given picture then clicking the ones the prompt suggests.
#         On the other hand, this function will get the image by relative path
#         'info/captcha.jpg', identify the corresponding characters and get to 
#         know what to find to click, and identify the eight small pictures in 
#         the overall picture and choose the ones that are conformed to the 
#         desired ones.Then it returns the answer, each two being a pair, meaning
#         the click position
# =============================================================================
        This function will show the users the captcha and format it and return
        the answer.
        @return: str
        """
        answer = ''
        pos_dict={1:"36,47,",
                  2:"110,43,",
                  3:"182,45,",
                  4:"260,44,",
                  5:"36,115,",
                  6:"115,113,",
                  7:"184,113,",
                  8:"264,113,"
                  }
        with PIL.Image.open(self.captcha_path) as img:
            print('Please input the numbers of the pictures in the captcha '
                  +'you want to choose\n(number ranges in [1~8] '
                  +'and please separate them with " "):')
            img.show()
            numbers = input()
            for number in numbers.split(' '):
                answer += pos_dict[int(number)]
        return answer[:-1]
        
        
    def log_in(self):
        """
        This function helps you log in your account in "kyfw.12306.cn",
        it is based on the private functions below:
            (1)_captcha_identify
            (2)_get_passengers
            
        @return: bool, showing whether it succeeds
        """
        self.browser.visit(self.login_page_url)
        s = requests.session()
        headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
        captcha_page = ''
        #deal with captcha-check
        while('4' not in captcha_page):
            s.cookies.clear_session_cookies()
            captcha_get_url = "https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.9670588224384102"
            r = s.get(captcha_get_url)
            with open(self.captcha_path,'wb') as f:
                f.write(r.content)
            captcha = self._captcha_identify()
            captcha_data = {'answer':captcha,'login_site':'E','rand':'sjrand'}
            captcha_check_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
            captcha_page = s.post(captcha_check_url,data=captcha_data,headers=headers,verify=False)
            captcha_page = captcha_page.text
            print(captcha_page)
        print('captcha success')
        #deal with username password
        login_data = {'username':self.username,'password':self.password,'appid':'otn'}
        login_url = "https://kyfw.12306.cn/passport/web/login"
        r = s.post(login_url,data=login_data,headers=headers,verify=False)
        j = json.loads(r.text)
        if(j["result_message"] != "登录成功"):
            return False
        #if successful, it continues to get cookies
        print("username and password are both right")
        url1 = "https://kyfw.12306.cn/otn/login/userLogin"
        r = s.post(url1,data={'_json_att':''},headers=headers,verify=False)
        #print(r.text)
        url2 = "https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin"
        r = s.get(url2,headers=headers,verify=False)
        #print(r.text)
        url3 = "https://kyfw.12306.cn/passport/web/auth/uamtk"
        r = s.post(url3,data={'appid':'otn'},headers=headers,verify=False)
        #print(r.text)
        j = json.loads(r.text)
        url4 = "https://kyfw.12306.cn/otn/uamauthclient"
        r = s.post(url4,data={'tk':j['newapptk']},headers=headers,verify=False)
        #print(r.text)
        url5 = url1
        r = s.get(url5,headers=headers,verify=False)
        #print(r.text)
        r = s.get(self.my_homepage_url,headers=headers,verify=False)
        #print(r.text)
        #submit the cookies to the chromedriver
        self.browser._cookie_manager.add(s.cookies)
        self.browser.visit(self.my_homepage_url)
        sleep(1)
        if(self.browser.url != self.my_homepage_url):
            raise Exception("The process of getting cookies gets wrong.")
        print('log in successfully')
        return True
    
    def reset_info(self,new_username,new_pwd):
        """
        This function allows you to reset the information of the users.
        It aims to deal with the circumstances such as:
            (1)The user inputs the wrong information and can't log in the site
            (2)...
        @para: new_username, new_pwd are str
        @return: None
        """
        #So far it is only suitable before you log in
        self.username = new_username
        self.password = new_pwd
       # self.query_logs = []
        
    def _get_passengers(self):
        """
        This function get the list of the names of the contacts of the user,
        and the names contain brackets and "学生" when he/her is a student
        @return: list(str)
        """
        self.browser.visit("https://kyfw.12306.cn/otn/passengers/init")
        soup = bs(self.browser.html,"html.parser")
        tr_list = soup.find("tbody",id="passengerAllTable").find_all("tr")
        passengers_list = []
        for tr in tr_list:
            td_list = tr.find_all("td")
            for i in range(len(td_list)):
                if (i % 8 == 1):
                    name = str(td_list[i].string)
                elif (i % 8 ==5):
                    if("学生" in td_list[i]):
                        name = name + "(学生)"
                    passengers_list.append(name)
        return passengers_list
        
    def _query(self,from_station,to_station,date):
        """
        This function queries the site of the information belows:
            where do you start? (it can be city name or station name)
            where is your destination? (it can be city name or station name)
            what date is it for you to depart? (eg. 2018-01-28)
        And it makes the browser, Chrome, loads the query page and returns the
        correspoding html of the page
        Note: the date format must be corrected before being the the argument, 
        and the date should never be out of the bookable time bound. If the date
        is out of the bookable time bound, it will return a default page given
        by the site as the one when we input the out-bound date by hand. Often 
        it's the tickets page whose date is the lower bound of the bookable 
        bound.
        
        @para: from_station, to_station, date are str
        @return: str
        """
        self.browser.visit(self.ticket_url)
        try :
            #initiate the date
            self.browser.cookies.add({'_jc_save_fromDate':date})
            self.browser.reload()
            #cope with exception from the input format error
            from_station_abbr = getAbbr(from_station)
            to_station_abbr = getAbbr(to_station)
            if(from_station_abbr == ''):
                raise Exception("The from_station doesn't exist")
            if (to_station_abbr == ''):
                raise Exception("The to_station doesn't exist")
            #initiate the from_station
            self.browser.evaluate_script(
                    'document.getElementById("fromStation").value="'
                    + from_station_abbr + '"'
                    )
            #initiate the to_station
            self.browser.evaluate_script(
                    'document.getElementById("toStation").value="'
                    + to_station_abbr + '"'
                    )
            #query with clicking the button
            self.browser.find_link_by_text('查询').click()
            sleep(3)
            return self.browser.html
    # =============================================================================
    #             query_url = "https://kyfw.12306.cn/otn/leftTicket/query?"
    #             + "leftTicketDTO.train_date=" + date
    #             + "&leftTicketDTO.from_station=" + from_station_abbr
    #             + "&leftTicketDTO.to_station=" + to_station_abbr
    #             + "&purpose_codes=ADULT"
    # =============================================================================
        except :
            print("Error. The browser will quit soon.")
            self.browser.screenshot(name='error_of_fun_query')
            self.browser.quit()
            raise
    
    def _prettify_html(self,html):
        '''
        This function get the information of the train out of the html
        
        @para: html is str
        @return: list(dict()), attention: it's [{}] when no thing is found,
        and the structure of dict() is as follows:
            tickets_dict = {
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
                 #if it's unbookable, it'll be None
                }
        '''
        if(html == ''):
            return [{}]
        tickets_list = []
        book_btn_list = self.browser.find_link_by_text('预订')
        book_btn_list_ptr = 0;
        soup = bs(html,'html.parser')
        tr_list = soup.find('tbody',id='queryLeftTable').find_all('tr')
        #there are no tickets at all
        if (tr_list == []):
            return [{}]
        for tr in tr_list:
            td_table = tr.find_all('td')
            #when <tr> has <td>
            if(td_table != []):
                tickets_dict = {
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
                'book_btn':None#if it's unbookable, it'll be None
                }
                #update the tickets_dict
                #the first <td>
                info_list = [td for td in td_table[0].strings]
                if(' 'in info_list):
                    info_list.remove(' ')
                info_list.remove('查看票价')
                del info_list[len(info_list) - 1]#delete "当/次日到达"
                tickets_dict['trainNumber'] = info_list[0]
                tickets_dict['fromStation'] = info_list[1]
                tickets_dict['toStation'] = info_list[2]
                tickets_dict['departTime'] = info_list[3]
                tickets_dict['arriveTime'] = info_list[4]
                tickets_dict['period'] = info_list[5]
                #the following <td>s except the last one
                tickets_dict['specialSeat'] = td_table[1].string
                tickets_dict['oneClassSeat'] = td_table[2].string
                tickets_dict['twoClassSeat'] = td_table[3].string
                tickets_dict['advancedSoftSleeper'] = td_table[4].string
                tickets_dict['softSleeper'] = td_table[5].string
                tickets_dict['hardSleeper'] = td_table[6].string
                tickets_dict['motionSleeper'] = td_table[7].string
                tickets_dict['softSeat'] = td_table[8].string
                tickets_dict['hardSeat'] = td_table[9].string
                tickets_dict['noSeat'] = td_table[10].string
                if(td_table[12].find('a') != None):
                    tickets_dict['bookable'] = True
                    tickets_dict['book_btn'] = book_btn_list[book_btn_list_ptr]
                    book_btn_list_ptr = book_btn_list_ptr + 1
                else:
                    tickets_dict['bookable'] = False
                    tickets_dict['book_btn'] = None
                tickets_list.append(tickets_dict)
                del tickets_dict
        return tickets_list
    
    def _book(self,button,passengers_list):
        """
        This function will book the ticket which the button belongs to for the
        passengers in the passengers_list. If it succeeds, it returns True
        
        @para: button is <splinter.driver.webdriver.WebDriverElement>
               and passengers_list is list(str)
        @return: bool
        """
        try:
            button.click()
            #book_url = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"
            #if (self.browser.url != book_url):
            #    raise Exception("The button fails.")
            #we have entered the booking page
            #and we click all the passengers
            for passenger in passengers_list:
                #we click the last according to the structure of the webpage
                print(passenger)
                #print(self.browser.html)
                while(self.browser.is_element_not_present_by_text(passenger)):
                    pass
                self.browser.find_by_text(passenger).last.click()
                #consider the case where the passenger is a student
                #and a window will alert, we need to cope with it
                if ("学生" in passenger):
                    self.browser.find_by_id("dialog_xsertcj_ok").last.click()
            self.browser.find_link_by_text("提交订单").first.click()
            #cope with window alert again
            while(self.browser.is_element_not_visible_by_xpath('//*[@id="qr_submit_id"]')):
                pass
            self.browser.find_by_id("qr_submit_id").first.click()
# =============================================================================
#             success_url_text = "https://kyfw.12306.cn/otn//payOrder/init"
#             if (success_url_text in self.browser.url):
#                 print("book the ticket(s) successfully!")
#                 return True
#             else:
#                 raise Exception("Browser fails to load into the paying page.")
# =============================================================================
            print("book the ticket(s) successfully!")
            return True
        except:
            print("Exception is raised in the booking process.")
            self.browser.screenshot(name="error_of_fun_book")
            raise
            return False
        
    def get_tickets_info(self,from_station,to_station,date,is_future=False):
        """
        This function is based on the private function:
            (1)_query
            (2)_prettify_html
        This function will log what the user query and the parameter date is
        able to be out of bookable time bound with only one day, so we set a
        new boolean parameter is_future to show whether the date is out of 
        the bookable time bound
        
        @para: from_station,to_station,date are str, is_future is bool
        @return: list(dict())
        """
        d = datetime.datetime(int(date.split('-')[0]),
                              int(date.split('-')[1]),
                              int(date.split('-')[2]))
        #information goes into the query_logs
        self.query_logs.append({'from_station' : from_station
                                ,'to_station' : to_station
                                ,'date' : date
                                ,'is_future' : is_future
                                ,'query_time': str(d.today())})
        if (is_future):
            #we get the date minus one day
            d -= datetime.timedelta(days = 1)
            date = str(d).split(' ')[0]
        html = self._query(from_station,to_station,date)
        tickets_list = self._prettify_html(html)
        #remember to set all tickets unbookable if it's in future
        if (is_future):
            for ticket in tickets_list:
                ticket['bookable'] = False
                ticket['book_btn'] = None
        return tickets_list
    
    def book_tickets_on_sale(self,tickets_dict,date,passengers_list):
        """
        This function is based on the private function below:
            (1)_book
        This function aims to book the tickets that are in the BOOKABLE time
        bound, which means that the page for the tickets is shown on the site. 
        If the tickets are not on sale or sold out, then we repeat reloading the 
        page and let this function watch over the page until the it finds the
        tickets available again, so when someone else refunds the tickets
        we can book the tickets at once. And if the tickets have remainders,
        we can book it at once, too.
        
        @para: tickets_dict is dict, passengers_list is list(str),date is str
            the structure of the dict is as follows:
            tickets_dict = {
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
                 #if it's unbookable, it'll be None
                }
        @return: bool, showing whether it succeeds booking the tickets
        """
        if (tickets_dict["bookable"] == True):
            #now it has remainders
            self._book(tickets_dict["book_btn"],passengers_list)
            return True
        else:
            #it is sold out now, we query again to see whether it's available
            html = self._query(tickets_dict["fromStation"],
                        tickets_dict["toStation"],
                        date)
            tickets_list = self._prettify_html(html)
            trial_times = 0
            while (True):
                #only when it's available we break out of the loop
                #every loop means one times to query
                book_btn = None
                trial_times += 1
                print(str(trial_times)+"th tries.")
                for ticket in tickets_list:
                    if (ticket["trainNumber"] == tickets_dict["trainNumber"]
                    and ticket["departTime"] == tickets_dict["departTime"]
                    and ticket["bookable"] == True):
                        book_btn = ticket["book_btn"]
                        break
                #if we find it bookable
                if (book_btn != None):
                    self._book(book_btn,passengers_list)
                    break
                #else we query again, but before query we need to sleep
                sleep(3)
                self.browser.find_link_by_text("查询").first.click()
                sleep(1)
                tickets_list = self._prettify_html(self.browser.html)
            return True
        
    def book_tickets_in_future(self,tickets_dict,date,passegers_list,hour=8,minute=0):
        """
        This function is based on the private function below:
            (1)_book
            (2)book_tickets_on_sale
        This function aims to book the tickets that are in the UNBOOKABLE time
        bound, and the date only exceeds the bound by one day. So we calculate
        the duration between now and the time user wants us to begin snatching
        (tomorrow hour:minute:00 we will wake up and start checking and snatching),
        and we let it sleep until the time is up. Then we query the site to see 
        whether the tickets are offered. And if they're offered, we can use the
        private function (2)book_tickets_on_sale to get the tickets!
        
        @para: tickets_dict is dict, passengers_list is list(str),date is str
               hour and minute are int
            the structure of the dict is as follows:
            tickets_dict = {
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
                 #if it's unbookable, it'll be None
                }
        @return: bool, showing whether it succeeds booking the tickets
        """
        #wait until the tickets are available
        snatch_time = datetime.datetime(int(date.split('-')[0]),
                                        int(date.split('-')[1]),
                                        int(date.split('-')[2]),
                                        hour,minute,0)
        #the duration between now and the snatch-time(default tomorrow 8:00)
        duration = snatch_time - snatch_time.today()
        sleep(int(duration.total_seconds()) + 1)
        #time seems to be up
        #then we need to check whether the tickets are available
        date_in_Chinese_format = (date.split('-')[1] + '月' 
                                    + date.split('-')[2] + '日')
        trial_times = 0
        while (True):
            html = self._query(tickets_dict['fromStation'],
                    tickets_dict['toStation'],
                    date)
            trial_times += 1
            print(str(trial_times) + 'th tries.')
            soup = bs(html,'html.parser')
            if (date_in_Chinese_format
                in str(soup.find('div',id="sear-result"))):
                print("The tickets page is available now! we'll buy it now!")
                break
            sleep(5)#after 5s we check again 
        #since the tickets are available, we can buy it
        self.book_tickets_on_sale(tickets_dict,date,passegers_list)
        return True
        
    def __del__(self):
        """
        Remember to quit the browser
        
        @return: None
        """
        self.browser.quit()
    
def main():
    t = Tickets('','')
    t.log_in()
    
if __name__ == '__main__':
    main()
    
    
        
        
        
        
