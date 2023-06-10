patrones={}
repeticiones={}
contador=1
datos = open("Tipos.txt" , "r", encoding='utf-8')
linea=datos.readline()
texto=""
while(True):
    linea=datos.readline()
    if len(linea)>1: texto+=linea
    else:
        if not(texto in patrones): patrones.update({texto:{"valor":0,"name": "Patron "}})
        patrones[texto]["valor"]+=1
        texto=""
    if linea==(""): break
datos.close()

resultados = open("Patrones.txt" , "w", encoding='utf-8')
print(len(patrones))
for i in patrones.keys():
    if not(patrones[i]['valor'] in repeticiones): repeticiones.update({patrones[i]['valor']:0})
    repeticiones[patrones[i]['valor']]+=1
    if patrones[i]['valor']>1:
        resultados.write("Patron "+str(contador)+"\n"); contador+=1
        resultados.write(f"Repeticiones {patrones[i]['valor']}\n")
        resultados.write(f"{i}\n")
resultados.close()
for i in sorted(repeticiones.keys()):
    print(f"{repeticiones[i]} estructura/s con {i} repeticion/es")

