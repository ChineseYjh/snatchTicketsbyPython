# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 14:43:08 2018

@author: ChineseYjh
"""
import os
import requests

root = 'info/identify_pics'
img_number = 100
class ScrapeImage():
    
    def scrape_12306(self):
        img_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image'\
        +'?login_site=E&module=login&rand=sjrand'
        if (not os.path.exists(root)):
            os.mkdir(root)
        for i in range(img_number):
            img = requests.get(img_url,verify=False)
            with open(root+'/test'+str(i)+'.jpg','wb') as f:
                f.write(img.content)
            print(str(i) + 'th scrape')
        print('scrape 12306 completes.')
                
if __name__ == '__main__':
    scraper = ScrapeImage()
    scraper.scrape_12306()
    
