from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import ssl

resultado = open ('VocabulariosV4.csv', 'w', encoding='utf-8'); resultado.truncate();
resultado.write ('Vocabulario;Uri;Respuesta;Acceso;Tag;\n')
##CARGA TODOS LOS VOCABULARIOS Y URI'S DE LOV
voc={}
tag={}
con=0
url = 'https://lov.linkeddata.es/dataset/lov/api/v2/vocabulary/list'
data = requests.get(url)
if data.status_code == 200:
    data = data.json()
    for i in data:
        con+=1
        voc.update({i["prefix"] : i["uri"]})
    print(f'Vocabularios cargados : {con}')
else: print('Error en la uri de vocabularios\nIntentelo de nuevo más tarde')

##CARGA RESPUESTA URI Y CARGA LAS ETIQUETAS
con=0
for i in voc.keys():
    url = "https://lov.linkeddata.es/dataset/lov/api/v2/vocabulary/info?vocab="+i
    data = requests.get(url)
    if data.status_code == 200:
        data = data.json()
        tags=data['tags']
        try:
            req=requests.get(voc[i], timeout=5)
            aux = req.status_code
        except:
            aux=504
        text=i+';'+voc[i]+';'+str(aux)+";"
        try:
            if aux == 200 :
                other = Request(voc[i], headers={'User-Agent': 'Mozilla/5.0'})
                soup =  BeautifulSoup(urlopen(other, timeout=5, context=ssl.SSLContext()).read())
                text+="si;"
            else:
                text+="no;"                
        except:
                text+="no;"
        for e in range(0,len(tags)):
            if not(tags[e] in tag): tag.update({tags[e]:[]})
            tag[tags[e]].append(i)
            text+=tags[e]+";"
        text+='\n'
        print(text)
        con+=1
        resultado.write(text)
        #print(f"{con} - {i} - {aux} - {valor} : {tags}")
    else: print('Error en la uri de etiquetas\nIntentelo de nuevo más tarde')
print(f'Etiquetas diferentes cargadas : {len(tag)}')
resultado.close()
for i in sorted(tag.keys()):
    print(f'{i} : {len(tag[i])}')
print('Datos guardados en Vocabularios.csv')
