#coding=gbk

import sys
import itertools
import urllib2
import json
import logging
from bs4 import BeautifulSoup
import multiprocessing
import traceback
import re

c_BrandListUrl = 'http://m.xiaohongshu.com/api/snsweb/v1/tags/brand?page=%d'
c_BrandUrl = 'http://m.xiaohongshu.com/tag/brand/%s'
c_Concurrency = 100
c_Pattern = re.compile(ur'(.*衣|.*服|.*装|T恤|背心|外套|.*裙|.*裤)')
c_Output = 'brand/brand.txt'

def list_brand(pid):
    res = []
    for page in itertools.count(pid, c_Concurrency):
        try:
            logging.error('page=%d' % page)
            Url = c_BrandListUrl % page
            response = urllib2.urlopen(Url)
            html = response.read().decode('utf-8')
        
            js = json.loads(html)
            brands = js['data']
            if len(brands) == 0:
                break
            for brand in brands:
                tag, labels = one_brand(brand['id'])
                if tag:
                    res.append((brand['name'], labels))
        except Exception, e:
            logging.error('func=%s e=%s' % ('list_brand', e))
    return res

def one_brand(id):
    labels = []
    try:
        Url = c_BrandUrl % id
        response = urllib2.urlopen(Url)
        html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
    
        sections = soup.find_all('section', class_='mod-tag-list')
        if len(sections) == 0:
            return False, []
        ul = sections[0].ul
        labels = [li.text for li in ul.find_all('li')]
        if u'穿搭' not in labels:
            return False, labels
        for text in labels:
            if c_Pattern.match(text):
                return True, labels
    except Exception, e:
        logging.error('func=%s url=%s e=%s' % ('one_brand', Url, e))

    return False, labels

if __name__ == '__main__':
    pool = multiprocessing.Pool(c_Concurrency)
    res_list = pool.map(list_brand, range(1, 1+c_Concurrency))
    logging.error('process work done')

    fout = open(c_Output, 'w')
    for res in res_list:
        for name, labels in res:
            print >>fout, '\t'.join([name.encode('gb18030'), ','.join(labels).encode('gb18030')])
    fout.flush()
    fout.close()
