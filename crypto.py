########################################
# CRYPTO WALLET BY GIORGIO LEGGIO 2021 #
########################################

from websocket import create_connection
from datetime import datetime
import websocket
import time 
import os
import json
from ast import literal_eval
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
import os.path
import getpass



os.system('color')
os.system('cls') 

# ----------  COSTANTI & VARIABILI -------------

# --- COSTANTI COLORI ---
# COMANDI FORMATTAZIONE
CEND      = '\33[0m'
CBOLD     = '\33[1m'
CITALIC   = '\33[3m'
CURL      = '\33[4m'
CBLINK    = '\33[5m'
CBLINK2   = '\33[6m'
CSELECTED = '\33[7m'
# COLORE TESTO
CBLACK  = '\33[30m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'
CBLUE   = '\33[34m'
CVIOLET = '\33[35m'
CBEIGE  = '\33[36m'
CWHITE  = '\33[37m'
CGREY    = '\33[90m'
CRED2    = '\33[91m'
CGREEN2  = '\33[92m'
CYELLOW2 = '\33[93m'
CBLUE2   = '\33[94m'
CVIOLET2 = '\33[95m'
CBEIGE2  = '\33[96m'
CWHITE2  = '\33[97m'
# COLORE EVIDENZIAZIONE SFONDO
CBLACKBG  = '\33[40m'
CREDBG    = '\33[41m'
CGREENBG  = '\33[42m'
CYELLOWBG = '\33[43m'
CBLUEBG   = '\33[44m'
CVIOLETBG = '\33[45m'
CBEIGEBG  = '\33[46m'
CWHITEBG  = '\33[47m'
CGREYBG    = '\33[100m'
CREDBG2    = '\33[101m'
CGREENBG2  = '\33[102m'
CYELLOWBG2 = '\33[103m'
CBLUEBG2   = '\33[104m'
CVIOLETBG2 = '\33[105m'
CBEIGEBG2  = '\33[106m'
CWHITEBG2  = '\33[107m'

LISTA_SIMBOLI = ["btc", "eth", "forth", "ltc", "bnb", "egld", "dot", "link", "uni", "ada", "matic", "xmr", "sol", "luna", "nano"]

wallet_personale = {}
valore_tot_wallet = 0
prec_valore_tot_wallet = 0
lista_simboli_valori = {}
prec_lista_simboli_valori = {}
lista_wallet_valori = {}
dict_storico = {}
privacy = True

# ----------  FUNZIONI -------------
def make_password(password, salt):
	kdf = PBKDF2HMAC(
		algorithm=hashes.SHA256(),
		length=32,
		salt=salt,
		iterations=100000,
		backend=default_backend()
	)
	return base64.urlsafe_b64encode(kdf.derive(password))
    
def converti_timestamp(timestamp):
    # TIMESTAMP
    str_time = str(timestamp)
    time = int(str_time[:10])
    time_date = datetime.fromtimestamp(time)
    return time_date
    
def aggiorna_massimali(totale):
    global max_tot 
    global min_tot
    if max_tot < totale+wallet_personale["usdt"]:
        max_tot = totale+wallet_personale["usdt"]
    if min_tot > totale+wallet_personale["usdt"]:
        min_tot = totale+wallet_personale["usdt"]
    print ('Aggiornamento Massimali: Min: {:.2f} Max: {:.2f}'.format(min_tot, max_tot))


# ---------  PARTE 0 - caricamento wallet personale criptato --------------
password = getpass.getpass(CRED+'Password:')
password = password.encode()

# --- Controlla se esiste file criptato: ---
if os.path.isfile('encrypted.key'): # file esiste   
    print (CBLUE2+"File encrypted.key trovato.",'yellow')
    # carica contenuto file su variabile cipher_text_utf8
    with open("encrypted.key", "r") as file_to_decrypt:
        cipher_text_utf8 = file_to_decrypt.read()
    # ritaglia il salt dai primi 24 byte
    salt = base64.b64decode(cipher_text_utf8[:24].encode("utf-8"))
    cipher_suite = Fernet(make_password(password, salt))
    
    # prova a decifrare con la password data
    try: # password corretta
        plain_text = cipher_suite.decrypt(cipher_text_utf8[24:].encode("utf-8"))
        plain_text_utf8 = plain_text.decode("utf-8")
        # Scriviamo quindi il testo decifrato sul file decrypted.txt:
        
        messaggio_decriptato = plain_text_utf8
        print ("Messaggio decriptato")
        #print (messaggio_decriptato)
        wallet_personale = literal_eval(messaggio_decriptato)
        #print ("Var dict:")
        #print (wallet_personale) 
    except: # password errata
        print ('Password Errata!')
else: # file criptato non esiste crearlo da file se presente?
    print ("File encrypted.key non trovato.")
    # controlla se esiste un file da criptare con password
    if os.path.isfile('da_criptare.txt'): # file da criptare presente
        # Cifratura       
        # Il messaggio da cifrare è all'interno di un file:
        print ("File da_criptare.txt trovato.")
        print ("Apertura file da_criptare.txt")
        with open("da_criptare.txt", "r") as file_to_encrypt:
            messaggio = file_to_encrypt.read()
        # salt da numero casuale    
        salt = os.urandom(16)
        print ("Salt:{}".format(salt))
        # codifica il messaggio
        key = make_password(password, salt)
        cipher_suite = Fernet(key)
        # codifica il messaggio criptato in utf-8
        cipher_text = cipher_suite.encrypt(messaggio.encode("utf-8"))
        # aggiunge il salt in testa al messaggio perche per decodificarlo serve sia password che salt
        cipher_text_utf8 = base64.b64encode(salt).decode('utf-8') + cipher_text.decode('utf-8')
        
        # Scriviamo quindi il valore cifrato su un nuovo file:
        encrypted_file = open("encrypted.key", "w")
        encrypted_file.write(cipher_text_utf8)
        encrypted_file.close()
        print ("File encrypted.key salvato")
    else: # file da criptare non presente
        print ("File da_criptare.txt non trovato.")
        print ('''Creare file 'da_criptare.txt' e all'interno il wallet in questo formato:
        # Creare file 'da_criptare.txt' e all'interno il wallet in questo formato:
        
        --da_criptare.txt--
        "btc":0.0,  
        "eth":0.0, 
        "forth":0.0, 
        "ltc":0.0, 
        "bnb":0.0, 
        "egld":0.0, 
        "dot":0.0, 
        "link":0.0, 
        "uni":0.0, 
        "ada":0.0, 
        "matic":0.0, 
        "xmr":0.0, 
        "sol":0.0, 
        "luna":0.0, 
        "nano":0.0,
        "usdt":0.00
        --------------------''')
  
# ---------  PARTE 1 - caricamento primi dati dal web --------------
lista_wallet_valori["usdt"] = wallet_personale["usdt"]
os.system('cls') 

# --- Caricamento valori salvati
try: # Prova ad aprire file valori salvati  
    with open('values.log') as f: # Apertura file
        min_tot = float(f.readline())
        max_tot = float(f.readline())
        prec_time_date = f.readline()
        dict_storico = f.readline()
        dict_storico = literal_eval(dict_storico)
        #print (min_tot, max_tot, prec_time_date)
    f.closed
    print ("Caricati valori da file log")
except: # File valori salvati non presente
    print("!! FILE LOG NON TROVATO !!")    
    max_tot = 0.00
    min_tot = 10000000000000.00
    prec_time_date = "no time prec"

print(CVIOLET+"Connessione Avvenuta")
print(CVIOLET+"Receiving...")
    
for x in range(len(LISTA_SIMBOLI)): # Stampa primi valori 
    # Ricava i valori della candela caricandoli dalla LISTA_SIMBOLI
    # connessione websocket
    ws = create_connection("wss://stream.binance.com:9443/ws/"+LISTA_SIMBOLI[x]+"usdt@kline_1m")
    message =  ws.recv()
    
    # scorporamento json
    json_message = json.loads(message)
    pair = candle = json_message['s']
    candle = json_message['k']  # GRUPPO VALORI CANDELA
    timestamp = json_message['E']  # TEMPO CANDELA
    valore = candle['c']  # VALORE CANDELA
    
    # Variabili candela
    time_date = converti_timestamp(timestamp)
    valore = float(valore)
    # carica i valori dei token posseduti nelle variabili
    quantita_token_in_wallet = wallet_personale[str(LISTA_SIMBOLI[x])] # carica numero di monete possedute dal wallet personale
    token_in_wallet_valore = quantita_token_in_wallet * valore # calcola il valore in usdt della singola moneta
    valore_tot_wallet += token_in_wallet_valore # aggiorna il valore totale del wallet con quello del token del ciclo
    
    # Stampa la riga della moneta in questo formato
    #      btc      51000.00         0.50282639 btc            25644.15 usdt
    if privacy:
        print ('{}{}{:6s}{}{:10.2f}{} || *** {}{}{:6s}{}{:10.2f} {}usdt'.format(CBOLD,CRED,LISTA_SIMBOLI[x], CYELLOW, valore,CBLUE, CBOLD,CRED,LISTA_SIMBOLI[x],CYELLOW, token_in_wallet_valore,CEND))
    else:
        print ('{:6s}{:10.2f} || {:18}{:6s}{:10.2f} usdt'.format(LISTA_SIMBOLI[x], valore, quantita_token_in_wallet,LISTA_SIMBOLI[x], token_in_wallet_valore))
    # Aggiorna la lista simbolo/valore formato
    # {btc:51000.00, eth:3800}
    lista_simboli_valori.update({LISTA_SIMBOLI[x]:valore})
    
    # Aggiorna la lista simbolo/valore nel wallet formato
    # {btc:25500.00, eth:4000}
    lista_wallet_valori.update({LISTA_SIMBOLI[x]:token_in_wallet_valore})
# stampe finali
print ("usdt         1.00               {:.0f} usdt            {:.2f} usdt".format(wallet_personale["usdt"],wallet_personale["usdt"]))
print ()
print ('TOTALE: {:.2f} USDT'.format(valore_tot_wallet+wallet_personale["usdt"]))
print (time_date)
#time.sleep(60)
ws.close()

prec_valore_tot_wallet = valore_tot_wallet
aggiorna_massimali(valore_tot_wallet)
valore_tot_wallet = 0
prec_lista_simboli_valori = lista_simboli_valori.copy()


# ---------  PARTE 2 - LOOP AGGIORNAMENTO TOKEN-------------

while True: # ciclo infinito
    #LISTA_SIMBOLI = ["btc", "eth", "forth", "ltc", "bnb", "egld", "dot", "link", "uni", "ada", "matic", "xmr", "sol", "luna", "nano"]
    for z in range(len(LISTA_SIMBOLI)): # ciclo z  lento di caricamento valore dal web, lento es. ..btc 
        # Ricava i valori della candela caricandoli dalla LISTA_SIMBOLI
        
        # connessione websocket
        ws = create_connection("wss://stream.binance.com:9443/ws/"+LISTA_SIMBOLI[z]+"usdt@kline_1m")
        message =  ws.recv()
        
        # scorporamento json
        json_message = json.loads(message)
        pair = candle = json_message['s']
        candle = json_message['k']  # GRUPPO VALORI CANDELA
        timestamp = json_message['E']  # TEMPO CANDELA
        valore = candle['c']  # VALORE CANDELA
        
        # Variabili candela
        time_date = converti_timestamp(timestamp)
        valore = float(valore)
        
        # carica i valori dei token posseduti nelle variabili
        quantita_token_in_wallet = wallet_personale[str(LISTA_SIMBOLI[z])] # es. 0.5
        token_in_wallet_valore = quantita_token_in_wallet * valore # es. 0.5 * 50000
        valore_tot_wallet += token_in_wallet_valore # es. 25000 + 1000
        lista_simboli_valori.update({LISTA_SIMBOLI[z]:valore}) # es. {btc:50000}
        
        # Inizio disegno tabella istantanea
        os.system('cls') 
        if privacy:
            for y in range(len(LISTA_SIMBOLI)): # ciclo y di aggiornamento tabella veloce es.:  ▼ btc      45964.28         0.50282639 btc            23112.05 usdt
                if not y == z+1: # se il rigo non è il precedente del ciclo z di aggiornamento valore
                    # valore precedente token piu alto, caso ribassista
                    if prec_lista_simboli_valori.get(LISTA_SIMBOLI[y])>lista_simboli_valori.get(LISTA_SIMBOLI[y]):
                        print ('{}▼ {}{:6s}{}{:10.2f}{} || {}{}*** {:6s}{}{:10.2f} {}usdt'.format(CRED,CRED,LISTA_SIMBOLI[y],CRED, lista_simboli_valori.get(LISTA_SIMBOLI[y]),CYELLOW2,CBOLD,CBEIGE, LISTA_SIMBOLI[y],CYELLOW, lista_simboli_valori.get(LISTA_SIMBOLI[y]) * wallet_personale.get(LISTA_SIMBOLI[y]),CEND))
                    # valore precedente token piu basso, caso rialzista
                    if prec_lista_simboli_valori.get(LISTA_SIMBOLI[y])<lista_simboli_valori.get(LISTA_SIMBOLI[y]):
                        print ('{}▲ {}{:6s}{}{:10.2f}{} || {}{}*** {:6s}{}{:10.2f} {}usdt'.format(CBLUE2 ,CBLUE,LISTA_SIMBOLI[y],CBLUE, lista_simboli_valori.get(LISTA_SIMBOLI[y]),CYELLOW2,CBOLD,CBEIGE, LISTA_SIMBOLI[y],CYELLOW, lista_simboli_valori.get(LISTA_SIMBOLI[y]) * wallet_personale.get(LISTA_SIMBOLI[y]),CEND))
                
                if y == z+1: # se il rigo disegnato è precedente al prossimo aggiornamento web
                    # stampa con "..." il token
                    print ('{}..{}{:6s}{}{:10.2f}{} || {}{}*** {:6s}{}{:10.2f} {}usdt'.format(CBEIGE2,CBEIGE,LISTA_SIMBOLI[y],CYELLOW, lista_simboli_valori.get(LISTA_SIMBOLI[y]),CYELLOW2,CBOLD,CBEIGE, LISTA_SIMBOLI[y],CYELLOW, lista_simboli_valori.get(LISTA_SIMBOLI[y]) * wallet_personale.get(LISTA_SIMBOLI[y]),CEND))

                if y >= z and not y == z+1 and not y == z: # se il rigo disegnato è ancora da aggiornare web
                    print ('{}• {}{:6s}{}{:10.2f}{} || {}{}*** {:6s}{}{:10.2f} {}usdt'.format(CBEIGE2,CYELLOW,LISTA_SIMBOLI[y],CYELLOW, lista_simboli_valori.get(LISTA_SIMBOLI[y]),CYELLOW2,CBOLD,CBEIGE, LISTA_SIMBOLI[y],CYELLOW, lista_simboli_valori.get(LISTA_SIMBOLI[y]) * wallet_personale.get(LISTA_SIMBOLI[y]),CEND))
            lista_wallet_valori.update({LISTA_SIMBOLI[z]:token_in_wallet_valore}) # aggiorna il valore ciclo z lento caricato dal web es: {btc:25000}
            # somma il totale della lista valori token posseduti
            somma = float(sum(lista_wallet_valori.values()))
            # stampe finali 
            print ("• usdt        1.00 || *** usdt     {:.2f} usdt".format(wallet_personale["usdt"]))
            print ()
            print ('{}{}TOTALE: {:8.2f}{} USDT (In aggiornamento...)'.format(CBOLD, CYELLOW2, somma, CEND))
            print (CVIOLET)
            print ('{}{}'.format(CVIOLET, prec_time_date))
            print ('TOTALE: {:.2f} USDT'.format(prec_valore_tot_wallet + wallet_personale["usdt"]))
            print ('Min: {:.2f}\nMax: {:.2f}'.format(min_tot, max_tot))
            print (CEND)
        if not privacy:
            for y in range(len(LISTA_SIMBOLI)): # ciclo y di aggiornamento tabella veloce es.:  ▼ btc      45964.28         0.50282639 btc            23112.05 usdt
                if not y == z+1: # se il rigo non è il precedente del ciclo z di aggiornamento valore
                    # valore precedente token piu alto, caso ribassista
                    if prec_lista_simboli_valori.get(LISTA_SIMBOLI[y])>lista_simboli_valori.get(LISTA_SIMBOLI[y]):
                        print ('▼ {:8s} {:8.2f} {:18} {:12s} {:10.2f} usdt'.format(LISTA_SIMBOLI[y], lista_simboli_valori.get(LISTA_SIMBOLI[y]), wallet_personale.get(LISTA_SIMBOLI[y]),LISTA_SIMBOLI[y], lista_simboli_valori.get(LISTA_SIMBOLI[y]) * wallet_personale.get(LISTA_SIMBOLI[y])))
                    # valore precedente token piu basso, caso rialzista
                    if prec_lista_simboli_valori.get(LISTA_SIMBOLI[y])<lista_simboli_valori.get(LISTA_SIMBOLI[y]):
                        print ('▲ {:8s} {:8.2f} {:18} {:12s} {:10.2f} usdt'.format(LISTA_SIMBOLI[y], lista_simboli_valori.get(LISTA_SIMBOLI[y]), wallet_personale.get(LISTA_SIMBOLI[y]),LISTA_SIMBOLI[y], lista_simboli_valori.get(LISTA_SIMBOLI[y]) * wallet_personale.get(LISTA_SIMBOLI[y])))
                
                if y == z+1: # se il rigo disegnato è precedente al prossimo aggiornamento web
                    # stampa con "..." il token
                    print ('..{:8s} {:8.2f} {:18} {:12s} {:10.2f} usdt'.format(LISTA_SIMBOLI[y], lista_simboli_valori.get(LISTA_SIMBOLI[y]), wallet_personale.get(LISTA_SIMBOLI[y]),LISTA_SIMBOLI[y], lista_simboli_valori.get(LISTA_SIMBOLI[y]) * wallet_personale.get(LISTA_SIMBOLI[y])))

                if y >= z and not y == z+1 and not y == z: # se il rigo disegnato è ancora da aggiornare web
                    print ('• {:8s} {:8.2f} {:18} {:12s} {:10.2f} usdt'.format(LISTA_SIMBOLI[y], lista_simboli_valori.get(LISTA_SIMBOLI[y]), wallet_personale.get(LISTA_SIMBOLI[y]),LISTA_SIMBOLI[y], lista_simboli_valori.get(LISTA_SIMBOLI[y]) * wallet_personale.get(LISTA_SIMBOLI[y])))
            lista_wallet_valori.update({LISTA_SIMBOLI[z]:token_in_wallet_valore}) # aggiorna il valore ciclo z lento caricato dal web es: {btc:25000}
            # somma il totale della lista valori token posseduti
            somma = float(sum(lista_wallet_valori.values()))
            # stampe finali 
            print ("• usdt         1                  {:.0f} usdt            {:.2f} usdt".format(wallet_personale["usdt"],wallet_personale["usdt"]))
            print ()
            print ('TOTALE: {:8.2f} USDT (In aggiornamento...)'.format(somma))
            print ()
            print ('{}'.format(prec_time_date))
            print ('TOTALE: {:.2f} USDT'.format(prec_valore_tot_wallet + wallet_personale["usdt"]))
            print ('Min: {:.2f}\nMax: {:.2f}'.format(min_tot, max_tot))
    # --------- PARTE 3 - FINE DEL CICLO Z DI AGGIORNAMENTO WEB
    
    dict_storico.update({str(time_date):somma})
    aggiorna_massimali(valore_tot_wallet)
    prec_lista_simboli_valori = lista_simboli_valori.copy()
    prec_time_date = time_date
    prec_valore_tot_wallet = valore_tot_wallet
    
    # Salvataggio file
    print ("Salvataggio file log")
    file = open('values.log', 'w')
    file.write("{}\n".format(min_tot))
    file.write("{}\n".format(max_tot))
    file.write("{}\n".format(prec_time_date))
    file.write("{}\n".format(dict_storico))
    file.close()
            
    valore_tot_wallet = 0
    ws.close()   