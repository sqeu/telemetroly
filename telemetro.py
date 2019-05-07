# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 15:02:48 2019

@author: S80240
"""

import telemetroly
from tqdm import tqdm 
import datetime

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)

months=[]
for month in range(1, 13):
    month_str=str(last_day_of_month(datetime.date(2009, month, 1)))
    months.append(month_str[-2:]+'-'+month_str[5:7]+'-'+month_str[:4])

#for month in months[4:]:
for month in months[:-1]:
    query='afp'
    minDate='01'+month[2:]
    maxDate=month
    page=33
            
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


query='Thiago Alcántara tendrá que volver a operarse tras recaer de su lesión'
minDate='01-10-2014'
maxDate='31-10-2014'
bad_chars='[(){}<>,.@;:"\'?¿!¡/|]' 


#q=next(search_query)
#print(q.bib['title'].replace(' ','_'))

search_query = telemetroly.search_pubs_query(query,minDate,maxDate)

f= open("1.txt","a+")#,errors = 'ignore'
for q in tqdm(search_query):
    f.write(q.bib['title']+"|"+q.bib['kicker']+"|"+q.bib['date']+"|"+q.bib['link']+"|"+q.bib['summary']+"|"+q.bib['body']+"\n")
f.close()
