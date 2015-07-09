#coding=utf-8
#获取人人相册图片

import os
import re
from lxml import html
import requests
import ConfigParser

def get_config():
	config = ConfigParser.RawConfigParser()  #生成config对象
	config.read('config.ini') #读取配置文件
	return config

def get_url(config):
	person_dict = {}
	url_pre = "http://photo.renren.com/photo/"
	person_id = config.options('person')
	for id in person_id:
		person_dict[id] = url_pre + id.strip() + "/albumlist/v7#"
	return person_dict

def headers(config):
	headers = {
				'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
				'Accept-Encoding':'gzip, deflate, sdch',
				'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
				'Connection':'keep-alive',
				'Host':'photo.renren.com',
				'RA-Sid':'7C4D1DF6-20150705-065431-804159-c1fc8d',
				'RA-Ver':'3.0.1',
				'Referer':'http://photo.renren.com/photo/284894340/albumlist/v7',
				'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
	}
	headers['Cookie'] = config.get('cookie', 'cookie')
	return headers

def request(url,headers):
	response = requests.get(url,headers=headers)
	return response

def get_albums(response):
	body = html.fromstring(response.text)
	js = body.xpath('//script/text()') #获取js段代码
	js = map(lambda x : x.encode('utf-8'), js) #转换成utf-8
	album_js = js[3] #相册号所在的js段
	#正则匹配albumList
	album_raw = re.findall(r"'albumList':\s*(\[.*?\]),", album_js)[0]
	album_list = eval(album_raw) #执行js代码
	album_url_dict = {}
	for album in album_list:
		if album['sourceControl'] == 99:
			album_url = 'http://photo.renren.com/photo/'+str(album['ownerId'])+'/album-'+album['albumId']+'/v7'
			album_url_dict[album['albumId']] = {}
			album_url_dict[album['albumId']]['album_url'] = album_url
			album_url_dict[album['albumId']]['photo_count'] = album['photoCount']
			album_url_dict[album['albumId']]['album_name'] = album['albumName']	
	return album_url_dict

def get_imgs(album_url_dict, headers):
	img_dict = {}
	for key, val in album_url_dict.iteritems():
		album_url = val['album_url']
		response = request(album_url, headers)
		parsed_body = html.fromstring(response.text)
		js = parsed_body.xpath('//script/text()')
		text = js[3].encode('utf-8')
		image_list = re.findall(r'"url":"(.*?)"', text)
		img_dict[key] = image_list
	return img_dict

def download_img(img_dict, album_url_dict, start_dir):
	for album_id, image_list in img_dict.iteritems():
		cur_dir = start_dir + album_url_dict[album_id]['album_name'].replace(' ', '_')
        
		if not os.path.exists(cur_dir):
			os.makedirs(cur_dir)

		image_list = map(lambda x: x.replace('\\', ''), image_list)
		for url in image_list:
			print url + "  start!"
			response = requests.get(url)
			with open(cur_dir + '/' + url.split('/')[-1], 'wb') as f:
				f.write(response.content)
                
			print url + "  done!"

if __name__ == '__main__':
	config = get_config()
	url = get_url(config)
	headers = headers(config)
	for rid,url in url.iteritems():
		name = config.get('person', rid)
		print 'start downloading' + ' ' + name + '\'s albums!'
		print '----------------------------------------'
		start_dir = config.get('dir', 'start_dir') + name + '/'
        response = request(url, headers)
        album_url_dict = get_albums(response)
        img_dict = get_imgs(album_url_dict, headers)
        download_img(img_dict, album_url_dict, start_dir)
        print '----------------------------------------'
        print 'end downloading!'