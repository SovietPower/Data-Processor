import os
from secrets import choice
import xlrd
from random import randint, uniform

PATH = os.path.dirname(os.path.abspath(__file__))

# 1k/sheet 2k/uid
# 0-24: 5w	-49: 10w
L = 40
R = 49
f = open(PATH + '\\user_insert_'+str(L)+'_'+str(R)+'.sql', 'w', encoding='utf-8')

if L == 0:
	f.write('delete from user;\n')
	f.write('alter table user AUTO_INCREMENT 1;\n\n')
f.write('insert into user(username, gender, age, province, city, district) values\n')

genders = ['男', '男', '女', '女', '女', '女', '保密']

wb_add = xlrd.open_workbook(PATH + '\\address.xlsx')
sh_add = wb_add.sheet_by_name('Sheet1')
nrows_add = sh_add.nrows

def RandAge():
	if randint(1, 4) == 0: # 1/4
		return 'null'
	x = randint(1, 5)
	# 1/5
	if x <= 1:
		return randint(14, 17)
	# 3/5
	if x <= 4:
		return randint(18, 25)
	# 1/5
	return randint(26, 35)

def AddQuotes(s):
	return '\''+s+'\''

def CheckNRows():
	for i in range(L, R+1):
		for j in range(1, 3):
			wb = xlrd.open_workbook(PATH + '\\username\\username_'+str(i)+'_'+str(j)+'.xls')
			sh = wb.sheet_by_name('new')
			if sh.nrows != 1000:
				print('Sheet username', i, j, 'has a row number of', sh.nrows)

def main():
	CheckNRows()

	for i in range(L, R+1):
		for j in range(1, 3):
			print('Working on sheet: username', i, j)

			wb = xlrd.open_workbook(PATH + '\\username\\username_'+str(i)+'_'+str(j)+'.xls')
			sh = wb.sheet_by_name('new')
			nrows = sh.nrows
			assert(nrows == 1000)
			for k in range(0, nrows):
				username = sh.row_values(k)[0]
				gender = choice(genders)
				age = RandAge()

				address = sh_add.row_values(randint(0, nrows_add-1))
				province = AddQuotes(address[0]) if randint(1, 20)>1 else 'null' # 1/20
				city = AddQuotes(address[1]) if province[0]!='n' and randint(1, 10)>1 else 'null' # 1/10
				district = AddQuotes(address[2]) if city[0]!='n' and randint(1, 3)>1 else 'null' # 1/3

				# 注意 province, city, district 在内容中加引号
				lastChar = ","
				if i == R and j == 2 and k == nrows-1:
					lastChar = ";"
				f.write('''('%s', '%s', %s, %s, %s, %s)%s\n''' % (username, gender, age, province, city, district, lastChar))

main()
f.close()

