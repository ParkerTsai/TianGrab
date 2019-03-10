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
print("---天空相本擷取程式-完整相本版---")
print("---------------------------------")
print("當下載失敗時請檢察")
print("1. 相本名稱是否有不能當資料夾名稱的字元")
print("2. 相本是否設有密碼")
print("3. 程式若異常關閉請聯絡程式設計師")
print("---------------------------------")
name = input("請輸入您的天空部落帳號(EX: http://XXX.tian.yam.com 則輸入XXX): ") 
npages = input("請輸入您的相本總頁數: ")


base_url = 'https://' + name + '.tian.yam.com'

page_list =[]
for page in range(1,int(npages)+1):
    response = urlopen(base_url+'/albums?page=' + str(page))
    html = response.read().decode("utf8")
    soup = BeautifulSoup(html, "html.parser")
    anchors = soup.find_all('a')
    for i in range(len(anchors)):
        sub_url = anchors[i]['href']
        if sub_url.find('/album/') == 0:
            new_url = base_url + sub_url
            page_list.append(new_url)
    response.close()

page_list = list(set(page_list))
len(page_list)

for n in range(0,len(page_list)):
    start = page_list[n].find('yam.com/album/')
    albumID = page_list[n][start+14:len(page_list[n])]
    base_url = page_list[n]
    response = urlopen(base_url)
    html = response.read().decode("utf8")
    soup = BeautifulSoup(html, "html.parser");
    response.close()
    anchors = soup.find_all('script')
    SaveDirectory = os.getcwd()
#    if soup.find('h1')==None:
#        album_name = '無標題-可能需密碼?'
#    else:
#        album_name = soup.find('h1').text
#    if soup.find('div',class_ = 'album-des')==None:
#        album_des = '無敘述'
#    else:
#        album_des = soup.find('div',class_ = 'album-des').text
    if soup.find('h1'):
        album_name = soup.find('h1').text
        album_des = soup.find('div',class_ = 'album-des').text
        album_name = album_name.replace('/','')
        album_name = album_name.replace('\\','')
        album_name = album_name.replace('*','')
        album_name = album_name.replace(':','')
        album_name = album_name.replace('<','')
        album_name = album_name.replace('>','')
        album_name = album_name.replace('|','')
        album_name = album_name.replace('?','')
        SaveAs = SaveDirectory + '\\TianYam\\'+ name + '\\' + albumID + '_' + album_name + '\\'
        if not os.path.exists(SaveAs):
            os.makedirs(SaveAs)
            print('Grabbing:'+ album_name +', Saved in :' + SaveAs)
            f = open(SaveAs + 'Album.txt','w', encoding = 'utf8')
            err=f.write(album_name + '\r\n');
            err=f.write(album_des);
            err=f.close();
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
#                if d['photos'][i]['name'] == '':
#                    SavePath = SaveAs + str(nimages)
#                else:
#                    SavePath = SaveAs + d['photos'][i]['name']
                    SavePath = SaveAs + str(nimages) + '.' + filetype
                    with open(SavePath, 'wb') as file:
                        err=file.write(r.content)
                        err=file.close()
                    nimages = nimages +1
                lP = d['lastPage']
                pages = pages + 1
            print(str(nimages) + ' images!')
os.system("pause")


