# -*- coding: big5 -*-
#  Edit 2018/08/19 Ver 1.0.1
#  �[�J��ܬO���O�n�t�~�x�s���x�����Ϥ�
#  ����r�ɪ����|���Ƨ��

from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import requests
import json


headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
print("---�Ѫų����^���{��-��@�����峹��---")
print("---------------------------------")
print("��U�����Ѯɽ��˹�   0. ���S�������r!")
print("1. �����峹�W�٬O�_��������Ƨ��W�٪��r��")
print("2. �����ɩҦb���|���O�_���s�b����Ψ�L�D�^��r��")
print("3. �����峹�O�_�]���K�X")
print("4. �{���Y���`�����Цh����X���A���p���{���]�p�v")
print("---------------------------------")
name = input("�п�J�z���Ѫų����b��(EX: http://XXX.tian.yam.com �h��JXXX): ") 
postID = input("�п�J�z��������峹ID(EX: http://XXX.tian.yam.com/posts/987645 �h��J987645): ")
newImage = input("�аݳ����椤���Ϥ��ݭn�t�~�x�s��? �Фj�g��JY or N (Y/N): ") 

base_url = 'https://' + name + '.tian.yam.com'
SaveDirectory = os.getcwd()
SaveAs = SaveDirectory + '\\TianYam\\'+ name + '\\'
if not os.path.exists(SaveAs):
    os.makedirs(SaveAs)
response = None
response = urlopen(base_url + '/posts/' + postID)
if response == None:
    print(base_url + '/posts/' + postID + '�^������: ���˹������m�O�_���T�A�O�_�i�H�����s�W�Ϊ̭��s����@��(�]���ѪŦ��ɭԩǩǪ�)')
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
# �¤�r����
        f = open(SaveAs + post_title1 + '.txt','w', encoding = 'utf8')
        err=f.write(post_title)
        err=f.write('\r\n')
        err=f.write(post_des)
        err=f.write('\r\n')
        err=f.write(post_content)
        err=f.close();
# ��������
        if not os.path.exists(SaveAs + '\\' + post_title1): #��Ƨ��Screate�L��ܥ��ۥ��٨S���Q����L
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
                            print('oops!: ' + src + '�n���S����! ���˹�Ϥ����}�O�_�ॿ�`�s�W�A�άO�A����@�M(�]���ѪŦ��ɭԩǩǪ�)') 
            h = open(SaveAs + post_title1 + '.htm','w', encoding = 'utf8')
            err=h.write(html)
            err=h.close()
            print(' : �U������!')
        else:
            print(' : ��Ƨ��w�g�s�b!')
    print('Finish!')