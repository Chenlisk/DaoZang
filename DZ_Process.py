import datetime
import os
import re
import sys
import time

def main(base=0):
    path='H:\\WORKSPACE\\DaoZ\\html'
    fileList = os.listdir(path)
    top = len(fileList)

    if base!=0:
        top=base+1

    for i in range(base, top):
        print(datetime.datetime.now(),'--$:',str(i+1).rjust(4,'0'),'/',len(fileList),'---$:',fileList[i])
        data=readFile(path+'\\'+fileList[i])
        data=preProcess(data)
        data=process(data)
        addr='result\\'+fileList[i].replace('html','txt')
        writeFile(addr,data)
        # time.sleep(1)
    
#==========================================================    
def preProcess(data):
    data=getStr(data,'<div class="mw-parser-output">','<div class="printfooter">')

    data=removeNestTag(data,'<table','</table>')
    data=removeNestTag(data,'<ul>','</ul>')
    data=re.sub(r'<ol class="references">(.|\n)+?</ol>','',data)
    data=re.sub(r'<h\d(.|\n)+?</h\d>','\n##HHH\n',data)    #段间分割

    data=re.sub(r'<!--(.|\n)+?-->','\n',data)
    data=re.sub(r'<noscript>(.|\n)+?</noscript>','\n',data)

    data=re.sub(r'\n</p>','</p>\n',data)
    data=re.sub(r'<p>','$P',data)
    data=re.sub(r'&#91;','[',data)
    data=re.sub(r'&#93;',']',data)
    data=re.sub(r'&lt;','',data)
    data=re.sub(r'&gt;','',data)
    data=re.sub(r'<b>\(注\)</b>\d{1,3}','',data)
    
    # data=removeNestTag(data,'<div','</div>')&#91;1&#93;   
    # data=re.sub(r'<a .+?</a>','',data)

    data=re.sub(r'(	|　| )','',data)
    data=re.sub(r'<.+?>','',data)
    data=re.sub(r'\n','',data)
    data=re.sub(r'#\d+','',data)
    data=re.sub(r'(〈|〉)','',data)
    data=re.sub(r'(〔|〕)','',data)
    data=re.sub(r'（.+?）','',data)
    data=re.sub(r'\[.+?\]','',data)

    data=re.sub(r'△','',data)
    data=re.sub(r'[①②③④⑤⑥⑦⑧⑨⑩⑪⑫]','',data)

    lsp=data.split('$P')
    for i in range(0,len(lsp)):
        s=lsp[i]
        
        if s.count('，') + s.count('。') == 0:
            s=''      

        lsp[i]=s        
    data=''.join(lsp)

    data=re.sub(r'##HHH','\n\n',data)
    data=re.sub(r'\n\n+','\n\n',data)
    data=data.lstrip('\n').rstrip('\n')
    return data

def getStr(data,head,tial):
    h=data.find(head)+len(head)
    da=data[h:]
    t =h+da.find(tial)    
    return data[h:t]

def process(data):
    lsp=data.split('\n\n')
    for i in range(0,len(lsp)):
        s=lsp[i]

        if s.count('，') + s.count('。') <= 1:
            s=''      

        if (s.endswith('。') or s.endswith('？') or  s.endswith('！') or  s.endswith('”') or  s.endswith(' 」'))==False:
            if s.count('。') + s.count('，') !=0:
                s+='。'    
            else:
                s=''

        lsp[i]=s        
    data='\n\n'.join(lsp)

    data=re.sub(r'\n\n+','\n\n',data)
    data=data.lstrip('\n').rstrip('\n')
    
    return data

def removeNestTag(data,t_head,t_tail):#delete nest tag
    while data.find(t_head)!=-1:
        h=data.rfind(t_head)
        t=h+data[h:].find(t_tail)
        data=data[0:h]+data[t+len(t_tail):]
    return data

def  readFile(filedir):
    with open(filedir, "r", encoding='utf-8') as f :
        string = f.read()
    return string

def writeFile(filedir,string):
    path = filedir[0:filedir.rfind("\\")]
    if not os.path.exists(path):
        os.makedirs(path) 
    with open(filedir, "w+", encoding='utf-8') as f:
        f.write(string)

#==========================================================
if __name__ == '__main__':
    if len(sys.argv) > 1:
        x = sys.argv[1]
        x = int(x)
        main(x-1)
    else:
        main()
#==========================================================
