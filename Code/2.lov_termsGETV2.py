from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from datetime import datetime
from os import startfile
import ssl

resultado = open ('Terms.csv', 'w', encoding='utf-8'); resultado.truncate();
resultado.write ('CLASE;TIPO;REFERENCIAS;DATASETS;DOCUMENTACION')
for page in range (0,7669):
    req = Request(url=('https://lov.linkeddata.es/dataset/lov/terms?&page='+str(page)), headers={'User-Agent': 'Mozilla/5.0'})
    soup =  BeautifulSoup(urlopen(req, context=ssl.SSLContext()).read())
    tags=soup('a')
    con=0; robin=0; actual=[]
    for i in tags:
        con+=1
        if con>5 and con<46:
            robin+=1
            aux=i.getText().strip()
            if robin==1:
                for i in range(0,len(aux)):
                    if aux[i]==":": tipo=aux[i+1:]; break
            elif robin==2: clase=aux
            elif robin==3:
                aux=aux.replace(",","")
                valor=""; lod=""; espacios=0
                if len(aux)>20:
                    for i in range(0,len(aux)):
                        if aux[i]==" ": espacios+=1
                        if espacios==0: valor+=aux[i]
                        if espacios==3: lod+=aux[i]
                        if espacios==4: break
                    valor=int(valor); lod=int(lod)
                else: valor=0; lod=0
            else: resultado.write(clase+";"+tipo+";"+str(valor)+";"+str(lod)+";"+aux+";\n")
            if robin==4:robin=0
    print(page)
resultado.close()



