# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from bookinfo.models import BookInfo
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
		return {'bookName':book_name, 'img':book_img,'author':auth, 'type':type, 'intro':intro.replace('\r', '')}
	else:
		return None

def get_base_link_by_uctxt(book_name):
	# url = 'http://www.xbiquge.la/xiaoshuodaquan/'
	name = book_name
	book_name = book_name.encode('gbk')
	book_name = quote(book_name, 'gbk')
	url = 'http://www.uctxt.com/modules/article/search.php?searchkey='
	header = {
		'Connection': 'keep-alive',
		'Cache-Control': 'max-age=0',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.9',
		'Host': 'www.uctxt.com',
		'Cookie': 'Hm_lvt_4ef9ed7e24c0e6760022d4bfb41097c1=1550327101; UM_distinctid=168f6b235684b2-0f1b29310037e1-4313362-100200-168f6b23569bf; CNZZDATA1271009271=2453161-1550322613-%7C1550322613; jieqiVisitTime=jieqiArticlesearchTime%3D1550327721; Hm_lpvt_4ef9ed7e24c0e6760022d4bfb41097c1=1550327722'
	}
	html = requests.get(url + book_name, headers = header)
	html.encoding='gbk'
	soup = BeautifulSoup(html.text, 'lxml')
	title = soup.head.title.text
	if title[0] =='“':

		book_ul = soup.find("div", {"class":"list-lastupdate"}).ul
		for i in range(1,len(book_ul.contents),2):
			li = book_ul.contents[i]
			if name == li.contents[1].a.string:
				link = li.contents[1].a.get('href')
				last_chapter = li.contents[1].small.a.string
				updated = li.contents[2].contents[2].string
				return "http://www.uctxt.com" + link
	else:
		join_bookcase = soup.find("a", {"href": "javascript:void(0)"})
		onclick = join_bookcase['onclick']
		id = onclick[onclick.find('(')+1:onclick.find(',')]
		if len(id) < 4:
			pre = '0'
		else:
			pre = id[0:-3]
		return "http://www.uctxt.com/book/%s/%s/"%(pre,id)
	# print(html.text)
	return ""

def get_last_chapter(book_name):
	name = book_name
	book_name = book_name.encode('gbk')
	book_name = quote(book_name, 'gbk')
	url = 'http://www.uctxt.com/modules/article/search.php?searchkey='
	header = {
		'Connection': 'keep-alive',
		'Cache-Control': 'max-age=0',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.9',
		'Host': 'www.uctxt.com',
		'Cookie': 'Hm_lvt_4ef9ed7e24c0e6760022d4bfb41097c1=1550327101; UM_distinctid=168f6b235684b2-0f1b29310037e1-4313362-100200-168f6b23569bf; CNZZDATA1271009271=2453161-1550322613-%7C1550322613; jieqiVisitTime=jieqiArticlesearchTime%3D1550327721; Hm_lpvt_4ef9ed7e24c0e6760022d4bfb41097c1=1550327722'
	}
	html = requests.get(url + book_name, headers = header)
	html.encoding='gbk'
	soup = BeautifulSoup(html.text, 'lxml')
	title = soup.head.title.text
	last_chapter_info = {}
	if title[0] =='“':

		book_ul = soup.find("div", {"class":"list-lastupdate"}).ul
		for i in range(1,len(book_ul.contents),2):
			li = book_ul.contents[i]
			if name == li.contents[1].a.string:
				# link = li.contents[1].a.get('href')
				last_chapter = li.contents[1].small.a.string
				updated = li.contents[2].contents[2].string
				last_chapter_info['lastChapter'] = last_chapter
				last_chapter_info['updated'] = updated
				last_chapter_info["referenceSource"] = "default"
				return last_chapter_info
	else:
		root = soup.find('p', {'class':'stats'})
		last_chapter = root.span.a.string
		updated = root.contents[1].contents[5].string
		last_chapter_info['lastChapter'] = last_chapter
		last_chapter_info['updated'] = updated
		last_chapter_info["referenceSource"] = "default"
		return last_chapter_info
	# print(html.text)


def bookinfo(request):

	# bookinfo: http://yourbuffslonnol.com/BookService/bookinfo?word=%E5%9C%A3%E5%A2%9F
	# lastChapter:http://api05iye5.zhuishushenqi.com/book?view=updated&id=59ba0dbb017336e411085a4e
	if request.method == 'GET':
		book_info = {}
		book_name = request.GET.get("word")
		try:
			book_object = BookInfo.objects.get(bookName=book_name)
			print(book_object)
		except:
			book_object = None
		if book_object is not None:

			base_link = get_base_link_by_uctxt(book_name) #base_link:http://www.uctxt.com/book/23/23365/
			base_link = [{"tag":'uctxt','url':'http://www.uctxt.com', 'link':base_link}]
			book_info['baseLink'] = str(base_link)
			BookInfo.objects.update(base_link=book_info.get('baseLink'))
			book_info['id'] = str(book_object.id)
			book_info['bookName'] = book_object.bookName
			book_info['author'] = book_object.author
			book_info['img'] = book_object.img
			book_info['type'] = book_object.type
			book_info['intro'] = book_object.intro
			book_info = [book_info]
			return HttpResponse(json.dumps(book_info, ensure_ascii=False))
		else:
			book_info = get_book_by_qidian(book_name)
			if book_info is None:
				return HttpResponse(json.dumps([], ensure_ascii=False))
			base_link = get_base_link_by_uctxt(book_name) #base_link:http://www.uctxt.com/book/23/23365/
			base_link = [{"tag":'uctxt','url':'http://www.uctxt.com', 'link':base_link}]
			book_info['baseLink'] = str(base_link)
			book_object = BookInfo.objects.create(bookName = book_info.get('bookName'), author=book_info.get('author'), img=book_info.get('img'), type=book_info.get('type'), intro=book_info.get('intro'), base_link=book_info.get('baseLink'))

			book_info['id'] = str(book_object.id)
			book_info = [book_info]
			return HttpResponse(json.dumps(book_info, ensure_ascii=False))


def last_chapter(request):
	if request.method == 'GET':
		ids = request.GET.get('bookid')
		print(ids)
		ids = str(ids).split(',')
		last_chapters = []
		for id in ids:
			try:
				book_object = BookInfo.objects.get(id=id)
			except:
				continue
			if book_object:
				last_chapter_info = get_last_chapter(book_object.bookName)
				last_chapter_info['_id'] = str(book_object.id)
				last_chapter_info['author'] = book_object.author
				last_chapters.append(last_chapter_info)

		return HttpResponse(json.dumps(last_chapters, ensure_ascii=False))
