# -*- coding: utf-8 -*-
"""
Created on Sun May 13 13:59:05 2018

@author: ChineseYjh
"""
from requests import get
import os

station_names_url = "https://kyfw.12306.cn/otn/resources/js/framework"\
+ "/station_name.js?station_version=1.9053"
dir_path = "info/"
file_path = dir_path + "station_names.txt"

#scrape information from the page
#note: return str
def scrapeInfo(url):
    try:
        r = get(url,headers={"user-agent":"Mozilla/5.0"},verify=False)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        print("error from function 'scrapeInfo'")
        return ''
    
#make the information neat in the dictionary
#note: text is str, return dict
def prettifyInfo(text):
    if (text == ''):
        print("error from function 'prettifyInfo'")
        return {}
    infoList = text.split('|')
    infoDict = {}
    for i in range(len(infoList)):
        if (i % 5 == 1):
            address = infoList[i]
        elif (i % 5 == 2):
            abbr = infoList[i]#station abbreviation
            infoDict[address] = [abbr]
        elif(i % 5 == 3):
            initial = infoList[i][0].upper()#the initial of the station name
            infoDict[address].append(initial)
    return infoDict

#store the information into a text file called "station_names"
#note: dictInfo is dict, return bool
def storeInfo(dictInfo):
    if (dictInfo == {}):
        print("error from function 'storeInfo'")
        return False
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    makeFile = True
    if os.path.exists(file_path):
        print("The text file has existed. Would you get it updated?")
        if((input('Input "yes" if you want '
                  +'or "no" if you don\'t\n')).lower() == "no"):
            makeFile = False
    if(makeFile):
        with open(file_path,'w') as f:
            for address, abbr_initial in dictInfo.items():
                f.write(address + ':' + abbr_initial[0]
                + ',' + abbr_initial[1] + '\n')
    return makeFile

#get the initial of the station name
def getInitial(station_name):
    initial = ''
    with open(file_path) as f:
        for i in f.readlines():
            if (i.split(':')[0] == station_name):
                initial = i.split(',')[1].strip()
                break;
    return initial

#get the abbr of the station name
def getAbbr(station_name):
    abbr = ''
    with open(file_path) as f:
        for i in f.readlines():
            #print(i)
            if (i.split(':')[0] == station_name):
                abbr = i.split(':')[1].split(',')[0]
                break;
    return abbr

def main():
    station_names_text = scrapeInfo(station_names_url)
    station_names_dict = prettifyInfo(station_names_text)
    if (storeInfo(station_names_dict)):
        print("Complete")

if __name__ == "__main__":
    main()

