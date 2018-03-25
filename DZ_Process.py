import os
import re
import sys
#==========================================================
def main():
    path='H:\\WORKSPACE\\DaoZ\\html'
    fileList = os.listdir(path)
    for i in range(0,len(fileList)):
        print(str(i+1).rjust(3,'0'),'/',len(fileList),'---$: ',fileList[i])
        data=readFile(path+'\\'+fileList[i])
        data=preprocess(data)
        if data!=None:
            addr='result\\'+fileList[i].replace('html','txt')
            writeFile(addr,data)
    
#==========================================================    
def preprocess(data):
    h=data.find('<div class="mw-parser-output">')+len('<div class="mw-parser-output">')
    t =data.find('<div class="printfooter">')
    data=data[h:t]

    data=removeNestTag(data,'<table','</table>')
    data=re.sub(r'\n','',data)
    data=re.sub(r'<h\d(.|\n)+?</h\d>','\n',data)
    data=re.sub(r'<noscript>(.|\n)+?</noscript>','\n',data)
    data=re.sub(r'<!--(.|\n)+?-->','\n',data)

    data=re.sub(r'<div class="toctitle"(.|\n)+?</div>','',data)
    data=re.sub(r'<div id="toc" class="toc">(.|\n)+?</div>','',data)
    data=re.sub(r'<div class="thumb(.|\n)+?</div>','',data)
    data=re.sub(r' <a href="/wiki(.|\n)+?<img alt(.|\n)+?</a>','',data)
    data=re.sub(r'<a href=(.|\n)+?title=(.|\n)+?>','',data)
    data=re.sub(r'<ol class="references">(.|\n)+?</ol>','',data)
    data=re.sub(r'<sup id="cite_ref(.|\n)+?</a></sup>','',data)

    # data=re.sub(r'：</p>','：',data)
    # data=re.sub(r'，</p>','，',data)
    data=re.sub(r'</p>','\n\n',data)
    data=re.sub(r'<p>','',data) 
    # data=re.sub(r'：</li>','：',data)
    # data=re.sub(r'，</li>','，',data)
    # data=re.sub(r'</li>','\n\n',data)

    data=re.sub(r'（.+?）','',data)
    data=re.sub(r'<span(.|\n)+?>','',data)
    data=re.sub(r'</span>','',data) 
    data=re.sub(r'<br />','',data)
    data=re.sub(r'</div>','',data)     
    data=re.sub(r'</a>','',data)   
    data=re.sub(r'(	|　| )','',data)  
    data=re.sub(r'[<>〈〉]','',data)   

    data=re.sub(r'&lt;','<',data)   
    data=re.sub(r'&gt;','>',data)

    data=re.sub(r'\n\n+','\n\n',data)
    data=re.sub(r'：\n\n','：',data)
    data=re.sub(r'，\n\n','，',data)
    data=data.lstrip('\n').rstrip('\n')


    lsp=data.split('\n\n')
    for i in range(0,len(lsp)):
        s=lsp[i]

        s=s.replace('\n','')
        
        # if (s.endswith('。') or s.endswith('？') or  s.endswith('！') or  s.endswith('」') or s.endswith('』'))==False:
        #     if s.count('。') > 5 and s.count('，') > 5:
        #         s+='。'    
        #     else:
        #         s=''
        if s.count('，') == 0 and s.count('。') == 0:
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
    main()
#==========================================================
