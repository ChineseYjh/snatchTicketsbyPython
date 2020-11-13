# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 21:28:30 2018

@author: ChineseYjh
"""
import os
import PIL
import requests
import re
import json

def captcha(img_path):
    captcha = ""
    pos_dict={1:"36,47,",
              2:"110,43,",
              3:"182,45,",
              4:"260,44,",
              5:"36,115,",
              6:"115,113,",
              7:"184,113,",
              8:"264,113,"
              }
    numbers = []
    with PIL.Image.open(img_path) as img:
        #get the keyword, less accurate
        keyword_box = (120,0,290,25)
        keyword_img = img.crop(keyword_box)
        file_name = 'temp_waste.jpg'
        keyword_img.save(file_name)
        s = requests.session()
        r = s.post("http://cn.docs88.com/pdftowordupload2.php",
                   data={'Filename':file_name,'sourcename': file_name,
                         'sourcelanguage': 'cn','desttype': 'txt',
                         'Upload': 'Submit Query'},
                   files={'Filedata':open(file_name,'rb')})
        rr = s.get('http://cn.docs88.com/'+r.text[3:])
        rr.encoding = 'utf-8'
        keyword = rr.text.strip()
        print("The keyword:", keyword)
        #identify the 8 pictures, more accurate
        pictures_list = []
        for row in range(2):
            for col in range(4):
                pictures_list.append(
                        img.crop((col*73,40+row*73,(col+1)*73,40+(row+1)*73)))
        count = 0
        for picture in pictures_list:
            count += 1
            picture.save(file_name)
            #get the queryString--vs  
            vs_page = s.get('http://image.baidu.com/?fr=shitu',
            headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'},
            verify=False).text 
            vs_id=re.findall('window.vsid = "(.*?)"',vs_page)[0]
            #upload the picture
            r = s.post("https://image.baidu.com/pcdutu/a_upload?fr=html5&target=pcSearchImage&needJson=true"
                       ,data={'pos':'upload','uptype':'upload_pc','fm':'home'}
                       ,files={'file':open(file_name,'rb')},headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
                       ,verify=False)
            j = json.loads(r.text)
            #check the result
            url = 'http://image.baidu.com/pcdutu?queryImageUrl='+j['url']+'&querySign='+j['querySign']+'fm=index&uptype=upload_pc&result=result_camera&vs='+vs_id
            r = s.get(url,headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
            ,verify=False)
            r.encoding = 'utf-8'
            picture_keywords = re.findall('"keyword":"(.*?)"',r.text)
            for picture_keyword in picture_keywords:
                print('The picture description:', picture_keyword)
                for word in keyword:
                    if (word in picture_keyword):
                        numbers.append(count)
                        break
        for number in numbers:
            captcha += pos_dict[number]
        return keyword,captcha[:-1]

def main():
# =============================================================================
#     path = 'info/captcha_tests/'
#     for i in range(101):
#         keyword, answer = captcha(path+'test'+str(i)+'.jpg')
#         os.rename(path+'test'+str(i)+'.jpg',
#                   path+'test'+str(i)+keyword+'+'+answer+'.jpg')
# =============================================================================
    s = requests.session()
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
    captcha_get_url = "https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.9670588224384102"
    r = s.get(captcha_get_url)
    with open('info/captcha.jpg','wb') as f:
        f.write(r.content)
    answer = captcha('info/captcha.jpg')
    captcha_data = {'answer':answer,'login_site':'E','rand':'sjrand'}
    captcha_check_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
    captcha_page = s.post(captcha_check_url,data=captcha_data,headers=headers,verify=False)
    captcha_page = captcha_page.text
    print(captcha_page)
    
if __name__ == '__main__':
    main()
        
