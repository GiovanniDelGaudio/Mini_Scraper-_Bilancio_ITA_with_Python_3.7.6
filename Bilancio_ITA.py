#-_- CODING : UTF-8 °-°
"""
@AUTHOR: JOH4CK(JOHNNY DEL GAUDIO)

MINI SCRAPING SULLA BORSA  E ANDAMENTO DELLA QUOTA ITALIANA 
PARTENDO DA GENNAIO 01 2000 AD OGGI.

SITO DI RIFERIMENTO YAHOO FINANCE E API YAHOO
IN QUESTO ESEMPIO SI USA YAHOO API PER EFFETUARE SCAPING
IN REAL TIME

USO A SCOPO DIMOSTRATIVO

IN QUESTO MINI SCRAPING, VIENE UTILIZZATO PRINCIPALMENTE:

LA LIBRERIA PANDAS PER PER LA MANIPOLAZIONE DI DATI IN FORMATO SEQUENZIALE O TABELLARE, QUALI SERIE TEMPORALI O DATI DI MICROARRAY.
CARATTERISTICHE PRINCIPALI DI PANDAS SONO:
-------------------------------------------------
CARICAMENTO E SALVATAGGIO DI FORMATI STANDARD PER DATI TABELLARI, QUALI CSV (COMMA-SEPARATED VALUES), TSV (TAB-SEPARATED VALUES), FILE EXCEL E FORMATI PER DATABASE

SEMPLICITÀ NELLA ESECUZIONE DI OPERAZIONI DI INDICIZZAZIONE E AGGREGAZIONE DI DATI

SEMPLICITÀ NELLA ESECUZIONE DI OPERAZIONI NUMERICHE E STATISTICHE

SEMPLICITÀ NELLA VISUALIZZAZIONE DEI RISULTATI DELLE OPERAZIONI
-------------------------------------------------
LA LIBRERIA MATPLOTLIB libreria per la realizzazione di grafici estremamente potente e flessibile.

Il modulo pyplot della libreria permette di realizzare in maniera semplice moltissimi tipi di plots.

Il modulo si importa di solito rinominandolo plt
-----------------------------------------------------
Infine libreria NUMPY:
---------------------------------------------------
è una libreria open source per il linguaggio di programmazione Python, che aggiunge supporto a grandi matrici e array multidimensionali insieme a una vasta collezione di funzioni matematiche di alto livello
--------------------------------------------------


L'ALGORITMO VISUALIZZA IN REAL TIME IL GRAFICO ESPONENZIALE
"""

from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime




INIZIO_DATA = '2000-01-01'
FINE_DATA  =  str(datetime.now().strftime('%Y-%m-%d'))

IT_STOCK = 'ITLMS.MI'


def get_stati(stock_data):
    return {
        'ultimo': np.mean(stock_data.tail(1)),
        'short_mean': np.mean(stock_data.tail(20)),
        'long_mean': np.mean(stock_data.tail(200)),
        'short_rolling': stock_data.rolling(window=20).mean(),
        'long_rolling': stock_data.rolling(window=200).mean()
    
    }

def pulisci_data(stock_data,col):
    weekgiorni = pd.date_range(start=INIZIO_DATA, end=FINE_DATA)
    pulisci_data = stock_data[col].reindex(weekgiorni)
    return pulisci_data.fillna(method='ffill')
  
  
def crea_plot(stock_data, ticker):
    stati = get_stati(stock_data)
    plt.subplots(figsize=(12,8))
    plt.style.use('dark_background')
    plt.plot(stock_data, label=ticker)
    plt.plot(stati['short_rolling'], label='Media di 20 giorni')
    plt.plot(stati['long_rolling'],label='Media di 200 giorni')
    plt.title('Andamento Borsa in REALTIME')
    plt.xlabel('Date giornaliere')
    plt.ylabel('Chiusura in quota bancaria(p)')
    plt.legend()
    
    plt.show()
  
  
def get_data(ticker):
    try:
        stock_data = data.DataReader(ticker,
                                     'yahoo',
                                     INIZIO_DATA,
                                     FINE_DATA)
        adj_close = pulisci_data(stock_data, 'Adj Close')
        crea_plot(adj_close, ticker)
       
    
    except RemoteDataError:
        print('Non è stato possibile trovare un dato per {t}'.format(t=ticker))
        
get_data(IT_STOCK)
