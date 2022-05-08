# 删除了：去哪儿测试景点
# 共509

import xlrd
import requests

wb = xlrd.open_workbook(r'E:\Poetic Journey\Data Processor\Scenery Picture\sh_pic.xlsx', encoding_override='utf-8')
st = wb.sheet_by_name('sheet1')

f = open(r'E:\Poetic Journey\Data Processor\Scenery Picture\scenery_picture_insert.sql', 'w', encoding='utf-8')

f.write('delete from scenery_picture;\n\n')
f.write('insert into scenery_picture(scenery_id, pic_id, pic) values\n')

def GetImage(url, name):
	result = requests.get(url)
	while result.status_code != 200:
		result = requests.get(url)
	with open('E:\\Poetic Journey\\Data Processor\\Scenery Picture\\sh\\' + name, "wb") as f:
		f.write(result.content)
		print("正在下载", name)

def main():
	nRows = st.nrows
	for i in range(1, nRows):
	# for i in range(1, 5):
		# print(i)
		arr = st.row_values(i)
		code = arr[1]

		scenery_id = i
		pic_id = 1

		start = code.find('src="')
		while start >= 0:
			suffix = '.jpg'
			end = code.find('.jpg', start)
			next_start = code.find('src="', start+1)
			if end == -1 or (next_start != -1 and end > next_start):
				suffix = '.png'
				end = code.find('.png', start)

			url = code[start+5:end+4]
			print(url)
			if (url[8:23] == 'mp-piao-admincp'):
				break

			img_name = str(scenery_id)+'_'+str(pic_id)+suffix
			key = 'Data/Scenery Picture/'+img_name
			GetImage(url, img_name)

			f.write(
			'''(%d, %d, '%s')%s\n''' % (scenery_id, pic_id, key, ',' if i!=nRows-1 else ';'))

			pic_id += 1
			start = next_start


main()
f.close()

