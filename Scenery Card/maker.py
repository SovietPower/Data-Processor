from random import randint, uniform, choice

f = open(r'E:\Poetic Journey\Data Processor\Scenery Card\scenery_card_insert.sql', 'w', encoding='utf-8')

f.write('delete from scenery_card;\n')
f.write('alter table scenery_card AUTO_INCREMENT 1;\n\n')
f.write('insert into scenery_card(scenery_id, user_id, title, content, score, likes, create_time) values\n')

title_str = ['分享', '一个', '大型生态公园', '市区内的', '知名主题乐园', '江南园林风格', '超级棒的体验']
content_str = title_str[:]
content_str += ['，', '。', '！', '玩的很开心，', '值得一试！', '用户觉得很好', '名声在外', '服务态度很好', '路上不堵，', '免费入场，', '每一帧都是热爱', '老少皆宜的', '沪上赏花好去处', '很一般', '说实话一般，', '没什么特色，', '不', '值得游玩', '很好', '超级棒', '很nice', '导游人特别的好，', '很愉快', '特别推荐！']

def Make(arr, length):
	res = ''
	while len(res)<length:
		res += choice(arr)
	return res

def RandTime():
	return '20220'+str(randint(1,9))+str(randint(10,28))+str(randint(10,23))+str(randint(10,59))+str(randint(10,59))

def main():
	total = 100
	for count in range(1, total+1):
		scenery_id = randint(1, 509)
		user_id = randint(1, 100)

		title = Make(title_str, randint(4, 10))
		content = Make(content_str, randint(8, 30))
		score = uniform(0, 5.0)
		likes = randint(0, 10)
		time = RandTime()

		f.write(
			'''(%d, %d, '%s', '%s', %.1f, %d, %s)%s\n''' % (scenery_id, user_id, title, content, score, likes, time, ',' if count!=total else ';'))


main()
f.close()

