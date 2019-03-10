# -*- coding: big5 -*-
#  Edit 2018/08/19 Ver 1.0.1
#  加入選擇是不是要另外儲存網誌內的圖片
#  有文字檔的不會重複抓取

from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import requests
import json


headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
print("---天空部落擷取程式-單一部落文章版---")
print("---------------------------------")
print("當下載失敗時請檢察   0. 有沒有打錯字!")
print("1. 部落文章名稱是否有不能當資料夾名稱的字元")
print("2. 執行檔所在路徑中是否有存在中文或其他非英文字元")
print("3. 部落文章是否設有密碼")
print("4. 程式若異常關閉請多執行幾次，或聯絡程式設計師")
print("---------------------------------")
name = input("請輸入您的天空部落帳號(EX: http://XXX.tian.yam.com 則輸入XXX): ") 
postID = input("請輸入您的部落格文章ID(EX: http://XXX.tian.yam.com/posts/987645 則輸入987645): ")
newImage = input("請問部落格中的圖片需要另外儲存嗎? 請大寫輸入Y or N (Y/N): ") 

base_url = 'https://' + name + '.tian.yam.com'
SaveDirectory = os.getcwd()
SaveAs = SaveDirectory + '\\TianYam\\'+ name + '\\'
if not os.path.exists(SaveAs):
    os.makedirs(SaveAs)
response = None
response = urlopen(base_url + '/posts/' + postID)
if response == None:
    print(base_url + '/posts/' + postID + '擷取不能: 請檢察網站位置是否正確，是否可以直接連上或者重新執行一次(因為天空有時候怪怪的)')
else:
    html = response.read().decode("utf8")
    soup = BeautifulSoup(html, "html.parser")
    response.close()
    if(soup.find('h1')!= None):
        post_title = str(postID) + '_' + soup.find('h1').text
        print(post_title, end = "")
        post_content = soup.find('div',class_ = 'post-content inner').text
        anchors = soup.find_all('li')
        for i in range(0, len(anchors)):
            if anchors[i].has_attr('meta-description'):
                post_des = soup.find_all('li')[i]['meta-description']
                i = len(anchors)
        post_title1 = post_title.replace('/','')
        post_title1 = post_title1.replace('\\','')
        post_title1 = post_title1.replace('*','')
        post_title1 = post_title1.replace(':','')
        post_title1 = post_title1.replace('<','')
        post_title1 = post_title1.replace('>','')
        post_title1 = post_title1.replace('|','')
        post_title1 = post_title1.replace('?','')
        post_title1 = post_title1.replace('.','')
# 純文字部分
        f = open(SaveAs + post_title1 + '.txt','w', encoding = 'utf8')
        err=f.write(post_title)
        err=f.write('\r\n')
        err=f.write(post_des)
        err=f.write('\r\n')
        err=f.write(post_content)
        err=f.close();
# 網頁部分
        if not os.path.exists(SaveAs + '\\' + post_title1): #資料夾沒create過表示本相本還沒有被抓取過
            os.makedirs(SaveAs + '\\' + post_title1)
            if newImage == 'Y':
                nimages = 0;
                anchors = soup.find_all('img')
                for anchor in anchors:
                    src = anchor['src']
                    filetype = src[-3:]
                    if src[0:4] == 'http':
                        filetype = src[-3:]
                        SavePath = '.\\' + post_title1 + '\\' + str(nimages) +'.' + filetype
                        html = html.replace(src, SavePath,1)
                        SavePath = SaveAs + post_title1 + '\\' + str(nimages) +'.' + filetype
                        r = None
                        r = requests.get(src)
                        if r != None:
                            with open(SavePath, 'wb') as file:
                                err=file.write(r.content)
                                err=file.close()
                            nimages=nimages+1
                        else:
                            print('oops!: ' + src + '好像沒抓到喔! 請檢察圖片網址是否能正常連上，或是再執行一遍(因為天空有時候怪怪的)') 
            h = open(SaveAs + post_title1 + '.htm','w', encoding = 'utf8')
            err=h.write(html)
            err=h.close()
            print(' : 下載完成!')
        else:
            print(' : 資料夾已經存在!')
    print('Finish!')