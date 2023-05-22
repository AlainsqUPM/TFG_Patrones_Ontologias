from rdflib import Graph

contador=0
anonimizador=1
filtro={}
etiquetas={}
etiqueta={}
uri={}
vocabulario={}

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
datos.close()

datos = open("Estructuras_detectadas.csv" , "r", encoding='utf-8')
linea=datos.readline(); columna = linea.split(";")
while(True):
    linea=datos.readline(); columna = linea.split(";")
    if columna[0]==(""): break
    vocabulario.update({columna[0]:int(columna[1])})
datos.close()
            
def parsear(i):
    
    def sujeto(i, text, con, patron1):
        for e in sujetos[i]:
            if con>0 and e!="rdfs:type":
                #predicado
                llave2=e
                if not(llave2 in patron1): patron1.update({llave2:{"Key":str(e)}})
            for a in range(0, len(sujetos[i][e])):
                if con>0 and e!="rdfs:type":
                    #objeto
                    try:
                        if "Literal" in sujetos[i][e][a]:llave3="Literal"
                        elif "Property" in sujetos[sujetos[i][e][a]]["rdfs:type"][0]: llave3="Propiedad"
                        elif "xsd" in sujetos[sujetos[i][e][a]]["rdfs:type"][0] or "Literal" in sujetos[i][e][a]: llave3="Literal"
                        else: llave3=sujetos[sujetos[i][e][a]]["rdfs:type"][0]
                    except:
                        if "Anonimo" in sujetos[i][e][a]: llave3="Anonimo"
                        else: llave3=sujetos[i][e][a]
                    if not(llave3 in patron1[llave2]): patron1[llave2].update({llave3:{"Key":str(sujetos[i][e][a])}})
                    if sujetos[i][e][a] in sujetos and sujetos[i][e][a]!=i:
                        if "Anonimo" in sujetos[i][e][a] or sujetos[i][e][a] in filtro:
                            sujeto(sujetos[i][e][a], text+"   |  ",con+1, patron1[llave2][llave3])   
                    
                if con==0:
                    if sujetos[i][e][a] in sujetos and sujetos[i][e][a]!=i:
                        #sujeto
                        try: llave1=sujetos[i]["rdfs:type"][0]
                        except: llave1=i
                        if not(llave1 in patron1): patron1.update({llave1:{"Key":str(i)}})
                        
                        #predicado
                        llave2=e
                        if not(llave2 in patron1[llave1]): patron1[llave1].update({llave2:{"Key":str(e)}})

                        #objeto
                        try: llave3=sujetos[sujetos[i][e][a]]["rdfs:type"][0]
                        except:
                            if "Anonimo" in sujetos[i][e][a]: llave3="Anonimo"
                            else: llave3=sujetos[i][e][a]
                        if not(llave3 in patron1[llave1][llave2]): patron1[llave1][llave2].update({llave3:{"Key":str(sujetos[i][e][a])}})
                        sujeto(sujetos[i][e][a], text+"   |  ", con+1, patron1[llave1][llave2][llave3])
                           
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
            elif"Ref" in tipo and i!=2:
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
                if i!=2:
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
    
    def verPatronReal(text, patron):
        for i in sorted(patron.keys()):
            if i!="Key":
                resultados.write(text+patron[i]["Key"]+"\n")
                verPatronReal(text+"   |",patron[i])

    def verPatronTipo(text, patron):
        for i in sorted(patron.keys()):
            if i!="Key":
                resultados.write(text+i+"\n")
                verPatronTipo(text+"   |",patron[i])

    def compararPatron():
        try:
            #1patron['owl:Class']['rdfs:subClassOf']['owl:Restriction']['owl:allValuesFrom']['Literal']
            #1patron['owl:Class']['rdfs:subClassOf']['owl:Restriction']['owl:onProperty']['Propiedad']
            #1patron['owl:Class']['rdfs:subClassOf']['owl:Restriction']['owl:someValuesFrom']['owl:Class']
            #2patron['owl:Class']['rdfs:subClassOf']['owl:Class']['owl:unionOf']['Anonimo']
            #2patron['owl:Class']['rdfs:subClassOf']['owl:Restriction']['owl:onProperty']['Propiedad']
            #3patron['owl:Class']['owl:disjointWith']['owl:Class']
            #3patron['owl:Class']['rdfs:subClassOf']['owl:Class']['owl:disjointWith']['owl:Class']
            #3patron['owl:Class']['rdfs:subClassOf']['owl:Class']['rdfs:subClassOf']['owl:Class']
            patron['owl:Class']['rdfs:isDefinedBy']['owl:Ontology']
            patron['owl:Class']['rdfs:subClassOf']['owl:Class']
            patron['owl:Class']['owl:disjointWith']['owl:Class']
            return 1
        except:
            return 0

    global contador
    relativo=0
    patron={}
    sujetos={}
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
        patron.clear()
        sujeto(i,"", 0, patron)
        resultado=compararPatron()
        if resultado==1:
            contador+=1
            relativo+=1
            resultados.write("\nPatron tipo\n")
            verPatronTipo("",patron)
            resultados.write("\nPatron real\n")
            verPatronReal("",patron)
    anonimizador=1
    return relativo
    
resultados = open ('Patron_encontrados.txt', 'w', encoding='utf-8')
total=0
for i in vocabulario.keys():
    resultados.write(f"{i}: {vocabulario[i]} estructuras totales\n")
    relativo=parsear(i)
    if relativo>0 :
        total+=1
        print(f"{i}: {relativo} de {vocabulario[i]}")
        resultados.write(f"{i}: {relativo} estructuras filtradas\n")
print(f"\nVocabularios con patrón: {total}")
print(f"\nEstructuras encontradas totales: {contador}")
resultados.write(f"\nVocabularios con patrón: {total}")
resultados.write(f"\nEstructuras encontradas: {contador}")
resultados.close()
