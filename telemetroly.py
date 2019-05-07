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
    'accept-language': 'es-AR,es',
    #Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml'
    }
_HOST = 'http://www.telemetro.com'
_NEWSSEARCH = '/busqueda/?page={0}&text={1}&minDate={2}&maxDate={3}&contentType=NWS'
_SESSION = requests.Session()
_PAGESIZE = 100
_ENCODING='utf-8'
bad_chars = [' \ufeff','\u200e','\u200f']
def _get_page(pagerequest):
    """Return the data for a page on telemetro.com"""
    # Note that we include a sleep to avoid overloading the scholar server
    time.sleep(3+random.uniform(2, 6))
    _GOOGLEID = hashlib.md5(str(random.random()).encode('utf-8')).hexdigest()[:16]
    _COOKIES = {'GSP': 'ID={0}:CF=4'.format(_GOOGLEID)}
    try:
        resp_url = _SESSION.get(pagerequest, headers=_HEADERS, cookies=_COOKIES)
    except:
        print("Error controlado: ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response',))")
        time.sleep(3+random.uniform(2, 6))
        #_SESSION.get(pagerequest, headers=_HEADERS, cookies=_COOKIES)
        resp_url = requests.get(pagerequest)
    if resp_url.status_code == 200:
        return resp_url.text
    elif resp_url.status_code == 520:
        print("Error controlado: 520: ('Origin Error')")
        return _get_page(pagerequest)
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
        if resultList.find('blockquote'):
            for u in resultList.findAll('blockquote', {"class" : lambda L: L and L.startswith('instagram')}):
                #unwanted = resultList.find('blockquote')
                u.extract()
        for row in resultList.findAll("p", {"class": 'mce'}):
            if summary == "":
                summary = row.text
            else:  
                #and not row.find('a').has_attr('target')            
                if  not row.find('a') and not row.has_attr('dir') and not row.has_attr('lang'):
                    body = body +" <br>"+ row.text
        if summary.strip(' ') == "" or body == "":
            for row in resultList.findAll("div", {"class": 'mce'}):
                if summary.strip(' ') == "":
                    summary = row.text
                else:           
                    if not row.find('a') and not row.has_attr('dir') and not row.has_attr('lang'):
                        body = body +" <br>"+ row.text
            if body == "":
                old_summary=summary.replace("\x92","'").replace("\x93",'"').replace("\x94",'"')
                summary=""
                #One p tag
                for row in old_summary.split('. '):
                    if summary == "":
                        summary = row + "."
                    else:             
                        body = body +". <br> "+ row
                body=body[1:]        
    return (summary,body)
        
        
class Publication(object):
    """Returns an object for a single publication"""
    def __init__(self, __data):
        self.bib = dict()
        
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
        bib_title = __data.find('a').text
        bib_summary=body[0]
        bib_body=body[1]
        for bad_char in bad_chars:
            bib_title=bib_title.replace(bad_char,'')
            bib_summary=bib_summary.replace(bad_char,'')
            bib_body=bib_body.replace(bad_char,'')
            
        self.bib['title'] = bib_title
        self.bib['summary']=bib_summary
        self.bib['body']=bib_body
                
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