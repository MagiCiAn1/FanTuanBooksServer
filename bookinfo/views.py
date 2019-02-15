# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import json
import requests
from bs4 import BeautifulSoup
# Create your views here.


def get_book_by_qidian(book_name):
	start_url = 'https://www.qidian.com/search'
	html = requests.get(start_url + '?kw=%s'%book_name).content
	soup = BeautifulSoup(html, 'lxml')
	book_list_tag = soup.find("div",{"class":"book-img-text"})
	search_book =  book_list_tag.contents[1].contents[1].contents

	book_get_name = search_book[3].h4.a.text
	if book_name == book_get_name:
		book_img = 'https:'+search_book[1].a.img['src']
		auth = search_book[3].p.contents[2].text
		type = search_book[3].p.contents[5].text
		intro = search_book[3].contents[5].text
		return {'book_img':book_img,'auth':auth, 'type':type, 'intro':intro.replace('\r', '')}


def get_base_link_by_xbiquge(book_name):
	url = 'http://www.xbiquge.la/xiaoshuodaquan/'



def bookinfo(request):
	if request.method == 'GET':
		book_info = {}
		book_name = request.GET.get("word")
		book_info = get_book_by_qidian(book_name)
		get_base_link_by_xbiquge(book_name)
		return HttpResponse(json.dumps(book_info))
