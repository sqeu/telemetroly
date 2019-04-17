# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 11:03:22 2019

@author: S80240
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from bs4 import BeautifulSoup

import hashlib
import pprint
import random
import requests
import time

_GOOGLEID = hashlib.md5(str(random.random()).encode('utf-8')).hexdigest()[:16]
_COOKIES = {'GSP': 'ID={0}:CF=4'.format(_GOOGLEID)}
_HEADERS = {
    'accept-language': 'en-US,en',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml'
    }
_HOST = 'http://www.telemetro.com'
_NEWSSEARCH = '/busqueda/?page={0}&text={1}&minDate={2}&maxDate={3}&contentType=NWS'
_SESSION = requests.Session()
_PAGESIZE = 100
_ENCODING='utf-8'

def _get_page(pagerequest):
    """Return the data for a page on telemetro.com"""
    # Note that we include a sleep to avoid overloading the scholar server
    time.sleep(2+random.uniform(0, 6))
    _GOOGLEID = hashlib.md5(str(random.random()).encode('utf-8')).hexdigest()[:16]
    _COOKIES = {'GSP': 'ID={0}:CF=4'.format(_GOOGLEID)}
    resp_url = _SESSION.get(pagerequest, headers=_HEADERS, cookies=_COOKIES)
    if resp_url.status_code == 200:
        return resp_url.text
    else:
        raise Exception('Error: {0} {1}'.format(resp_url.status_code, resp_url.reason))
        
def _get_soup(pagerequest):
    """Return the BeautifulSoup for a page"""
    html = _get_page(pagerequest)
    return BeautifulSoup(html, 'lxml')

def _search_in_soup(soup):
    """Generator that returns Publication objects from the search page"""
    while True:
        resultList = soup.find("div", {"class" : "lst-search-results"})
        for row in resultList.findAll("div", {"class": lambda L: L and L.startswith('mt')}):
            yield Publication(row)
        next_= soup.find("a", {"class": lambda L: L and L.startswith('btn btn-next page')})
        if next_:
            soup = _get_soup(_HOST+next_['href'])
        else:
            break

def search_pubs_query(query,minDate,maxDate,pageNumber=1):
    """Search by scholar query and return a generator of Publication objects"""
    soup = _get_soup(_HOST+_NEWSSEARCH.format(pageNumber,query,minDate,maxDate))
    return _search_in_soup(soup)

def _body_in_soup(article_soup):
    """Generator that returns Publication objects from the search page"""
    summary=""
    body=""
    for resultList in article_soup.findAll("div", {"class" : lambda L: L and L.startswith('mce-body')}):
        for row in resultList.findAll("p", {"class": 'mce'}):
            if summary == "":
                summary = row.text
            else:  
                #and not row.find('a').has_attr('target')            
                if not row.find('a') and not row.has_attr('dir') and not row.has_attr('lang'):
                    body = body +" <br>"+ row.text
    return (summary,body)
        
        
class Publication(object):
    """Returns an object for a single publication"""
    def __init__(self, __data):
        self.bib = dict()
        self.bib['title'] = __data.find('a').text
        if __data.find('span'):
            self.bib['kicker'] = __data.find('span').text
        else:
            self.bib['kicker'] = ""
        if __data.find('small'):
            self.bib['date'] = __data.find('small')['title']
        else:
            self.bib['date'] = ""
        self.bib['link'] = __data.find('a',href=True)['href']
        
        article_soup = _get_soup(_HOST+__data.find('a',href=True)['href'])
        body=_body_in_soup(article_soup)
        
        self.bib['summary']=body[0]
        self.bib['body']=body[1]
                
    def __str__(self):
        return pprint.pformat(self.__dict__)
    
def get_pdf(url):
    soup = _get_soup(url,True)
    head = soup.findAll("head")
    url = None
    for row in head:
        if row.find("meta",{'name':'citation_pdf_url'}) is not None:
            url = row.find("meta",{'name':'citation_pdf_url'})['content']
    return url
                
    

#from tqdm import tqdm
#query='bcp'
#resultado = search_pubs_query('bcp')
#q=next(resultado)
#print(q)
#q.bib['title']

#f= open(query+".txt","x+")
#for q in tqdm(resultado):
#    try:
#        f.write(q.bib['title'].replace(' ','_')+"|"+q.bib['link']+"|"+q.bib['author']+"\n")
#    except ValueError as e:
#        print(e.__context__)
#f.close()