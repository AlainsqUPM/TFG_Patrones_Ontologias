from os import startfile
from rdflib import Graph

anonimizador=1
filtro={}
etiquetas={}
etiqueta={}
sujetos={}
anonimos={}
conAnonimo={}
uri={}
show={}
vocabularios={}
visitado=[]

def ex(fichero): startfile(fichero+".txt")

datos = open("file/Terms_selected.csv" , "r", encoding='utf-8')
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

datos = open("file/Terms_selectedTUTOR.csv" , "r", encoding='utf-8')
linea=datos.readline(); columna = linea.split(";")
while(True):
    linea=datos.readline(); columna = linea.split(";")
    if columna[0]==(""): break
    show.update({columna[0]+":"+columna[1]:0})
datos.close()

datos = open("file/vocabulariosV4.csv" , "r", encoding='utf-8')
linea=datos.readline(); columna = linea.split(";")
while(True):
    linea=datos.readline(); columna = linea.split(";")
    if columna[0]==(""): break
    uri.update({columna[1]:columna[0]})
    vocabularios.update({columna[0]:0})
datos.close()
            
def parsear(i):
    def tag(new,i,tipo):
        global anonimizador
        tag=""
        text=""
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
                        for e in new:
                            text+=e
                            if e == "#" or e== "/"  : text=""
                        tag+=":"+text
                    else:
                        for e in new:
                            text+=e
                            if e== "/" or e == "#": text=""
                        tag="#"+text                  
            elif "Literal" in tipo:tag="Literal ["+new+"]"
        if tag=="":
            tag="None"
            print(f"{i}-{new}-{tipo}")
        return (tag)

    name="rdf/"+i+".rdf"
    g = Graph()
    g.parse(name)
    for e in g:
        if len(e)==3:
            tag1=tag(str(e[0]),1,str(type(e[0])))
            tag2=tag(str(e[1]),2,str(type(e[1])))
            tag3=tag(str(e[2]),3,str(type(e[2])))
            #print(f"{tag1} -> {tag2} -> {tag3}")
        if tag1 != "None" and tag2 != "None" and tag3 != "None":
            if not(tag1 in sujetos): sujetos.update({tag1: {}})
            if not(tag2 in sujetos[tag1]): sujetos[tag1].update({tag2: []})
            if not(tag3 in sujetos[tag1][tag2]): sujetos[tag1][tag2].append(tag3)
            if "Anonimo" in tag3: conAnonimo.update({tag1:0})

def showReal(i, text, c):
    if not(i in visitado):
        visitado.append(i)
        if c == 0: resultados.write(text+i+"\n")
        for e in sorted(sujetos[i].keys()):
            if e in show.keys() and e!="rdfs:type":
                 for a in sorted(sujetos[i][e]):
                    resultados.write(text+"  |"+e+"\n")
                    resultados.write(text+"  |  |"+a+"\n")
                    if a in sujetos and a!=i and not("#" in a):
                        showReal(a, text+"  |  |", 1)

def showTipo(i, text, c):
    if not(i in visitado):
        visitado.append(i)
        if c == 0:
            try:resultad.write(text+sujetos[i]["rdfs:type"][0]+"\n")
            except:
                print(sujetos[i])
                if "Anonimo" in i: resultad.write(text+"Anonimo"+"\n")
                elif "#" in i: resultad.write(text+"#Desconocido"+"\n")
                elif "Literal" in i: resultad.write(text+"Literal"+"\n")
                else: resultad.write(text+i+"\n")     
        for e in sorted(sujetos[i].keys()):
            if e in show.keys() and e!="rdfs:type":
                for a in sorted(sujetos[i][e]):
                    resultad.write(text+"  |"+e+"\n")
                    try:
                        if "#" in sujetos[a]["rdfs:type"][0]:resultad.write(text+"  |  |#Desconocido\n")
                        elif "Anonimo" in sujetos[a]["rdfs:type"][0]:resultad.write(text+"  |  |Anonimo\n")
                        else: resultad.write(text+"  |  |"+sujetos[a]["rdfs:type"][0]+"\n")
                    except:
                        if "Anonimo" in a: resultad.write(text+"  |  |"+"Anonimo"+"\n")
                        elif "#" in a: resultad.write(text+"  |  |"+"#Desconocido"+"\n")
                        elif "Literal" in a: resultad.write(text+"  |  |"+"Literal"+"\n")
                        else: resultad.write(text+"  |  |"+a+"\n")
                    if a in sujetos and a!=i and not("#" in a):
                        showTipo(a, text+"  |  |", 1)

result = open ("Result.csv", 'w', encoding='utf-8'); result.truncate();
result.write("Vocabulario;Encontrados;\n")
resultad = open ("Tipos.txt", 'w', encoding='utf-8'); resultad.truncate();
resultados = open ("Original.txt", 'w', encoding='utf-8'); resultad.truncate();
for name in vocabularios:
    try:
        doit={}
        sujetos.clear()
        anonimos.clear()
        anonimizador=1
        parsear(name)
        contador=0
        for e in sorted(sujetos.keys()):
            if "rdfs:subClassOf" in sujetos[e]:
                for a in sorted(sujetos[e]["rdfs:subClassOf"]):
                    if a in sujetos and "Anonimo" in a:
                        contador+=1
                        visitado=[]
                        resultados.write("\n")
                        resultados.write(e+"\n")
                        resultados.write("  |rdfs:subClassOf\n")
                        showReal(a,"  |  |",0)
                        resultad.write("\n")
                        resultad.write("owl:Class\n")
                        resultad.write("  |rdfs:subClassOf\n")
                        visitado=[]
                        showTipo(a,"  |  |",0)
            if "owl:equivalentClass" in sujetos[e]:
                for a in sorted(sujetos[e]["owl:equivalentClass"]):
                    if a in sujetos and "Anonimo" in a:
                        contador+=1
                        visitado=[]
                        resultados.write("\n")
                        resultados.write(e+"\n")
                        resultados.write("  |rdfs:subClassOf\n")
                        showReal(a,"  |  |",0)
                        resultad.write("\n")
                        resultad.write("owl:Class\n")
                        resultad.write("  |rdfs:subClassOf\n")
                        visitado=[]
                        showTipo(a,"  |  |",0)
        result.write(name+";"+str(contador)+";\n")        
        print(f"{name} - {contador}")
    except:None
resultados.close()
resultad.close()
    #ex(name)
result.close()




















