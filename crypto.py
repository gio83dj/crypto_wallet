# ALT+0 FOLDall
# ALT+1 UNFOLDall
# To select a specific environment, use the Python: Select Interpreter command from the Command Palette (Ctrl+Shiftdestro+P)
########################################
# CRYPTO WALLET BY GIORGIO LEGGIO 2022 #
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


# COSTANTI
CEND, CBOLD, CRED, CGREEN, CYELLOW, CBLUE, CVIOLET, CBEIGE, CWHITE, CGREY, CRED2, CGREEN2, CYELLOW2, CBLUE2, CBEIGE2, CWHITE2, CREDBG, CBLUEBG = '\33[0m', '\33[1m', '\33[31m', '\33[32m', '\33[33m', '\33[34m', '\33[35m', '\33[36m', '\33[37m', '\33[90m', '\33[91m', '\33[92m', '\33[93m', '\33[94m', '\33[96m', '\33[97m', '\33[41m', '\33[44m'

CRITTOGRAFIA = False
LINUX = False
LISTA_SIMBOLI = []
MAX_RIBASSO = -30
MAX_RIALZO = 30
COL_TABELLA = CYELLOW + CBOLD

os.system('color')
if LINUX:
    os.system('clear')
else:
    os.system('cls')


# ---------- VARIABILI -------------
wallet_personale = {}
valore_tot_wallet = 0
lista_simboli_quotazioni = {}
lista_simboli_score = {}
min_score_token = {}
max_score_token = {}
prec_lista_simboli_quotazioni = {}
lista_wallet_valori_in_usdt = {}
storico_totali = {}
global privacy
privacy = False
score = 0
contatore_cicli = 0
prima_volta = True
chiusura_forzata = 0


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
    if max_tot < totale:
        max_tot = totale
    if min_tot > totale:
        min_tot = totale
    print('Aggiornamento Massimali: Min: {:.2f} Max: {:.2f}'.format(min_tot, max_tot))


def aggiorna_massimali_token():
    global max_score_token
    global min_score_token
    for x in range(len(LISTA_SIMBOLI)):
        if lista_simboli_score[LISTA_SIMBOLI[x]] > max_score_token[LISTA_SIMBOLI[x]]:
            max_score_token[LISTA_SIMBOLI[x]] = lista_simboli_score[LISTA_SIMBOLI[x]]
        if lista_simboli_score[LISTA_SIMBOLI[x]] < min_score_token[LISTA_SIMBOLI[x]]:
            min_score_token[LISTA_SIMBOLI[x]] = lista_simboli_score[LISTA_SIMBOLI[x]]


def colorizza(X_ICONA, X_SIMBOLO, X_NUMERO_TOKEN_IN_WALLET, X_SIMBOLO2, X_VALORE_TOKEN_IN_WALLET, X_USDT, X_SCORE,
              X_QUOTAZIONE):
    global COL_ICONA
    global COL_SIMBOLO
    global COL_NUMERO_TOKEN_IN_WALLET
    global COL_SIMBOLO2
    global COL_VALORE_TOKEN_IN_WALLET
    global COL_USDT
    global COL_SCORE
    global COL_QUOTAZIONE
    COL_ICONA = X_ICONA
    COL_SIMBOLO = X_SIMBOLO
    COL_NUMERO_TOKEN_IN_WALLET = X_NUMERO_TOKEN_IN_WALLET
    COL_SIMBOLO2 = X_SIMBOLO2
    COL_VALORE_TOKEN_IN_WALLET = X_VALORE_TOKEN_IN_WALLET
    COL_USDT = X_USDT
    COL_SCORE = X_SCORE
    COL_QUOTAZIONE = X_QUOTAZIONE


def splash():
    COL_SPLASH_FRAME = CBOLD + CVIOLET
    COL_SPLASH_TEXT = CBOLD + CYELLOW2
    print(f'''
    {COL_SPLASH_FRAME}                     ########################################
                         # {COL_SPLASH_TEXT}CRYPTO WALLET BY GIORGIO LEGGIO 2022 {COL_SPLASH_FRAME}#
                         ########################################
    ''')


def disegna_riga(simbolo):
    if privacy:
        print(
            f'{COL_TABELLA}║ {COL_ICONA}{simbolo} {COL_SIMBOLO}{LISTA_SIMBOLI[y]:6s}{COL_QUOTAZIONE}{lista_simboli_quotazioni.get(LISTA_SIMBOLI[y]):10.2f} {COL_TABELLA}║║ *** ║║ {COL_SCORE}SCORE: {lista_simboli_score.get(LISTA_SIMBOLI[y]):4} {CEND} {CWHITE}{CREDBG}{min_score_token[LISTA_SIMBOLI[y]]:^6} {CBLUEBG}{max_score_token[LISTA_SIMBOLI[y]]:^6}{CEND}{COL_TABELLA}║')
    if not privacy:
        print(
            f'{COL_TABELLA}║ {COL_ICONA}{simbolo} {COL_SIMBOLO}{LISTA_SIMBOLI[y]:6s}{COL_QUOTAZIONE}{lista_simboli_quotazioni.get(LISTA_SIMBOLI[y]):10.2f} {COL_TABELLA}║║ {COL_NUMERO_TOKEN_IN_WALLET}{wallet_personale[LISTA_SIMBOLI[y]]: >18.8f} {COL_SIMBOLO2}{LISTA_SIMBOLI[y]: <6s}{COL_VALORE_TOKEN_IN_WALLET}{lista_simboli_quotazioni.get(LISTA_SIMBOLI[y]) * wallet_personale.get(LISTA_SIMBOLI[y]):> 10.2f} {COL_USDT}usdt{COL_TABELLA} ║║ {COL_SCORE}SCORE: {lista_simboli_score.get(LISTA_SIMBOLI[y]):4} {CEND} {CWHITE}{CREDBG}{min_score_token[LISTA_SIMBOLI[y]]:^6} {CBLUEBG}{max_score_token[LISTA_SIMBOLI[y]]:^6}{CEND}{COL_TABELLA}║')


def disegna_riga_usdt(simbolo):
    usdt_string = 'usdt'
    if privacy:
        usdt = 000
        print(
            f'{COL_TABELLA}║ {COL_ICONA}{simbolo} {COL_SIMBOLO}{usdt_string:6s}{COL_QUOTAZIONE}{1:10.2f} {COL_TABELLA}║║ *** ║║ {CEND}{COL_SCORE}SCORE:  ---   ---    ---  {COL_TABELLA}║')
    if not privacy:
        usdt = wallet_personale['usdt']
        print(
            f'{COL_TABELLA}║ {COL_ICONA}{simbolo} {COL_SIMBOLO}{usdt_string:6s}{COL_QUOTAZIONE}{1:10.2f} {COL_TABELLA}║║ {COL_NUMERO_TOKEN_IN_WALLET}{usdt: >18.8f} {COL_SIMBOLO2}{usdt_string: <6s}{COL_VALORE_TOKEN_IN_WALLET}{usdt:> 10.2f} {COL_USDT}usdt{COL_TABELLA} ║║ {COL_SCORE}SCORE:{CEND}  ---   ---    ---  {COL_TABELLA}║')


def disegna_riga_prima(simbolo):
    print(
        f'{CBOLD}{CRED}{LISTA_SIMBOLI[y]:6s}{CYELLOW}{valore:10.2f}{CBLUE} ║  *** {CBOLD}{CRED}{LISTA_SIMBOLI[y]:6s}{CYELLOW}{token_in_wallet_valore:10.2f} {CEND}usdt')


def disegna_tabella_giu():
    if privacy == False:
        print(
            COL_TABELLA + "╚════════════════════╩╩══════════════════════════════════════════╩╩═══════════════════════════╝")
    if privacy == True:
        print(COL_TABELLA + "╚════════════════════╩╩═════╩╩═══════════════════════════╝")


def disegna_tabella_su():
    if privacy == False:
        print(
            COL_TABELLA + "╔════════════════════╦╦══════════════════════════════════════════╦╦═══════════════════════════╗")
    if privacy == True:
        print(COL_TABELLA + "╔════════════════════╦╦═════╦╦═══════════════════════════╗")


def carica_log_txt():
    global messaggio_log
    if os.path.isfile('log.txt'):  # file esiste
        print(CRED2 + "File log.txt trovato.")
        with open("log.txt", "r") as file:
            messaggio_log = file.read()
            print ("File caricato in memoria!")
            print (messaggio_log)

def decripta_log_key():
    global messaggio_log
    global salt
    if not prima_volta:
        if os.path.isfile('log.key'):  # file esiste
            print(CRED2 + "File log.key trovato.")
            # carica contenuto file su variabile messaggio_cifrato_log_utf8
            with open("log.key", "r") as file_to_decrypt:
                messaggio_cifrato_log_utf8 = file_to_decrypt.read()
            # ritaglia il salt dai primi 24 byte
            salt = base64.b64decode(messaggio_cifrato_log_utf8[:24].encode("utf-8"))
            cipher_suite = Fernet(make_password(password, salt))
            # prova a decifrare con la password data
            try:  # password corretta
                plain_text = cipher_suite.decrypt(messaggio_cifrato_log_utf8[24:].encode("utf-8"))
                messaggio_log = plain_text.decode("utf-8")
                print(CBLUE + "Messaggio decriptato")
            except:  # password errata
                print('Password Errata!')
        else:
            print('File log.key non trovato')


def carica_log():
    global min_tot
    global max_tot
    global storico_totali
    global prec_lista_simboli_quotazioni
    global lista_simboli_score
    global contatore_cicli
    global min_score_token
    global max_score_token
    global wallet_personale
    index = 0
    for line in messaggio_log.splitlines():
        if index == 0:
            wallet_personale = line
            wallet_personale = literal_eval(wallet_personale)
        if index == 1:
            min_tot = float(line)
        if index == 2:
            max_tot = float(line)
        if index == 3:
            storico_totali = line
            storico_totali = literal_eval(storico_totali)
        if index == 4:
            prec_lista_simboli_quotazioni = line
            prec_lista_simboli_quotazioni = literal_eval(prec_lista_simboli_quotazioni)
        if index == 5:
            lista_simboli_score = line
            lista_simboli_score = literal_eval(lista_simboli_score)
        if index == 6:
            contatore_cicli = int(line)
        if index == 7:
            min_score_token = line
            min_score_token = literal_eval(min_score_token)
        if index == 8:
            max_score_token = line
            max_score_token = literal_eval(max_score_token)

        index += 1


def salva_log_key():
    messaggio_log_da_salvare = str(wallet_personale) + '\n' + str(min_tot) + '\n' + str(max_tot) + '\n' + str(
        storico_totali) + '\n' + str(prec_lista_simboli_quotazioni) + '\n' + str(lista_simboli_score) + '\n' + str(
        contatore_cicli) + '\n' + str(min_score_token) + '\n' + str(max_score_token) + '\n'
    if not os.path.isfile('log.key'):
        global salt
        salt = os.urandom(16)
    print("Salt:{}".format(salt))
    # codifica il messaggio
    key = make_password(password, salt)
    cipher_suite = Fernet(key)
    # codifica il messaggio criptato in utf-8
    cipher_text = cipher_suite.encrypt(messaggio_log_da_salvare.encode("utf-8"))
    # aggiunge il salt in testa al messaggio perche per decodificarlo serve sia password che salt
    messaggio_cifrato_log_utf8 = base64.b64encode(salt).decode('utf-8') + cipher_text.decode('utf-8')
    # Scriviamo quindi il valore cifrato su un nuovo file:
    encrypted_file = open("log.key", "w")
    encrypted_file.write(messaggio_cifrato_log_utf8)
    encrypted_file.close()

def salva_log():
    # Creiamo variabile da scrivere sul file log.txt
    messaggio_log_da_salvare = str(wallet_personale) + '\n' + str(min_tot) + '\n' + str(max_tot) + '\n' + str(
        storico_totali) + '\n' + str(prec_lista_simboli_quotazioni) + '\n' + str(lista_simboli_score) + '\n' + str(
        contatore_cicli) + '\n' + str(min_score_token) + '\n' + str(max_score_token) + '\n'        
    # Scriviamo quindi il valore del messaggio su un nuovo file:
    file = open("log.txt", "w")
    file.write(messaggio_log_da_salvare)
    file.close()


# ---------  PARTE 0 - caricamento wallet personale criptato --------------
print(CBLUEBG, CBOLD)

if LINUX:
    os.system('clear')
else:
    os.system('cls')
splash()
if CRITTOGRAFIA:
    password = getpass.getpass(CBOLD + CRED + 'Password:' + CEND)  # richiedi password
    password = password.encode()

if LINUX:
    os.system('clear')
else:
    os.system('cls')
splash()
print()

print(CEND)

# ---------  PARTE 1 - CARICAMENTO DATI DA FILE O DAL WEB --------------

# --- Caricamento wallet criptato log.key o wallet.txt
if CRITTOGRAFIA:
    if not os.path.isfile('log.key'):  # file key criptato non esiste crearlo da file se presente?
        print("File log.key non trovato.")
        # controlla se esiste un file wallet.txt da criptare con password
        if os.path.isfile('wallet.txt'):  # file da criptare presente
            print("File wallet.txt trovato.")
            print("Apertura file wallet.txt")
            with open("wallet.txt", "r") as file_to_encrypt:
                wallet_personale = file_to_encrypt.read()
                wallet_personale = literal_eval(wallet_personale)
                LISTA_SIMBOLI = list(wallet_personale.keys())
                LISTA_SIMBOLI.remove("usdt")
                for item in wallet_personale:
                    lista_simboli_score[item] = 0

                min_score_token = lista_simboli_score.copy()
                max_score_token = lista_simboli_score.copy()
                prima_volta = True
        else:  # file da criptare non presente, creo wallet.txt ed esco
            print("File wallet.txt non trovato.")
            file1 = open('wallet.txt', 'w')
            file1.write(
                '{"btc":0.0, "eth":0.0, "usdt":0.00}')
            file1.close()
            print('''Creato file 'wallet.txt'. Aprire con un editor di testo e modificare valori monete posseduti. "btc":0.0, "eth":0.0 "usdt":0.00 --------------------''')
            quit()
    if os.path.isfile('log.key'):  # esiste log -> prima_volta = False
        prima_volta = False
else: # NON CRITTOGRAFIA
    if not os.path.isfile('log.txt'):  # file log non esiste crearlo da file se presente?
        print("File log.txt non trovato.")
        # controlla se esiste un file wallet
        if os.path.isfile('wallet.txt'):  # file wallet.txt presente
            print("File wallet.txt trovato.")
            print("Apertura file wallet.txt")
            with open("wallet.txt", "r") as file_wallet:
                wallet_personale = file_wallet.read()
                wallet_personale = literal_eval(wallet_personale)
                LISTA_SIMBOLI = list(wallet_personale.keys())
                LISTA_SIMBOLI.remove("usdt")
                for item in wallet_personale:
                    lista_simboli_score[item] = 0

                min_score_token = lista_simboli_score.copy()
                max_score_token = lista_simboli_score.copy()
                prima_volta = True
        else:  # file wallet.txt non presente, creo wallet.txt ed esco
            print("File wallet.txt non trovato.")
            file1 = open('wallet.txt', 'w')
            file1.write('{"btc":0.0, "eth":0.0, "usdt":0.00}')
            file1.close()
            print('''Creato file 'wallet.txt'. Aprire con un editor di testo e modificare valori monete posseduti. "btc":0.0, "eth":0.0 "usdt":0.00 --------------------''')
            quit()
    if os.path.isfile('log.txt'):  # esiste log -> prima_volta = False
        prima_volta = False

# --- PRIMA VOLTA?
if not prima_volta:  # non prima_volta
    print("File di salvataggio presente. Inizio caricamento valori.")
    # Prova ad aprire file valori salvati 
    if CRITTOGRAFIA: 
        decripta_log_key()
    else:
        carica_log_txt()
    
    carica_log()
    
    print(wallet_personale)

    LISTA_SIMBOLI = list(wallet_personale.keys())
    LISTA_SIMBOLI.remove("usdt")

    #for item in wallet_personale:
    #    lista_simboli_score[item] = 0

    lista_wallet_valori_in_usdt["usdt"] = wallet_personale["usdt"]
    print("Caricati valori da file log")
    for item in wallet_personale:  # carica la moltiplicazione dei valori precedenti in variabile lista_wallet_valori_in_usdt
        if item != 'usdt':
            print(prec_lista_simboli_quotazioni[item])
            print(wallet_personale[item])
            moltiplica = prec_lista_simboli_quotazioni[item] * wallet_personale[item]
            print(moltiplica)
            lista_wallet_valori_in_usdt.update({item: moltiplica})
else:  # prima_volta
    print(CRED + "PRIMA VOLTA...")
    #lista_wallet_valori_in_usdt.update({'usdt': wallet_personale['usdt']})
    print("File di salvataggio non presente.")
    max_tot = 0.00
    min_tot = 10000000000000.00
    print(CVIOLET + "Connessione Avvenuta")
    print(CVIOLET + "Receiving...")
    for y in range(len(LISTA_SIMBOLI)):  # Stampa primi valori
        # Ricava i valori della candela caricandoli dalla LISTA_SIMBOLI
        # connessione websocket
        ws = create_connection("wss://stream.binance.com:9443/ws/" + LISTA_SIMBOLI[y] + "usdt@kline_1m")
        message = ws.recv()
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
        token_in_wallet_valore = wallet_personale[
                                     str(LISTA_SIMBOLI[y])] * valore  # calcola il valore in usdt della singola moneta
        valore_tot_wallet += token_in_wallet_valore  # aggiorna il valore totale del wallet con quello del token del ciclo
        # Stampa la riga della moneta in questo formato: btc      51000.00         0.0 btc          
        colorizza(CBLUEBG + CBOLD, CWHITE2, CWHITE2, CWHITE2, CWHITE2, CWHITE2, CWHITE2, CWHITE2)
        disegna_riga_prima(':')
        # Aggiorna la lista simbolo/valore formato {btc:51000.00, eth:3800}
        lista_simboli_quotazioni.update({LISTA_SIMBOLI[y]: valore})
        # Aggiorna la lista simbolo/valore nel wallet formato
        # {btc:25500.00, eth:4000}
        lista_wallet_valori_in_usdt.update({LISTA_SIMBOLI[y]: token_in_wallet_valore})
        lista_wallet_valori_in_usdt.update({"usdt":wallet_personale['usdt']})
    # stampe finali
    print("usdt         1.00               {:.0f} usdt            {:6.2f} usdt".format(wallet_personale["usdt"],
                                                                                       wallet_personale["usdt"]))
    print()
    print(time_date)
    # time.sleep(60)
    ws.close()
    somma = float(sum(lista_wallet_valori_in_usdt.values()))
    aggiorna_massimali(somma)
    prec_lista_simboli_quotazioni = lista_simboli_quotazioni.copy()
    prima_volta = False

lista_simboli_quotazioni = prec_lista_simboli_quotazioni.copy()

# ---------  PARTE 2 - LOOP AGGIORNAMENTO TOKEN-------------
print(CVIOLET + "Connessione Avvenuta")
print(CVIOLET + "Receiving...")
print(min_score_token)
print(max_score_token)
aggiorna_massimali_token()


prima_volta = False
while True:  # ciclo infinito
    contatore_cicli += 1
    for z in range(len(LISTA_SIMBOLI)):  # ciclo z lento di caricamento valore dal web, lento es. ..btc
        # Inizio disegno tabella istantanea
        if LINUX:
            os.system('clear')
        else:
            os.system('cls')
        print(CBOLD)
        splash()
        disegna_tabella_su()
        for y in range(len(LISTA_SIMBOLI)):  # ciclo y di REFRESH tabella veloce
            if y == z:  # se il rigo disegnato è in aggiornamento (..)
                colorizza(CBLUEBG + CBOLD, CWHITE2, CWHITE2, CWHITE2, CWHITE2, CWHITE2, CWHITE2, CWHITE2)
                disegna_riga('.')
            if y < z:  # se il rigo disegnato è già stato aggiornato web (▼=▲)
                if prec_lista_simboli_quotazioni.get(LISTA_SIMBOLI[y]) == lista_simboli_quotazioni.get(
                        LISTA_SIMBOLI[y]):  # CASO UGUALE
                    colorizza(CYELLOW + CBOLD, CYELLOW, CGREEN2, CBEIGE2, CBEIGE2, CYELLOW2, CYELLOW, CGREEN)
                    if int(lista_simboli_score[LISTA_SIMBOLI[y]]) > MAX_RIALZO:  # BULLISH
                        COL_SCORE = CBLUEBG + CWHITE
                    if int(lista_simboli_score[LISTA_SIMBOLI[y]]) < MAX_RIALZO and int(
                            lista_simboli_score[LISTA_SIMBOLI[y]]) > MAX_RIBASSO:  # NEUTRALE
                        COL_SCORE = CGREEN
                    if int(lista_simboli_score[LISTA_SIMBOLI[y]]) < MAX_RIBASSO:  # BEARISH
                        COL_SCORE = CREDBG + CWHITE
                    disegna_riga('=')

                if prec_lista_simboli_quotazioni.get(LISTA_SIMBOLI[y]) > lista_simboli_quotazioni.get(
                        LISTA_SIMBOLI[y]):  # CASO RIBASSISTA
                    colorizza(CRED + CBOLD, CRED, CGREEN2, CBEIGE, CBEIGE2, CYELLOW2, CYELLOW, CGREEN)
                    if int(lista_simboli_score[LISTA_SIMBOLI[y]]) > MAX_RIALZO:  # BULLISH
                        COL_SCORE = CBLUEBG + CWHITE
                    if int(lista_simboli_score[LISTA_SIMBOLI[y]]) < MAX_RIALZO and int(
                            lista_simboli_score[LISTA_SIMBOLI[y]]) > MAX_RIBASSO:  # NEUTRALE
                        COL_SCORE = CGREEN
                    if int(lista_simboli_score[LISTA_SIMBOLI[y]]) < MAX_RIBASSO:  # BEARISH
                        COL_SCORE = CREDBG + CWHITE
                    disegna_riga('▼')

                if prec_lista_simboli_quotazioni.get(LISTA_SIMBOLI[y]) < lista_simboli_quotazioni.get(
                        LISTA_SIMBOLI[y]):  # CASO RIALZISTA
                    colorizza(CBLUE2 + CBOLD, CBLUE2, CGREEN2, CBEIGE, CBEIGE2, CYELLOW2, CYELLOW, CGREEN)
                    if int(lista_simboli_score[LISTA_SIMBOLI[y]]) > MAX_RIALZO:  # BULLISH
                        COL_SCORE = CBLUEBG + CWHITE
                    if int(lista_simboli_score[LISTA_SIMBOLI[y]]) < MAX_RIALZO and int(
                            lista_simboli_score[LISTA_SIMBOLI[y]]) > MAX_RIBASSO:  # NEUTRALE
                        COL_SCORE = CGREEN
                    if int(lista_simboli_score[LISTA_SIMBOLI[y]]) < MAX_RIBASSO:  # BEARISH
                        COL_SCORE = CREDBG + CWHITE
                    disegna_riga('▲')
            if y > z:  # se il rigo disegnato è ancora da aggiornare web (•)
                colorizza(CYELLOW2 + CBOLD, CGREY, CGREEN2, CGREY, CBEIGE2, CGREEN, CYELLOW2, CGREEN)
                if int(lista_simboli_score[LISTA_SIMBOLI[y]]) > MAX_RIALZO:  # BULLISH
                    COL_SCORE = CBLUEBG + CWHITE
                if int(lista_simboli_score[LISTA_SIMBOLI[y]]) < MAX_RIALZO and int(
                        lista_simboli_score[LISTA_SIMBOLI[y]]) > MAX_RIBASSO:  # NEUTRALE
                    COL_SCORE = CGREEN
                if int(lista_simboli_score[LISTA_SIMBOLI[y]]) < MAX_RIBASSO:  # BEARISH
                    COL_SCORE = CREDBG + CWHITE
                disegna_riga('•')
                # somma il totale della lista valori token posseduti
        somma = float(sum(lista_wallet_valori_in_usdt.values()))
        # stampe finali
        colorizza(CYELLOW2 + CBOLD, CGREY, CGREEN2, CGREY, CBEIGE2, CGREEN, CYELLOW2, CGREEN)
        disegna_riga_usdt('•')
        disegna_tabella_giu()
        print()
        try:  # si confrontano gli ultimi 2 valori storico tot per dare i colori
            if int(storico_totali[list(storico_totali.keys())[-1]]) > int(
                    storico_totali[list(storico_totali.keys())[-2]]):
                COL_TOTALE = CBLUE
            if int(storico_totali[list(storico_totali.keys())[-1]]) < int(
                    storico_totali[list(storico_totali.keys())[-2]]):
                COL_TOTALE = CRED
            if int(storico_totali[list(storico_totali.keys())[-1]]) == int(
                    storico_totali[list(storico_totali.keys())[-2]]):
                COL_TOTALE = CYELLOW
        except:  # se non si trovano valori
            COL_TOTALE = CYELLOW
        print(
            f'{CBOLD}{COL_TOTALE}TOTALE: {somma:8.2f} USDT {CEND}{somma/lista_simboli_quotazioni.get("btc"):2.8f} BTC          (In aggiornamento...). {CBOLD + CVIOLET}Ciclo n° {contatore_cicli:} {CEND} Errori: {chiusura_forzata}')
        print(CWHITE)
        print(f'{CREDBG} {min_tot:.2f} {CBLUEBG} {max_tot:.2f}{CEND}')

        # Ricava i valori della candela caricandoli dalla LISTA_SIMBOLI
        # connessione websocket
        try:  # connessione websocket
            ws = create_connection("wss://stream.binance.com:9443/ws/" + LISTA_SIMBOLI[z] + "usdt@kline_1m")
            message = ws.recv()
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
            # aggiorna il valore ciclo z lento caricato dal web es: {btc:25000}
            token_in_wallet_valore = wallet_personale[str(
                LISTA_SIMBOLI[z])] * valore  # calcola il valore in usdt della singola moneta
            lista_wallet_valori_in_usdt.update({LISTA_SIMBOLI[z]: token_in_wallet_valore})
            token_in_wallet_valore = wallet_personale[str(LISTA_SIMBOLI[z])] * valore  # es. 0.5 * 50000
            lista_simboli_quotazioni.update({LISTA_SIMBOLI[z]: valore})  # es. {btc:50000}
            # Score
            if prec_lista_simboli_quotazioni.get(LISTA_SIMBOLI[z]) == lista_simboli_quotazioni.get(
                    LISTA_SIMBOLI[z]):  # Score 0
                score = 0
            if prec_lista_simboli_quotazioni.get(LISTA_SIMBOLI[z]) > lista_simboli_quotazioni.get(
                    LISTA_SIMBOLI[z]):  # Score -1
                score = -1
            if prec_lista_simboli_quotazioni.get(LISTA_SIMBOLI[z]) < lista_simboli_quotazioni.get(
                    LISTA_SIMBOLI[z]):  # Score 1
                score = 1
            lista_simboli_score[LISTA_SIMBOLI[z]] += score  # Aggiorna punteggio score del singolo token
        except:  # problema connessione chiudi ws
            print("PROBLEMA CONNESSIONE")
            ws.close()
            chiusura_forzata += 1

    # --------- PARTE 3 - FINE DEL CICLO Z DI AGGIORNAMENTO WEB   
    storico_totali.update({str(time_date): somma})
    aggiorna_massimali(somma)
    prec_lista_simboli_quotazioni = lista_simboli_quotazioni.copy()
    if CRITTOGRAFIA:
        salva_log_key()
    else:
        salva_log()

    ws.close()
    aggiorna_massimali_token()
