#利用splinter库可以在载入网页时执行javascript代码，从而得到最终展现的静态页面 

#coding=gbk
from splinter import Browser
import os, sys, time

#全局计数器
img_num = 0

#浏览器
br = Browser('chrome')

#输出文件
fout = open('img_result.txt', 'w')

#url
beauty_home_url = 'http://page.renren.com/601003665/album'

#主页面
def beauty_home():
	#浏览所有的分页面
	for i in range(54):
		beauty_page_url = beauty_home_url + '?curpage=' + str(i)
		beauty_page(beauty_page_url)
		
def beauty_page(url):
	print 'page_url=', url
	br.visit(url)
	
	#抓取所有的url
	url_list = []
	for div in br.find_by_css('div.picitem '):
		try:
			a = div.find_by_tag('a').first
			url = a['href']
			url_list.append(url)
		except:
			continue
	
	#遍历所有的url
	for url in url_list:
		beauty_nav(url)
	
def beauty_nav(url):
	print 'nav_url=', url
	br.visit(url)
	
	url_list = []
	for td in br.find_by_css('td.photoPan '):
		try:
			a = td.find_by_tag('a').first
			url = a['href']
			url_list.append(url)
		except:
			continue
	
	for url in url_list:
		beauty_final(url)

def beauty_final(url):
	global img_num
	img_num += 1
	print 'img_num=', img_num, 'beauty_final=', url
	br.visit(url)
	time.sleep(5)
	
	try:
		img = br.find_by_id('photo').first
		print img['src']
		if img['src'] != 'http://s.xnimg.cn/a.gif': #没有加载完成
			print >> fout, img['src']
			fout.flush()
	except:
		return
	
	
	
if __name__ == '__main__':
	beauty_home()
	#beauty_final('http://page.renren.com/601003665/photo/7831703770') #测试链接
	
	#关闭浏览器
	try:
		br.quit()
	except:
		pass
	
	fout.flush()
	fout.close()
