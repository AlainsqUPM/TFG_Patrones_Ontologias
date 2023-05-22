import requests

vocabularios=["saref4envi"]
sitios=["https://saref.etsi.org/saref4envi/"]
etiquetas=[]

for i in range(0, len(sitios)):
    try:
        url = sitios[i]
        response = requests.get(url, timeout=5, headers={'Accept': 'application/turtle'})
        name= "rdf/"+vocabularios[i]+".rdf"
        with open( name, 'wb') as f: f.write(response.content)
        print(f"{vocabularios[i]} : si")
    except: print(f"{vocabularios[i]} : no")
