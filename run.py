#!/usr/bin/env python
# coding:utf8

import time
import sys
reload(sys)
sys.setdefaultencoding( "utf8" )
from flask import *
import warnings
warnings.filterwarnings("ignore")
# import MySQLdb
# import MySQLdb.cursors
from config import *
import random
import math
import urllib2
import urllib
import json
import jieba.analyse
from bs4 import BeautifulSoup

headers = {}
headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"

app = Flask(__name__)
app.config.from_object(__name__)

# 连接数据库
def connectdb():
	db = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWORD, db=DATABASE, port=PORT, charset=CHARSET, cursorclass = MySQLdb.cursors.DictCursor)
	db.autocommit(True)
	cursor = db.cursor()
	return (db,cursor)

# 关闭数据库
def closedb(db,cursor):
	db.close()
	cursor.close()

# 首页
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/cloud', methods=['POST'])
def cloud():
	data = request.form
	url = data['url']
	content = ''

	try:
		req = urllib2.Request(url=url, headers=headers)
		response = urllib2.urlopen(req)
		result = response.read()
		html = BeautifulSoup(result)
		content = unicode(html.get_text())
	except Exception, e:
		pass
	else:
		pass
	finally:
		pass

	tmp = ''
	for x in xrange(0, len(content)):
		if content[x] >= u'\u4e00' and content[x] <= u'\u9fa5':
			tmp += content[x]
	content = tmp

	content = jieba.analyse.extract_tags(content, topK=50, withWeight=True, allowPOS=())

	maxn = -999
	minn = 999
	for c in content:
		if maxn < c[1]:
			maxn = c[1]
		if minn > c[1]:
			minn = c[1]

	colors = ['rgba(84, 148, 191, 1)','rgba(221, 107, 102, 1)','rgba(230, 157, 135, 1)','rgba(234, 126, 83, 1)','rgba(243, 230, 162, 1)']

	data = [{'name':c[0], 'value':int((c[1] - minn) / (maxn - minn) * 50), 'itemStyle':{'normal':{'color':colors[int(math.floor(random.random() * 5))]}}} for c in content]

	return json.dumps({"ok": True, "data": data})

if __name__ == '__main__':
	app.run(debug=True)