# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 09:40:26 2019

@author: S80240
"""

import telemetroly
from tqdm import tqdm 

query='Salud de Pelé mejora, sale de terapia intensiva y camina en su habitación'
minDate='01-12-2014'
maxDate='31-12-2014'
page=1


#q=next(search_query)
#print(q.bib['title'].replace(' ','_'))

search_query = telemetroly.search_pubs_query(query,minDate,maxDate,page)

result = next(search_query)
result.bib['summary']
result.bib['body']

f= open("..//test.txt","a+")#,errors = 'ignore'
for q in tqdm(search_query):
    f.write(q.bib['title']+"|"+q.bib['kicker']+"|"+q.bib['date']+"|"+q.bib['link']+"|"+q.bib['summary']+"|"+q.bib['body']+"\n")

f.close()

resp_url.text ='hi'

import requests
text = requests.get("http://192.168.99.100:32776/solr/viabcp/select?q=Text%3Abcp+beneficios+mivivienda+credito&fl=id%2C+Document%2C+Link&df=Text&wt=json&indent=true&hl=true&hl.fl=Text&hl.simple.pre=%3Cb%3E&hl.simple.post=%3C%2Fb%3E&hl.snippets=2&rows=2")

js = text.json()
li = js["response"]["docs"]
hl = js["highlighting"]
hl['2706efab-84c1-4e62-95aa-b00b1c848032']
for i in range(len(li)):
    _id=li[i]['id']
    li[i]['hl']=hl[_id]['Text']

li

f= open("..//test.txt","r",newline='\n')#,errors = 'ignore'
for l in f:
    print(l)
    
import csv
with open("..//test.txt", 'rU') as csvIN:
   outCSV=[field.strip() for row in csv.reader(csvIN, delimiter='|') 
              for field in row if field]

i=2
new_lines=[]
while i < len(outCSV):
#for i in range(2,len(outCSV),6):
    #i=14
    line=outCSV[i-2:i+4]
    potential_date = line[2]
    if potential_date[4]=='-' and  potential_date[7]=='-' and line[3].find('html')>0:
        i+=6
    else:
        pre_line=new_lines[len(new_lines)-1]
        pre_i=i-3
        while potential_date[4]!='-' and  potential_date[7]!='-' and line[3].find('html')<0:       
                i+=1
                line=outCSV[i-2:i+4]
                potential_date = line[2]
                while len(potential_date)<10:
                    i+=1
                    line=outCSV[i-2:i+4]
                    potential_date = line[2]

        limit_i=i-2
        print("pre"+str(pre_i))
        print("limit"+str(limit_i))
        clean_body=True
        for j in range(pre_i,limit_i):
            paragraph=outCSV[j]
            if paragraph.find('<br>')<0:
                pre_line[4]=pre_line[4]+paragraph
            else:
                if clean_body:
                    clean_body = False
                    pre_line[5]=''
                pre_line[5]=pre_line[5]+paragraph
        i+=6
        new_lines.pop(len(new_lines)-1)
        new_lines.append(pre_line)
    new_lines.append(line)
    
    break


with open("..//afp31-05-2008.txt","r") as csvfile:
     spamreader = csv.reader(csvfile, delimiter='|')
     for row in spamreader:
         print(row)
         
