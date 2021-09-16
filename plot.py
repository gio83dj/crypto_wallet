########################################
# CRYPTO GRAFICO BY GIORGIO LEGGIO 2021#
########################################

import matplotlib.pyplot as plt
from collections import OrderedDict
from ast import literal_eval

plt.style.use('ggplot')
index = 0
datax = []
datay = []
data = {}

try:
    # Apertura file
    with open('values.log') as f:
        min_tot = float(f.readline())
        max_tot = float(f.readline())
        prec_time_date = f.readline()
        data = f.readline()
        #print (min_tot, max_tot, prec_time_date)
    f.closed
    print ("Caricati valori da file log")
except:
    print("!! FILE LOG NON TROVATO !!")    
    max_tot = 0.00
    min_tot = 10000000000000.00
    prec_time_date = "error"


data = literal_eval(data)
#print (len(data))
items = list(data.items())


numero_valori_grafico = input("Quanti punti vuoi nel grafico? Max {} \nPremi invio per 1000 .".format(len(data)))
if numero_valori_grafico == "":
    #numero_valori_grafico = len(data)
    numero_valori_grafico = 1000
else:
    numero_valori_grafico = int(numero_valori_grafico)

for x in items[-numero_valori_grafico:]:
    #print (x[0])
    datax.append(x[0])
    datay.append(x[1])    
    index += 1
#print(type(items))

plt.plot(datax,datay)
plt.ylabel('some numbers')
plt.show()