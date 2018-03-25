import urllib.request
import requests
import re
import os

#   a='''<li>《<ahref="/wiki/%E5%A4%AA%E4%B8%8A%E5%B0%8E%E5%BC%95%E4%B8%89%E5%85%89%E5%AF%B6%E7%9C%9F%E5%A6%99%E7%B6%93" title="太上導引三光寶真妙經">太上導引三光寶真妙經</a>》一卷</li>
#                         <li>《<a href="/w/index.php?title=%E5%A4%AA%E4%B8%8A%E4%BF%AE%E7%9C%9F%E9%AB%94%E5%85%83%E5%A6%99%E9%81%93%E7%B6%93&amp;action=edit&amp;redlink=1" class="new" title="太上修真體元妙道經（页面不存在）">太上修真體元妙道經</a>》一卷</li>'''

content='/wiki/%E6%AD%A3%E7%B5%B1%E9%81%93%E8%97%8F'
root='https://zh.wikisource.org'

def writeFile(filedir,string):
    if filedir.find('/')!=-1:
        path = filedir[0:filedir.rfind("/")]
        if not os.path.exists(path):
            os.makedirs(path) 
    with open(filedir, "w+", encoding='utf-8') as f:
        f.write(string)

# def getHtml(url):
#     with urllib.request.urlopen(url) as f:
#         data = f.read().decode('utf-8')
#     return data

def requestHtml(url):
    response  = requests.get(url)
    response.enconding = "utf-8"
    return response.text


def Process(data):
    plist=re.findall(r'<li>《<a href=.+?</li>',data)
    print('Sum:',len(plist))

    dic=[]
    for i in range(0,len(plist)):
        s=plist[i]
        if s.find('（页面不存在）')!=-1:
            s='###'+s
            u=None
        else:
            u=re.search(r'href=".+?"',s, re.M|re.I).group()
            u=u.replace('href="','').replace('"','')
            
        s=re.sub(r'</?li>','',s)
        s=re.sub(r'<a href=.+?>','',s)
        s=re.sub(r'</a>','',s)
        s=re.sub(r'\t','',s)

        if (u!=None):
            dic.append({'name':s,'url':root+u})        
        plist[i]=s

    string='\n'.join(plist)
    writeFile('list.txt',string)   
    print('Useful:',len(dic))
    writeFile('dic.txt',str(dic)) 

    for i in range(0,len(dic)):
        u=dic[i]['url']
        n=dic[i]['name']+'.html'
        d=requestHtml(u) 
        writeFile('html/'+n,d)
        print(i+1,'/',len(dic),'  ',n)

def main():
    catalog=requestHtml(root+content)
    writeFile('ztdz.html',catalog)
    Process(catalog)

if __name__ == '__main__':
    main()
    

    




