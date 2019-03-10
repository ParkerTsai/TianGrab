# -*- coding: big5 -*-
#  Edit 2018/08/14 Ver 1.0.0
#  LogIn/password
#  discription

from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import requests
import json

headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
print("---天空相本擷取程式-單一相本版---")
print("---------------------------------")
print("當下載失敗時請檢察")
print("1. 相本名稱是否有不能當資料夾名稱的字元")
print("2. 相本是否設有密碼")
print("3. 程式若異常關閉請聯絡程式設計師")
print("---------------------------------")
name = input("請輸入您的天空部落帳號(EX: http://XXX.tian.yam.com 則輸入XXX): ") 
nalbum = input("請輸入您想抓取的相本ID(EX: http://XXX.tian.yam.com/987645 則輸入987645): ")

albumID = nalbum
base_url = 'https://' + name + '.tian.yam.com/album/' + albumID
response = urlopen(base_url)
html = response.read().decode("utf8")
soup = BeautifulSoup(html, "html.parser");
response.close()
SaveDirectory = os.getcwd()
SaveAs = SaveDirectory + '\\TianYam\\'+ name + '\\' + albumID + '\\'
if not os.path.exists(SaveAs):
    os.makedirs(SaveAs)
print('Grabbing:'+ base_url +', Saved in :' + SaveAs)
fetch_url = 'https://' + name + '.tian.yam.com/ajax/album/fetch'
lP = False
pages = 1
nimages = 0
while lP == False:
    res = requests.post(fetch_url,headers = headers, data = {'albumId':albumID,'page':str(pages)})
    res.close()
    d = json.loads(res.text)
    for i in range(0,len(d['photos'])):
        r = requests.get(d['photos'][i]['url'])
        filetype = d['photos'][i]['url'][-3:]
        SavePath = SaveAs + str(nimages) + '.' + filetype
        with open(SavePath, 'wb') as file:
            err=file.write(r.content)
            err=file.close()
        nimages = nimages +1
    lP = d['lastPage']
    pages = pages + 1
print(str(nimages) + ' images!')





