# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 12:56:07 2018
@author: ZHILANGTAOSHA
"""
import urllib
import urllib.request as urllib2
import time
try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup
import re
import sys
import requests
import json
import pandas as pd
def set_headers(base_url):
    """
    Set up headers to fake as a browser visit
    """
    headers  = {'http://toy1.weather.com.cn/search?':{
                        'Host': 'toy1.weather.com.cn',
                        'Connection': 'keep-alive',
                        'Accept': '*/*',
                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
                        'Referer': 'http://www.weather.com.cn/',
                        'Accept-Encoding': 'gzip, deflate, sdch',
                        'Accept-Language': 'en-US,en;q=0.8'
                    },
            'http://d1.weather.com.cn/sk_2d/':{
                            'Host': 'd1.weather.com.cn',
                            'Connection': 'keep-alive',
                            #('Cache-Control','max-age=0'),
                            'Accept': '*/*',
                            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
                            'Referer': 'http://www.weather.com.cn/weather1d/{0}.shtml',
                            'Accept-Encoding': 'gzip, deflate, sdch',
                            'Accept-Language': 'en-US,en;q=0.8'
            }
        }
    return headers[base_url]
def search_city_weather(cityname="yangzhou"):
    """
    This is a cross-site request.
    @cityname:search cityname
    @callback:callback function
    @_:time stamp in micro-seconds
    """
    base_url = "http://toy1.weather.com.cn/search?"
    data = [("cityname",cityname),
            ("callback","success_jsonpCallback"),
            ("_",str(int(time.time()*1000)))]
    payload = urllib.parse.urlencode(data)
    url = base_url + "{0}".format(payload)
    headers = set_headers(base_url)
    print ("Request URL: " + url)
    req = urllib2.Request(url, data=None, headers=dict(headers))
    f = urllib2.urlopen(req)
    results = f.read()
    cities = parse_city(results.decode('utf-8'))
    return cities
def parse_city(results):
    pattern_all = re.compile(r'[^[]*(\[.*\])')
    cities_str = pattern_all.findall(results)[0]
    pattern_cities = re.compile(r'(\{\".+?\":\".+?\"\})')
    cities = pattern_cities.findall(cities_str)
    pattern_city_info = re.compile(r':\"(.+?)\"')
    for i in range(len(cities)):
        cities[i] = pattern_city_info.findall(cities[i])[0].split('~')
    return cities
def get_sk(citycode):
    beijing_url = 'http://d1.weather.com.cn/sk_2d/%s.html'%citycode
    headers = {
                            'Host': 'd1.weather.com.cn',
                            'Connection': 'keep-alive',
                            #('Cache-Control','max-age=0'),
                            'Accept': '*/*',
                            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
                            'Referer': 'http://www.weather.com.cn/weather1d/%s.shtml'%citycode,
                            'Accept-Encoding': 'gzip, deflate, sdch',
                            'Accept-Language': 'en-US,en;q=0.8'}
    r = requests.get(beijing_url, headers=headers,timeout=10)
    r.encoding = 'utf8'
    weather = json.loads(r.text[13:])
    return weather
def get_text(i):
    if i.get('title') == None:
        text = i.text
    else:
        text = str(i.get('title')) + i.text
    return text
def get_dail(citycode):
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'}
    url = "http://www.weather.com.cn/weather1d/%s.shtml"%citycode
    web_data = requests.get(url, headers=headers)
    web_data.encoding = 'utf-8'
    content = web_data.text
    soup = BeautifulSoup(content, 'lxml')
    jg = soup.find_all('div', class_ = "today clearfix")[0]
    drqk = jg.find_all('ul', class_ = "clearfix")[0].find_all('span')
    jg = [get_text(i) for i in drqk]
    jg = pd.DataFrame(jg)
    return jg
def get_7d(citycode):
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'}
    url = "http://www.weather.com.cn/weather/%s.shtml"%citycode
    web_data = requests.get(url, headers=headers)
    web_data.encoding = 'utf-8'
    content = web_data.text
    soup = BeautifulSoup(content, 'lxml')
    jg = soup.find_all('div', class_ = "c7d")[0]
    drqk = jg.find_all('ul', class_ ="t clearfix")[0].find_all('li')[1:]
    c7d = []
    for i in drqk:
        c7d.append(re.sub('\n+','\n',i.text).split('\n')[1:-1])
    fx = []
    for i in drqk:
        fx.append(str(i.find_all('span')[-2].get('title')))
    c7d = pd.DataFrame(c7d)
    c7d['nf'] = fx
    c7d.columns = ['c7drq','c7dtq','c7dwd','c7dfj','c7dfx']
    c7dz = c7d.head(1).loc[0].to_dict()
    for i in c7d.index[1:]:
        ls = c7d.loc[i]
        ls.index = ls.index + str(i)
        ls = ls.to_dict()
        c7dz.update(ls)
    return c7dz