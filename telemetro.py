# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 15:02:48 2019

@author: S80240
"""

import telemetroly
from tqdm import tqdm 

query='afp'
minDate='01-05-2016'
maxDate='31-05-2016'
page=1

bad_chars='[(){}<>,.@;:"\'?¿!¡/|]' 


#q=next(search_query)
#print(q.bib['title'].replace(' ','_'))

search_query = telemetroly.search_pubs_query(query,minDate,maxDate,page)

f= open("..//"+query+maxDate+".txt","a+")#,errors = 'ignore'
for q in tqdm(search_query):
    try:
        f.write(q.bib['title']+"|"+q.bib['kicker']+"|"+q.bib['date']+"|"+q.bib['link']+"|"+q.bib['summary']+"|"+q.bib['body']+"\n")
    except: 
        f_e= open("..//"+query+maxDate+"_exception.txt","a+")
        f_e.write(q.bib['title']+"|"+q.bib['kicker']+"|"+q.bib['date']+"|"+q.bib['link']+"\n")
        f_e.close()
f.close()




##################################
q1= next(search_query)
print(q1)


query='Grupo de Lima pide cambio de gobierno en Venezuela "sin uso de la fuerza"'
minDate='01-02-2019'
maxDate='28-02-2019'
bad_chars='[(){}<>,.@;:"\'?¿!¡/|]' 


#q=next(search_query)
#print(q.bib['title'].replace(' ','_'))

search_query = telemetroly.search_pubs_query(query,minDate,maxDate)

f= open("1.txt","a+")#,errors = 'ignore'
for q in tqdm(search_query):
    f.write(q.bib['title']+"|"+q.bib['kicker']+"|"+q.bib['date']+"|"+q.bib['link']+"|"+q.bib['summary']+"|"+q.bib['body']+"\n")
f.close()
