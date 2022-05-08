# 删除了：去哪儿测试景点
# 共509

import xlrd


wb = xlrd.open_workbook(r'E:\Poetic Journey\Data Processor\Scenery\sh.xlsx', encoding_override='utf-8')
st = wb.sheet_by_name('sheet1')

f = open(r'E:\Poetic Journey\Data Processor\Scenery\scenery_insert.sql', 'w', encoding='utf-8')

def FindShiPos(address):
	pos = -1
	for i in range(len(address)):
		if (address[i] == '市'):
			pos = i
			break
	if (pos == -1):
		for i in range(1, len(address)):
			if (address[i-1] == '上' and address[i] == '海'):
				pos = i
				break
	return pos

def FindQuPos(address, shi_pos):
	pos = -1
	for i in range(len(address)):
		if (address[i] == '区'):
			pos = i
			break
	if pos-shi_pos > 4:
		pos = -1
	return pos

def StringToFloat(str):
	return float(str) if str!='' else 0

f.write('insert into scenery(scenery_name, province, city, district, street, intro, open_time, level, score, price) values\n')

nRows = st.nrows
for i in range(1, nRows):
# for i in range(1, 5):
	arr = st.row_values(i)
	address = arr[2]
	province = '上海市'
	city = '上海市'
	shi_pos = FindShiPos(address)
	qu_pos = FindQuPos(address, shi_pos)
	# print(address, 'shi_pos:', shi_pos, 'qu_pos:', qu_pos)
	if (qu_pos > 0):
		assert(qu_pos > shi_pos)

	district = address[shi_pos+1:qu_pos+1] if qu_pos>0 else ''
	street = address[qu_pos+1:] if qu_pos>0 else address[shi_pos+1:]

	intro = arr[6]
	open_time = arr[7] if arr[7]!='暂无' else ''
	level = arr[1]
	score = StringToFloat(arr[3])
	price = StringToFloat(arr[5][1:])

	# print(i)
	f.write(
	'''('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %.1f, %.1f)%s\n''' % (arr[0], province, city, district, street, intro, open_time, level, score, price, ',' if i!=nRows-1 else ';'))

	# print(st.row_values(i))


f.close()

