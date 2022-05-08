from random import randint, uniform

f = open(r'E:\Poetic Journey\Data Processor\Tag\tag_table_insert.sql', 'w', encoding='utf-8')

f.write('delete from tag_table;\n')
f.write('alter table tag_table AUTO_INCREMENT 1;\n\n')
f.write('insert into tag_table(tag) values\n')

tag_arr = ['公园', '博物馆', '观光', '学生最爱', '商场', '花', '民俗', '古镇', '历史', '迪士尼', '游乐场', '美景', '名胜', '主题体验', '海滨', '动植物园', '游船', '农家田园', '游泳', '海洋馆', '水上乐园']


def main():
	total = len(tag_arr)
	for count in range(1, total+1):
		f.write(
			'''('%s')%s\n''' % (tag_arr[count-1], ',' if count!=total else ';'))

main()
f.close()

