import os
import re
import sys
import random
import requests
import urllib.request
#==========================================================
path='H:\\WORKSPACE\\DaoZ\\html'
root='https://zh.wikisource.org'


def main(base=0):
    # preprocess()

    string=readFile('suburl.txt')
    ulist=string.split('\n')
    top=len(ulist)
    base-=1

    for i in range(base,top):
        name=url=ulist[i]
        url=re.sub(r'<href="','',url)
        url=re.sub(r'" name=.+?>','',url)
        name= re.sub(r'<href.+?name="','',name)
        name=re.sub(r'">','',name)
        name='html_2/'+str(i+1).rjust(4,'0')+'-'+re.sub(r'/','-',name)+'.html'
        data=getHtml(url)    
        writeFile(name,data)
        print(i+1,'/',len(ulist),'  ',name)
    
#==========================================================    
def preprocess():
    fileList = os.listdir(path)
    subUrl=''
    for i in range(0,len(fileList)):
        name=fileList[i]
        print(str(i+1).rjust(3,'0'),'/',len(fileList),'---$: ',name)
        data=readFile(path+'\\'+name)

        h=data.find('<div class="mw-parser-output">')+len('<div class="mw-parser-output">')
        t =data.find('<div class="printfooter">')
        data=data[h:t]
        ulist=re.findall(r'<li><a href=.+?</a></li>',data)
        tlis='\n'.join(ulist)
        subUrl+=tlis+'\n'

    subUrl=re.sub(r'</?li>','',subUrl)
    subUrl=re.sub(r'>.+</a>','>',subUrl)
    subUrl=re.sub(r'<a ','<',subUrl)
    
    subUrl=re.sub(r'/wiki',root+'/wiki',subUrl)
    subUrl=re.sub(r'title','name',subUrl)
    subUrl=re.sub(r'<href=.+?（页面不存在）">','',subUrl)    
    subUrl=re.sub(r'<href=.+?全覽.+?>','',subUrl)    
    subUrl=re.sub(r'\n+','\n',subUrl)
    subUrl=subUrl.lstrip('\n').rstrip('\n')
    
    writeFile('suburl.txt',subUrl)

def getHtml(url):
    with urllib.request.urlopen(url) as f:
        data = f.read().decode('utf-8')
    return data

def requestHtml(url):
    response  = requests.get(url)
    response.enconding = "utf-8"
    return response.text

def  readFile(filedir):
    with open(filedir, "r", encoding='utf-8') as f :
        string = f.read()
    return string

def writeFile(filedir,string):
    if filedir.find('/')!=-1:
        path = filedir[0:filedir.rfind("/")]
        if not os.path.exists(path):
            os.makedirs(path) 
    with open(filedir, "w+", encoding='utf-8') as f:
        f.write(string)
#==========================================================
if __name__ == '__main__':
    if len(sys.argv)>1 :
        x=sys.argv[1]
        x=int(x)
        main(x)
    else:
        print('Please input base number!')
        # main()
#==========================================================
