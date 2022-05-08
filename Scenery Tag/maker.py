from random import randint, uniform

f = open(r'E:\Poetic Journey\Data Processor\Scenery Tag\scenery_tag_insert.sql', 'w', encoding='utf-8')

f.write('delete from scenery_tag;\n')
f.write('alter table scenery_tag AUTO_INCREMENT 1;\n\n')
f.write('insert into scenery_tag(scenery_id, tag_id) values\n')

# todo 检查重复

def main():
	st = set()
	total = 100
	for count in range(1, total+1):
		scenery_id = randint(1, 509)

		tag_id = randint(1, 21)
		while (scenery_id, tag_id) in st:
			tag_id = randint(1, 21)
		st.add((scenery_id, tag_id))

		f.write(
			'''(%d, %d)%s\n''' % (scenery_id, tag_id, ',' if count!=total else ';'))


main()
f.close()

