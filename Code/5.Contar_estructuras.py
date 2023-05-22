from rdflib import Graph

estructuras=0
anonimizador=1
filtro={}
etiquetas={}
etiqueta={}
vocabularios={}
uri={}

datos = open("Terms_selected.csv" , "r", encoding='utf-8')
linea=datos.readline(); columna = linea.split(";")
while(True):
    linea=datos.readline(); columna = linea.split(";")
    if columna[0]==(""): break
    label=columna[4].replace("\n","")
    filtro.update({label:0})
    filtro.update({columna[0]+":"+columna[1]:0})
    etiquetas.update({label:0})
    etiqueta.update({label:(columna[0]+":"+columna[1])})
datos.close()

datos = open("vocabulariosV4.csv" , "r", encoding='utf-8')
linea=datos.readline(); columna = linea.split(";")
while(True):
    linea=datos.readline(); columna = linea.split(";")
    if columna[0]==(""): break
    uri.update({columna[1]:columna[0]})
    vocabularios.update({columna[0]:0})
datos.close()
            
def parsear(i):
    
    def sujeto(i, text, con):
        global estructuras
        for e in sujetos[i]:
            for a in range(0, len(sujetos[i][e])):
                if con==0:
                    if sujetos[i][e][a] in sujetos and sujetos[i][e][a]!=i:
                        estructuras+=1
                        sujeto(sujetos[i][e][a], text+"   |  ", con+1)  
                if con>0:
                    if sujetos[i][e][a] in sujetos and sujetos[i][e][a]!=i:
                        if "Anonimo" in sujetos[i][e][a] or sujetos[i][e][a] in filtro:
                            sujeto(sujetos[i][e][a], text+"   |  ",con+1)
                       
    def tag(new,i,tipo):
        global anonimizador
        tag=""
        if new in etiqueta:
            tag=etiqueta[new]
            etiquetas[new]+=1
        else:
            if "BNode" in tipo:
                if not(new in anonimos):
                    tag = "Anonimo"+str(anonimizador)
                    anonimos.update({new: tag})
                    anonimizador+=1
                else: tag=anonimos[new]
            elif"Ref" in tipo:
                for i in uri.keys():
                    if i in new:
                        tag= uri[i]
                        text=""
                        for e in new:
                            text+=e
                            if e == "#" or e== "/"  : text=""
                        tag+=":"+text
            elif "Literal" in tipo: tag="Literal"
            else:
                for i in uri.keys():
                    if i in new:
                        tag= uri[i]
                        text=""
                        for e in new:
                            text+=e
                            if e == "#" or e== "/": text=""
                        tag+=":"+text               
        if tag=="": tag="None"
        return (tag)

    sujetos={}
    objetos={}
    anonimos={}
    name="rdf/"+i+".rdf"
    g = Graph()
    g.parse(name)
    for e in g:
        if len(e)==3:
            tag1=tag(str(e[0]),1,str(type(e[0])))
            tag2=tag(str(e[1]),2,str(type(e[1])))
            tag3=tag(str(e[2]),3,str(type(e[2])))
        if tag1 != "None" and tag2 != "None" and tag3 != "None":
            if not(tag1 in sujetos): sujetos.update({tag1: {}})
            if not(tag2 in sujetos[tag1]): sujetos[tag1].update({tag2: []})
            if not(tag3 in sujetos[tag1][tag2]): sujetos[tag1][tag2].append(tag3)

    for i in sorted(sujetos.keys()):
        sujeto(i,"", 0);    
    anonimizador=1
    return estructuras

resultados = open ('Estructuras_detectadas.csv', 'w', encoding='utf-8'); resultados.truncate();
resultados.write("Vocabulario;Estructuras;\n")
for i in sorted(vocabularios.keys()):
    estructuras=0
    try:
        resultado=parsear(i)
        if resultado>0: print(f"{i}: {resultado}")
        if resultado>0: resultados.write(i+";"+str(resultado)+";\n")
    except: None
resultados.close()
    


