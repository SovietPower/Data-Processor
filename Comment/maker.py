from random import randint, uniform, choice

f = open(r'E:\Poetic Journey\Data Processor\Comment\comment_insert.sql', 'w', encoding='utf-8')

f.write('delete from comment;\n')
f.write('alter table comment AUTO_INCREMENT 1;\n\n')
f.write('insert into comment(card_id, comment_id, user_id, comment_text, comment_time) values\n')

comment_str = ['，', '。', '！', '玩的很开心，', '值得一试！', '用户觉得很好', '名声在外', '服务态度很好', '路上不堵，', '免费入场，', '每一帧都是热爱', '老少皆宜的', '沪上赏花好去处', '很一般', '说实话一般，', '没什么特色，', '不', '值得游玩', '很好', '超级棒', '很nice', '导游人特别的好，', '很愉快', '特别推荐！']

def Make(arr, length):
	res = ''
	while len(res)<length:
		res += choice(arr)
	return res

def RandTime():
	return '20220'+str(randint(1,4))+str(randint(10,28))+str(randint(10,23))+str(randint(10,59))+str(randint(10,59))

def main():
	d = dict()
	total = 100
	for count in range(1, total+1):
		card_id = randint(1, 20)
		user_id = randint(1, 100)

		if not d.get(card_id):
			d[card_id] = 1
		else:
			d[card_id] += 1
		comment_id = d[card_id]

		text = Make(comment_str, randint(4, 20))
		time = RandTime()

		f.write(
			'''(%d, %d, %d, '%s', %s)%s\n''' % (card_id, comment_id, user_id, text, time, ',' if count!=total else ';'))


main()
f.close()

