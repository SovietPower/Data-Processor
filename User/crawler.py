from turtle import goto
import requests
import json
import time
import random
import xlwt
import os

PATH = os.path.dirname(os.path.abspath(__file__))

main_url = 'https://weibo.com/ajax/friendships/friends?relate=fans&page=3&uid=2106192855&type=fans&newFollowerCount=0'
headers = {
	# ua代理
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
	# 登录信息
	'cookie': 'REPLACE WITH your cookie.'
}


uids = ['2106192855', '2656274875', '1241148864', '1195230310', '1192329374',
	'1195242865', '2440179153', '1288739185', '1642351362', '1730077315',
	'5310675167', '1280761142', '1792673805', '5397477824', '2105807580',
	'6864439668', '1688511087', '2610239182', '6190030326', '1733152694',
	'2639360335', '3099016097', '2025442435', '6550815288', '1563926367',
	# 5w (25)
	'7255435816', '1644461042', '2395743084', '2090591961', '1689219395',
	'2891529877', '1687442081', '2110705772', '1752467960', '1650450024',
	'2360812967', '2370784220', '1822398137', '1039916297', '1344757242',
	'1769985142', '6850370174', '2548864682', '1830483711', '2189608911',
	'1502844527', '1919114090', '1781462195', '1721159394', '1760607222'
	# 10w (50)
	]
	# '', '', '', '', '',
# next now: 20
# 1k/sheet 2k/uid

def CheckDuplicatedUID():
	for i in range(0, len(uids)):
		for j in range(0, len(uids)):
			if uids[i] == uids[j] and i != j:
				print('Duplicated UID:', i, j, uids[i])
				assert(False)
	assert(len(set(uids)) == len(uids))

def main():
	CheckDuplicatedUID()
	Crawl(42, 1)
	return
	for now in range(47, len(uids) if False else 50):
		for part in [1, 2]:
			Crawl(now, part)

def Crawl(now, part):
	# now = len(uids)-1
	uid = uids[now]
	xls_number = str(now) + '_' + str(part)

	wb = xlwt.Workbook()
	ws = wb.add_sheet('new')

	total = 0
	# ws.write(0, 0, 'name')
	# ws.write(0, 1, 'description')

	print('crawling with uid:', uid, ' now:', now, ' part:', part)
	rg = range(99, 49, -1) if part==1 else range(49, -1, -1)
	for page_number in rg:
		time.sleep(random.random() * 2)
		# print('crawling on page', page_number, 'with uid:', uid, ' now:', now)

		url = 'https://weibo.com/ajax/friendships/friends?relate=fans&page='+str(page_number)+'&uid='+uid+'&type=fans&newFollowerCount=0'
		retry_count = 0
		while True:
			response = requests.get(url=url, headers=headers)
			if response.status_code == 200:
				text = response.text.encode("gbk", "ignore").decode("gbk", "ignore")
				# print('text:', text)
				content = json.loads(text)  # 将文本转为json格式
				# print('content:', content)

				try:
					data = content['users']
					for user in data:
						name = str(user['name'])
						description = str(user['description'])
						# print(name, description)
						ws.write(total, 0, name)
						ws.write(total, 1, description)
						total += 1
					break
				except:
					print('Failed in page', page_number)
					pass
			else:
				print('Wrong status in page', page_number, 'with code', response.status_code)
			retry_count += 1
			print('Retry to crawl page', page_number)
			if retry_count > 3:
				break

	wb.save(PATH+'\\username\\username_'+xls_number+'.xls')

main()
