from rdflib import Graph
filtro={}
etiquetas={}
etiqueta={}
datos={}
vocabularios={}

datos = open("VocabulariosV4.csv" , "r", encoding='utf-8')
linea=datos.readline(); columna = linea.split(";")
while(True):
    linea=datos.readline(); columna = linea.split(";")
    if columna[0]==(""): break
    vocabularios.update({columna[0]: 0})
datos.close()

datos = open("Terms_selected.csv" , "r", encoding='utf-8')
linea=datos.readline(); columna = linea.split(";")
while(True):
    linea=datos.readline(); columna = linea.split(";")
    if columna[0]==(""): break
    label=columna[4].replace("\n","")
    filtro.update({label:0})
    etiquetas.update({label:0})
    etiqueta.update({label:(columna[0]+":"+columna[1])})
datos.close

datos = open("Terms.csv" , "r", encoding='utf-8')
linea=datos.readline(); columna = linea.split(";")
while(True):
    linea=datos.readline(); columna = linea.split(";")
    if columna[0]==(""): break
    label=columna[4].replace("\n","")
    etiquetas.update({label:0})
    etiqueta.update({label:(columna[0]+":"+columna[1])})
datos.close

resultados = open("ParseoFiltradoRDF.csv", "w", encoding='utf-8')
text="Vocabulario;Tuplas;Etiquetas;Repeticiones;"
for i in filtro.keys():text+=etiqueta[i]+";"
resultados.write(text+"\n")
for i in vocabularios:
    for e in etiquetas.keys(): etiquetas[e]=0
    try:
        print(i)
        con=0
        relativo=0
        filtrados=0
        name="rdf/"+i+".rdf"
        g = Graph()
        g.parse(name)
        text=i+";"+str(len(g))+";"
        for e in g:
            if len(e)==3:
                label1=str(e[0])
                label2=str(e[1])
                label3=str(e[2])
                if label1 in filtro:
                    etiquetas[label1]+=1; con+=1
                    filtro[label1]+=1
                    if etiquetas[label1] == 1: relativo+=1
                if label2 in filtro:
                    etiquetas[label2]+=1; con+=1
                    filtro[label2]+=1
                    if etiquetas[label2] == 1: relativo+=1
                if label3 in filtro:
                    etiquetas[label3]+=1; con+=1
                    filtro[label3]+=1
                    if etiquetas[label3] == 1: relativo+=1
                
        text+=str(relativo)+";"+str(con)+";"
        for e in filtro.keys():
            if e in filtro: text+=str(etiquetas[e])+";"   
        resultados.write(text+"\n")
    except: print("   Error al leer RDF")
resultados.close()
for e in filtro.keys():
            print(f"{etiqueta[e]} = {filtro[e]}")
print("Resultados guardados en csv")
