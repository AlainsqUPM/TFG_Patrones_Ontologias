import requests

vocabularios=[]
sitios=[]
etiquetas=[]

datos = open("VocabulariosV4.csv" , "r", encoding='utf-8')
resultados = open("DescargasRDF.csv", "w", encoding='utf-8')
linea=datos.readline(); columna = linea.split(";")
while(True):
    linea=datos.readline(); columna = linea.split(";")
    if columna[0]==(""): break
    vocabularios.append(columna[0])
    sitios.append(columna[1])
datos.close()

for i in range(0, len(sitios)):
    try:
        url = sitios[i]
        response = requests.get(url, timeout=5, headers={'Accept': 'application/rdf+xml'})
        name= "rdf/"+vocabularios[i]+".rdf"
        with open( name, 'wb') as f: f.write(response.content)
        print(f"{vocabularios[i]} : si")
        resultados.write(vocabularios[i]+";si\n")
    except: print(f"{vocabularios[i]} : no"); resultados.write(vocabularios[i]+";no\n")
resultados.close()
